import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# All GHG emissions are expressed in grams of CO₂-equivalent (g CO₂e), and all energy consumption values are in watt-hours (Wh).
EF_of_electricity = np.random.triangular(left=0.0009, mode=0.3589, right=0.8713, size=10000)
fuel_economy = np.random.triangular(24, 35, 48, 10000)
from Raw_material_extraction_for_one_ASSB_cell import (GHG_emissions_of_material_inputs_for_one_ASSB_cell, Embodied_energy_of_material_inputs_for_one_ASSB_cell)
from Manufacturing_phase_for_one_ASSB_cell import (GHG_emissions_of_manufacturing_one_ASSB_cell , Energy_consumption_of_manufacturing_one_ASSB_cell)
from EoL_phase_for_one_ASSB_cell import (Total_energy_consumption_to_recycle_one_ASSB_cell, Total_GHG_emissions_to_recycle_one_ASSB_cell, Total_avoided_GHG_emissions, Total_avoided_energy_consumption)

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
Total_05X_charge_energy = generate_triangular_samples_from_excel("0.5X_Total_charge_energy.xlsx")
Total_05X_discharge_energy = generate_triangular_samples_from_excel("0.5X_Total_discharge_energy.xlsx")
Total_1X_charge_energy = generate_triangular_samples_from_excel("1X_Total_charge_energy.xlsx")
Total_1X_discharge_energy = generate_triangular_samples_from_excel("1X_Total_discharge_energy.xlsx")
Total_2X_charge_energy = generate_triangular_samples_from_excel("2X_Total_charge_energy.xlsx")
Total_2X_discharge_energy = generate_triangular_samples_from_excel("2X_Total_discharge_energy.xlsx")

#====================Scenario 1.1: 0.5X Lifetime, Retire LIB at 80% SOH====================
g_GHG_emissions_per_lifetime_kWh_05_80 = 1000*((GHG_emissions_of_material_inputs_for_one_ASSB_cell+
                                     GHG_emissions_of_manufacturing_one_ASSB_cell +
                                     Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                     Total_avoided_GHG_emissions+Total_05X_charge_energy[80]*EF_of_electricity)/(Total_05X_discharge_energy[80]))

Wh_energy_consumption_per_lifetime_kWh_05_80 = 1000*((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                                      Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_05X_charge_energy[80]
                                             )/(Total_05X_discharge_energy[80]))

g_GHG_emissions_per_100miles_05_80 = g_GHG_emissions_per_lifetime_kWh_05_80 * fuel_economy
Wh_energy_consumption_per_100miles_05_80 = Wh_energy_consumption_per_lifetime_kWh_05_80 * fuel_economy

#====================Scenario 1.2: 0.5X Lifetime, Retire LIB at 75% SOH====================
g_GHG_emissions_per_lifetime_kWh_05_75 = 1000*((GHG_emissions_of_material_inputs_for_one_ASSB_cell+
                                     GHG_emissions_of_manufacturing_one_ASSB_cell +
                                     Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                     Total_avoided_GHG_emissions+Total_05X_charge_energy[75]*EF_of_electricity)/(Total_05X_discharge_energy[75]))

Wh_energy_consumption_per_lifetime_kWh_05_75 = 1000*((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                                      Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_05X_charge_energy[75]
                                             )/(Total_05X_discharge_energy[75]))
g_GHG_emissions_per_100miles_05_75 = g_GHG_emissions_per_lifetime_kWh_05_75 * fuel_economy
Wh_energy_consumption_per_100miles_05_75 = Wh_energy_consumption_per_lifetime_kWh_05_75 * fuel_economy

#====================Scenario 1.3: 0.5X Lifetime, Retire LIB at 70% SOH====================
g_GHG_emissions_per_lifetime_kWh_05_70 = 1000*((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                     GHG_emissions_of_manufacturing_one_ASSB_cell +
                                     Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                     Total_avoided_GHG_emissions + Total_05X_charge_energy[70] * EF_of_electricity) /
                                     (Total_05X_discharge_energy[70]))

