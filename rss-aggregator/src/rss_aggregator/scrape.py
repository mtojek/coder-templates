from typing import cast, List

import calendar
from datetime import datetime, UTC
import html
import time
import logging

import feedparser

from rss_aggregator.config import settings
from rss_aggregator.logger import setup_logging
from rss_aggregator.models import Article
from rss_aggregator.transformer import keyword_extractor, embedder

logger = logging.getLogger(__name__)


def scrape() -> None:
    setup_logging()

    for feed in settings.feeds:
        logger.info(f"Fetching feed: {feed.name} ({feed.feed_id})")

        # TODO: client/server error
        # TODO: async workflow
        parsed = feedparser.parse(feed.url)
        for entry in parsed.entries:
            article = transform_parsed(feed.feed_id, entry)
            logger.info(f"Found link: {article.link} (published at: {article.published_at})")

            # TODO check last published at

            article = attach_transformers(article)
            return

            # TODO db add & commit

def transform_parsed(feed_id: str, parsed : feedparser.FeedParserDict) -> Article:
    return Article(
        feed_id=feed_id,
        title=html.unescape(parsed.title), # type: ignore
        summary=html.unescape(parsed.summary), # type: ignore
        link=parsed.link, # type: ignore
        published_at=transform_datetime(parsed.published_parsed), # type: ignore
    )

def attach_transformers(article: Article) -> Article:
    transformer_input : str = f"{article.title}. {article.summary}"
    keywords = keyword_extractor.extract_keywords(transformer_input, top_n=5)
    hashtags = [kw[0] for kw in keywords]
    embeddings = embedder.encode(transformer_input)
    article.hashtags = cast(List[str], hashtags)
    article.embeddings = cast(List[float], embeddings)
    return article

def transform_datetime(struct_time: time.struct_time) -> datetime:
    return datetime.fromtimestamp(calendar.timegm(struct_time), tz=UTC)