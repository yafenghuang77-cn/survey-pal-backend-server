from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Survey Pal API"
    app_version: str = "0.1.0"
    environment: Literal["local", "test", "staging", "production"] = "local"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    database_url: SecretStr = SecretStr(
        "postgresql+asyncpg://survey_pal:survey_pal@localhost:5432/survey_pal"
    )
    database_pool_size: int = Field(default=10, ge=1)
    database_max_overflow: int = Field(default=20, ge=0)
    database_pool_timeout_seconds: float = Field(default=5.0, gt=0)

    redis_cache_url: SecretStr = SecretStr("redis://localhost:6379/0")
    redis_broker_url: SecretStr = SecretStr("redis://localhost:6380/0")
    redis_socket_timeout_seconds: float = Field(default=2.0, gt=0)

    jwt_secret_key: SecretStr = SecretStr("change-me-before-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=15, ge=1)
    refresh_token_expire_days: int = Field(default=30, ge=1)

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    sentry_dsn: str | None = None

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        if isinstance(value, str) and not value.lstrip().startswith("["):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
