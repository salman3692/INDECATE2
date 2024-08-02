import os

file_path = 'combinations_specific4.csv'

if os.path.isfile(file_path):
    print(f"File found at {file_path}")
else:
    print(f"File not found at {file_path}")
