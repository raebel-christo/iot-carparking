import pymongo
import datetime
import pytz
import time

uri = "mongodb+srv://raebelchristo:amber47@cluster0.c50zie8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
database = pymongo.MongoClient(uri)



mydb = database['carparking']
#print(database.list_database_names())

collec = mydb['cars']

#print(database.list_collection_names())

current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

x = collec.insert_one({
    "slot":"1",
    "plate":"TN04 GY3321",
    "in_time":current_time
})

print(x)

x = collec.insert_one({
    "slot":"2",
    "plate":"TN42 XL4221",
    "in_time":current_time
})

print("Sleeping")
time.sleep(10)
current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
collec.update_one({"slot":"2"}, {"$set":{"out_time":current_time}})

print(x)
