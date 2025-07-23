from fastapi import FastAPI
from rss_aggregator.api import articles_router
import uvicorn

app = FastAPI(
    title="RSS Aggregator API",
    description="Aggregates and searches RSS feed content using vector embeddings.",
    version="0.1.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

def start() -> None:
    uvicorn.run("rss_aggregator.main:app", host="0.0.0.0", port=8080, reload=True)

app.include_router(articles_router, prefix="/api/v1")