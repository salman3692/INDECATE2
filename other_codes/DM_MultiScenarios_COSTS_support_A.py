import pandas as pd

# Load the Excel file
file_path = r'c:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_TESTING.xlsx'
xls = pd.ExcelFile(file_path)

# List of scenarios
scenarios = ['path_2024', 'path_2030', 'path_2040', 'path_2050']

# List of specific cost variables to extract
cost_variables = [
    'NG Furnace Cinv', 'H2 Furnace Cinv', 'EL furnace Cinv', 'NG Oxy Cinv', 'Hyb Cinv',
    'Flat_glass Cinv', 'ORC Cinv', 'CCS Cinv', 'Boiler Cinv', 'CPU Cinv', 'ASU Cinv',
    'Elec op', 'H2 op', 'NG op', 'CO2 op'
]

# Create a dictionary to store data for each scenario
scenario_data = {scenario: [] for scenario in scenarios}

# Create a list to store the names of sheets that were processed
processed_sheets = []

# Loop through each sheet (technology) in the Excel file
for sheet_index, sheet_name in enumerate(xls.sheet_names):
    # Read the sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Check if the DataFrame is empty
    if df.empty:
        print(f"Skipping empty sheet: '{sheet_name}'")
        continue

    # Check the actual column names
    print(f"Column names in '{sheet_name}': {df.columns.tolist()}")

    # Determine the correct column name for the 'Lines'
    line_column_name = df.columns[0]  # Assuming the first column is the one we're looking for

    # Filter the DataFrame to include only the specified cost variables
    df_filtered = df[df[line_column_name].isin(cost_variables)]
    
    # Check if relevant cost variables are found in this sheet
    if df_filtered.empty:
        print(f"Skipping sheet '{sheet_name}' as no relevant cost variables found.")
        continue

    # If it's the first technology, save the cost variable tags
    if sheet_index == 0:
        cost_variable_tags = df_filtered[line_column_name].tolist()

    # Track the sheet name that was processed
    processed_sheets.append(sheet_name)

    # Loop through each scenario (2024, 2030, 2040, 2050)
    for i, scenario in enumerate(scenarios, start=1):
        # Extract the values for the scenario
        scenario_data[scenario].append(df_filtered.iloc[:, i].tolist())

# Create a new Excel writer object
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    # Loop through each scenario and create a new sheet with combined data
    for scenario in scenarios:
        # Create a DataFrame for the scenario with cost variables as rows
        scenario_df = pd.DataFrame(scenario_data[scenario]).transpose()
        
        # Set the column names as the processed technology names (only the ones that were processed)
        scenario_df.columns = processed_sheets
        
        # Insert the cost variable tags in the first column
        scenario_df.insert(0, 'Cost Variables', cost_variable_tags)
        
        # Save the combined DataFrame to a new sheet named after the scenario
        scenario_df.to_excel(writer, sheet_name=f'{scenario}', index=False)

print("Scenario sheets created successfully.")