Wh_energy_consumption_per_lifetime_kWh_05_70 = 1000*((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_05X_charge_energy[70]) /
                                             (Total_05X_discharge_energy[70]))
g_GHG_emissions_per_100miles_05_70 = g_GHG_emissions_per_lifetime_kWh_05_70 * fuel_economy
Wh_energy_consumption_per_100miles_05_70 = Wh_energy_consumption_per_lifetime_kWh_05_70 * fuel_economy

#====================Scenario 1.4: 0.5X Lifetime, Retire LIB at 65% SOH====================
g_GHG_emissions_per_lifetime_kWh_05_65 = 1000*((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                     GHG_emissions_of_manufacturing_one_ASSB_cell +
                                     Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                     Total_avoided_GHG_emissions + Total_05X_charge_energy[65] * EF_of_electricity) /
                                     (Total_05X_discharge_energy[65]))

Wh_energy_consumption_per_lifetime_kWh_05_65 = 1000*((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_05X_charge_energy[65]) /
                                             (Total_05X_discharge_energy[65]))
g_GHG_emissions_per_100miles_05_65 = g_GHG_emissions_per_lifetime_kWh_05_65 * fuel_economy
Wh_energy_consumption_per_100miles_05_65 = Wh_energy_consumption_per_lifetime_kWh_05_65 * fuel_economy

#====================Scenario 2.1: 1X Lifetime, Retire LIB at 80% SOH====================
g_GHG_emissions_per_lifetime_kWh_1X_80 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_1X_charge_energy[80] * EF_of_electricity) /
                                       (Total_1X_discharge_energy[80]))

Wh_energy_consumption_per_lifetime_kWh_1X_80 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_1X_charge_energy[80]) /
                                             (Total_1X_discharge_energy[80]))
g_GHG_emissions_per_100miles_1X_80 = g_GHG_emissions_per_lifetime_kWh_1X_80 * fuel_economy
Wh_energy_consumption_per_100miles_1X_80 = Wh_energy_consumption_per_lifetime_kWh_1X_80 * fuel_economy

#====================Scenario 2.2: 1X Lifetime, Retire LIB at 75% SOH====================
g_GHG_emissions_per_lifetime_kWh_1X_75 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_1X_charge_energy[75] * EF_of_electricity) /
                                       (Total_1X_discharge_energy[75]))

Wh_energy_consumption_per_lifetime_kWh_1X_75 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_1X_charge_energy[75]) /
                                             (Total_1X_discharge_energy[75]))
g_GHG_emissions_per_100miles_1X_75 = g_GHG_emissions_per_lifetime_kWh_1X_75 * fuel_economy
Wh_energy_consumption_per_100miles_1X_75 = Wh_energy_consumption_per_lifetime_kWh_1X_75 * fuel_economy

#====================Scenario 2.3: 1X Lifetime, Retire LIB at 70% SOH====================
g_GHG_emissions_per_lifetime_kWh_1X_70 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_1X_charge_energy[70] * EF_of_electricity) /
                                       (Total_1X_discharge_energy[70]))

Wh_energy_consumption_per_lifetime_kWh_1X_70 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_1X_charge_energy[70]) /
                                             (Total_1X_discharge_energy[70]))
g_GHG_emissions_per_100miles_1X_70 = g_GHG_emissions_per_lifetime_kWh_1X_70 * fuel_economy
Wh_energy_consumption_per_100miles_1X_70 = Wh_energy_consumption_per_lifetime_kWh_1X_70 * fuel_economy

#====================Scenario 2.4: 1X Lifetime, Retire LIB at 65% SOH====================
g_GHG_emissions_per_lifetime_kWh_1X_65 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_1X_charge_energy[65] * EF_of_electricity) /
                                       (Total_1X_discharge_energy[65]))

