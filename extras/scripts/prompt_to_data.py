import csv
import re

input_path = '2023-11-05_AI_Evaluated.csv'


def replace_word_in_csv(file_path = input_path):
    # Read the CSV file
    with open(file_path, 'r', newline='',encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

    line = ""
    new = []
    # Make modifications to the data
    for row in data:
        for i, value in enumerate(row):
            line = line + row[i] + " - "
            
        line = line[:-3].replace(': true', ',true').replace(': false', ',false')
        line = re.sub(r'\b\d+\.\s*', '', line)
        print(line)
        new.append(line)
        line=""
        
    #print(new)

    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'boolean'])
        for line in new:
            writer.writerow(line.split(','))








#replace_word_in_csv()





'''
def replace_word_in_csv(file_path, old_word, new_word):
    # Read the CSV file
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Make modifications to the data
    for row in data:
        for i, value in enumerate(row):
            row[i] = value.replace(old_word, new_word)

    # Write the updated data back to the CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Replace 'old_word' with 'new_word' in the entire CSV file
replace_word_in_csv(input_path, 'No', 'false')

'''