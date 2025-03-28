import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

Industry = 'Glass'
Product = 'Glass'

# Check the scenario and set variables accordingly
scenario = 4  # Change this value to select the scenario

# Define Excel file and sheet name
excel_file_path = r'c:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_270225.xlsx'
sheet_name = 'SUM'

# Read data from the Excel file
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# Find the cost for "base_case" in the 2024 scenario
base_case_row = df[df.iloc[:, 0] == "base_case"]  # Assuming "base_case" is in the first column
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

# Create a 2D scatter plot
fig, ax = plt.subplots()

# Define 10 unique markers (for base cases)
base_markers = ['o', 's', '^', 'D', 'v', '>', '<', 'p', '*', 'h']

# Normalize and map the color to spec_energy values
norm = Normalize(vmin=min(spec_energy), vmax=max(spec_energy))
cmap = plt.get_cmap('turbo')

# Dictionary to assign markers for unique base technologies
marker_dict = {}

# Store legend entries (to avoid duplicates)
legend_entries = {}

# Loop through each case and plot
for i, case in enumerate(df['Case']):
    base_name = case.replace('_CC', '')  # Remove '_CC' to get base technology name
    
    # Assign a unique marker
    if base_name not in marker_dict:
        marker_dict[base_name] = base_markers[len(marker_dict) % len(base_markers)]
    
    marker = marker_dict[base_name]  # Get marker for this technology
    color = cmap(norm(spec_energy[i]))  # Define color based on spec_energy

    # Define fill properties
    if '_CC' in case:
        facecolor = 'none'  # No fill for CC cases
        edgecolor = color  # Border color based on spec_energy
        linewidth = 1.5
    else:
        facecolor = color  # Filled for non-CC cases
        edgecolor = 'black'  # Black border for better visibility
        linewidth = 1.2

    # Plot point
    ax.scatter(cost[i], emissions[i], marker=marker, s=70, 
               facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)

    # Store legend entry once per base_name (avoid duplicates)
    if base_name not in legend_entries:
        legend_entries[base_name] = (marker, base_name)

# Plot the vertical dotted line for base case cost in 2024 scenario
if not base_case_row.empty:
    ax.axvline(base_case_cost, color='gray', linestyle='--', linewidth=1, label='Base Case (2024)')

# Set labels for the axes
ax.set_xlabel(f'Cost (€/t of {Product})')
ax.set_ylabel(f'Emissions (direct + indirect) (t of CO$_{{2}}$/t of {Product})')

# Set x-axis limits based on cost data
x_min = min(cost) - 30  # Adjust as needed
x_max = max(cost) + 30  # Adjust as needed
ax.set_xlim(x_min, x_max)

# Add a color bar representing Spec Energy
sm = ScalarMappable(norm=norm, cmap=cmap)
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label(f'Specific Energy Consumption (GJ/t of {Product})')

# Set title for the plot
plt.title(plot_title)

# Create legend handles for "Without CC" and "With CC" using generic markers
solid_marker_legend = plt.Line2D([0], [0], marker='o', color='black', markersize=7, linestyle='None', 
                                 markerfacecolor='gray', markeredgewidth=1, label="Without CC")
hollow_marker_legend = plt.Line2D([0], [0], marker='o', color='black', markersize=7, linestyle='None', 
                                  markerfacecolor='none', markeredgewidth=1.5, label="With CC")

# Combine all legend entries (Base Technologies + CC Representation)
all_legend_handles = [plt.Line2D([0], [0], marker=m, color='black', markersize=7, linestyle='None', 
                                 markerfacecolor='black', markeredgewidth=1, label=label) 
                      for m, label in legend_entries.values()]

all_legend_handles.append(solid_marker_legend)  # Add solid marker legend (Without CC)
all_legend_handles.append(hollow_marker_legend)  # Add hollow marker legend (With CC)

# Add single combined legend
ax.legend(handles=all_legend_handles, fontsize='small', ncol=1)

# Set the size of the plot
plt.gcf().set_size_inches(6, 6)

# Save the plot with the title and scenario condition
plot_file_path = f"{plot_title.replace(' ', '_').lower()}_scenario_{scenario}.png"
# plt.savefig(plot_file_path)

# Show the plot
plt.show()
