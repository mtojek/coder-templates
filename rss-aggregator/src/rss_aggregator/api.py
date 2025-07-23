from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from rss_aggregator.db import get_db
from rss_aggregator.models import Article
from rss_aggregator.schemas import ArticleRead

articles_router = APIRouter()

@articles_router.get("/articles", response_model=List[ArticleRead], tags=["articles"])
def search_articles(
    q: Optional[str] = Query(None, description="Search term for article title"),
    after: Optional[datetime] = Query(None, description="Return articles published after this timestamp"),
    before: Optional[datetime] = Query(None, description="Return articles published before this timestamp"),
    hashtags: Optional[List[str]] = Query(None, description="Filter by any of these hashtags"),
    limit: int = Query(10, ge=1, le=50, description="Limit the number of results"),
    db: Session = Depends(get_db),
) -> List[Article]:
    query = db.query(Article)

    if after:
        query = query.filter(Article.published_at > after)
    if before:
        query = query.filter(Article.published_at < before)
    if hashtags:
        query = query.filter(Article.hashtags.overlap(hashtags))  # ANY match
    if q:
        query = query.filter(Article.title.ilike(f"%{q}%"))

    query = query.order_by(Article.published_at.desc()).limit(limit)
    return query.all()
