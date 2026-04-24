import os
import json

# Define the path
input_folder = 'new_datas'

# Initialize the count
total_count = 0

# Process each JSON file in the input folder
for filename in os.listdir(input_folder):
    # Check if the filename matches the pattern (only date, no "_")
    if filename.endswith('.json') and '_' not in filename:
        json_file_path = os.path.join(input_folder, filename)

        # Read the JSON file and count the elements
        with open(json_file_path, mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            count = len(data)
            total_count += count
            print(f"{filename}: {count} elements")

print(f"Total number of elements in the matching JSON files: {total_count}")