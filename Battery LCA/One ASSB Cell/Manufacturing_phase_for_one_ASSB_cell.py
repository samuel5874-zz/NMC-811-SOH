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

ASSB_cell_dimensions = generate_samples_from_excel("ASSB cell dimensions.xlsx")
from Raw_material_extraction_for_one_ASSB_cell import Material_inputs_for_one_ASSB_cell

#Calculate manufacturing phase energy consumption for one ASSB cell
Energy_consumption_of_producing_Li_foil_for_one_ASSB_cell =ASSB_cell_dimensions['Width of negative electrode'] * ASSB_cell_dimensions['Length of negative electrode']/22.75*118.7/1000
Energy_consumption_of_positive_electrode_preparation_mixing_for_one_ASSB_cell = 280.45/67.38*Material_inputs_for_one_ASSB_cell['NMC811']/4.65
Energy_consumption_of_electroyte_preparation_mixing_for_one_ASSB_cell =280.45/67.38*Material_inputs_for_one_ASSB_cell['Li3PS4']/1.87
Energy_consumption_of_positive_electrode_coating_for_one_ASSB_cell =1148.95/207* ASSB_cell_dimensions['Length of positive electrode']
Energy_consumption_of_electrolyte_coating_for_one_ASSB_cell = 1148.95/207* ASSB_cell_dimensions['Length of electrolyte']
Energy_consumption_of_positive_electrode_and_electrolyte_calendering_for_one_ASSB_cell =36.59/207*ASSB_cell_dimensions['Length of electrolyte']
Energy_consumption_of_slitting_for_one_ASSB_cell = 69.1/416*(ASSB_cell_dimensions['Length of positive electrode']+ASSB_cell_dimensions['Length of electrolyte'])
Energy_consumption_of_negative_electrode_notching_for_one_ASSB_cell = 69.08/209*ASSB_cell_dimensions['Length of negative electrode']
Energy_consumption_of_positive_electrode_and_electrolyte_notching_for_one_ASSB_cell = 65.05/207*ASSB_cell_dimensions['Length of electrolyte']
Energy_consumption_of_stacking_for_one_ASSB_cell = 197
Energy_consumption_of_pressing_for_one_ASSB_cell = 16
Energy_consumption_of_welding_for_one_ASSB_cell = 74
Energy_consumption_of_X_ray_inspection_for_one_ASSB_cell = 16
Energy_consumption_of_inserting_cell_in_container_for_one_ASSB_cell = 41
Energy_consumption_of_dry_room_and_dry_room_control_system_for_one_ASSB_cell = 2644
Energy_consumption_of_formation_cycling_for_one_ASSB_cell = 2954.95

Energy_consumption_of_manufacturing_one_ASSB_cell = (
    Energy_consumption_of_producing_Li_foil_for_one_ASSB_cell +
    Energy_consumption_of_positive_electrode_preparation_mixing_for_one_ASSB_cell +
    Energy_consumption_of_electroyte_preparation_mixing_for_one_ASSB_cell +
    Energy_consumption_of_positive_electrode_coating_for_one_ASSB_cell +
    Energy_consumption_of_electrolyte_coating_for_one_ASSB_cell +
    Energy_consumption_of_positive_electrode_and_electrolyte_calendering_for_one_ASSB_cell +
    Energy_consumption_of_slitting_for_one_ASSB_cell +
    Energy_consumption_of_negative_electrode_notching_for_one_ASSB_cell +
    Energy_consumption_of_positive_electrode_and_electrolyte_notching_for_one_ASSB_cell +
    Energy_consumption_of_stacking_for_one_ASSB_cell +
    Energy_consumption_of_pressing_for_one_ASSB_cell +
    Energy_consumption_of_welding_for_one_ASSB_cell +
    Energy_consumption_of_X_ray_inspection_for_one_ASSB_cell +
    Energy_consumption_of_inserting_cell_in_container_for_one_ASSB_cell +
    Energy_consumption_of_dry_room_and_dry_room_control_system_for_one_ASSB_cell +
    Energy_consumption_of_formation_cycling_for_one_ASSB_cell
)
EF_of_electricity = np.random.triangular(left=0.0009, mode=0.3589, right=0.8713, size=10000)
GHG_emissions_of_manufacturing_one_ASSB_cell = Energy_consumption_of_manufacturing_one_ASSB_cell*EF_of_electricity
