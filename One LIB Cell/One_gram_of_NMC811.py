import pandas as pd
import numpy as np

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
Inputs_for_one_gram_of_NMC811 = generate_samples_from_excel("Inputs for one gram of NMC811.xlsx")
EF_of_inputs_for_one_gram_of_NMC811 = generate_samples_from_excel("EF of inputs for one gram of NMC811.xlsx")
EE_of_inputs_for_one_gram_of_NMC811 = generate_samples_from_excel("EE of inputs for one gram of NMC811.xlsx")

# Calculate the GHG emissions of one gram of NMC811
# Step 1: Get list of common variables
common_vars = set(Inputs_for_one_gram_of_NMC811.keys()) & set(EF_of_inputs_for_one_gram_of_NMC811.keys())

# Step 2: Initialize array to hold total GHG emissions for each simulation
GHG_emissions_of_one_gram_of_NMC811 = np.zeros(n_simulations)

# Step 3: Dot product: sum(input_amount[i] * EF[i]) for all variables
for var in common_vars:
    GHG_emissions_of_one_gram_of_NMC811 += Inputs_for_one_gram_of_NMC811[var] * EF_of_inputs_for_one_gram_of_NMC811[var]  # element-wise multiplication

# Calculate the embodied energy of one gram of NMC811
# Step 1: Get list of common variables
common_vars = set(Inputs_for_one_gram_of_NMC811.keys()) & set(EE_of_inputs_for_one_gram_of_NMC811.keys())

# Step 2: Initialize array to hold total GHG emissions for each simulation
Embodied_energy_of_one_gram_of_NMC811 = np.zeros(n_simulations)

# Step 3: Dot product: sum(input_amount[i] * EF[i]) for all variables
for var in common_vars:
    Embodied_energy_of_one_gram_of_NMC811 += Inputs_for_one_gram_of_NMC811[var] * EE_of_inputs_for_one_gram_of_NMC811[var]  # element-wise multiplication

