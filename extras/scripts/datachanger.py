import os
import csv
import json

# Define the paths
input_folder = 'datas'
output_folder = 'new_datas'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process each CSV file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(input_folder, filename)
        json_file_path = os.path.join(output_folder, filename.replace('.csv', '.json'))

        # Read the CSV file
        with open(csv_file_path, mode='r', encoding='ISO-8859-1') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = list(csv_reader)

        # Write the JSON file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)

print("CSV files have been converted to JSON files.")


