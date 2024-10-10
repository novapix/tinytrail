import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from logger import  logger
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    logger.error("MONGO_URI not set")
    exit(1)

try:
    client = AsyncIOMotorClient(MONGO_URI)
    client.admin.command('ping')
    db = client.url_shortener
    url_collection = db.urls
    logger.info("Successfully connected to the MongoDB database.")
except PyMongoError as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    exit(1)
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
    exit(1)
