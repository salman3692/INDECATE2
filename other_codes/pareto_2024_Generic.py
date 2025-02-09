import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

Industry = 'Glass'
Product = 'Glass'

# Check the scenario and set variables accordingly
scenario = 1  # Change this value to select the scenario

# Define Excel file and sheet name
excel_file_path = r'c:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_TESTING.xlsx'
sheet_name = 'SUM'

# Read data from the Excel file
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# Find the cost for "Base Case" in the 2024 scenario
base_case_row = df[df.iloc[:, 0] == "Base_Case"]  # Assuming "Base Case" is in the first column
if not base_case_row.empty:
    base_case_cost = base_case_row['2024_Scenario'].values[0]  # Get the value for 2024_Scenario

# Based on the scenario, choose the correct cost and title
if scenario == 1:
    cost = df['2024_Scenario'].tolist()
    plot_title = '2024 Scenario'
elif scenario == 2:
    cost = df['2030_Scenario'].tolist()
    plot_title = '2030 Scenario'
elif scenario == 3:
    cost = df['2040_Scenario'].tolist()
    plot_title = '2040 Scenario'
elif scenario == 4:
    cost = df['2050_Scenario'].tolist()
    plot_title = '2050 Scenario'
else:
    print("Scenario not recognized")
    exit()

# Extract data for emissions and specific energy
emissions = df['EI'].tolist()
spec_energy = df['Spec_Energy'].tolist()

# Create a 2D scatter plot with a color bar
fig, ax = plt.subplots()

# Define 10 markers for different cases
markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*', 'h']

# Normalize and map the color to spec_energy values
norm = Normalize(vmin=min(spec_energy), vmax=max(spec_energy))
cmap = plt.get_cmap('gnuplot_r')

# Loop through each case and plot with a unique marker and color
for i, case in enumerate(df['Case']):
    marker = markers[i % len(markers)]  # Cycle through markers if more cases than markers
    color = cmap(norm(spec_energy[i]))
    ax.scatter(cost[i], emissions[i], marker=marker, s=60, label=case, color=color)

# Plot the vertical dotted line for base case cost in 2024 scenario
if not base_case_row.empty:
    ax.axvline(base_case_cost, color='gray', linestyle='--', linewidth=1, label='Base Case (2024)')

# Set labels for the axes
ax.set_xlabel(f'Cost (€/t of {Product})')
ax.set_ylabel(f'Emissions (t of CO$_{{2}}$/t of {Product})')

# Set x-axis limits based on cost data
x_min = min(cost) - 30  # Adjust as needed
x_max = max(cost) + 30  # Adjust as needed
ax.set_xlim(x_min, x_max)

# Add a color bar representing Spec Energy
sm = ScalarMappable(norm=norm, cmap=cmap)
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label(f'Spec Energy (GJ/t of {Product})')

# Set title for the plot
plt.title(plot_title)

# Add legend with proper settings
ax.legend(fontsize='small', ncol=1)

# Set the size of the plot
plt.gcf().set_size_inches(6, 6)

# Save the plot with the title and scenario condition
plot_file_path = f"{plot_title.replace(' ', '_').lower()}_scenario_{scenario}.png"
# plt.savefig(plot_file_path)

# Show the plot
plt.show()
