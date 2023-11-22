from fastapi import FastAPI
from routes import api_router

app=FastAPI()

app.include_router(api_router)


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ihonore:Password1@cluster0.quzypvy.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged. Successfully connected to MongoDB!🟢")
except Exception as e:
    print(e)