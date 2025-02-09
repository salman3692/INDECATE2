import pandas as pd

Industry = 'Glass'
plant_capacity = 33333.33 #kg/hr
plant_capacity_an = plant_capacity * 8.76 #kg/hr

kW_to_GJ_f = 3600/(plant_capacity*1000)

# Define the file path
file_path = r'c:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_TESTING.xlsx'

# Create an empty DataFrame to store the results
results_df = pd.DataFrame()

# Define a function to calculate the required variables from the sheet data
def calculate_variables(sheet_name, data):
    # Define the energy variable names
    variable_map = {
        "NGFurnace_NG demand": 'NGFurnace_NG',
        "NGOxyFurnace_NG demand": 'NGOxyFurnace_NG',
        "HybFurnace_NG demand": 'HybFurnace_NG',
        "HybFurnace_EL demand": 'HybFurnace_EL',
        "H2furnace_H2 demand": 'H2furnace_H2',
        "Boiler_NG demand": 'Boiler_NG',
        "Furnace_EL demand": 'Furnace_EL',
        "ELFurnace_EL demand": 'ELFurnace_EL',
        "CPU_EL demand": 'CPU_EL',
        "ASU_EL demand": 'ASU_EL',
        "Elec supply": 'Elec_supply',
        "CCS_EL demand": 'CCS_EL',
        "Scope1 Emissions": 'Scope1_Em',
        "total impact": 'EI',

    }
    
    # Initialize a dictionary to store calculated variables
    calculated_vars = {}

    # Check if the 'Lines' column exists
    if 'Lines' in data.columns:
        for variable, short_name in variable_map.items():
            # Search for the variable in the 'Lines' column and get the corresponding value
            row = data.loc[data['Lines'] == variable]
            value = row.iloc[0, 1] if not row.empty else None  # Adjust column index if needed

            if value is not None:
                calculated_vars[short_name] = value
            else:
                print(f"{variable} not found in sheet: {sheet_name}")

    # Perform calculations
    if calculated_vars:
        Qth_Furnace = (
            calculated_vars.get('NGFurnace_NG')*kW_to_GJ_f if pd.notna(calculated_vars.get('NGFurnace_NG')) and calculated_vars.get('NGFurnace_NG') != 0 else
            calculated_vars.get('NGOxyFurnace_NG')*kW_to_GJ_f if pd.notna(calculated_vars.get('NGOxyFurnace_NG')) and calculated_vars.get('NGOxyFurnace_NG') != 0 else
            calculated_vars.get('HybFurnace_NG')*kW_to_GJ_f if pd.notna(calculated_vars.get('HybFurnace_NG')) and calculated_vars.get('HybFurnace_NG') != 0 else
            calculated_vars.get('H2furnace_H2')*kW_to_GJ_f if pd.notna(calculated_vars.get('H2furnace_H2')) and calculated_vars.get('H2furnace_H2') != 0 else
            0
        )
        # print(Qth_Furnace)
        
        # Initialize Qel_Furnace to 0
        Qel_Furnace = 0

        # Get the values of Furnace_EL, ELFurnace_EL, and HYBFurnace_EL
        furnace_el = calculated_vars.get('Furnace_EL')
        elfurnace_el = calculated_vars.get('ELFurnace_EL')
        hybfurnace_el = calculated_vars.get('HybFurnace_EL')

        # Multiply only if the value is not None
        furnace_el = furnace_el * kW_to_GJ_f if furnace_el is not None else 0
        elfurnace_el = elfurnace_el * kW_to_GJ_f if elfurnace_el is not None else 0
        hybfurnace_el = hybfurnace_el * kW_to_GJ_f if hybfurnace_el is not None else 0

        # Initialize a list of the values to check for existence
        values = [furnace_el, elfurnace_el, hybfurnace_el]

        # Filter out NaN or zero values from the list
        valid_values = [val for val in values if pd.notna(val) and val != 0]

        # If any valid values exist, sum them; otherwise, Qel_Furnace stays as 0
        if valid_values:
            Qel_Furnace = sum(valid_values)

        # print(Qel_Furnace)

        # Logic for Qth_WHR based on sheet name
        if sheet_name == 'NG_CC':
            Qth_WHR = (calculated_vars.get('Boiler_NG', 0) * kW_to_GJ_f * 0.85 - calculated_vars.get('Scope1_Em', 0) * 9 * 0.83334 * kW_to_GJ_f)  # For 90% capture rate: Boiler energy - (captured emissions * specific energy for capture)
        elif sheet_name == 'H2_CC':
            Qth_WHR = (-calculated_vars.get('Scope1_Em', 0) * 9 * 0.83334 * kW_to_GJ_f)  # For 90% capture rate: captured emissions * specific energy for capture
        else:
            Qth_WHR = 0  # Default case

        Qel_CCS = calculated_vars.get('CCS_EL', 0)*kW_to_GJ_f
        Qth_boiler = calculated_vars.get('Boiler_NG', 0)*kW_to_GJ_f
        Qel_CPU = calculated_vars.get('CPU_EL', 0)*kW_to_GJ_f
        Qel_ASU = calculated_vars.get('ASU_EL', 0)*kW_to_GJ_f
        Qel_WHR = - calculated_vars.get('Elec_supply', 0)*kW_to_GJ_f
        Qth_CCS = Qth_boiler - Qth_WHR
        EI = calculated_vars.get('EI', 0)/plant_capacity_an

        return {
            'Qth-Furnace': Qth_Furnace,
            'Qel-Furnace': Qel_Furnace,
            'Qth-CCS': Qth_CCS,
            'Qel-CCS': Qel_CCS,
            'Qth-boiler': Qth_boiler,
            'Qel-CPU': Qel_CPU,
            'Qel-ASU': Qel_ASU,
            'Qth-WHR': Qth_WHR,
            'Qel-WHR': Qel_WHR,
            'EI': EI,

        }
    else:
        print(f"No valid data found for calculations in sheet: {sheet_name}")
        return None

# Read the Excel file and process each sheet
with pd.ExcelFile(file_path) as xls:
    sheet_names = xls.sheet_names
    for sheet_name in sheet_names:
        # Read the current sheet
        data = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Calculate variables for the current sheet
        calculated_vars = calculate_variables(sheet_name, data)

        if calculated_vars:
            # If it's the first sheet, initialize the DataFrame
            if results_df.empty:
                results_df = pd.DataFrame(calculated_vars, index=[sheet_name])
            else:
                # Concatenate results to the DataFrame
                results_df = pd.concat([results_df, pd.DataFrame(calculated_vars, index=[sheet_name])])

# Transpose the DataFrame to get variables as rows and sheets as columns
results_df = results_df.T

# Save the results to a new sheet in the same Excel file
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    results_df.to_excel(writer, sheet_name='energy breakdown')

print("Data extraction and calculations completed successfully.")
