import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# === LIB data ===
lib_data = {
    "80%": (473.53, 130.17, 868.17, 1185.68, 1043.72, 1338.25),
    "75%": (471.52, 126.55, 861.09, 1178.11, 1047.44, 1320.16),
    "70%": (470.12, 124.87, 858.39, 1173.19, 1048.49, 1307.16),
    "65%": (469.83, 125.39, 861.81, 1170.73, 1041.55, 1310.81)
}

# === ASSB data ===
assb_data = {
    "0.5X_80%": (610.77, 262.79, 1009.78, 1587.81, 1403.74, 1779.76),
    "0.5X_75%": (581.93, 233.09, 976.78, 1500.50, 1333.86, 1676.77),
    "0.5X_70%": (564.58, 214.03, 954.28, 1447.67, 1286.47, 1618.25),
    "0.5X_65%": (552.74, 201.73, 943.85, 1411.58, 1261.16, 1572.36),
    "1X_80%": (524.47, 180.13, 912.54, 1330.13, 1188.70, 1481.67),
    "1X_75%": (511.07, 163.35, 901.53, 1289.39, 1152.15, 1432.10),
    "1X_70%": (503.10, 155.94, 890.80, 1264.27, 1131.76, 1405.89),
    "1X_65%": (499.65, 147.65, 891.89, 1252.14, 1119.70, 1393.24),
    "2X_80%": (481.18, 136.53, 868.44, 1201.29, 1073.44, 1333.74),
    "2X_75%": (475.96, 127.61, 868.31, 1184.02, 1058.68, 1318.32),
    "2X_70%": (473.30, 123.98, 856.01, 1175.63, 1054.93, 1305.93),
    "2X_65%": (472.45, 122.38, 869.51, 1170.96, 1046.58, 1303.66)
}

# === Convert to DataFrame ===
lib_df = pd.DataFrame([
    {"Scenario": f"LIB {k}", "Mean GHG": v[0], "Lower GHG": v[1], "Upper GHG": v[2],
     "Mean Energy": v[3], "Lower Energy": v[4], "Upper Energy": v[5]} for k, v in lib_data.items()
])

assb_df = pd.DataFrame([
    {"Scenario": f"ASSB {k}", "Mean GHG": v[0], "Lower GHG": v[1], "Upper GHG": v[2],
     "Mean Energy": v[3], "Lower Energy": v[4], "Upper Energy": v[5]} for k, v in assb_data.items()
])

# === Combine and reorder ===
ordered_df = pd.concat([assb_df.sort_values("Scenario"), lib_df.sort_values("Scenario")], ignore_index=True)

# === Custom color mapping ===
color_map = {
    "ASSB_0.5X": "#2b8ad6",
    "ASSB_1X": "#63b2ee",
    "ASSB_2X": "#99c9f5",
    "LIB": "#f89588"
}

def assign_custom_color(scenario):
    if "0.5X" in scenario:
        return color_map["ASSB_0.5X"]
    elif "1X" in scenario:
        return color_map["ASSB_1X"]
    elif "2X" in scenario:
        return color_map["ASSB_2X"]
    elif "LIB" in scenario:
        return color_map["LIB"]
    else:
        return "gray"

ordered_df["GroupColor"] = ordered_df["Scenario"].apply(assign_custom_color)
x = np.arange(len(ordered_df))

# === Create combined figure ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios': [1, 1]})

# === Plot GHG Emissions ===
ax1.bar(x, ordered_df["Mean GHG"],
        yerr=[ordered_df["Mean GHG"] - ordered_df["Lower GHG"],
              ordered_df["Upper GHG"] - ordered_df["Mean GHG"]],
        capsize=5, color=ordered_df["GroupColor"])
ax1.set_ylabel("GHG Emissions (g CO₂e/kWh)")
ax1.set_title("GHG Emissions per Lifetime kWh (with 95% CI)")
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# === Plot Energy Consumption ===
ax2.bar(x, ordered_df["Mean Energy"],
        yerr=[ordered_df["Mean Energy"] - ordered_df["Lower Energy"],
              ordered_df["Upper Energy"] - ordered_df["Mean Energy"]],
        capsize=5, color=ordered_df["GroupColor"])
ax2.set_ylabel("Energy Consumption (Wh/kWh)")
ax2.set_title("Energy Consumption per Lifetime kWh (with 95% CI)")
ax2.set_xticks(x)
ax2.set_xticklabels(ordered_df["Scenario"], rotation=90)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# === Shared legend below ===
patches = [mpatches.Patch(color=hex_color, label=label) for label, hex_color in color_map.items()]
legend = fig.legend(handles=patches, loc="lower center", ncol=4, bbox_to_anchor=(0.5, 0.02))
legend.get_frame().set_linewidth(0)  # Remove border around legend

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()


#--------------------Per 100 miles-------------------
# === LIB data (per 100 miles) - converted to kg and kWh ===
lib_data_100miles = {
    "80%": (17046.03/1000, 4392.46/1000, 32880.21/1000, 42236.14/1000, 30633.52/1000, 55172.78/1000),
    "75%": (16967.45/1000, 4272.89/1000, 32575.44/1000, 41937.69/1000, 30474.16/1000, 54463.95/1000),
    "70%": (16942.82/1000, 4288.20/1000, 32646.60/1000, 41844.05/1000, 30476.40/1000, 54517.50/1000),
    "65%": (16965.25/1000, 4191.69/1000, 32782.15/1000, 41828.09/1000, 30495.55/1000, 54480.99/1000)
}

