import pandas as pd
import numpy as np
from Raw_material_extraction_for_one_ASSB_cell import Material_inputs_for_one_ASSB_cell
# All GHG emissions are expressed in grams of CO₂-equivalent (g CO₂e), and all energy consumption values are in watt-hours (Wh).
EF_of_electricity = np.random.triangular(left=0.0009, mode=0.3589, right=0.8713, size=10000)
EF_of_natural_gas= np.random.triangular(0.2446, 0.2458, 0.2774, 10000)
#--------------------Pretreatment--------------------
#Step 1. Discharge
Energy_consumption_of_discharge = 3.74*66.92*0.98

#Step2. Component Separation
DME_inputs = 124 * Material_inputs_for_one_ASSB_cell['Li'] * 0.05 + \
               0.867 * (
                   Material_inputs_for_one_ASSB_cell['NMC811'] +
                   Material_inputs_for_one_ASSB_cell['Carbon Black'] +
                   Material_inputs_for_one_ASSB_cell['PVDF'] +
                   Material_inputs_for_one_ASSB_cell['Al'] +
                   Material_inputs_for_one_ASSB_cell['Cu'] +
                   Material_inputs_for_one_ASSB_cell['Li3PS4']
               ) * 2 / 5
FeCl3_inputs = 7.79*1.05*Material_inputs_for_one_ASSB_cell['Li']
NaOH_inputs = 0.741*7.79*0.05*Material_inputs_for_one_ASSB_cell['Li']
Na2CO3_inputs = 7.64*Material_inputs_for_one_ASSB_cell['Li']
NMF_inputs = 0.05*Material_inputs_for_one_ASSB_cell['Li3PS4']/50*1011
EtOH_inputs = 0.789 * (
                   Material_inputs_for_one_ASSB_cell['NMC811'] +
                   Material_inputs_for_one_ASSB_cell['Carbon Black'] +
                   Material_inputs_for_one_ASSB_cell['PVDF'] +
                   Material_inputs_for_one_ASSB_cell['Al'] +
                   Material_inputs_for_one_ASSB_cell['Cu'] ) * 2 / 5
EF_of_DME = 2.12
EE_of_DME = 19.79
EF_of_FeCl3 = 1.033
EE_of_FeCl3 = 4.83
EF_of_NaOH = 1.8298
EE_of_NaOH = 8.971
EF_of_Na2CO3 = 0.6812
EE_of_Na2CO3 = 1.644
EF_of_NMF = 4.0088
EE_of_NMF = 36.446
EF_of_EtOH = np.random.triangular(left=0.1362,mode=0.1465,right=0.4526,size=10000)
EE_of_EtOH = np.random.triangular(left=11.24,mode=12.96,right=19.17,size=10000)

Energy_to_recycle_Naph = Material_inputs_for_one_ASSB_cell['Li']*19.29/1000*1809*195/3600/0.7
Energy_to_recycle_DME = 124 * Material_inputs_for_one_ASSB_cell['Li']*60*2.14/3600/0.7
Energy_to_recrystallize_LiPS =(NMF_inputs*20*125.2*(240-25))/(59.07*3600)/0.7
Energy_to_dry_black_mass_step_IV= 840.1*65/3600/0.7/1000*(
                   Material_inputs_for_one_ASSB_cell['NMC811'] +
                   Material_inputs_for_one_ASSB_cell['Carbon Black'] +
                   Material_inputs_for_one_ASSB_cell['PVDF'] +
                   Material_inputs_for_one_ASSB_cell['Al'] +
                   Material_inputs_for_one_ASSB_cell['Cu'] +
                   Material_inputs_for_one_ASSB_cell['Li3PS4'])
Energy_to_dry_black_mass_step_V= 840.1*65/3600/0.7/1000*(
                   Material_inputs_for_one_ASSB_cell['NMC811'] +
                   Material_inputs_for_one_ASSB_cell['Carbon Black'] +
                   Material_inputs_for_one_ASSB_cell['PVDF'] +
                   Material_inputs_for_one_ASSB_cell['Al'] +
                   Material_inputs_for_one_ASSB_cell['Cu'])

