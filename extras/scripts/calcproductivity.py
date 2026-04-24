import csv
import json


def calc(date):

    # Read the first CSV file with boolean values
    with open(date+'_AI_Evaluated.csv', 'r',encoding='utf-8') as file1:
        reader1 = csv.reader(file1)
        next(reader1, None)  # Skip the header
        data1 = list(reader1)

    # Read the second CSV file with numerical values
    with open(date+'.csv', 'r',encoding='utf-8') as file2:
        reader2 = csv.reader(file2)
        next(reader2, None)  # Skip the header
        data2 = list(reader2)

    # Combine the data from both files into a new list
    merged_data = []
    for row1, row2 in zip(data1, data2):
        merged_row = [row1[0], row2[1], row1[1]]
        merged_data.append(merged_row)

    prod = 0
    unprod = 0

    for data in merged_data:
        name,time,bool = data[0], float(data[1]), data[2]
        
        if bool == 'true':
            prod += time
        elif bool == 'false':
            unprod += time
            
            
    print(f"Productive time: {round((prod/3600),2)} hours")
    print(f"Unproductive time: {round((unprod/3600),2)} hours")
    total_time = prod + unprod
    prod_percentage = round((prod / total_time) * 100, 2)
    unprod_percentage = round(100 - prod_percentage, 2)
    print(f"Productive percentage: {prod_percentage}%")
    print(f"Unproductive percentage: {unprod_percentage}%")
    
    return [prod_percentage,unprod_percentage]
    
    
date = input("Enter the date: ")

data = calc(date)

# Create a dictionary to store the data
result = {
    "Productive Percentage": data[0],
    "Unproductive Percentage": data[1]
}

# Convert the dictionary to JSON
json_data = json.dumps(result)

# Write the JSON data to a file
filename = f"{date}_prod_percent.json"
with open(filename, 'w') as file:
    file.write(json_data)


