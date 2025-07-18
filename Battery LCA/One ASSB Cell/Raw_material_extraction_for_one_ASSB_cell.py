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

Material_inputs_for_one_ASSB_cell = generate_samples_from_excel("Material inputs for one ASSB cell.xlsx")
EF_of_material_inputs_for_one_ASSB_cell = generate_samples_from_excel("EF of material inputs for one ASSB cell.xlsx")
EE_of_material_inputs_for_one_ASSB_cell = generate_samples_from_excel("EE of material inputs for one ASSB cell.xlsx")

# Calculate the GHG emissions of material inputs for one ASSB cell
# Step 1: Get list of common variables
common_vars = set(Material_inputs_for_one_ASSB_cell.keys()) & set(EF_of_material_inputs_for_one_ASSB_cell.keys())

# Step 2: Initialize array to hold total GHG emissions for each simulation
GHG_emissions_of_material_inputs_for_one_ASSB_cell = np.zeros(n_simulations)

# Step 3: Dot product: sum(input_amount[i] * EF[i]) for all variables
from One_gram_of_NMC811 import GHG_emissions_of_one_gram_of_NMC811
# First, sum GHG emissions from all materials (excluding NMC811)
for var in common_vars:
    GHG_emissions_of_material_inputs_for_one_ASSB_cell += (
        Material_inputs_for_one_ASSB_cell[var] * EF_of_material_inputs_for_one_ASSB_cell[var]
    )

# Then, separately add the GHG emissions from NMC811
# (amount of NMC811 used × GHG emissions per gram of NMC811)
GHG_emissions_of_material_inputs_for_one_ASSB_cell += (
    Material_inputs_for_one_ASSB_cell["NMC811"] * GHG_emissions_of_one_gram_of_NMC811
)

# Calculate the embodied energy of material inputs for one ASSB cell
# Step 1: Get list of common variables
common_vars = set(Material_inputs_for_one_ASSB_cell.keys()) & set(EE_of_material_inputs_for_one_ASSB_cell.keys())

# Step 2: Initialize array to hold total GHG emissions for each simulation
Embodied_energy_of_material_inputs_for_one_ASSB_cell = np.zeros(n_simulations)

# Step 3: Dot product: sum(input_amount[i] * EE[i]) for all variables

from One_gram_of_NMC811 import Embodied_energy_of_one_gram_of_NMC811
# First, sum embodied energy of all materials (excluding NMC811)
for var in common_vars:
    Embodied_energy_of_material_inputs_for_one_ASSB_cell += (
        Material_inputs_for_one_ASSB_cell[var] * EE_of_material_inputs_for_one_ASSB_cell[var]
    )

# Then, separately add the embodied energy of NMC811
# (amount of NMC811 used × embodied energy per gram of NMC811)
Embodied_energy_of_material_inputs_for_one_ASSB_cell += (
    Material_inputs_for_one_ASSB_cell["NMC811"] * Embodied_energy_of_one_gram_of_NMC811)
# 打印出有哪些变量造成了 NaN
for var in common_vars:
    a = Material_inputs_for_one_ASSB_cell[var]
    b = EF_of_material_inputs_for_one_ASSB_cell[var]
    if np.isnan(a).any():
        print(f"{var}: Material input contains NaN")
    if np.isnan(b).any():
        print(f"{var}: EF contains NaN")