#Step3. Secondary Separation and Calcination
Energy_consumption_of_comminution = 1700/55
Energy_consumption_of_dense_media_separation = 4000/55
Energy_consumption_of_screening = 5400/55
Energy_consumption_of_electrostatic_separation = 1100/55

Electricity_consumption_of_calcination = (np.random.uniform(0.0234, 0.0258, 10000))*(Material_inputs_for_one_ASSB_cell["NMC811"]+Material_inputs_for_one_ASSB_cell["Carbon Black"]+Material_inputs_for_one_ASSB_cell["PVDF"])
Natural_gas_consumption_of_calcination = 170.444*(Material_inputs_for_one_ASSB_cell["NMC811"]+Material_inputs_for_one_ASSB_cell["Carbon Black"]+Material_inputs_for_one_ASSB_cell["PVDF"])/1000
Field_GHG_emissions = 1.374*Material_inputs_for_one_ASSB_cell["PVDF"]+3.664*Material_inputs_for_one_ASSB_cell["Carbon Black"]

#Step 4. Calculate Total GHG Emissions and Energy Consumption
Total_energy_consumption_in_pretreatment = (
    Energy_consumption_of_discharge +
    DME_inputs * EE_of_DME +
    FeCl3_inputs * EE_of_FeCl3 +
    NaOH_inputs * EE_of_NaOH +
    Na2CO3_inputs * EE_of_Na2CO3 +
    NMF_inputs * EE_of_NMF +
    EtOH_inputs * EE_of_EtOH
) + (
    Energy_to_recycle_Naph +
    Energy_to_recycle_DME +
    Energy_to_recrystallize_LiPS +
    Energy_to_dry_black_mass_step_IV +
    Energy_to_dry_black_mass_step_V
) + (
    Energy_consumption_of_comminution +
    Energy_consumption_of_dense_media_separation +
    Energy_consumption_of_screening +
    Energy_consumption_of_electrostatic_separation
) + Electricity_consumption_of_calcination + Natural_gas_consumption_of_calcination

Total_GHG_emissions_in_pretreatment = (
    EF_of_electricity * (
        Energy_consumption_of_discharge +
        Energy_to_recycle_Naph +
        Energy_to_recycle_DME +
        Energy_to_recrystallize_LiPS +
        Energy_to_dry_black_mass_step_IV +
        Energy_to_dry_black_mass_step_V +
        Energy_consumption_of_comminution +
        Energy_consumption_of_dense_media_separation +
        Energy_consumption_of_screening +
        Energy_consumption_of_electrostatic_separation +
        Electricity_consumption_of_calcination
    ) +
    Natural_gas_consumption_of_calcination * EF_of_natural_gas +
    Field_GHG_emissions +
    DME_inputs * EF_of_DME +
    FeCl3_inputs * EF_of_FeCl3 +
    NaOH_inputs * EF_of_NaOH +
    Na2CO3_inputs * EF_of_Na2CO3 +
    NMF_inputs * EF_of_NMF +
    EtOH_inputs * EF_of_EtOH
)

#--------------------Leaching and Metal Recovery--------------------
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
Material_inputs_for_recycling_one_gram_of_NMC811 = generate_samples_from_excel("Material inputs for recycling one gram of NMC811.xlsx")
EF_of_material_inputs_for_recycling_one_gram_of_NMC811 = generate_samples_from_excel("EF of material inputs for recycling one gram of NMC811.xlsx")
EE_of_material_inputs_for_recycling_one_gram_of_NMC811 = generate_samples_from_excel("EE of material inputs for recycling one gram of NMC811.xlsx")

common_vars = set(EE_of_material_inputs_for_recycling_one_gram_of_NMC811) & set(Material_inputs_for_recycling_one_gram_of_NMC811) & set(EF_of_material_inputs_for_recycling_one_gram_of_NMC811.keys())

