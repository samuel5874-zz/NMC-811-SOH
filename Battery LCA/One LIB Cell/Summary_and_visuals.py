import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# All GHG emissions are expressed in grams of CO₂-equivalent (g CO₂e), and all energy consumption values are in watt-hours (Wh).
EF_of_electricity = np.random.triangular(left=0.0009, mode=0.3589, right=0.8713, size=10000)
fuel_economy = np.random.triangular(24, 35, 48, 10000)
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
Total_charge_energy = generate_triangular_samples_from_excel("Total_charge_energy.xlsx")
Total_discharge_energy = generate_triangular_samples_from_excel("Total_discharge_energy.xlsx")

#====================Scenario 1: Retire LIB at 80% SOH====================
g_GHG_emissions_per_lifetime_kWh_80 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell+
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions+Total_charge_energy[80]*EF_of_electricity)/(Total_discharge_energy[80]))
g_GHG_emissions_per_100miles_80 = g_GHG_emissions_per_lifetime_kWh_80 * fuel_economy

Wh_energy_consumption_per_lifetime_kWh_80 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption + Total_charge_energy[80]
                                             )/(Total_discharge_energy[80]))
Wh_energy_consumption_per_100miles_80 = Wh_energy_consumption_per_lifetime_kWh_80 * fuel_economy

#====================Scenario 2: Retire LIB at 75% SOH====================
g_GHG_emissions_per_lifetime_kWh_75 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell +
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions + Total_charge_energy[75] * EF_of_electricity) /
                                     (Total_discharge_energy[75]))
g_GHG_emissions_per_100miles_75 = g_GHG_emissions_per_lifetime_kWh_75 * fuel_economy

Wh_energy_consumption_per_lifetime_kWh_75 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption + Total_charge_energy[75]) /
                                             (Total_discharge_energy[75]))
Wh_energy_consumption_per_100miles_75 = Wh_energy_consumption_per_lifetime_kWh_75 * fuel_economy


#====================Scenario 3: Retire LIB at 70% SOH====================
g_GHG_emissions_per_lifetime_kWh_70 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell +
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions + Total_charge_energy[70] * EF_of_electricity) /
                                     (Total_discharge_energy[70]))
g_GHG_emissions_per_100miles_70 = g_GHG_emissions_per_lifetime_kWh_70 * fuel_economy

Wh_energy_consumption_per_lifetime_kWh_70 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption + Total_charge_energy[70]) /
                                             (Total_discharge_energy[70]))
Wh_energy_consumption_per_100miles_70 = Wh_energy_consumption_per_lifetime_kWh_70 * fuel_economy


#====================Scenario 4: Retire LIB at 65% SOH====================
g_GHG_emissions_per_lifetime_kWh_65 = 1000*((GHG_emissions_of_material_inputs_for_one_LIB_cell +
                                     GHG_emissions_of_manufacturing_one_LIB_cell +
                                     GHG_emissions_of_recycling_one_LIB_cell -
                                     Total_avoided_GHG_emissions + Total_charge_energy[65] * EF_of_electricity) /
                                     (Total_discharge_energy[65]))
g_GHG_emissions_per_100miles_65 = g_GHG_emissions_per_lifetime_kWh_65 * fuel_economy

Wh_energy_consumption_per_lifetime_kWh_65 = 1000*((Embodied_energy_of_material_inputs_for_one_LIB_cell +
                                             Energy_consumption_of_manufacturing_one_LIB_cell +
                                             Energy_consumption_of_recycling_one_LIB_cell -
                                             Total_avoided_energy_consumption + Total_charge_energy[65]) /
                                             (Total_discharge_energy[65]))
Wh_energy_consumption_per_100miles_65 = Wh_energy_consumption_per_lifetime_kWh_65 * fuel_economy

def print_summary(name, data, unit="g CO₂e", is_avoided=False, width=35):
    if is_avoided:
        mean_val = -data.mean()
        lower = -np.percentile(data, 97.5)
        upper = -np.percentile(data, 2.5)
        print(f"{name:<{width}} Mean: -{mean_val:,.2f} {unit}\t95% CI: [-{upper:,.2f}, -{lower:,.2f}] {unit}")
    else:
        mean_val = data.mean()
        lower = np.percentile(data, 2.5)
        upper = np.percentile(data, 97.5)
        print(f"{name:<{width}} Mean: {mean_val:,.2f} {unit}\t95% CI: [{lower:,.2f}, {upper:,.2f}] {unit}")

