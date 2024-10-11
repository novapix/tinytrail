from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from logger import logger
from database import get_url_collection
from models import URLCreate
from utils import get_unique_short_code

router = APIRouter()

@router.post("/shorten")
async def shorten_url(request: URLCreate):
    try:
        url_collection = get_url_collection()
        short_code = await get_unique_short_code()
        url_data = request.model_dump()
        url_data["short_code"] = short_code

        await url_collection.insert_one(url_data)
        logger.info("URL data inserted successfully.")
        return {
            "short_code": short_code,
            "original_url": url_data["url"],
            "message": "URL shortened successfully."
        }
    except PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
