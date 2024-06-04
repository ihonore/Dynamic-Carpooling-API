import logging
from fastapi import FastAPI
from routes import api_router
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
app.include_router(api_router)

uri = os.getenv("MONGODB_URI")
if not uri:
    logger.error("MONGODB_URI environment variable is not set")
    raise ValueError("MONGODB_URI environment variable is not set")

# Create a new client and connect to the server
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    logger.info("Pinged. Successfully connected to MongoDB!🟢")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)