from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from logger import logger
from database import get_url_collection
from models import URLCreate, URLResponse
from utils import get_unique_short_code

router = APIRouter()

@router.post("/shorten")
async def shorten_url(request: URLCreate) -> URLResponse:
    try:
        url_collection = get_url_collection()
        if url_collection is None:
            raise Exception("URL COLLECTION IS NONE")
        short_code = await get_unique_short_code(url_collection=url_collection)
        current_time = datetime.now(timezone.utc)
        url_data = {
            "url": str(request.url),
            "shortCode": short_code,
            "createdAt": current_time,
            "updatedAt": current_time
        }

        result = await url_collection.insert_one(url_data)
        logger.info("URL data inserted successfully.")
        return URLResponse(
            id=str(result.inserted_id),
            url=request.url,
            shortCode=short_code,
            createdAt=url_data["createdAt"],
            updatedAt=url_data["updatedAt"]
        )
    except PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
