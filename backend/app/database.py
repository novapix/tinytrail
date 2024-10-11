import os
from logger import logger

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.errors import PyMongoError

client: AsyncIOMotorClient | None = None
url_collection: AsyncIOMotorCollection | None  = None


async def initialize_db() -> None:
    global client, url_collection
    MONGO_URI = os.getenv("MONGO_URI")
    if not MONGO_URI:
        logger.error("MONGO_URI not set")
        exit(1)

    try:
        client = AsyncIOMotorClient(MONGO_URI)
        await client.admin.command('ping')
        logger.info("MongoDB server pinged successfully.")
        db = client["url_shortener"]

        collections = await db.list_collection_names()

        if 'urls' not in collections:
            logger.info("Collection 'urls' does not exist, creating...")
            await db.create_collection('urls')
            logger.info("'urls' collection created.")

        url_collection = db.urls
        logger.info("Successfully connected to the MongoDB database.")
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        exit(1)


async def close_db() -> None:
    global client
    if client is not None:
        try:
            client.close()
            logger.info("MongoDB connection closed successfully.")
        except Exception as e:
            logger.error(f"Error while closing MongoDB connection: {e}")
        finally:
            client = None
    else:
        logger.info("No active MongoDB connection to close.")

def get_url_collection() -> AsyncIOMotorCollection:
    return url_collection