Total_EE_factor_of_material_inputs_for_recycling_one_gram_of_NMC811 = np.zeros(n_simulations)
for var in common_vars:
    Total_EE_factor_of_material_inputs_for_recycling_one_gram_of_NMC811 += (
        EE_of_material_inputs_for_recycling_one_gram_of_NMC811[var] *
        Material_inputs_for_recycling_one_gram_of_NMC811[var]
    )
Embodied_energy_of_material_inputs_for_recycling_one_cell_NMC811=Total_EE_factor_of_material_inputs_for_recycling_one_gram_of_NMC811*Material_inputs_for_one_ASSB_cell["NMC811"]

Total_EF_factor_of_material_inputs_for_recycling_one_gram_of_NMC811 = np.zeros(n_simulations)
for var in common_vars:
    Total_EF_factor_of_material_inputs_for_recycling_one_gram_of_NMC811 += (
        EF_of_material_inputs_for_recycling_one_gram_of_NMC811[var] *
        Material_inputs_for_recycling_one_gram_of_NMC811[var]
    )
GHG_emissions_of_material_inputs_for_recycling_one_cell_NMC811=Total_EE_factor_of_material_inputs_for_recycling_one_gram_of_NMC811*Material_inputs_for_one_ASSB_cell["NMC811"]

Energy_consumption_of_filtration_in_leaching = 4*700/55

#--------------------Summary--------------------
Total_energy_consumption_to_recycle_one_ASSB_cell = (
    Total_energy_consumption_in_pretreatment +
    Energy_consumption_of_filtration_in_leaching +
    Embodied_energy_of_material_inputs_for_recycling_one_cell_NMC811
)

Total_GHG_emissions_to_recycle_one_ASSB_cell = (
    Total_GHG_emissions_in_pretreatment +
    GHG_emissions_of_material_inputs_for_recycling_one_cell_NMC811 +
    Energy_consumption_of_filtration_in_leaching * EF_of_electricity
)

#====================Outputs from recycling one ASSB cell====================
Recovered_Al=0.83*Material_inputs_for_one_ASSB_cell["Al"]
Recovered_Cu=0.83*Material_inputs_for_one_ASSB_cell["Cu"]
Recovered_CoOH2=0.98*0.0605*1.576*Material_inputs_for_one_ASSB_cell["NMC811"]
Recovered_NiOH2=0.98*0.4825*1.578*Material_inputs_for_one_ASSB_cell["NMC811"]
Recovered_MnOH2=0.98*0.0565*1.619*Material_inputs_for_one_ASSB_cell["NMC811"]
Recovered_Li2CO3=0.9*0.0713*5.32*Material_inputs_for_one_ASSB_cell["NMC811"]+0.98*5.32*Material_inputs_for_one_ASSB_cell["Li"]
Recovered_LiPS= 0.98*Material_inputs_for_one_ASSB_cell["Li3PS4"]
recovered_materials = [
    Recovered_Al,
    Recovered_Cu,
    Recovered_CoOH2,
    Recovered_NiOH2,
    Recovered_MnOH2,
    Recovered_Li2CO3,
    Recovered_LiPS
]

#Calculate avoided GHG emissions
EF_of_avoided_materials = generate_samples_from_excel("Avoided_EF_of_outputs_from_recycling_one_ASSB_cell.xlsx")
EF_samples = list(EF_of_avoided_materials.values())
avoided_GHG_results = [
    recovered_materials[i] * EF_samples[i]
    for i in range(len(recovered_materials))
]
Total_avoided_GHG_emissions = sum(avoided_GHG_results)

#Calculate avoided Energy Consumption
EE_of_avoided_materials = generate_samples_from_excel("Avoided_EE_of_outputs_from_recycling_one_ASSB_cell.xlsx")
EE_samples = list(EE_of_avoided_materials.values())
avoided_energy_consumption = [
    recovered_materials[i] * EE_samples[i]
    for i in range(len(recovered_materials))
]
Total_avoided_energy_consumption = sum(avoided_energy_consumption)
