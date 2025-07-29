from typing import List
from sqlalchemy import Column, Float, Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    link = Column(Text)
    published_at = Column(TIMESTAMP)
    hashtags: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False)
    embeddings: Mapped[List[float]] = mapped_column(ARRAY(Float), nullable=False)