"""
Centralized settings management using pydantic-settings.
Loads only required API keys from environment variables / .env
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # API Keys
    groq_api_key: str = ""
    weather_api_key: str = ""
    exchange_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()