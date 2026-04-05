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

    # LLM adapter safety defaults
    llm_max_tokens: int = 4000
    llm_max_retries: int = 2
    llm_retry_backoff_ms: int = 150
    llm_circuit_breaker_threshold: int = 5
    llm_circuit_breaker_cooldown_ms: int = 10000
    llm_circuit_breaker_half_open_max_calls: int = 1
    llm_circuit_breaker_backend: str = "memory"
    llm_circuit_breaker_redis_url: str = "redis://redis:6379/0"
    llm_circuit_breaker_redis_prefix: str = "cb:llm_router:"


settings = Settings()
