import string
import random
from pymongo.errors import PyMongoError

from logger import logger
from database import get_url_collection

ALPHABETS = string.ascii_letters + string.digits
SHORT_CODE_LENGTH = 6

def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    return ''.join(random.choices(ALPHABETS, k=length))


async def get_unique_short_code():
    url_collection = get_url_collection()
    while True:
        short_code = generate_short_code()
        try:
            existing = await url_collection.find_one({"short_code": short_code})
            if existing is None:
                return short_code

        except PyMongoError as e:
            logger.error(f"Database error: {e}")
            raise