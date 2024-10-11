from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
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
        current_time =  datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
        url_data = {
            "url": str(request.url),
            "shortCode": short_code,
            "createdAt": current_time,
            "updatedAt": current_time,
            "accessCount": 0
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")


@router.get("/shorten/{short_code}")
async def get_original_url(short_code: str) -> URLResponse:
   try:
       url_collection = get_url_collection()
       if url_collection is None:
           raise Exception("URL COLLECTION IS NONE")
       url_entry = await url_collection.find_one({"shortCode": short_code})
       if not url_entry:
           logger.warning("Short Code not assigned")
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")

       return URLResponse(
           id=str(url_entry["_id"]),
           url=url_entry["url"],
           shortCode=url_entry["shortCode"],
           createdAt=url_entry["createdAt"],
           updatedAt=url_entry.get("updatedAt")
       )
   except PyMongoError as e:
       logger.error(f"Database error: {e}")
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error.")
   except HTTPException as http_ex:
       logger.error(f"HTTP error occurred: {http_ex.detail}")
       raise http_ex
   except Exception as e:
       logger.error(f"An unexpected error occurred: {e}")
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred.")

