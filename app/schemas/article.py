from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ArticleResponse(ArticleBase):
    id: int
    author: str
    rating: float
    published: datetime
    author_id: int

    class Config:
        from_attributes = True