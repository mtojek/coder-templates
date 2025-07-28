import calendar
from datetime import datetime, UTC
import html
import time

import feedparser

from rss_aggregator.config import settings
from rss_aggregator.models import Article


def scrape() -> None:

    for feed in settings.feeds:
        print(f"Fetching feed: {feed.name} ({feed.feed_id})")

        # TODO: client/server error
        # TODO: async workflow
        parsed = feedparser.parse(feed.url) # type: ignore
        for entry in parsed.entries: # type: ignore
            article = transform_parsed(feed.feed_id, entry) # type: ignore
            print(article)
            return

            # TODO check last published at
            # TODO db add & commit

def transform_parsed(feed_id: str, parsed : feedparser.FeedParserDict) -> Article:
    return Article(
        feed_id=feed_id,
        title=html.unescape(parsed.title), # type: ignore
        summary=html.unescape(parsed.summary), # type: ignore
        link=parsed.link, # type: ignore
        published_at=transform_datetime(parsed.published_parsed) # type: ignore
        # hashtags=
    )

def transform_datetime(struct_time: time.struct_time) -> datetime:
    print(struct_time)
    return datetime.fromtimestamp(calendar.timegm(struct_time), tz=UTC)

