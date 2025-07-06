import pandas as pd
import numpy as np
import Raw_material_extraction_for_one_LIB_cell
# Every energy consumption value is in Wh, and every GHG emission value is in g CO₂e.


#--------------------Step 1 Pretreatment--------------------
Energy_consumption_of_discharge = 3.74*66.92*0.98
Energy_consumption_of_comminution = 1700/55
Energy_consumption_of_dense_media_separation = 4000/55
Energy_consumption_of_screening = 5400/55
Energy_consumption_of_high_intensity_magnetic_separation = 6700/55
Energy_consumption_of_electrostatic_separation = 1100/55
Energy_consumption_of_filtration_in_step1 = 700/55

#--------------------Step 2 Cathode crushing and soaking--------------------
from Raw_material_extraction_for_one_LIB_cell import Material_inputs_for_one_LIB_cell
Energy_consumption_of_crushing =0.3556*(Material_inputs_for_one_LIB_cell["NMC811"]+Material_inputs_for_one_LIB_cell["Carbon Black"]+Material_inputs_for_one_LIB_cell["PVDF"]+Material_inputs_for_one_LIB_cell["Al"])
Energy_consumption_of_soaking = 75*(0.583*Material_inputs_for_one_LIB_cell["NMP"]+0.278*(Material_inputs_for_one_LIB_cell["NMC811"]+Material_inputs_for_one_LIB_cell["Carbon Black"]+Material_inputs_for_one_LIB_cell["PVDF"])+0.25*Material_inputs_for_one_LIB_cell["Al"])/0.75/1000

#--------------------Step 3 Filtration and calcination--------------------
Energy_consumption_of_filtration_in_step3 = 700/55
Electricity_consumption_of_calcination = (np.random.uniform(0.0234, 0.0258, 10000))*(Material_inputs_for_one_LIB_cell["NMC811"]+Material_inputs_for_one_LIB_cell["Carbon Black"]+Material_inputs_for_one_LIB_cell["PVDF"])
Natural_gas_consumption_of_calcination = 170.444*(Material_inputs_for_one_LIB_cell["NMC811"]+Material_inputs_for_one_LIB_cell["Carbon Black"]+Material_inputs_for_one_LIB_cell["PVDF"])/1000
Field_GHG_emissions = 1.374*Material_inputs_for_one_LIB_cell["PVDF"]+3.664*Material_inputs_for_one_LIB_cell["Carbon Black"]
#--------------------Step 4 Grinding--------------------
Energy_consumption_of_grinding = (np.random.triangular(2.78, 355.56, 2515.50, 10000))*Material_inputs_for_one_LIB_cell["NMC811"]/1000

#--------------------Step 5 Leaching and metal recovery--------------------
n_simulations = 10000
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
Material_inputs_for_recycling_one_LIB_cell = generate_samples_from_excel("Material inputs for recycling one LIB cell.xlsx")
EF_of_material_inputs_for_recycling_one_LIB_cell = generate_samples_from_excel("EF of material inputs for recycling one LIB cell.xlsx")
EE_of_material_inputs_for_recycling_one_LIB_cell = generate_samples_from_excel("EE of material inputs for recycling one LIB cell.xlsx")

common_vars = set(EE_of_material_inputs_for_recycling_one_LIB_cell) & set(Material_inputs_for_recycling_one_LIB_cell) & set(EF_of_material_inputs_for_recycling_one_LIB_cell.keys())

Total_EE_factor_of_material_inputs_for_recycling_one_LIB_cell = np.zeros(n_simulations)
for var in common_vars:
    Total_EE_factor_of_material_inputs_for_recycling_one_LIB_cell += (
        EE_of_material_inputs_for_recycling_one_LIB_cell[var] *
        Material_inputs_for_recycling_one_LIB_cell[var]
    )
Embodied_energy_of_material_inputs_for_recycling_one_LIB_cell=Total_EE_factor_of_material_inputs_for_recycling_one_LIB_cell*Material_inputs_for_one_LIB_cell["NMC811"]

