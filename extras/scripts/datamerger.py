import json
import os

# Define the folder containing the JSON files
folder_path = 'new_datas'

# Get the list of files in the folder
files = os.listdir(folder_path)

# Filter out the date JSON files and AI evaluated JSON files
date_files = [f for f in files if f.endswith('.json') and not '_' in f]
ai_evaluated_files = [f for f in files if f.endswith('_AI_Evaluated.json')]

print("Date JSON files:", len(date_files))
print("AI Evaluated JSON files:", len(ai_evaluated_files))

# Read and process date files and AI evaluated files
for date_file, ai_file in zip(date_files, ai_evaluated_files):
    with open(os.path.join(folder_path, date_file), 'r', encoding='utf-8') as date_f, \
         open(os.path.join(folder_path, ai_file), 'r', encoding='utf-8') as ai_f:
        
        date_data = json.load(date_f)
        ai_data = json.load(ai_f)
        
        # Skip if AI evaluated file is empty or the number of elements is not equal
        if not ai_data or len(date_data) != len(ai_data):
            print(f"Skipping {date_file} and {ai_file} due to mismatch or empty AI evaluated file.")
            continue
        
        merged_data = []
        for date_entry, ai_entry in zip(date_data, ai_data):
            merged_entry = {
                'name': date_entry['name'],
                'time': date_entry['time'],
                'boolean': ai_entry['boolean']
            }
            merged_data.append(merged_entry)
    
    # Write the merged data back to the original date file
    with open(os.path.join(folder_path, date_file), 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, indent=2)

    print(f"Merged data written to {date_file}")