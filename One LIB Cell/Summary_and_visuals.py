import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Raw_material_extraction_for_one_LIB_cell import (GHG_emissions_of_material_inputs_for_one_LIB_cell, Embodied_energy_of_material_inputs_for_one_LIB_cell)
from Manufacturing_phase_for_one_LIB_cell import (GHG_emissions_of_manufacturing_one_LIB_cell, Energy_consumption_of_manufacturing_one_LIB_cell)
from EoL_phase_for_one_LIB_cell import (Energy_consumption_of_recycling_one_LIB_cell, GHG_emissions_of_recycling_one_LIB_cell, Total_avoided_GHG_emissions, Total_avoided_energy_consumption)

n_simulations = 10000
def generate_triangular_samples_from_excel(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()

    samples = {}
    for _, row in df.iterrows():
        var_name = row['Retiring at (%)']
        samples[var_name] = np.random.triangular(
            row['Low'], row['Baseline'], row['High'], size=n_simulations
        )
    return samples
Total_charging_energy = generate_triangular_samples_from_excel("Total_Charging_Energy_for_MC.xlsx")

#====================Scenario 1: Retire LIB at 80% SOH====================
g_GHG_emissions_per_lifetime_kWh_80 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell+
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions )/(3.74*66.92*Total_charging_energy[80]))

Wh_energy_consumption_per_lifetime_kWh_80 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption
                                             )/(3.74*66.92*Total_charging_energy[80]))

#====================Scenario 2: Retire LIB at 75% SOH====================
g_GHG_emissions_per_lifetime_kWh_75 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell+
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions )/(3.74*66.92*Total_charging_energy[75]))

Wh_energy_consumption_per_lifetime_kWh_75 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption
                                             )/(3.74*66.92*Total_charging_energy[75]))

#====================Scenario 3: Retire LIB at 70% SOH====================
g_GHG_emissions_per_lifetime_kWh_70 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell+
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions )/(3.74*66.92*Total_charging_energy[70]))

Wh_energy_consumption_per_lifetime_kWh_70 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption
                                             )/(3.74*66.92*Total_charging_energy[70]))

#====================Scenario 4: Retire LIB at 65% SOH====================
g_GHG_emissions_per_lifetime_kWh_65 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell+
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions )/(3.74*66.92*Total_charging_energy[65]))

Wh_energy_consumption_per_lifetime_kWh_65 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption
                                             )/(3.74*66.92*Total_charging_energy[65]))

#====================Visual 1 Retire at different SOHs====================
# Scenario labels
scenarios = ['80% SOH', '75% SOH', '70% SOH', '65% SOH']

# GHG Emissions data
ghg_data = [
    g_GHG_emissions_per_lifetime_kWh_80,
    g_GHG_emissions_per_lifetime_kWh_75,
    g_GHG_emissions_per_lifetime_kWh_70,
    g_GHG_emissions_per_lifetime_kWh_65
]

# Energy Consumption data
energy_data = [
    Wh_energy_consumption_per_lifetime_kWh_80,
    Wh_energy_consumption_per_lifetime_kWh_75,
    Wh_energy_consumption_per_lifetime_kWh_70,
    Wh_energy_consumption_per_lifetime_kWh_65
]

# Function to compute means and 95% CI error bars
def summarize(data_list):
    means = [np.mean(arr) for arr in data_list]
    lower_bounds = [np.percentile(arr, 2.5) for arr in data_list]
    upper_bounds = [np.percentile(arr, 97.5) for arr in data_list]
    errors = [ [mean - low, high - mean] for mean, low, high in zip(means, lower_bounds, upper_bounds) ]
    return means, np.array(errors).T  # shape (2, N) for yerr

# Plot GHG Emissions
ghg_means, ghg_errors = summarize(ghg_data)
plt.figure(figsize=(8, 5))
plt.bar(scenarios, ghg_means, yerr=ghg_errors, capsize=5)
plt.ylabel("g CO₂-eq per lifetime kWh")
plt.title("GHG Emissions (95% Confidence Interval)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Plot Energy Consumption
energy_means, energy_errors = summarize(energy_data)
plt.figure(figsize=(8, 5))
plt.bar(scenarios, energy_means, yerr=energy_errors, capsize=5)
plt.ylabel("Wh per lifetime kWh")
plt.title("Energy Consumption (95% Confidence Interval)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

#====================Visual 2 Contributions of different phases====================
# Calculate averages
avg_material = np.mean(GHG_emissions_of_material_inputs_for_one_LIB_cell)
avg_manufacturing = np.mean(GHG_emissions_of_manufacturing_one_LIB_cell)
avg_recycling = np.mean(GHG_emissions_of_recycling_one_LIB_cell)
avg_avoided = -np.mean(Total_avoided_GHG_emissions)  # negative value for plotting

# Plot
fig, ax = plt.subplots(figsize=(6, 6))

# Positive stacked bars
ax.bar("LIB Cell", avg_material, label="Raw Material Extraction")
ax.bar("LIB Cell", avg_manufacturing, bottom=avg_material, label="Manufacturing")
ax.bar("LIB Cell", avg_recycling, bottom=avg_material + avg_manufacturing, label="Recycling")

# Negative bar for avoided emissions
ax.bar("LIB Cell", avg_avoided, bottom=0, label="Avoided Emissions")

# Formatting
ax.set_ylabel("GHG Emissions (g CO₂-eq)")
ax.set_title("Average GHG Emissions for One LIB Cell (Including Avoided Emissions)")
ax.axhline(0, color='black', linewidth=1)
ax.legend()
plt.tight_layout()
plt.show()

