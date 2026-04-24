# import os
# import json

# # Define the path
# input_folder = 'new_datas'
# list = []

# # Process each JSON file in the input folder
# for filename in os.listdir(input_folder):
    
    
#     # Check if the filename matches the pattern (only date, no "_")
#     if filename.endswith('.json') and 'AI_Evaluated' in filename:
#         json_file_path = os.path.join(input_folder, filename)

#         # Read the JSON file and convert the format
#         with open(json_file_path, mode='r', encoding='utf-8') as json_file:
#             data = json.load(json_file)
#             for entry in data:
  
#                 list.append({key: entry[key] for key in ["input", "output"]})



# new_json_file_path = "data_set.json"
# print(new_json_file_path)


# with open(new_json_file_path, mode='w', encoding='utf-8') as new_json_file:
#     json.dump(list, new_json_file, indent=2)

# print(f"{filename}: {len(data)} elements converted")

# import os
# import json

# # Define the path
# input_folder = 'new_datas'

# names = []

# # Process each JSON file in the input folder
# for filename in os.listdir(input_folder):
#     # Check if the filename matches the pattern (only date, no "_")
#     if filename.endswith('.json') and '_' not in filename:
#         json_file_path = os.path.join(input_folder, filename)

#         # Read the JSON file and convert the format
#         with open(json_file_path, mode='r', encoding='utf-8') as json_file:
#             data = json.load(json_file)
#             names.extend([item['name'] for item in data])
        
#         # Write the new format to a new JSON file
#         new_json_file_path = os.path.join(input_folder, f"{filename}_names.json")
#         with open(new_json_file_path, mode='w', encoding='utf-8') as new_json_file:
#             json.dump(names, new_json_file, indent=2)
            
#         print(f"{filename}: {len(names)} elements converted")
        
import json
import os

true_processes = []
false_processes = []
        
true_processes_folder = 'true_processes.txt'
false_processes_folder = 'false_processes.txt'

with open(true_processes_folder, mode='r', encoding='utf-8') as file:
    true_processes = file.read().splitlines()
    
with open(false_processes_folder, mode='r', encoding='utf-8') as file:
    false_processes = file.read().splitlines()
    
print(f"True processes: {len(true_processes)}")
print(f"False processes: {len(false_processes)}")

instructions =  """I will provide a process title representing a currently running process on a computer. Your task is to analyze the process to determine if it is directly productive for a SOFTWARE DEVELOPER.  
Return your output as boolean, where it corresponds to the productivity status of the respective process. Do not include any additional text or explanation in your response."""

final_data = []

for process in true_processes:
    final_data.append({"instruction": instructions,"input": process, "output": "True"})
    
for process in false_processes:
    final_data.append({"instruction": instructions,"input": process, "output": "False"})
    
    
# randomize the index of the data

import random

random.shuffle(final_data)

final_file_path = 'final_data_set.json'

with open(final_file_path, mode='w', encoding='utf-8') as file:
    json.dump(final_data, file, indent=2)