from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JobPilot Pi"
    environment: str = "development"
    secret_key: str = Field(default="change-me", min_length=8)
    access_token_expire_minutes: int = 720
    allowed_origins: list[str] = [
        "http://192.168.0.249:5000",
        "http://localhost:5000",
        "http://localhost:5173",
    ]

    bootstrap_admin_email: str = "avkc@jobpilot.local"
    bootstrap_admin_password: str | None = None
    bootstrap_admin_force_password_change: bool = True

    database_url: str = "postgresql+psycopg://jobpilot:jobpilot@db:5432/jobpilot"

    openai_api_key: str | None = None
    ai_provider: str = "openai"
    ai_model: str = "gpt-4o-mini"

    default_scan_interval_minutes: int = 5
    max_upload_mb: int = 5
    upload_dir: str = "backend/uploads"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
