import pandas as pd
import numpy as np
# All GHG emissions are expressed in grams of CO₂-equivalent (g CO₂e), and all energy consumption values are in watt-hours (Wh).

# === Step 1: Load and Interpolate ===
df = pd.read_excel("Use phase for one LIB cell.xlsx")
df = df.set_index('Cycle Number')
full_index = pd.RangeIndex(start=int(df.index.min()), stop=int(df.index.max()) + 1, step=1)
df_full = df.reindex(full_index)

columns_to_interpolate = ['Baseline', 'Low', 'High']
df_full[columns_to_interpolate] = df_full[columns_to_interpolate].interpolate(method='linear')
df_full[columns_to_interpolate] = (df_full[columns_to_interpolate] * 100).round().astype(int)
df_full = df_full.reset_index().rename(columns={'index': 'Cycle Number'})
df_full.to_excel("Full aging curve.xlsx", index=False)

# === Step 2: Define thresholds and generate truncated versions ===
thresholds = [80, 75, 70, 65]

for threshold in thresholds:
    df_copy = df_full.copy()
    for col in columns_to_interpolate:
        cutoff_index = df_copy[df_copy[col] < threshold].index.min()
        if pd.notna(cutoff_index):
            df_copy.loc[cutoff_index:, col] = pd.NA
    df_copy.to_excel(f"Retire_at_{threshold}percent.xlsx", index=False)

# === Step 3: Calculate Total Charging Energy per threshold and scenario ===
# === Configuration ===
voltage = 3.74  # V
initial_capacity = 66.92  # Ah
columns_to_calculate = ['Baseline', 'Low', 'High']
thresholds = [80, 75, 70, 65]

# === Output dictionaries ===
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

# === Loop through thresholds ===
for threshold in thresholds:
    file_path = f"Retire_at_{threshold}percent.xlsx"
    df_energy = pd.read_excel(file_path)

    discharge_results["Retiring at (%)"].append(threshold)
    charge_results["Retiring at (%)"].append(threshold)

    for col in columns_to_calculate:
        soh_series = df_energy[col]
        q_loss_series = 100 - soh_series
        efficiency_series = 95.82 - 0.2303 * q_loss_series
        efficiency_decimal = efficiency_series / 100

        # === Discharge energy per cycle ===
        discharge_energy_per_cycle = (soh_series / 100) * initial_capacity * voltage
        total_discharge_energy = discharge_energy_per_cycle.sum(skipna=True)
        discharge_results[col].append(total_discharge_energy)

        # === Charge energy per cycle ===
        charge_energy_per_cycle = discharge_energy_per_cycle / efficiency_decimal
        total_charge_energy = charge_energy_per_cycle.sum(skipna=True)
        charge_results[col].append(total_charge_energy)

    discharge_results["Distribution"].append("Triangular")
    charge_results["Distribution"].append("Triangular")

# === Save to two separate Excel files ===
discharge_df = pd.DataFrame(discharge_results)
charge_df = pd.DataFrame(charge_results)

discharge_df.to_excel("Total_discharge_energy.xlsx", index=False)
charge_df.to_excel("Total_charge_energy.xlsx", index=False)
