import re
import pandas as pd
from openpyxl import load_workbook

plant_capacity = 33333.33 #kg/hr
plant_capacity_an = plant_capacity * 8.76 #kg/hr

# Define the patterns and corresponding line descriptions
patterns_and_descriptions = [
    ("DefaultInvCost c1_Glass_NG_Furnace_NG_Furnace_Cinv                  c1_Glass_NG_Furnace_NG_Furnace", "NG Furnace Cinv"),
    ("DefaultInvCost c1_Glass_H2_Furnace_H2_Furnace_Cinv                  c1_Glass_H2_Furnace_H2_Furnace","H2 Furnace Cinv"),
    ("DefaultInvCost c1_Glass_EL_Furnace_el_Furnace_Cinv                  c1_Glass_EL_Furnace_el_Furnace","EL furnace Cinv"),
    ("DefaultInvCost c1_Glass_NGOxy_Furnace_NGOxy_Furnace_Cinv            c1_Glass_NGOxy_Furnace_NGOxy_Furnace", "NG Oxy Cinv"),
    ("DefaultInvCost c1_Glass_Hybrid_furnace_Hybrid_Furnace_Cinv          c1_Glass_Hybrid_furnace_Hybrid_Furnace", "Hyb Cinv"),
    ("DefaultInvCost c1_Glass_glass_float_glass_float_Cinv                c1_Glass_glass_float_glass_float", "Flat_glass Cinv"),
    ("DefaultInvCost c1_Glass_ORC_CO2_super_sCO2_supercycle_Cinv          c1_Glass_ORC_CO2_super_sCO2_supercycle", "ORC Cinv"),
    ("DefaultInvCost c1_Glass_CC_Units_CCSPost_Cinv                       c1_Glass_CC_Units_CCSPost", "CCS Cinv"),
    ("DefaultInvCost c1_Glass_BoilerCCS_Boiler_NG_Cinv                    c1_Glass_BoilerCCS_Boiler_NG", "Boiler Cinv"),
    ("DefaultInvCost c1_Glass_CC_Units_CPU4Oxy_Cinv                       c1_Glass_CC_Units_CPU4Oxy", "CPU Cinv"),
    ("DefaultInvCost c1_Glass_Air_separation_ASU_Cinv                     c1_Glass_Air_separation_ASU", "ASU Cinv"),
    ("DefaultOpCost  c1_world_mergedresource_dummy                        c1_world_mergedresource_Resource_Dummy","Dummy Cinv"),
    ("DefaultOpCost  c1_world_mergedresource_Resource_Electricity_Cost    c1_world_mergedresource_Resource_Electricity", "Elec op"),
    ("DefaultOpCost  c1_world_mergedresource_Resource_Hydrogen_Cost       c1_world_mergedresource_Resource_Hydrogen", "H2 op"),
    ("DefaultOpCost  c1_world_mergedresource_Resource_Naturalgas_Cost     c1_world_mergedresource_Resource_Naturalgas", "NG op"),
    ("DefaultOpCost  c1_world_mergedwaste_Environ_Cost                    c1_world_mergedwaste_Environ", "CO2 op"),
    ("DefaultOpCost  c1_world_mergedresource_dummy                        c1_world_mergedresource_Resource_Dummy","Dummy op"),
    ("KPI_impact =","EI_total"),
    ("layers_dummy               c1_world_mergedresource_Resource_Dummy","Dummy EI_total"),
    ("layers_hydrogen            c1_world_mergedresource_Resource_Hydrogen","H2 Demand"),
    ("layers_Electricity         c1_world_mergedresource_Resource_Electricity","Elec Demand"),
    ("layers_Naturalgas          c1_world_mergedresource_Resource_Naturalgas","NG demand"),
    ("layers_dummy               c1_world_mergedresource_Resource_Dummy","dummy demand"),
    ("layers_EnvCO2Em            c1_world_mergedwaste_Environ              1","Scope1 Emissions"),
    ("layers_IndEnvCO2Em         c1_world_mergedwaste_Ind_Emiss            1","Scope2 Emissions"),
    ("layers_IndEnvCO2Em         c1_world_mergedresource_Resource_Electricity    1","IndEmissionsElec"),
    ("layers_IndEnvCO2Em         c1_world_mergedresource_Resource_Hydrogen       1","IndEmissionsH2"),
    ("layers_IndEnvCO2Em         c1_world_mergedresource_Resource_Naturalgas     1","IndEmissionsNG")
]

sheet_name = 'H2+CC'