# === ASSB data (per 100 miles) - converted to kg and kWh ===
assb_data_100miles = {
    "0.5X_80%": (21900.28/1000, 9051.12/1000, 38791.25/1000, 56742.08/1000, 41158.22/1000, 74013.83/1000),
    "0.5X_75%": (20851.01/1000, 8070.71/1000, 37548.23/1000, 53582.07/1000, 38956.64/1000, 69678.05/1000),
    "0.5X_70%": (20221.48/1000, 7451.05/1000, 36862.04/1000, 51679.08/1000, 37646.54/1000, 66981.25/1000),
    "0.5X_65%": (19830.73/1000, 7033.40/1000, 36518.93/1000, 50455.95/1000, 36717.51/1000, 65424.09/1000),
    "1X_80%": (18791.18/1000, 6270.33/1000, 35054.15/1000, 47526.33/1000, 34586.36/1000, 61645.62/1000),
    "1X_75%": (18326.55/1000, 5671.20/1000, 34700.75/1000, 46060.95/1000, 33532.75/1000, 59661.36/1000),
    "1X_70%": (18057.00/1000, 5443.74/1000, 34325.69/1000, 45221.51/1000, 32882.94/1000, 58631.05/1000),
    "1X_65%": (17880.01/1000, 5240.18/1000, 34352.79/1000, 44665.49/1000, 32441.67/1000, 57725.29/1000),
    "2X_80%": (17242.19/1000, 4840.97/1000, 33324.04/1000, 42893.06/1000, 31262.42/1000, 55427.17/1000),
    "2X_75%": (17071.85/1000, 4590.98/1000, 33123.80/1000, 42331.10/1000, 30937.91/1000, 54698.60/1000),
    "2X_70%": (16958.50/1000, 4378.32/1000, 32857.16/1000, 41966.66/1000, 30481.58/1000, 54458.74/1000),
    "2X_65%": (16921.80/1000, 4299.69/1000, 33024.35/1000, 41804.93/1000, 30481.30/1000, 54048.88/1000)
}

# === Convert to DataFrame ===
lib_df = pd.DataFrame([
    {"Scenario": f"LIB {k}", "Mean GHG": v[0], "Lower GHG": v[1], "Upper GHG": v[2],
     "Mean Energy": v[3], "Lower Energy": v[4], "Upper Energy": v[5]} for k, v in lib_data_100miles.items()
])

assb_df = pd.DataFrame([
    {"Scenario": f"ASSB {k}", "Mean GHG": v[0], "Lower GHG": v[1], "Upper GHG": v[2],
     "Mean Energy": v[3], "Lower Energy": v[4], "Upper Energy": v[5]} for k, v in assb_data_100miles.items()
])

# === Combine and reorder ===
ordered_df = pd.concat([assb_df.sort_values("Scenario"), lib_df.sort_values("Scenario")], ignore_index=True)

# === Custom color mapping ===
color_map = {
    "ASSB_0.5X": "#2b8ad6",
    "ASSB_1X": "#63b2ee",
    "ASSB_2X": "#99c9f5",
    "LIB": "#f89588"
}

def assign_custom_color(scenario):
    if "0.5X" in scenario:
        return color_map["ASSB_0.5X"]
    elif "1X" in scenario:
        return color_map["ASSB_1X"]
    elif "2X" in scenario:
        return color_map["ASSB_2X"]
    elif "LIB" in scenario:
        return color_map["LIB"]
    else:
        return "gray"

ordered_df["GroupColor"] = ordered_df["Scenario"].apply(assign_custom_color)
x = np.arange(len(ordered_df))

# === Create combined figure ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True, gridspec_kw={'height_ratios': [1, 1]})

# === Plot GHG Emissions ===
ax1.bar(x, ordered_df["Mean GHG"],
        yerr=[ordered_df["Mean GHG"] - ordered_df["Lower GHG"],
              ordered_df["Upper GHG"] - ordered_df["Mean GHG"]],
        capsize=5, color=ordered_df["GroupColor"])
ax1.set_ylabel("GHG Emissions (kg CO₂e/100 miles)")
ax1.set_title("GHG Emissions per 100 miles (with 95% CI)")
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# === Plot Energy Consumption ===
ax2.bar(x, ordered_df["Mean Energy"],
        yerr=[ordered_df["Mean Energy"] - ordered_df["Lower Energy"],
              ordered_df["Upper Energy"] - ordered_df["Mean Energy"]],
        capsize=5, color=ordered_df["GroupColor"])
ax2.set_ylabel("Energy Consumption (kWh/100 miles)")
ax2.set_title("Energy Consumption per 100 miles (with 95% CI)")
ax2.set_xticks(x)
ax2.set_xticklabels(ordered_df["Scenario"], rotation=90)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# === Shared legend below ===
patches = [mpatches.Patch(color=hex_color, label=label) for label, hex_color in color_map.items()]
legend = fig.legend(handles=patches, loc="lower center", ncol=4, bbox_to_anchor=(0.5, 0.02))
legend.get_frame().set_linewidth(0)  # Remove border around legend

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()

# Set font sizes for all text elements (add this right before plt.show() for each figure)
plt.rc('axes', titlesize=16)    # Axes title size
plt.rc('axes', labelsize=14)    # X and Y labels size
plt.rc('xtick', labelsize=12)   # X tick labels size
plt.rc('ytick', labelsize=12)   # Y tick labels size
plt.rc('legend', fontsize=10)   # Legend font size

# For the first figure (per kWh)
plt.show()
fig.savefig("ghg_energy_per_kWh.png", dpi=300, bbox_inches='tight')

# For the second figure (per 100 miles)
plt.show()
fig.savefig("ghg_energy_per_100miles.png", dpi=300, bbox_inches='tight')