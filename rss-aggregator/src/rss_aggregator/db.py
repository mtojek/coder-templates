from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from rss_aggregator.config import settings
from rss_aggregator.models import Base

engine = create_engine(settings.database.url, echo=settings.database.echo)
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

def drop_db() -> None:
    print(f"Dropping all tables for database: {settings.database.url}")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped")
