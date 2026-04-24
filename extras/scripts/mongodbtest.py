import pymongo
import time
import datetime
import csv
import os

client = pymongo.MongoClient("mongodb://localhost:27017")
print(client)
db = client['THEAPP']

collection_names = db.list_collection_names()
print(sorted(collection_names))

dates = [date.split('.')[0] for date in os.listdir('trackingdata')]
print(dates)

for date in dates:
    
    current_date = date
    collection = db[current_date]
    path = "trackingdata/" + current_date + ".csv"
    with open(path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                collection.update_one({'Name': row[0]}, {'$set': {'Time': float(row[1])}}, upsert=True)
