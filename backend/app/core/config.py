from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = "postgresql+asyncpg://wishper:wishper@localhost:5432/wishper"
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    STORAGE_PATH: str = "/data/recordings"
    WHISPER_MODEL_SIZE: str = "base"
    WHISPER_COMPUTE_TYPE: str = "int8"
    MAX_UPLOAD_SIZE_MB: int = 500

    SUMMARY_MIN_SENTENCES: int = 3
    SUMMARY_MAX_SENTENCES: int = 10
    KEYWORDS_COUNT: int = 10
    CHUNK_DURATION_MINUTES: int = 15


@lru_cache
def get_settings() -> Settings:
    return Settings()
