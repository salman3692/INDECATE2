import csv
import re
import os

def check_layers_exist(location, file_path):
    # Define the layer identifiers for electricity, hydrogen, and natural gas
    NG          = f'c1_Glass_NG_Furnace_NG_Furnace'
    NG_oxy      = f'c1_Glass_NGOxy_Furnace_NGOxy_Furnace'
    Hyb         = f'c1_Glass_Hybrid_furnace_Hybrid_Furnace'
    EL          = f'c1_Glass_EL_Furnace_el_Furnace'
    H2          = f'c1_Glass_H2_Furnace_H2_Furnace'
    CC          = f'c1_Glass_CC_Units_CCSPost'
    CPU         = f'c1_Glass_CC_Units_CPU4Oxy'
    HR          = f'c1_Glass_ORC_CO2_super_sCO2_supercycle'

    prod_capacity = 33333.33  # kg/hr of flat glass

    # Patterns to extract production and capture values
    elec_demand_pattern = re.compile(r'layers_Electricity\s+c1_world_mergedresource_Resource_Electricity\s+1\s+(-?\d+\.\d+|-?\d+)')
    EI_pattern = re.compile(r'KPI_impact\s+(=)\s+(-?\d+\.\d+|-?\d+)')
    co2_capt_pattern = re.compile(r'layers_CO2\s+(c1_Glass_CC_Units_CCSPost|c1_Glass_CC_Units_CPU4Oxy)\s+1\s+(-?\d+\.\d+|-?\d+)')

    # Read the content of the results file
    try:
        with open(file_path) as file:
            content = file.read()
    except FileNotFoundError:
        # print(f"File not found: {file_path}")
        return 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0

    # Define regular expression patterns for each layer with word boundaries
    NG_pattern = re.compile(r'\b' + re.escape(NG) + r'\b')
    NG_oxy_pattern = re.compile(r'\b' + re.escape(NG_oxy) + r'\b')
    Hyb_pattern = re.compile(r'\b' + re.escape(Hyb) + r'\b')
    EL_pattern = re.compile(r'\b' + re.escape(EL) + r'\b')
    H2_pattern = re.compile(r'\b' + re.escape(H2) + r'\b')
    CC_pattern = re.compile(r'\b' + re.escape(CC) + r'\b')
    CPU_pattern = re.compile(r'\b' + re.escape(CPU) + r'\b')
    HR_pattern = re.compile(r'\b' + re.escape(HR) + r'\b')

    # Check if the layers exist for the given location
    c1 = 1 if re.search(NG_pattern, content) else 0
    c2 = 1 if re.search(NG_oxy_pattern, content) else 0
    c3 = 1 if re.search(Hyb_pattern, content) else 0
    c4 = 1 if re.search(EL_pattern, content) else 0
    c5 = 1 if re.search(H2_pattern, content) else 0
    c6 = 1 if re.search(CC_pattern, content) else 0
    c7 = 1 if re.search(CPU_pattern, content) else 0
    c8 = 1 if re.search(HR_pattern, content) else 0

    # Extract electricity production and CO2 capture values
    elec_demand_match = re.search(elec_demand_pattern, content)
    co2_capt_match = re.search(co2_capt_pattern, content)
    EI_match = re.search(EI_pattern, content)

    elec_demand = float(elec_demand_match.group(1)) / prod_capacity * 3.6 if elec_demand_match else 0.0 #in GJ/t
    co2_capt = float(co2_capt_match.group(2)) / prod_capacity if co2_capt_match else 0.0 #tCO2/tglass
    EI = float(EI_match.group(2)) / (prod_capacity*8.76) if EI_match else 0.0 #t/year
    # EI = float(EI_match.group(2)) * 8.76 / 1000 if EI_match else 0.0 #t/year

    return c1, c2, c3, c4, c5, c6, c7, c8, elec_demand, co2_capt, EI

# Create a list to store the results for each row
data = []

# TRL mapping dictionary
trl_mapping = {
    'H2_ORC_CC': 'Low: 3 - 4',
    'H2_ORC': 'Low: 3 - 4',
    'H2_CC': 'Low: 3 - 4',
    'Elec_ORC_CC': 'Medium: 6 - 7',
    'Elec': 'Medium: 6 - 7',
    'Elec_ORC': 'Medium: 6 - 7',
    'Elec_CC': 'Medium: 6 - 7',
    'Hyb_ORC_CC': 'Medium: 6 - 7',
    'Hyb_ORC': 'Medium: 6 - 7',
    'NGOxy_ORC_CC': 'High: 8',
    'NGOxy_ORC': 'High: 8',
    'NG_ORC_CC': 'High: 8',
    'NG_ORC': 'High: 9'
}

