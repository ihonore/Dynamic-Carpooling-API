from pymongo import MongoClient

client=MongoClient("mongodb+srv://ihonore:Password1@cluster0.quzypvy.mongodb.net/?retryWrites=true&w=majority")

db=client.carpooling_db


users_collection = db["users_collection"]
offers_collection = db["offers_collection"]
demands_collection = db["demands_collection"]

# offers_collection.delete_many({})
