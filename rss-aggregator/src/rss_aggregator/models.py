from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    link = Column(Text)
    published_at = Column(TIMESTAMP)
    hashtags = Column(ARRAY(String), nullable=False, default=[])
