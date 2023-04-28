import pymongo
import datetime
import pytz

uri = "mongodb+srv://raebelchristo:amber47@cluster0.c50zie8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
database = pymongo.MongoClient(uri)



mydb = database['carparking']
#print(database.list_database_names())

collec = mydb['cars']

#print(database.list_collection_names())

current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

x = collec.insert_one({
    "plate":"TN04 GY3321",
    "time":current_time
})

print(x)
