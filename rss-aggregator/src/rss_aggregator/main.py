from fastapi import FastAPI
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

def start():
    uvicorn.run("rss_aggregator.main:app", host="0.0.0.0", port=8080, reload=True)

# Include modular routes
# app.include_router(health.router)
# app.include_router(search.router)