Total_EF_factor_of_material_inputs_for_recycling_one_LIB_cell = np.zeros(n_simulations)
for var in common_vars:
    Total_EF_factor_of_material_inputs_for_recycling_one_LIB_cell += (
        EF_of_material_inputs_for_recycling_one_LIB_cell[var] *
        Material_inputs_for_recycling_one_LIB_cell[var]
    )
GHG_emissions_of_material_inputs_for_recycling_one_LIB_cell=Total_EF_factor_of_material_inputs_for_recycling_one_LIB_cell*Material_inputs_for_one_LIB_cell["NMC811"]

Energy_consumption_of_filtration_in_step5 = 4*700/55

#--------------------Summary--------------------
Total_electricity_consumption_of_recycling_one_LIB_cell = (
    Energy_consumption_of_discharge +
    Energy_consumption_of_comminution +
    Energy_consumption_of_dense_media_separation +
    Energy_consumption_of_screening +
    Energy_consumption_of_high_intensity_magnetic_separation +
    Energy_consumption_of_electrostatic_separation +
    Energy_consumption_of_filtration_in_step1 +
    Energy_consumption_of_crushing +
    Energy_consumption_of_soaking +
    Energy_consumption_of_filtration_in_step3 +
    Electricity_consumption_of_calcination +
    Energy_consumption_of_grinding +
    Energy_consumption_of_filtration_in_step5)

Energy_consumption_of_recycling_one_LIB_cell= Total_electricity_consumption_of_recycling_one_LIB_cell+Natural_gas_consumption_of_calcination+Embodied_energy_of_material_inputs_for_recycling_one_LIB_cell
GHG_emissions_of_recycling_one_LIB_cell = Field_GHG_emissions+(Total_electricity_consumption_of_recycling_one_LIB_cell)*(np.random.triangular(0.0009, 0.3589, 0.8713, 10000))+(Natural_gas_consumption_of_calcination)*(np.random.triangular(0.2446, 0.2458, 0.2774, 10000))+GHG_emissions_of_material_inputs_for_recycling_one_LIB_cell

#====================Outputs from recycling one LIB cell====================
#According to BatPaC, Al and Cu are assumed to have recovery rates of 83%, while Co, Ni, and Mn each achieve 98% recovery after leaching and precipitation. Li is recovered at 90%.
Recovered_Al=0.83*Material_inputs_for_one_LIB_cell["Al"]
Recovered_Cu=0.83*Material_inputs_for_one_LIB_cell["Cu"]
Recovered_CoOH2=0.98*0.0605*1.576*Material_inputs_for_one_LIB_cell["NMC811"]
Recovered_NiOH2=0.98*0.4825*1.578*Material_inputs_for_one_LIB_cell["NMC811"]
Recovered_MnOH2=0.98*0.0565*1.619*Material_inputs_for_one_LIB_cell["NMC811"]
Recovered_Li2CO3=0.9*0.0713*5.32*Material_inputs_for_one_LIB_cell["NMC811"]
recovered_materials = [
    Recovered_Al,
    Recovered_Cu,
    Recovered_CoOH2,
    Recovered_NiOH2,
    Recovered_MnOH2,
    Recovered_Li2CO3
]

#Calculate avoided GHG emissions
EF_of_avoided_materials = generate_samples_from_excel("Avoided_EF_of_outputs_from_recycling_one_LIB_cell.xlsx")
EF_samples = list(EF_of_avoided_materials.values())
avoided_GHG_results = [
    recovered_materials[i] * EF_samples[i]
    for i in range(len(recovered_materials))
]
Total_avoided_GHG_emissions = sum(avoided_GHG_results)

#Calculate avoided Energy Consumption
EE_of_avoided_materials = generate_samples_from_excel("Avoided_EE_of_outputs_from_recycling_one_LIB_cell.xlsx")
EE_samples = list(EE_of_avoided_materials.values())
avoided_energy_consumption = [
    recovered_materials[i] * EE_samples[i]
    for i in range(len(recovered_materials))
]
Total_avoided_energy_consumption = sum(avoided_energy_consumption)
