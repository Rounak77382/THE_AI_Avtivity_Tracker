import csv


def csvdata(path):
    
    print("converting data into prompt....",end="")
    datalist = []
    count = 1

    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        lines = list(reader)
        
        for line in lines:
            
            if len(line) == 2:
                name,time = line
                
                title = str(count) + "." + name.split(',')[0]
                title = title.replace(' - ', ',')
                datalist.append(title)
                count += 1
                
    datalist_str = '\n'.join(datalist)
                
                
    csv_data =  datalist_str    

    print("completed")
    
    return csv_data



#print(csvdata('2023-10-29.csv'))