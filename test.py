import csv
import itertools

# Define the values for cEE, cH2, cNG, and cCO2
cEE_values  = [0.01, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
cH2_values  = [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2]
cNG_values  = [0.01, 0.035, 0.055, 0.075, 0.1]
cCO2_values = [50, 100, 200, 300]

# Generate combinations using itertools.product
combinations = list(itertools.product(cEE_values, cH2_values, cNG_values, cCO2_values))

# Write the combinations to a CSV file
with open('combinations_2024.csv', 'w', newline='') as csvfile:
    fieldnames = ['cEE', 'cH2', 'cNG', 'cCO2']
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)

    for row in combinations:
        writer.writerow(row)