Wh_energy_consumption_per_lifetime_kWh_1X_65 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_1X_charge_energy[65]) /
                                             (Total_1X_discharge_energy[65]))
g_GHG_emissions_per_100miles_1X_65 = g_GHG_emissions_per_lifetime_kWh_1X_65 * fuel_economy
Wh_energy_consumption_per_100miles_1X_65 = Wh_energy_consumption_per_lifetime_kWh_1X_65 * fuel_economy

#====================Scenario 3.1: 2X Lifetime, Retire LIB at 80% SOH====================
g_GHG_emissions_per_lifetime_kWh_2X_80 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_2X_charge_energy[80] * EF_of_electricity) /
                                       (Total_2X_discharge_energy[80]))

Wh_energy_consumption_per_lifetime_kWh_2X_80 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_2X_charge_energy[80]) /
                                             (Total_2X_discharge_energy[80]))
g_GHG_emissions_per_100miles_2X_80 = g_GHG_emissions_per_lifetime_kWh_2X_80 * fuel_economy
Wh_energy_consumption_per_100miles_2X_80 = Wh_energy_consumption_per_lifetime_kWh_2X_80 * fuel_economy

#====================Scenario 3.2: 2X Lifetime, Retire LIB at 75% SOH====================
g_GHG_emissions_per_lifetime_kWh_2X_75 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_2X_charge_energy[75] * EF_of_electricity) /
                                       (Total_2X_discharge_energy[75]))

Wh_energy_consumption_per_lifetime_kWh_2X_75 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_2X_charge_energy[75]) /
                                             (Total_2X_discharge_energy[75]))
g_GHG_emissions_per_100miles_2X_75 = g_GHG_emissions_per_lifetime_kWh_2X_75 * fuel_economy
Wh_energy_consumption_per_100miles_2X_75 = Wh_energy_consumption_per_lifetime_kWh_2X_75 * fuel_economy

#====================Scenario 3.3: 2X Lifetime, Retire LIB at 70% SOH====================
g_GHG_emissions_per_lifetime_kWh_2X_70 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_2X_charge_energy[70] * EF_of_electricity) /
                                       (Total_2X_discharge_energy[70]))

Wh_energy_consumption_per_lifetime_kWh_2X_70 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_2X_charge_energy[70]) /
                                             (Total_2X_discharge_energy[70]))
g_GHG_emissions_per_100miles_2X_70 = g_GHG_emissions_per_lifetime_kWh_2X_70 * fuel_economy
Wh_energy_consumption_per_100miles_2X_70 = Wh_energy_consumption_per_lifetime_kWh_2X_70 * fuel_economy

#====================Scenario 3.4: 2X Lifetime, Retire LIB at 65% SOH====================
g_GHG_emissions_per_lifetime_kWh_2X_65 = 1000 * ((GHG_emissions_of_material_inputs_for_one_ASSB_cell +
                                       GHG_emissions_of_manufacturing_one_ASSB_cell +
                                       Total_GHG_emissions_to_recycle_one_ASSB_cell -
                                       Total_avoided_GHG_emissions + Total_2X_charge_energy[65] * EF_of_electricity) /
                                       (Total_2X_discharge_energy[65]))

Wh_energy_consumption_per_lifetime_kWh_2X_65 = 1000 * ((Embodied_energy_of_material_inputs_for_one_ASSB_cell +
                                             Energy_consumption_of_manufacturing_one_ASSB_cell +
                                             Total_energy_consumption_to_recycle_one_ASSB_cell -
                                             Total_avoided_energy_consumption + Total_2X_charge_energy[65]) /
                                             (Total_2X_discharge_energy[65]))
g_GHG_emissions_per_100miles_2X_65 = g_GHG_emissions_per_lifetime_kWh_2X_65 * fuel_economy
Wh_energy_consumption_per_100miles_2X_65 = Wh_energy_consumption_per_lifetime_kWh_2X_65 * fuel_economy

