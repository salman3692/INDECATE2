import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# Check the scenario and set variables accordingly
scenario = 4  # Change this value to select the scenario

if scenario == 1:
    excel_file_path = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_V2_031024.xlsx'
    sheet_name = 'SUM'
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    cost = df['2024_Scenario'].tolist()
    plot_title = '2024 Scenario'
elif scenario == 2:
    excel_file_path = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_V2_031024.xlsx'
    sheet_name = 'SUM'
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    cost = df['2030_Scenario'].tolist()
    plot_title = '2030 Scenario'
elif scenario == 3:
    excel_file_path = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_V2_031024.xlsx'
    sheet_name = 'SUM'
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    cost = df['2040_Scenario'].tolist()
    plot_title = '2040 Scenario'
elif scenario == 4:
    excel_file_path = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_V2_031024.xlsx'
    sheet_name = 'SUM'
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    cost = df['2050_Scenario'].tolist()
    plot_title = '2050 Scenario'
else:
    print("Scenario not recognized")
    exit()

# Extract data for each case
emissions = df['EI'].tolist()
spec_energy = df['Spec_Energy'].tolist()

# Create a 2D scatter plot with a color bar
fig, ax = plt.subplots()

# Define 10 markers for the 10 cases
markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*', 'h']

# Create a ScalarMappable for mapping the color to the spec_energy values
norm = Normalize(vmin=min(spec_energy), vmax=max(spec_energy))
cmap = plt.get_cmap('gnuplot_r')
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

# Loop through each case and plot with a unique marker and color
for i, case in enumerate(df['Case']):
    marker = markers[i % len(markers)]  # Cycle through markers if more cases than markers
    color = cmap(norm(spec_energy[i]))
    ax.scatter(cost[i], emissions[i], marker=marker, s=60, label=case, color=color)

# Set labels for the axes
ax.set_xlabel('Cost (€/t of Glass)')
ax.set_ylabel('Emissions (t of CO2/t of glass)')

# Set x-axis limits (for example, you can adjust the min and max values as needed)
# x_min = 200 # Adjust as needed
# x_max = 550  # Adjust as needed
x_min = min(cost) - 30  # Adjust as needed
x_max = max(cost) + 30  # Adjust as needed
ax.set_xlim(x_min, x_max)

# Add a color bar representing Spec Energy
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Spec Energy (GJ/t of glass)')  # Ensure the units match the data

# Set title for the plot
plt.title(plot_title)

# Add legend with proper settings
ax.legend(fontsize='small', ncol=1)

# Set the size of the plot
plt.gcf().set_size_inches(6, 6)

# Save the plot with the title and scenario condition
plot_file_path = f"{plot_title.replace(' ', '_').lower()}_scenario_{scenario}.png"
# plt.savefig(plot_file_path)

plt.show()