# Loop through the range from 1 to 749 (inclusive)
for i in range(1, 525):
    # Generate the file path for the current file
    file_path = rf'c:\Users\msalman\Desktop\OSMOSE ETs\Glass\results\Glass\run_009_Parallel_V6_C\s_{i:03}\opt\hc_0000.txt'

    # Check the layers for the current row (i)
    c1, c2, c3, c4, c5, c6, c7, c8, elec_demand, co2_capt, EI = check_layers_exist(i, file_path)

    # Initialize tech and TRL
    tech = ''
    TRL = ''

    # Determine the value for the tech column
    # NG Technology Conditions
    if c1 == 1 and c2 == 0 and c3 == 0 and c4 == 0 and c5 == 0:
        if c6 == 1 and c7 == 0 and c8 == 0:
            tech = 'NG_CC'
        elif c6 == 0 and c7 == 0 and c8 == 1:
            tech = 'NG_ORC'
        elif c6 == 1 and c7 == 0 and c8 == 1:
            tech = 'NG_ORC_CC'
    # NGOxy Technology Conditions
    elif c1 == 0 and c2 == 1 and c3 == 0 and c4 == 0 and c5 == 0:
        if c6 == 0 and c7 == 1 and c8 == 0:
            tech = 'NGOxy_CC'
        elif c6 == 0 and c7 == 0 and c8 == 1:
            tech = 'NGOxy_ORC'
        elif c6 == 0 and c7 == 1 and c8 == 1:
            tech = 'NGOxy_ORC_CC'
    # Hyb Technology Conditions
    elif c1 == 0 and c2 == 0 and c3 == 1 and c4 == 0 and c5 == 0:
        if c6 == 0 and c7 == 1 and c8 == 0:
            tech = 'Hyb_CC'
        elif c6 == 0 and c7 == 0 and c8 == 1:
            tech = 'Hyb_ORC'
        elif c6 == 0 and c7 == 1 and c8 == 1:
            tech = 'Hyb_ORC_CC'
    # Elec Technology Conditions
    elif c1 == 0 and c2 == 0 and c3 == 0 and c4 == 1 and c5 == 0:
        if c6 == 0 and c7 == 1 and c8 == 0:
            tech = 'Elec_CC'
        elif c6 == 0 and c7 == 0 and c8 == 0:
            tech = 'Elec'
        elif c6 == 0 and c7 == 1 and c8 == 1:
            tech = 'Elec_ORC'
    # H2 Technology Conditions
    elif c1 == 0 and c2 == 0 and c3 == 0 and c4 == 0 and c5 == 1:
        if c6 == 1 and c7 == 0 and c8 == 0:
            tech = 'H2_CC'
        elif c6 == 0 and c7 == 0 and c8 == 1:
            tech = 'H2_ORC'
        elif c6 == 1 and c7 == 0 and c8 == 1:
            tech = 'H2_ORC_CC'
    else:
        tech = 'Chankna'  # If none of the above conditions match

    # Assign TRL based on tech
    TRL = trl_mapping.get(tech, '')

    # Append the results to the list
    data.append([tech, elec_demand, co2_capt, EI, TRL])

# Specify the path to the existing CSV file
Output_file = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Parallel_V6_201224_C.csv'

# Check if the output file exists
if not os.path.exists(Output_file):
    raise FileNotFoundError(f"The file {Output_file} does not exist.")

# Read the existing CSV file
with open(Output_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)
    header = rows[0]  # Extract the header row

    # Ensure 'tech', 'elec_demand','co2_capt', 'EI', and 'TRL' columns exist
    required_columns = ['tech', 'elec_demand', 'co2_capt', 'EI', 'TRL']
    for col in required_columns:
        if col not in header:
            header.append(col)

    # Get indices for each column
    tech_index = header.index('tech')
    elec_demand_index = header.index('elec_demand')
    co2_capt_index = header.index('co2_capt')
    EI_index = header.index('EI')
    TRL_index = header.index('TRL')

    # Update header row
    rows[0] = header

    # Ensure there's enough rows in the CSV to accommodate new data
    existing_data_length = len(rows) - 1  # Exclude header
    data_length = len(data)
    if data_length > existing_data_length:
        for _ in range(data_length - existing_data_length):
            rows.append([''] * len(header))

    # Update rows with new data
    for i in range(1, len(rows)):
        if i-1 < data_length:
            row = rows[i]
            row.extend([''] * (len(header) - len(row)))  # Extend row if necessary
            row[tech_index] = data[i-1][0]
            row[elec_demand_index] = data[i-1][1]
            row[co2_capt_index] = data[i-1][2]
            row[EI_index] = data[i-1][3]
            row[TRL_index] = data[i-1][4]

# Write the updated data to the CSV file
with open(Output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print("Results saved successfully.")
