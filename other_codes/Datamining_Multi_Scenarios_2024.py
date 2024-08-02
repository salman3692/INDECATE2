import csv
import re
import os

def check_layers_exist(location, file_path):
    # Define the layer identifiers for electricity, hydrogen, and natural gas
    NG          = f'c1_Glass_NG_Furnace_NG_Furnace                  1'
    NG_oxy      = f'c1_Glass_NGOxy_Furnace_NGOxy_Furnace            1'
    Hyb         = f'c1_Glass_Hybrid_furnace_Hybrid_Furnace          1'
    EL          = f'c1_Glass_EL_Furnace_el_Furnace                  1'
    H2          = f'c1_Glass_H2_Furnace_H2_Furnace                  1'
    CCS         = f'c1_Glass_CC_Units_CCSPost                    1'
    CPU         = f'c1_Glass_CC_Units_CPU4Oxy                       1'
    # HREC        = f'c1_Glass_ORC_CO2_sCO2_transcycle             1'

    # Read the content of the results file
    try:
        with open(file_path) as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0, 0, 0, 0, 0, 0, 0

    # Define regular expression patterns for each layer with word boundaries
    NG_pattern = re.compile(r'\b' + re.escape(NG) + r'\b')
    NG_oxy_pattern = re.compile(r'\b' + re.escape(NG_oxy) + r'\b')
    Hyb_pattern = re.compile(r'\b' + re.escape(Hyb) + r'\b')
    EL_pattern = re.compile(r'\b' + re.escape(EL) + r'\b')
    H2_pattern = re.compile(r'\b' + re.escape(H2) + r'\b')
    CCS_pattern = re.compile(r'\b' + re.escape(CCS) + r'\b')
    CPU_pattern = re.compile(r'\b' + re.escape(CPU) + r'\b')
    # HREC_pattern = re.compile(r'\b' + re.escape(HREC) + r'\b')

    # Check if the layers exist for the given location
    c1 = 1 if re.search(NG_pattern, content) else 0
    c2 = 1 if re.search(NG_oxy_pattern, content) else 0
    c3 = 1 if re.search(Hyb_pattern, content) else 0
    c4 = 1 if re.search(EL_pattern, content) else 0
    c5 = 1 if re.search(H2_pattern, content) else 0
    c6 = 1 if re.search(CCS_pattern, content) or re.search(CPU_pattern, content) else 0
    # c8 = 1 if re.search(HREC_pattern, content) else 0

    return c1, c2, c3, c4, c5, c6

# Create a list to store the results for each row
data = []

# Loop through the range from 1 to 500 (inclusive)
for i in range(1, 436):
    # Generate the file path for the current file
    file_path = rf'C:\Users\msalman\Desktop\OSMOSE ETs\Glass\results\Glass\run_057_Parallel_V3\s_{i:03}\opt\hc_0000.txt'
    # Check the layers for the current file
    c1, c2, c3, c4, c5, c6 = check_layers_exist(i, file_path)
    
    # Determine the value for the 5th column
    if c1 == 1 and c2 == 0 and c3 == 0 and c4 == 0 and c5 == 0 and c6 == 0:
        tech = 'NG'
    elif c1 == 1 and c2 == 0 and c3 == 0 and c4 == 0 and c5 == 0 and c6 == 1:
        tech = 'NG_CC'
    elif c1 == 0 and c2 == 1 and c3 == 0 and c4 == 0 and c5 == 0 and c6 == 0:
        tech = 'NG_Oxy'
    elif c1 == 0 and c2 == 1 and c3 == 0 and c4 == 0 and c5 == 0 and c6 == 1:
        tech = 'NG_Oxy_CC'
    elif c1 == 0 and c2 == 0 and c3 == 1 and c4 == 0 and c5 == 0 and c6 == 0:
        tech = 'Hyb'
    elif c1 == 0 and c2 == 0 and c3 == 1 and c4 == 0 and c5 == 0 and c6 == 1:
        tech = 'Hyb_CC'
    elif c1 == 0 and c2 == 0 and c3 == 0 and c4 == 1 and c5 == 0 and c6 == 0:
        tech = 'EL'
    elif c1 == 0 and c2 == 0 and c3 == 0 and c4 == 1 and c5 == 0 and c6 == 1:
        tech = 'EL_CC'
    elif c1 == 0 and c2 == 0 and c3 == 0 and c4 == 0 and c5 == 1 and c6 == 0:
        tech = 'H2'
    elif c1 == 0 and c2 == 0 and c3 == 0 and c4 == 0 and c5 == 1 and c6 == 1:
        tech = 'H2_CC'
    else:
        tech = 'Chankna'  # If none of the above conditions match, leave the 5th column empty

    print(tech)
    data.append(tech)  # Append the result directly to the list

# Specify the path to the existing CSV file
Output_file = r'C:\Users\msalman\Desktop\OSMOSE ETs\Python work\Parallel_Glass_V3_2024\Parallel_V3_4.csv'

# Read the existing CSV file and append the results to the 'tech' column
with open(Output_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)
    header = rows[0]  # Extract the header row
    tech_index = header.index('tech')  # Find the index of 'tech' column
    
    # Ensure there's enough rows in the CSV to accommodate new data
    for _ in range(len(data) - (len(rows) - 1)):
        rows.append([''] * len(header))
    
    for i, row in enumerate(rows):
        if i > 0 and i-1 < len(data):  # Skip the header row and check if data is available
            row[tech_index] = data[i-1]  # Assign the result to the 'tech' column

# Write the updated data to the CSV file
with open(Output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)  # Write the updated rows

print("Results saved successfully.")
