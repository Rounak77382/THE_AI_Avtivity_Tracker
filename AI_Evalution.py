#cwirLrg1RNoV2ocNWrNoK2K4cFNzXnXXlrviooKW_9A4G-RHc96Wn8LOuFr_ZzHR1nTEIw.


from bardapi import Bard 
import data_to_prompt as dop
import csv
import os
import time
from bardapi import BardCookies
bard = BardCookies(token_from_browser=True)

try:
    
    path = '2023-11-14.csv'
    cd = dop.csvdata(path)
    
    Final_prompt = cd[1]
    csv_data = cd[0]
    
    print("sending data to AI for evalution....")

    while True:
        try:
            response = bard.get_answer(input_text = Final_prompt)['content']
            if len(response.split()) < 100:
                continue
            print(response)
            break
        except Exception as e:
            print("Error: " + str(e))
            if "HTTPSConnectionPool" in str(e):
                print("Waiting for 5 sec to retry.....")
                time.sleep(5)
                
                continue
            break
    
 
    print("completed")
    
    

    response_lines = response.split('\n')
    csv_data_lines = csv_data.split('\n')

        
        
        
    path1 = path.rsplit('.', 1)[0] + "_AI_Evaluated.csv"
    print("saving data to " + path1+"......",end="")
    processes = []
    
    """with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        lines = list(reader)
        
        for line in lines:
            if len(line) == 2:
                processes.append(str(line))"""
                
    
    with open(path1, 'a', encoding='utf-8') as file:
        
        for lines in response_lines:
            file.write(lines + '\n')

            
    print("completed")
           
        
        
except Exception as e:
    print("Error: " + str(e))


