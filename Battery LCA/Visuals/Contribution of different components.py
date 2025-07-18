import matplotlib.pyplot as plt
import numpy as np

#--------------------GHG Emissions--------------------
phases_stacked = ["Use Phase (Charging)", "Material Inputs", "Manufacturing", "Recycling"]
lib_ghg = [103632.47, 6866.95, 2928.05, 1726.03]
assb_ghg = [75889.81, 10902.92, 3572.59, 7554.12]
lib_ghg_avoided = -3612.10
assb_ghg_avoided = -7098.19

lib_ghg = [val / 1000 for val in lib_ghg]
assb_ghg = [val / 1000 for val in assb_ghg]
lib_ghg_avoided /= 1000
assb_ghg_avoided /= 1000

#--------------------Energy Consumption--------------------
lib_energy = [251776.02, 25989.00, 7153.14, 6909.14]
assb_energy = [184415.74, 35940.23, 8667.49, 19070.57]
lib_energy_avoided = -13462.09
assb_energy_avoided = -19153.47

lib_energy = [val / 1000 for val in lib_energy]
assb_energy = [val / 1000 for val in assb_energy]
lib_energy_avoided /= 1000
assb_energy_avoided /= 1000

#====================Plot Horizontal Figure====================
x = np.array([0, 0.4])
width = 0.18

colors = ['#C76DA2', '#A1A9D0', '#F0988C', '#96CCCB']
avoided_color = '#E7DAD2'
labels = phases_stacked + ['Avoided']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6), sharey=False)

# === GHG Emissions Plot ===
lib_cumsum = np.cumsum([0] + lib_ghg[:-1])
assb_cumsum = np.cumsum([0] + assb_ghg[:-1])
for i in range(len(phases_stacked)):
    ax1.bar(x[0], lib_ghg[i], bottom=lib_cumsum[i], width=width, color=colors[i])
    ax1.bar(x[1], assb_ghg[i], bottom=assb_cumsum[i], width=width, color=colors[i])
ax1.bar(x[0], lib_ghg_avoided, bottom=0, width=width, color=avoided_color)
ax1.bar(x[1], assb_ghg_avoided, bottom=0, width=width, color=avoided_color)
ax1.set_title('Lifetime GHG Emissions of one battery cell')
ax1.set_ylabel('kg CO₂e')
ax1.set_xticks(x)
ax1.set_xticklabels(['LIB', 'ASSB'])
ax1.axhline(0, color='black', linewidth=0.8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(True)
ax1.tick_params(axis='both', which='both', length=0)

# === Energy Plot ===
lib_cumsum = np.cumsum([0] + lib_energy[:-1])
assb_cumsum = np.cumsum([0] + assb_energy[:-1])
for i in range(len(phases_stacked)):
    ax2.bar(x[0], lib_energy[i], bottom=lib_cumsum[i], width=width, color=colors[i])
    ax2.bar(x[1], assb_energy[i], bottom=assb_cumsum[i], width=width, color=colors[i])
ax2.bar(x[0], lib_energy_avoided, bottom=0, width=width, color=avoided_color)
ax2.bar(x[1], assb_energy_avoided, bottom=0, width=width, color=avoided_color)
ax2.set_title('Lifetime energy use of one battery cell')
ax2.set_ylabel('kWh')
ax2.set_xticks(x)
ax2.set_xticklabels(['LIB', 'ASSB'])
ax2.axhline(0, color='black', linewidth=0.8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(True)
ax2.tick_params(axis='both', which='both', length=0)

# === Shared Legend ===
legend_handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colors] + \
                 [plt.Rectangle((0, 0), 1, 1, color=avoided_color)]

fig.subplots_adjust(right=0.75)  # leave space for legend
fig.legend(legend_handles, labels, loc='center left', bbox_to_anchor=(0.77, 0.5),
           frameon=False, bbox_transform=fig.transFigure)

#Set font size
ax1.set_title('Lifetime GHG Emissions of one battery cell', fontsize=14)
ax1.set_ylabel('kg CO₂e', fontsize=14)
ax1.set_xticklabels(['LIB', 'ASSB'], fontsize=14)

ax2.set_title('Lifetime energy use of one battery cell', fontsize=14)
ax2.set_ylabel('kWh', fontsize=14)
ax2.set_xticklabels(['LIB', 'ASSB'], fontsize=14)

fig.legend(legend_handles, labels, loc='center left', bbox_to_anchor=(0.77, 0.5),
           frameon=False, bbox_transform=fig.transFigure, fontsize=10)

plt.show()

# === Save the figure ===
fig.savefig("lifetime_ghg_energy_bars.png", dpi=300, bbox_inches='tight')