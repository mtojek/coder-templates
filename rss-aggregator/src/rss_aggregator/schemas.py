from pydantic import BaseModel
from datetime import datetime
from typing import List

class ArticleRead(BaseModel):
    id: int
    feed_id: str
    title: str
    summary: str | None
    link: str
    published_at: datetime
    hashtags: List[str]

    class Config:
        from_attributes = True