# Define input file paths with descriptive variable names
path_2024 = r'c:\Users\msalman\Desktop\OSMOSE ETs\Glass\results\Glass\run_060_testing\s_001\opt\hc_0000.txt'
path_2030 = r'c:\Users\msalman\Desktop\OSMOSE ETs\Glass\results\Glass\run_060_testing\s_002\opt\hc_0000.txt'
path_2040 = r'c:\Users\msalman\Desktop\OSMOSE ETs\Glass\results\Glass\run_060_testing\s_003\opt\hc_0000.txt'
path_2050 = r'c:\Users\msalman\Desktop\OSMOSE ETs\Glass\results\Glass\run_060_testing\s_004\opt\hc_0000.txt'

# Define output file path
output_file_path = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_V2_031024V2.xlsx'

# Load the existing workbook
workbook = load_workbook(output_file_path)

# Select the specified sheet or create it if it doesn't exist
if sheet_name in workbook.sheetnames:
    worksheet = workbook[sheet_name]
else:
    worksheet = workbook.create_sheet(title=sheet_name)

# Create a dictionary to store extracted data
extracted_data = {description: [] for _, description in patterns_and_descriptions}


# ##############################################################################################################################""
# Process each input file
for path_name, input_file_path in [('2024', path_2024), ('2030', path_2030), ('2040', path_2040), ('2050', path_2050)]:
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            for pattern, description in patterns_and_descriptions:
                if pattern in line:
                    # Extract the number value using regular expression
                    value_match = re.search(r'\d+(\.\d+)?$', line)
                    if value_match:
                        value = float(value_match.group())
                        extracted_data[description].append(value)


# Write header row
header_row = ['Lines', '2024', '2030', '2040', '2050']
worksheet.append(header_row)

# Write data rows
for pattern, description in patterns_and_descriptions:
    data_row = [description]
    for path_name in ['2024', '2030', '2040', '2050']:
        if extracted_data[description]:
            data_row.append(extracted_data[description].pop(0))
        else:
            data_row.append('')  # Add an empty cell for missing values
    worksheet.append(data_row)


# Calculate and append the sum row for "cinv" and "op"
cinv_sum_row = ['Spec Cinv']
op_sum_row = ['Spec Op']
energy_sum_row = ['Spec Energy']
emissions_row = ['Spec Emissions']

# Initialize column sums for elec, mol, and central
column_sums = [0.0, 0.0, 0.0, 0.0]
energy_column_sums = [0.0, 0.0, 0.0, 0.0]  # Separate sums for energy
emissions_column = [0.0, 0.0, 0.0, 0.0]  # Separate for emissions

for path_name in ['2024', '2030', '2040', '2050']:
    column_index = ['2024', '2030', '2040', '2050'].index(path_name) + 2  # Calculate the integer index for the column
    column_values = [data for data in worksheet.iter_cols(min_col=column_index, max_col=column_index, values_only=True)][0]

    cinv_values = []
    op_values = []
    energy_values = []
    emissions_values = []

    for i, description in enumerate([data[0] for data in worksheet.iter_rows(values_only=True)][1:]):
        value = column_values[i]
        
        if description is None:
            continue  # Skip this iteration if the description is None
        
        if isinstance(description, str) and description.lower().endswith('cinv'):
            if isinstance(value, (int, float)):
                cinv_values.append(value)
        elif isinstance(description, str) and description.lower().endswith('op'):
            if isinstance(value, (int, float)):
                op_values.append(value)
        elif isinstance(description, str) and description.lower().endswith('demand'):
            if isinstance(value, (int, float)):
                energy_values.append(value)
        elif isinstance(description, str) and description.lower().endswith('emissions'):
            if isinstance(value, (int, float)):
                emissions_values.append(value)

    cinv_sum = sum(cinv_values) / plant_capacity_an if cinv_values else 0.0
    FixOp_sum = 25201727  # EUR/yr
    op_sum = (sum(op_values) + FixOp_sum) / plant_capacity_an if op_values else 0.0
    energy_sum = sum(energy_values) / plant_capacity if energy_values else 0.0
    emissions_sum = sum(emissions_values) / plant_capacity if emissions_values else 0.0

    cinv_sum_row.append(cinv_sum)
    op_sum_row.append(op_sum)
    energy_sum_row.append(energy_sum)
    emissions_row.append(emissions_sum)

    # Update column sums
    column_sums[column_index - 2] += cinv_sum + op_sum
    energy_column_sums[column_index - 2] += energy_sum
    emissions_column[column_index - 2] += emissions_sum

# Add a row to sum "Cinv" and "Op" values
total_sum_row = ['Total Spec Cost (EUR/t)']
total_sum_row.extend(column_sums)

# Append the "Energy" sum row separately
worksheet.append(energy_sum_row)
worksheet.append(emissions_row)
worksheet.append(cinv_sum_row)
worksheet.append(op_sum_row)
worksheet.append(total_sum_row)


# Save the workbook to the specified output file
workbook.save(output_file_path)

##################################################################################################################