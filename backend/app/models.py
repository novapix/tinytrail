from pydantic import BaseModel,HttpUrl


class URLCreate(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    id: str
    url: HttpUrl
    short_code: str
    created_at: str
    updated_at: str
    access_count: int