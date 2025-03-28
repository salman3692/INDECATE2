import pandas as pd
import json

# Read Excel
file_path = r'c:\Users\msalman\Desktop\OSMOSE ETs\Python work\INDECATE2\data\Results_Scenarios_270225.xlsx'
df = pd.read_excel(file_path, sheet_name='SUM')

# Rename columns to match expected format
df.rename(columns={
    '2025_Scenario': '2025',
    '2030_Scenario': '2030',
    '2040_Scenario': '2040',
    '2050_Scenario': '2050',
    'Spec_Energy': 'Spec_Energy',
    'EI': 'EI'
}, inplace=True)

# Save to JSON
json_path = 'pareto_data.json'
df.to_json(json_path, orient='records', indent=2)
print(f"Data saved to {json_path}")
