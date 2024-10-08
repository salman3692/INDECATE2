import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_V2_031024.xlsx'
xls = pd.ExcelFile(file_path)

# Create a dictionary to store data from each sheet
data_dict = {}

# Loop through each sheet
for sheet_name in ['NG','NG+CC','NGOxy','NGOxy+CC','Hyb','Hyb+CC','EL','EL+CC','H2','H2+CC']:
    # Read the sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Find the row index where "Total Spec Cost (EUR/t)" is located
    total_spec_cost_row = df[df.iloc[:, 0] == "Total Spec Cost (EUR/t)"].index[0]
    EI_row = df[df.iloc[:, 0] == "EI_total"].index[0]
    Energy_row = df[df.iloc[:, 0] == "Spec Energy"].index[0]

    # Extract data from the row
    total_spec_cost_2024 = df.iloc[total_spec_cost_row, 1]
    total_spec_cost_2030 = df.iloc[total_spec_cost_row, 2]
    total_spec_cost_2040 = df.iloc[total_spec_cost_row, 3]
    total_spec_cost_2050 = df.iloc[total_spec_cost_row, 4]
    EI_total = df.iloc[EI_row, 1]
    Spec_energy = df.iloc[Energy_row, 1]

    # Store the data in the dictionary
    data_dict[sheet_name] = {
        '2024_Scenario': total_spec_cost_2024, 
        '2030_Scenario': total_spec_cost_2030, 
        '2040_Scenario': total_spec_cost_2040, 
        '2050_Scenario': total_spec_cost_2050,
        'EI': EI_total/(33333.33*8.76),
        'Spec_Energy': Spec_energy
    }

# Create a new DataFrame from the data dictionary
summary_df = pd.DataFrame.from_dict(data_dict, orient='index')

# Create a new sheet named "SUM" in the Excel file and save the summary data
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    summary_df.to_excel(writer, sheet_name='SUM')

# # Create a stacked column plot
# summary_df.plot(kind='bar', rot=0)
# plt.title('Stacked Column Plot of Summary Data')
# plt.xlabel('', fontsize=12)
# plt.ylabel('Total Cost (EUR/t of Glass)')
# plt.legend()
# plt.tight_layout()

# # Save the plot as an image
# plot_file_path = 'Scenarios2030v2.png'
# # plt.savefig(plot_file_path)

# print("Data extraction and summary sheet creation completed.")
# print(f"Stacked column plot saved as '{plot_file_path}'")
# plt.show()
