import requests
import json
import os
from datetime import datetime

# Function to extract processes from JSON file
def extract_processes_from_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Extract process names
        process_names = [entry.get("name", "") for entry in data if "name" in entry]
        return process_names
    except Exception as e:
        print(f"Error extracting processes: {e}")
        return []

# Path to the JSON file
json_file_path = r"new_datas/2025-01-23.json"

# Get the current file name without extension
current_file_name = os.path.basename(json_file_path).split('.')[0]
output_file = f"c:\\ProgramData\\THE_AI_Avtivity_Tracker\\new_datas\\{current_file_name}_AI_Evaluated.json"

# Extract process names
processes = extract_processes_from_json(json_file_path)

# Initialize results list
results = []

# API URL
url = "https://special-hound-devoted.ngrok-free.app/analyze"

# Process each process name individually
for process in processes:
    if not process:  # Skip empty process names
        continue
        
    # Prepare data for this individual process
    # Clean process name by removing browser info at the end (like " - Opera")
    cleaned_process = process
    browser_suffixes = [" - Opera", " - Chrome", " - Firefox", " - Edge", " - Safari"]
    for suffix in browser_suffixes:
        if process.endswith(suffix):
            cleaned_process = process[:process.rfind(suffix)]
            break
    
    data = {"process": [cleaned_process]}
    
    
    try:
        # Send request to API
        response = requests.post(url, json=data)
        result = response.json()
        
        # print(f"Response for {cleaned_process}: {result}")
        
        # Extract the 'productive' value from the response
        productive = result.get('productive', False)
        
        # Store result
        results.append({
            "input": process,
            "output": str(productive).lower()
        })
        
        # Print progress
        print(f"Processed: {process} -> {productive}")
        
    except Exception as e:
        print(f"Error processing '{process}': {e}")
        # Still add to results but mark as error
        results.append({
            "input": process,
            "output": "false"
        })

# Save results to JSON file
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")
except Exception as e:
    print(f"Error saving results to file: {e}")

# Print summary
print(f"\nProcessed {len(results)} processes")