from pydantic import BaseModel


class SettingsRead(BaseModel):
    app_name: str
    environment: str
    ai_provider: str
    ai_model: str
    openai_configured: bool
    default_scan_interval_minutes: int
    max_upload_mb: int


class ApiKeyStatus(BaseModel):
    configured: bool
