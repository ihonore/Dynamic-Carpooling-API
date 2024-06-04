from fastapi import FastAPI
from routes import api_router
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import uvicorn


# Load environment variables from .env file
load_dotenv()

app=FastAPI()

app.include_router(api_router)


uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged. Successfully connected to MongoDB!🟢")
except Exception as e:
    print(e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)