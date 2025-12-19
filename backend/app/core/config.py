from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core configuration
    database_url: str = "sqlite:///./offers.db"
    debug: bool = True

    # Pydantic Settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore unexpected env vars
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance so we don't re-parse .env multiple times.
    """
    return Settings()
