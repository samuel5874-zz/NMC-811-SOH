import pandas as pd

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
voltage = 3.74  # V
initial_capacity = 66.92  # Ah
columns_to_calculate = ['Baseline', 'Low', 'High']

# Prepare output structure
results_dict = {
    "Retiring at (%)": [],
    "Baseline": [],
    "Low": [],
    "High": [],
    "Distribution": []
}

for threshold in thresholds:
    file_path = f"Retire_at_{threshold}percent.xlsx"
    df_energy = pd.read_excel(file_path)

    results_dict["Retiring at (%)"].append(threshold)
    for col in columns_to_calculate:
        energy_per_cycle = (df_energy[col] / 100) * initial_capacity * voltage
        total_energy = energy_per_cycle.sum(skipna=True)
        results_dict[f"{col}"].append(total_energy)
    results_dict["Distribution"].append("Triangular")

# === Step 4: Save final table ===
energy_df_mc = pd.DataFrame(results_dict)
energy_df_mc.to_excel("Total_Charging_Energy_for_MC.xlsx", index=False)
print(energy_df_mc)

