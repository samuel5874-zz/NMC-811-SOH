import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
# All GHG emissions are expressed in grams of CO₂-equivalent (g CO₂e), and all energy consumption values are in watt-hours (Wh).

def process_lifetime_curve(input_file, output_file):
    # Load Excel file
    df = pd.read_excel(input_file)

    # Interpolation function
    def interpolate_integer_range(x_col):
        data = df[[x_col, 'Inputs']].dropna()
        f = interp1d(data[x_col], data['Inputs'], kind='linear', fill_value='extrapolate')
        x_new = np.arange(int(data[x_col].min()), int(data[x_col].max()) + 1)
        y_new = f(x_new)
        return pd.DataFrame({x_col: x_new, 'Interpolated Inputs': y_new})

    # Interpolate each column
    interp_baseline = interpolate_integer_range('Baseline')
    interp_low = interpolate_integer_range('Low')
    interp_high = interpolate_integer_range('High')

    # Determine full input range across all columns
    max_input = int(max(df['Baseline'].max(skipna=True),
                        df['Low'].max(skipna=True),
                        df['High'].max(skipna=True)))
    min_input = int(min(df['Baseline'].min(skipna=True),
                        df['Low'].min(skipna=True),
                        df['High'].min(skipna=True)))
    full_inputs = np.arange(min_input, max_input + 1)

    # Align interpolation to full input range
    def interpolate_to_full_range(interp_df, x_col):
        interp_series = pd.Series(index=full_inputs, dtype='float')
        interp_series.loc[interp_df[x_col].values] = interp_df['Interpolated Inputs'].values
        return interp_series.round().astype('Int64')

    baseline_series = interpolate_to_full_range(interp_baseline, 'Baseline')
    low_series = interpolate_to_full_range(interp_low, 'Low')
    high_series = interpolate_to_full_range(interp_high, 'High')

    # Combine into final DataFrame
    final_df = pd.DataFrame({
        'Inputs': full_inputs,
        'Baseline': baseline_series.values,
        'Low': low_series.values,
        'High': high_series.values
    })

    # Add Distribution column
    final_df.insert(4, 'Distribution', ['Distribution'] + ['Triangular'] * (len(final_df) - 1))

    # Save to Excel
    final_df.to_excel(output_file, sheet_name='Full Aging Curve', index=False)

# Run for all three files
process_lifetime_curve("2X lifetime.xlsx", "2X lifetime full aging curve.xlsx")
process_lifetime_curve("1X lifetime.xlsx", "1X lifetime full aging curve.xlsx")
process_lifetime_curve("0.5X lifetime.xlsx", "0.5X lifetime full aging curve.xlsx")

# === Configuration ===
voltage = 3.74  # V
initial_capacity = 66.92  # Ah
columns_to_calculate = ['Baseline', 'Low', 'High']
thresholds = [80, 75, 70, 65]
scenarios = ["2X", "1X", "0.5X"]

# === Main processing ===
for scenario in scenarios:
    df_full = pd.read_excel(f"{scenario} lifetime full aging curve.xlsx")

    discharge_results = {
        "Retiring at (%)": [],
        "Baseline": [],
        "Low": [],
        "High": [],
        "Distribution": []
    }

    charge_results = {
        "Retiring at (%)": [],
        "Baseline": [],
        "Low": [],
        "High": [],
        "Distribution": []
    }

    for threshold in thresholds:
        df_copy = df_full.copy()
        for col in columns_to_calculate:
            cutoff_index = df_copy[df_copy[col] < threshold].index.min()
            if pd.notna(cutoff_index):
                df_copy.loc[cutoff_index:, col] = pd.NA

        discharge_results["Retiring at (%)"].append(threshold)
        charge_results["Retiring at (%)"].append(threshold)

        for col in columns_to_calculate:
            soh_series = df_copy[col]
            q_loss_series = 100 - soh_series
            efficiency_series = 95.82 - 0.2303 * q_loss_series
            efficiency_decimal = efficiency_series / 100

            # === Discharge ===
            discharge_energy_per_cycle = (soh_series / 100) * initial_capacity * voltage
            total_discharge_energy = discharge_energy_per_cycle.sum(skipna=True)
            discharge_results[col].append(total_discharge_energy)

            # === Charge ===
            charge_energy_per_cycle = discharge_energy_per_cycle / efficiency_decimal
            total_charge_energy = charge_energy_per_cycle.sum(skipna=True)
            charge_results[col].append(total_charge_energy)

        discharge_results["Distribution"].append("Triangular")
        charge_results["Distribution"].append("Triangular")

    # Save each scenario to separate Excel files
    pd.DataFrame(discharge_results).to_excel(f"{scenario}_Total_discharge_energy.xlsx", index=False)
    pd.DataFrame(charge_results).to_excel(f"{scenario}_Total_charge_energy.xlsx", index=False)

