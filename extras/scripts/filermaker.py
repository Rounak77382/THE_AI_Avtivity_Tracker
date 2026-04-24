import os
import json
import re

# Define the folder path
folder_path = 'new_datas'

# List all files in the folder
files = os.listdir(folder_path)

# Filter for JSON files
json_files = [file for file in files if file.endswith('.json') and re.match(r'\d{4}-\d{2}-\d{2}\.json', file)]

# Check if length of json_files is 1/3 length of number of files in the folder, if true then end the program
if len(json_files) * 4 == len(files):
    print("All files are already processed")
    exit()

# Process each JSON file
for json_file in json_files:
    base_name = os.path.splitext(json_file)[0]
    
    short_json = f"{base_name}_short.json"
    ai_evaluated_json = f"{base_name}_AI_Evaluated.json"
    prod_percent_json = f"{base_name}_prod_percent.json"
    
    short_json_path = os.path.join(folder_path, short_json)
    ai_evaluated_json_path = os.path.join(folder_path, ai_evaluated_json)
    prod_percent_json_path = os.path.join(folder_path, prod_percent_json)
    
    # Check if the files already exist
    if not os.path.exists(short_json_path):
        with open(short_json_path, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(ai_evaluated_json_path):
        with open(ai_evaluated_json_path, 'w') as f:
            json.dump([], f)
    
    if not os.path.exists(prod_percent_json_path):
        with open(prod_percent_json_path, 'w') as f:
            json.dump({"Productive Percentage": 0, "Unproductive Percentage": 0}, f)
            
    if os.path.exists(short_json_path) and os.path.exists(ai_evaluated_json_path) and os.path.exists(prod_percent_json_path):
        print(f"Files for {base_name} already exist")