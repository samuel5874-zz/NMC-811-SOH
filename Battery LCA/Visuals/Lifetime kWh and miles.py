import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# All GHG emissions are expressed in grams of CO₂-equivalent (g CO₂e), and all energy consumption values are in watt-hours (Wh).
# Number of simulations
n_simulations = 10000
fuel_economy = np.random.triangular(24, 35, 48, 10000)

# Function to read Excel and generate Monte Carlo samples
def generate_samples_from_excel(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()  # Remove any extra spaces in column names
    samples = {}

    for _, row in df.iterrows():
        var_name = row['Retiring at (%)']
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

LIB_discharge_energy = generate_samples_from_excel("Total_discharge_energy.xlsx")
Lifetime_miles_LIB_80 = LIB_discharge_energy[80]/1000/fuel_economy*100
Lifetime_miles_LIB_75 = LIB_discharge_energy[75]/1000/fuel_economy*100
Lifetime_miles_LIB_70 = LIB_discharge_energy[70]/1000/fuel_economy*100
Lifetime_miles_LIB_65 = LIB_discharge_energy[65]/1000/fuel_economy*100

ASSB_05X_discharge_energy = generate_samples_from_excel("0.5X_Total_discharge_energy.xlsx")
Lifetime_miles_ASSB_05X_80 = ASSB_05X_discharge_energy[80]/1000/fuel_economy*100
Lifetime_miles_ASSB_05X_75 = ASSB_05X_discharge_energy[75]/1000/fuel_economy*100
Lifetime_miles_ASSB_05X_70 = ASSB_05X_discharge_energy[70]/1000/fuel_economy*100
Lifetime_miles_ASSB_05X_65 = ASSB_05X_discharge_energy[65]/1000/fuel_economy*100

ASSB_1X_discharge_energy = generate_samples_from_excel("1X_Total_discharge_energy.xlsx")
Lifetime_miles_ASSB_1X_80 = ASSB_1X_discharge_energy[80]/1000/fuel_economy*100
Lifetime_miles_ASSB_1X_75 = ASSB_1X_discharge_energy[75]/1000/fuel_economy*100
Lifetime_miles_ASSB_1X_70 = ASSB_1X_discharge_energy[70]/1000/fuel_economy*100
Lifetime_miles_ASSB_1X_65 = ASSB_1X_discharge_energy[65]/1000/fuel_economy*100

ASSB_2X_discharge_energy = generate_samples_from_excel("2X_Total_discharge_energy.xlsx")
Lifetime_miles_ASSB_2X_80 = ASSB_2X_discharge_energy[80]/1000/fuel_economy*100
Lifetime_miles_ASSB_2X_75 = ASSB_2X_discharge_energy[75]/1000/fuel_economy*100
Lifetime_miles_ASSB_2X_70 = ASSB_2X_discharge_energy[70]/1000/fuel_economy*100
Lifetime_miles_ASSB_2X_65 = ASSB_2X_discharge_energy[65]/1000/fuel_economy*100

#--------------------Do statistics for Lifetime Wh--------------------
scenarios = {
    'LIB': LIB_discharge_energy,
    'ASSB_05X': ASSB_05X_discharge_energy,
    'ASSB_1X': ASSB_1X_discharge_energy,
    'ASSB_2X': ASSB_2X_discharge_energy
}

thresholds = [80, 75, 70, 65]

for name, data in scenarios.items():
    print(f"\n=== {name} Discharge Energy ===")
    for threshold in thresholds:
        samples = data[threshold]
        mean = samples.mean()
        lower = np.percentile(samples, 2.5)
        upper = np.percentile(samples, 97.5)

        print(f"Retiring at {threshold}%:")
        print(f"  Mean: {mean:.2f} Wh")
        print(f"  95% Confidence Interval: [{lower:.2f}, {upper:.2f}] Wh")

#--------------------Do statistics for Lifetime miles--------------------
lifetime_miles_sources = {
    'LIB': LIB_discharge_energy,
    'ASSB_05X': ASSB_05X_discharge_energy,
    'ASSB_1X': ASSB_1X_discharge_energy,
    'ASSB_2X': ASSB_2X_discharge_energy
}

retire_levels = [80, 75, 70, 65]

for system_name, discharge_data in lifetime_miles_sources.items():
    print(f"\n=== {system_name} Lifetime Miles ===")
    for retire_at in retire_levels:
        lifetime_miles_samples = discharge_data[retire_at] / 1000 / fuel_economy * 100
        mean = lifetime_miles_samples.mean()
        lower = np.percentile(lifetime_miles_samples, 2.5)
        upper = np.percentile(lifetime_miles_samples, 97.5)

        print(f"Retiring at {retire_at}%:")
        print(f"  Mean: {mean:.2f} miles")
        print(f"  95% Confidence Interval: [{lower:.2f}, {upper:.2f}] miles")

#--------------------Figure--------------------
plt.rcParams.update({
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 10
})

# === Input data ===
retiring_levels = [80, 75, 70, 65]

wh_means = {
    "LIB": [235470.18, 259750.67, 277380.57, 291651.47],
    "ASSB_05X": [86325.16, 105629.21, 122772.88, 138075.28],
    "ASSB_1X": [172434.13, 211338.24, 244933.24, 275881.91],
    "ASSB_2X": [344505.30, 422406.78, 490296.07, 551479.71],
}
wh_ci = {
    "LIB": [(215334.12, 256967.81), (240133.77, 281430.89), (256627.78, 300641.51), (269568.53, 316583.16)],
    "ASSB_05X": [(80102.90, 93377.12), (97934.22, 114332.10), (113821.74, 132744.81), (128118.61, 149367.11)],
    "ASSB_1X": [(160052.02, 186553.57), (195759.42, 228485.99), (227188.08, 264989.77), (255818.94, 298305.28)],
    "ASSB_2X": [(319255.48, 372805.29), (391955.83, 457243.84), (454785.57, 530391.93), (511622.50, 596320.29)],
}

# Convert Wh → kWh
kwh_means = {k: [val / 1000 for val in v] for k, v in wh_means.items()}
kwh_ci = {
    k: [(low / 1000, high / 1000) for (low, high) in wh_ci[k]]
    for k in wh_ci
}

miles_means = {
    "LIB": [672.65, 741.94, 792.32, 833.16],
    "ASSB_05X": [246.60, 301.73, 350.69, 394.40],
    "ASSB_1X": [492.54, 603.68, 699.65, 788.06],
    "ASSB_2X": [984.10, 1206.54, 1400.55, 1575.31],
}
miles_ci = {
    "LIB": [(509.46, 892.36), (565.05, 982.82), (604.17, 1048.18), (631.95, 1106.69)],
    "ASSB_05X": [(187.47, 325.93), (230.22, 399.92), (267.64, 464.23), (299.97, 523.63)],
    "ASSB_1X": [(375.02, 654.08), (459.35, 797.56), (530.83, 925.98), (601.26, 1046.63)],
    "ASSB_2X": [(747.60, 1308.32), (920.12, 1596.85), (1070.32, 1859.76), (1199.65, 2080.30)],
}

# === Custom Colors ===
left_colors = {
    "LIB": "#8ECFC9",
    "ASSB_05X": "#FFBE7A",
    "ASSB_1X": "#FA7F6F",
    "ASSB_2X": "#82B0D2"
}
right_colors = ["#2878b5", "#9ac9db", "#f8ac8c", "#c82423"]  # SOH: 80 → 65

# === First figure: Discharge Energy ===
fig1, ax1 = plt.subplots(figsize=(7, 5))  # 独立图像

for name in kwh_means:
    y = kwh_means[name]
    yerr = [[y[i] - kwh_ci[name][i][0] for i in range(4)],
            [kwh_ci[name][i][1] - y[i] for i in range(4)]]
    linestyle = '--' if name == 'LIB' else '-'
    ax1.errorbar(
        retiring_levels, y, yerr=yerr, label=name, capsize=5, marker='o',
        linestyle=linestyle, color=left_colors[name], linewidth=2
    )

ax1.set_title("Total Discharge Energy vs. Retiring SOH")
ax1.set_xlabel("Retiring SOH (%)")
ax1.set_ylabel("Energy (kWh)")
ax1.set_xticks([80, 75, 70, 65])
ax1.set_xticklabels([80, 75, 70, 65])
ax1.legend(frameon=False)
ax1.grid(False)

plt.tight_layout()
plt.show()

# === Second figure: Lifetime Miles ===
fig2, ax2 = plt.subplots(figsize=(7, 5))  # 独立图像

bar_width = 0.2
x = np.arange(len(miles_means))  # 4 battery types

for i, level in enumerate(retiring_levels):
    y = [miles_means[b][i] for b in miles_means]
    yerr = [[y[j] - miles_ci[b][i][0] for j, b in enumerate(miles_means)],
            [miles_ci[b][i][1] - y[j] for j, b in enumerate(miles_means)]]
    ax2.bar(
        x + i * bar_width, y, width=bar_width, yerr=yerr,
        label=f"SOH {level}%", capsize=4, color=right_colors[i]
    )

ax2.set_title("Lifetime Miles by Battery Type")
ax2.set_xlabel("Battery Type")
ax2.set_ylabel("Lifetime Miles")
ax2.set_xticks(x + bar_width * 1.5)
ax2.set_xticklabels(list(miles_means.keys()))
ax2.legend(title="Retiring SOH", frameon=False)
ax2.grid(False)

plt.tight_layout()
plt.show()

fig1.savefig("discharge_energy.png", dpi=300, bbox_inches='tight')
fig2.savefig("lifetime_miles.png", dpi=300, bbox_inches='tight')