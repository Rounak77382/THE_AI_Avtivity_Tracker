'''
The code reads all the files in the "new_datas" folder of the current directory and processes the data in each file.
For each file, it checks if the file is a JSON file and does not contain an underscore in the filename.
If the conditions are met, the code reads the data from the file and processes it to create a new dictionary with the application names and total time spent.
'''

import os
import json

# Get a list of all files in the "new_datas" folder of the current directory
files = os.listdir("new_datas")

# Loop through each file
for file_name in files:
    # Check if the file is a JSON and does not contain '_'
    if file_name.endswith('.json') and '_' not in file_name:
        path = "new_datas/" + file_name
        print(f"Reading from {path}")
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                processed_data = {}

                for entry in data:
                    if 'name' in entry and 'time' in entry and entry['time'] is not None:
                        name = entry['name'].split(' - ')[-1]
                        time = float(entry['time'])

                        if name not in processed_data:
                            processed_data[name] = time
                        else:
                            processed_data[name] += time
                    else:
                        print(f"Skipping entry {entry} as it does not have 'name' and 'time' keys or 'time' is None")

            short_json_path = path.rsplit('.', 1)[0] + "_short.json"
            print(f"Writing to {short_json_path}")
            with open(short_json_path, 'w', encoding='utf-8') as file:
                json_data = [{"name": key, "time": str(value)} for key, value in processed_data.items()]
                json.dump(json_data, file, indent=2)
        except UnicodeDecodeError as e:
            print(f"Error reading {path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {path}: {e}")
#explain the code
