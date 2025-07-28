from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class DatabaseSettings(BaseModel):
    url: str
    echo: bool = False

class FeedSource(BaseModel):
    feed_id: str
    name: str
    url: str

class Settings(BaseSettings):
    database: DatabaseSettings
    feeds: list[FeedSource]

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    @classmethod
    def from_yaml(cls, path: Path = Path(__file__).resolve().parents[2] / "config.yaml"):
        with path.open("r") as f:
            data = yaml.safe_load(f)
        return cls(**data)


# Singleton instance to use throughout app
settings = Settings.from_yaml()