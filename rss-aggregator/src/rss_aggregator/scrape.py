from typing import cast, List

import calendar
from datetime import datetime, UTC
import html
import time
import logging

import feedparser
from sqlalchemy import select, func

from rss_aggregator.db import SessionLocal, Session
from rss_aggregator.config import settings
from rss_aggregator.logger import setup_logging
from rss_aggregator.models import Article
from rss_aggregator.transformer import keyword_extractor, embedder

logger = logging.getLogger(__name__)


def scrape() -> None:
    setup_logging()

    for feed in settings.feeds:
        logger.info(f"Fetching feed: {feed.name} ({feed.feed_id})")

        with SessionLocal() as db:
            last_published_at = get_last_published_at(db, feed.feed_id)
            if last_published_at != None:
                logger.info(f"Last published article at: {last_published_at}")

            # TODO: async workflow
            # FIXME: client/server error
            parsed = feedparser.parse(feed.url)
            for entry in parsed.entries:
                article = transform_parsed(feed.feed_id, entry)
                logger.info(f"Found link: {article.link} (published at: {article.published_at})")

                logger.info(f"article.published_at = {article.published_at} , last_published_at = {last_published_at}")
                if last_published_at and article.published_at <= last_published_at:
                    logger.info("Article already archieved")
                    continue
                else:
                    logger.info("Article not archieved yet")

                article = attach_embeddings(article)
                db.add(article)
                logger.info("Article archieved")

            db.commit()

def transform_parsed(feed_id: str, parsed : feedparser.FeedParserDict) -> Article:
    return Article(
        feed_id=feed_id,
        title=html.unescape(parsed.title), # type: ignore
        summary=html.unescape(parsed.summary), # type: ignore
        link=parsed.link,
        published_at=transform_datetime(parsed.published_parsed), # type: ignore
    )

def attach_embeddings(article: Article) -> Article:
    transformer_input : str = f"{article.title}. {article.summary}"
    keywords = keyword_extractor.extract_keywords(transformer_input, top_n=5)
    hashtags = [kw[0] for kw in keywords]
    embeddings = embedder.encode(transformer_input)
    article.hashtags = cast(List[str], hashtags)
    article.embeddings = cast(List[float], embeddings)
    return article

def transform_datetime(struct_time: time.struct_time) -> datetime:
    return datetime.fromtimestamp(calendar.timegm(struct_time), tz=UTC)

def get_last_published_at(db: Session, feed_id: str) -> datetime | None:
    stmt = (
        select(func.max(Article.published_at))
        .where(Article.feed_id == feed_id)
    )
    result = db.execute(stmt).scalar_one_or_none()
    return result