# # import os
# # import json

# # # Define the path
# # input_folder = 'new_datas'

# # # Initialize the count
# # total_count = 0

# # data = {}

# # # Process each JSON file in the input folder
# # for filename in os.listdir(input_folder):
# #     # Check if the filename matches the pattern (only date, no "_")
# #     if filename.endswith('.json') and '_' not in filename:
# #         json_file_path = os.path.join(input_folder, filename)

# #         # Read the JSON file and count the elements
# #         with open(json_file_path, mode='r', encoding='utf-8') as json_file:
# #             json_data = json.load(json_file)
            
# #             for entry in json_data:
# #                 try:
# #                     data[entry['name']] = entry['boolean']
# #                 except:
# #                     data[entry['name']] = None

# # #make a new json file and store all the names

# # formatted_data = [{'input': name, 'output': value} for name, value in data.items()]

# # with open('data_set.json', mode='w', encoding='utf-8') as json_file:
# #     json.dump(formatted_data, json_file, indent=2)


# import os
# import json


# instructions =  """I will provide a JSON file containing an array of process titles representing currently running processes on a computer. Your task is to analyze each process and determine if it is directly productive for a SOFTWARE DEVELOPER.  
# Return your output as a JSON array of booleans (e.g., `["true", "false", ...]`), where each element corresponds to the productivity status of the respective process in the input array. Ensure that the length of the output array matches the input array. Do not include any additional text or explanation in your response."""

# # Define the path
# input_folder = 'raw_data_set.json'

# # Read the JSON file and convert the format
# with open(input_folder, mode='r', encoding='utf-8') as json_file:
#     raw_data = json.load(json_file)

# # Initialize lists for inputs and outputs
# new_data = []


# import random

# i = 0
# while i < len(raw_data):
#     batch_size = random.randint(10, 50)
#     inputs = []
#     outputs = []
#     batch = raw_data[i:i+batch_size]
#     inputs.extend([entry['input'] for entry in batch])
#     outputs.extend([entry['output'] for entry in batch])

#     new_data.append({
#         "instruction": instructions,
#         "input": json.dumps(inputs),
#         "output": json.dumps(outputs)
#     })
    
#     print(f"Batch {i//batch_size} processed")
#     i += batch_size

# new_json_file_path = "ungrouped_real_data_set.json"

# with open(new_json_file_path, mode='w', encoding='utf-8') as new_json_file:
#     json.dump(new_data, new_json_file, indent=2)


    
# import os
# import json

# # Define the path
# input_folder = 'new_datas'

# # Initialize the count
# total_count = 0

# data = {}

# # Process each JSON file in the input folder
# for filename in os.listdir(input_folder):
#     # Check if the filename matches the pattern (only date, no "_")
#     if filename.endswith('.json') and '_' not in filename:
#         json_file_path = os.path.join(input_folder, filename)

#         # Read the JSON file and count the elements
#         with open(json_file_path, mode='r', encoding='utf-8') as json_file:
#             json_data = json.load(json_file)
            
#             for entry in json_data:
#                 try:
#                     data[entry['name']] = entry['boolean']
#                 except:
#                     data[entry['name']] = None

# #make a new json file and store all the names

# formatted_data = [{'input': name, 'output': value} for name, value in data.items()]

# with open('data_set.json', mode='w', encoding='utf-8') as json_file:
#     json.dump(formatted_data, json_file, indent=2)


import os
import json


instructions =  """I will provide a process title representing a currently running process on a computer. Your task is to analyze the process to determine if it is directly productive for a SOFTWARE DEVELOPER.  
Return your output as boolean, where it corresponds to the productivity status of the respective process. Do not include any additional text or explanation in your response."""

# Define the path
input_folder = 'raw_data_set.json'

# Read the JSON file and convert the format
with open(input_folder, mode='r', encoding='utf-8') as json_file:
    raw_data = json.load(json_file)

# Initialize lists for inputs and outputs
new_data = []


import random

i = 0
for data in raw_data:
    inputs = ''
    outputs = ''
    inputs = data['input']
    outputs = data['output']

    new_data.append({
        "instruction": instructions,
        "input": inputs,
        "output": outputs
    })
    
    print(f"Batch {i} processed")
    i += 1


new_json_file_path = "ungrouped_real_data_set.json"

with open(new_json_file_path, mode='w', encoding='utf-8') as new_json_file:
    json.dump(new_data, new_json_file, indent=2)


    
    