def print_summary(name, data, unit="g CO₂e", is_avoided=False):
    if is_avoided:
        mean_val = -data.mean()
        lower = -np.percentile(data, 97.5)
        upper = -np.percentile(data, 2.5)
        print(f"{name:<45} Mean: -{mean_val:,.2f} {unit}\t95% CI: [-{upper:,.2f}, -{lower:,.2f}] {unit}")
    else:
        mean_val = data.mean()
        lower = np.percentile(data, 2.5)
        upper = np.percentile(data, 97.5)
        print(f"{name:<45} Mean: {mean_val:,.2f} {unit}\t95% CI: [{lower:,.2f}, {upper:,.2f}] {unit}")

# === GHG Summary ===
print("\n=== GHG Emissions Summary for One ASSB Cell ===")
print_summary("1. Material Inputs", GHG_emissions_of_material_inputs_for_one_ASSB_cell)
print_summary("2. Manufacturing", GHG_emissions_of_manufacturing_one_ASSB_cell)
print_summary("3. Recycling", Total_GHG_emissions_to_recycle_one_ASSB_cell)
print_summary("4. Use Phase (Charging)", Total_1X_charge_energy[80] * EF_of_electricity)
print_summary("5. Avoided Emissions", Total_avoided_GHG_emissions, is_avoided=True)

# === Energy Summary ===
print("\n=== Energy Consumption Summary for One ASSB Cell ===")
print_summary("1. Material Inputs", Embodied_energy_of_material_inputs_for_one_ASSB_cell, unit="Wh")
print_summary("2. Manufacturing", Energy_consumption_of_manufacturing_one_ASSB_cell, unit="Wh")
print_summary("3. Recycling", Total_energy_consumption_to_recycle_one_ASSB_cell, unit="Wh")
print_summary("4. Use Phase (Charging)", Total_1X_charge_energy[80], unit="Wh")
print_summary("5. Avoided Energy Consumption", Total_avoided_energy_consumption, unit="Wh", is_avoided=True)

#--------------------Per lifetime kWh--------------------
# ========== Define scenarios and results ==========
ghg_energy_results = {
    "0.5X_80": (g_GHG_emissions_per_lifetime_kWh_05_80, Wh_energy_consumption_per_lifetime_kWh_05_80),
    "0.5X_75": (g_GHG_emissions_per_lifetime_kWh_05_75, Wh_energy_consumption_per_lifetime_kWh_05_75),
    "0.5X_70": (g_GHG_emissions_per_lifetime_kWh_05_70, Wh_energy_consumption_per_lifetime_kWh_05_70),
    "0.5X_65": (g_GHG_emissions_per_lifetime_kWh_05_65, Wh_energy_consumption_per_lifetime_kWh_05_65),

    "1X_80": (g_GHG_emissions_per_lifetime_kWh_1X_80, Wh_energy_consumption_per_lifetime_kWh_1X_80),
    "1X_75": (g_GHG_emissions_per_lifetime_kWh_1X_75, Wh_energy_consumption_per_lifetime_kWh_1X_75),
    "1X_70": (g_GHG_emissions_per_lifetime_kWh_1X_70, Wh_energy_consumption_per_lifetime_kWh_1X_70),
    "1X_65": (g_GHG_emissions_per_lifetime_kWh_1X_65, Wh_energy_consumption_per_lifetime_kWh_1X_65),

    "2X_80": (g_GHG_emissions_per_lifetime_kWh_2X_80, Wh_energy_consumption_per_lifetime_kWh_2X_80),
    "2X_75": (g_GHG_emissions_per_lifetime_kWh_2X_75, Wh_energy_consumption_per_lifetime_kWh_2X_75),
    "2X_70": (g_GHG_emissions_per_lifetime_kWh_2X_70, Wh_energy_consumption_per_lifetime_kWh_2X_70),
    "2X_65": (g_GHG_emissions_per_lifetime_kWh_2X_65, Wh_energy_consumption_per_lifetime_kWh_2X_65),
}

