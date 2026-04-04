"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # API
    api_title: str = "OmniExtract Gateway"
    api_version: str = "0.1.0"
    debug: bool = False

    # Registry
    registry_path: str = "registry/models.yaml"
    prebuilts_path: str = "prebuilts"

    # Cache / DB
    redis_url: str = "redis://redis:6379/0"
    sqlite_path: str = "data/omniextract.db"

    # Worker (Local models)
    worker_base_url: str = "http://worker:8001"

    # Default timeouts (seconds)
    http_timeout: int = 60


settings = Settings()
