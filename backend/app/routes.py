from typing import Any, Mapping, Optional

from fastapi import APIRouter, HTTPException, status, Response
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult, UpdateResult

from .logger import logger
from .database import get_url_collection
from .models import URLCreate, URLResponse, Message, DeletedMessage
from .utils import get_unique_short_code, get_current_time, find_url_by_short_code

router = APIRouter()


async def get_url_response(short_code: str) -> URLResponse:
    try:
        urls_collection: Optional[AsyncIOMotorCollection] = get_url_collection()
        if urls_collection is None:
            raise PyMongoError("URL COLLECTION IS NONE")

        url_entry: Optional[Mapping[str, Any]] = await find_url_by_short_code(
            short_code, urls_collection
        )
        if not url_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
            )

        return URLResponse(
            id=str(url_entry["_id"]),
            url=url_entry["url"],
            shortCode=url_entry["shortCode"],
            createdAt=url_entry["createdAt"],
            updatedAt=url_entry.get("updatedAt"),
        )
    except PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error."
        )
    except HTTPException as http_ex:
        logger.error(f"HTTP error occurred: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )

@router.post("/shorten")
async def shorten_url(request: URLCreate) -> URLResponse:
    try:
        urls_collection: Optional[AsyncIOMotorCollection] = get_url_collection()
        if urls_collection is None:
            raise Exception("URL COLLECTION IS NONE")
        short_code = await get_unique_short_code(url_collection=urls_collection)
        current_time = get_current_time()
        url_data = {
            "url": str(request.url),
            "shortCode": short_code,
            "createdAt": current_time,
            "updatedAt": current_time,
            "accessCount": 0,
        }

        result: InsertOneResult = await urls_collection.insert_one(url_data)
        logger.info("URL data inserted successfully.")
        return URLResponse(
            id=str(result.inserted_id),
            url=request.url,
            shortCode=short_code,
            createdAt=url_data["createdAt"],
            updatedAt=url_data["updatedAt"],
        )
    except PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error."
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


@router.get(
    "/shorten/{short_code}",
    response_model=URLResponse,
    responses={
        404: {"model": Message, "description": "The short URL was not found"},
        200: {
            "description": "Original URL retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "some_id",
                        "url": "https://example.com/original",
                        "shortCode": "abc123",
                        "createdAt": "2024-01-01T12:00:00",
                        "updatedAt": "2024-01-01T12:00:00",
                    }
                }
            },
        },
    },
)
async def get_original_url(short_code: str) -> URLResponse:
    return await get_url_response(short_code)


@router.get("/{short_code}/stats", response_model=URLResponse)
async def get_url_stats(short_code: str) -> URLResponse:
    return await get_url_response(short_code)


@router.put("/shorten/{short_code}")
async def update_long_url(url_update: URLCreate, short_code: str) -> URLResponse:
    try:
        urls_collection: Optional[AsyncIOMotorCollection] = get_url_collection()
        url_entry: Optional[Mapping[str, Any]] = await find_url_by_short_code(
            short_code, urls_collection
        )
        if not url_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
            )
        if urls_collection is None:
            raise Exception("URL COLLECTION IS NONE")
        update_result: UpdateResult = await urls_collection.update_one(
            {"shortCode": short_code},
            {"$set": {"url": str(url_update.url), "updatedAt": get_current_time()}},
        )
        if update_result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
            )

        updated_entry = await find_url_by_short_code(short_code,urls_collection)
        if not updated_entry:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Short URL not found after update",
            )

        return URLResponse(
            id=str(url_entry["_id"]),
            url=url_entry["url"],
            shortCode=url_entry["shortCode"],
            createdAt=url_entry["createdAt"],
            updatedAt=url_entry.get("updatedAt"),
        )
    except PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error."
        )
    except HTTPException as http_ex:
        logger.error(f"HTTP error occurred: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )



# noinspection DuplicatedCode
@router.delete("/shorten/{short_code}")
async def delete_url(short_code: str, response: Response) -> Message:
    try:
        urls_collection: Optional[AsyncIOMotorCollection] = get_url_collection()
        url_entry: Optional[Mapping[str, Any]] = await find_url_by_short_code(
            short_code, urls_collection
        )
        if not url_entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found"
            )
        if urls_collection is None:
            raise Exception("URL COLLECTION IS NONE")
        delete_result = await urls_collection.delete_one({"shortCode": short_code})
        if delete_result.deleted_count:
            response.status_code = status.HTTP_204_NO_CONTENT
            return DeletedMessage()
    except PyMongoError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error."
        )
    except HTTPException as http_ex:
        logger.error(f"HTTP error occurred: {http_ex.detail}")
        raise http_ex
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )



