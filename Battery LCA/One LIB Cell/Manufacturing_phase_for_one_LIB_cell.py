import pandas as pd
import numpy as np
# All GHG emissions are expressed in grams of CO₂-equivalent (g CO₂e), and all energy consumption values are in watt-hours (Wh).
# Number of simulations
n_simulations = 10000

# Function to read Excel and generate Monte Carlo samples
def generate_samples_from_excel(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()  # Remove any extra spaces in column names
    samples = {}

    for _, row in df.iterrows():
        var_name = row['Inputs']
        dist_type = row['Distribution'].strip().lower()

        if dist_type == 'uniform':
            samples[var_name] = np.random.uniform(row['Low'], row['High'], size=n_simulations)
        elif dist_type == 'triangular':
            samples[var_name] = np.random.triangular(row['Low'], row['Baseline'], row['High'], size=n_simulations)
        elif dist_type == 'point estimate':
            samples[var_name] = np.full(n_simulations, row['Baseline'])
        else:
            raise ValueError(f"Unsupported distribution type for variable '{var_name}': {row['Distribution']}")

    return samples

# Load and simulate for each Excel file
Manufacturing_energy_inputs_for_one_LIB_cell = generate_samples_from_excel("Manufacturing energy inputs for one LIB cell.xlsx")
EF_of_manufacturing_energy_inputs_for_one_LIB_cell = generate_samples_from_excel("EF of manufacturing energy inputs for one LIB cell.xlsx")

# Calculate the GHG emissions to manufacture one LIB cell
# Step 1: Get list of common variables
common_vars = set(Manufacturing_energy_inputs_for_one_LIB_cell.keys()) & set(EF_of_manufacturing_energy_inputs_for_one_LIB_cell.keys())

# Step 2: Initialize array to hold total GHG emissions for each simulation
GHG_emissions_of_manufacturing_one_LIB_cell = np.zeros(n_simulations)

# Step 3: Dot product: sum(input_amount[i] * EF[i]) for all variables
for var in common_vars:
    GHG_emissions_of_manufacturing_one_LIB_cell += Manufacturing_energy_inputs_for_one_LIB_cell[var] * EF_of_manufacturing_energy_inputs_for_one_LIB_cell[var]  # element-wise multiplication

# Calculate total energy consumption: sum of input values
Energy_consumption_of_manufacturing_one_LIB_cell = np.zeros(n_simulations)
for var in Manufacturing_energy_inputs_for_one_LIB_cell:
    Energy_consumption_of_manufacturing_one_LIB_cell += Manufacturing_energy_inputs_for_one_LIB_cell[var]