# ========== Output statistics ==========
print("=== GHG Emissions and Energy Consumption Summary ===")
for name, (ghg_array, energy_array) in ghg_energy_results.items():
    ghg_mean = np.mean(ghg_array)
    ghg_ci_lower = np.percentile(ghg_array, 2.5)
    ghg_ci_upper = np.percentile(ghg_array, 97.5)

    energy_mean = np.mean(energy_array)
    energy_ci_lower = np.percentile(energy_array, 2.5)
    energy_ci_upper = np.percentile(energy_array, 97.5)

    print(f"\n--- Scenario: {name} ---")
    print(f"GHG Emissions (g CO₂e/kWh): Mean = {ghg_mean:.2f}, 95% CI = [{ghg_ci_lower:.2f}, {ghg_ci_upper:.2f}]")
    print(
        f"Energy Consumption (Wh/kWh): Mean = {energy_mean:.2f}, 95% CI = [{energy_ci_lower:.2f}, {energy_ci_upper:.2f}]")


#--------------------Per 100 miles--------------------
# ========== Define scenarios and results ==========
ghg_energy_results_100miles = {
    "0.5X_80": (g_GHG_emissions_per_100miles_05_80, Wh_energy_consumption_per_100miles_05_80),
    "0.5X_75": (g_GHG_emissions_per_100miles_05_75, Wh_energy_consumption_per_100miles_05_75),
    "0.5X_70": (g_GHG_emissions_per_100miles_05_70, Wh_energy_consumption_per_100miles_05_70),
    "0.5X_65": (g_GHG_emissions_per_100miles_05_65, Wh_energy_consumption_per_100miles_05_65),

    "1X_80": (g_GHG_emissions_per_100miles_1X_80, Wh_energy_consumption_per_100miles_1X_80),
    "1X_75": (g_GHG_emissions_per_100miles_1X_75, Wh_energy_consumption_per_100miles_1X_75),
    "1X_70": (g_GHG_emissions_per_100miles_1X_70, Wh_energy_consumption_per_100miles_1X_70),
    "1X_65": (g_GHG_emissions_per_100miles_1X_65, Wh_energy_consumption_per_100miles_1X_65),

    "2X_80": (g_GHG_emissions_per_100miles_2X_80, Wh_energy_consumption_per_100miles_2X_80),
    "2X_75": (g_GHG_emissions_per_100miles_2X_75, Wh_energy_consumption_per_100miles_2X_75),
    "2X_70": (g_GHG_emissions_per_100miles_2X_70, Wh_energy_consumption_per_100miles_2X_70),
    "2X_65": (g_GHG_emissions_per_100miles_2X_65, Wh_energy_consumption_per_100miles_2X_65),
}

# ========== Output statistics ==========
print("\n=== GHG Emissions and Energy Consumption per 100 miles Summary ===")
for name, (ghg_array, energy_array) in ghg_energy_results_100miles.items():
    ghg_mean = np.mean(ghg_array)
    ghg_ci_lower = np.percentile(ghg_array, 2.5)
    ghg_ci_upper = np.percentile(ghg_array, 97.5)

    energy_mean = np.mean(energy_array)
    energy_ci_lower = np.percentile(energy_array, 2.5)
    energy_ci_upper = np.percentile(energy_array, 97.5)

    print(f"\n--- Scenario: {name} ---")
    print(f"GHG Emissions (g CO₂e/100miles): Mean = {ghg_mean:.2f}, 95% CI = [{ghg_ci_lower:.2f}, {ghg_ci_upper:.2f}]")
    print(f"Energy Consumption (Wh/100miles): Mean = {energy_mean:.2f}, 95% CI = [{energy_ci_lower:.2f}, {energy_ci_upper:.2f}]")
