from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class Message(BaseModel):
    message: str

class DeletedMessage(Message):
    custom_msg: str = "Short URL Deleted Successfully"

class URLBase(BaseModel):
    url: HttpUrl


class URLCreate(URLBase):
    pass


class URLResponse(URLBase):
    id: str
    shortCode: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None


class URLStats(URLResponse):
    accessCount: int