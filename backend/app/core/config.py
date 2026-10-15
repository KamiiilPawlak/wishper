from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://wishper:wishper@localhost:5432/wishper"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    storage_path: str = "/data/recordings"
    whisper_model_size: str = "base"
    whisper_compute_type: str = "int8"
    max_upload_size_mb: int = 500

    summary_min_sentences: int = 3
    summary_max_sentences: int = 10
    keywords_count: int = 10
    chunk_duration_minutes: int = 15


@lru_cache
def get_settings() -> Settings:
    return Settings()