# === GHG Summary for One LIB Cell ===
print("\n=== GHG Emissions Summary for One LIB Cell ===")
print_summary("1. Material Inputs", GHG_emissions_of_material_inputs_for_one_LIB_cell)
print_summary("2. Manufacturing", GHG_emissions_of_manufacturing_one_LIB_cell)
print_summary("3. Use Phase (Charging)", Total_charge_energy[80] * EF_of_electricity)
print_summary("4. Recycling", GHG_emissions_of_recycling_one_LIB_cell)
print_summary("5. Avoided Emissions", Total_avoided_GHG_emissions, is_avoided=True)

# === Energy Summary for One LIB Cell ===
print("\n=== Energy Consumption Summary for One LIB Cell ===")
print_summary("1. Material Inputs", Embodied_energy_of_material_inputs_for_one_LIB_cell, unit="Wh")
print_summary("2. Manufacturing", Energy_consumption_of_manufacturing_one_LIB_cell, unit="Wh")
print_summary("3. Use Phase (Charging)", Total_charge_energy[80], unit="Wh")
print_summary("4. Recycling", Energy_consumption_of_recycling_one_LIB_cell, unit="Wh")
print_summary("5. Avoided Energy Consumption", Total_avoided_energy_consumption, unit="Wh", is_avoided=True)


def report_lifetime_performance(name, ghg_array, energy_array):
    ghg_mean = np.mean(ghg_array)
    ghg_ci = np.percentile(ghg_array, [2.5, 97.5])

    energy_mean = np.mean(energy_array)
    energy_ci = np.percentile(energy_array, [2.5, 97.5])

    print(f"\n=== Scenario: Retire at {name}% SoH ===")
    print(f"GHG Emissions per Lifetime kWh: {ghg_mean:.2f} g CO₂e "
          f"[95% CI: {ghg_ci[0]:.2f}, {ghg_ci[1]:.2f}]")
    print(f"Energy Consumption per Lifetime kWh: {energy_mean:.2f} Wh "
          f"[95% CI: {energy_ci[0]:.2f}, {energy_ci[1]:.2f}]")


# Call the renamed function
report_lifetime_performance(80, g_GHG_emissions_per_lifetime_kWh_80, Wh_energy_consumption_per_lifetime_kWh_80)
report_lifetime_performance(75, g_GHG_emissions_per_lifetime_kWh_75, Wh_energy_consumption_per_lifetime_kWh_75)
report_lifetime_performance(70, g_GHG_emissions_per_lifetime_kWh_70, Wh_energy_consumption_per_lifetime_kWh_70)
report_lifetime_performance(65, g_GHG_emissions_per_lifetime_kWh_65, Wh_energy_consumption_per_lifetime_kWh_65)


def report_performance_per_100miles(name, ghg_array, energy_array):
    """
    Print GHG and energy consumption per 100 miles with 95% confidence interval.
    """
    ghg_mean = np.mean(ghg_array)
    ghg_ci = np.percentile(ghg_array, [2.5, 97.5])

    energy_mean = np.mean(energy_array)
    energy_ci = np.percentile(energy_array, [2.5, 97.5])

    print(f"\n=== Scenario: Retire at {name}% SoH ===")
    print(f"{'GHG Emissions per 100 miles:':40} {ghg_mean:,.2f} g CO₂e\t"
          f"[95% CI: {ghg_ci[0]:,.2f}, {ghg_ci[1]:,.2f}]")
    print(f"{'Energy Consumption per 100 miles:':40} {energy_mean:,.2f} Wh\t"
          f"[95% CI: {energy_ci[0]:,.2f}, {energy_ci[1]:,.2f}]")

# === Call the function for each SoH scenario ===
report_performance_per_100miles(80, g_GHG_emissions_per_100miles_80, Wh_energy_consumption_per_100miles_80)
report_performance_per_100miles(75, g_GHG_emissions_per_100miles_75, Wh_energy_consumption_per_100miles_75)
report_performance_per_100miles(70, g_GHG_emissions_per_100miles_70, Wh_energy_consumption_per_100miles_70)
report_performance_per_100miles(65, g_GHG_emissions_per_100miles_65, Wh_energy_consumption_per_100miles_65)
