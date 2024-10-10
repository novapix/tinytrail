import string
import random

from database import url_collection

ALPHABETS = string.ascii_letters + string.digits
SHORT_CODE_LENGTH = 6


def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    return ''.join(random.choices(ALPHABETS, k=length))


async def get_unique_short_code() -> str:
    while True:
        short_code = generate_short_code()
        existing = await url_collection.find_one()
        if not existing:
            return short_code