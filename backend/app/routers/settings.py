from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.settings import ApiKeyStatus, SettingsRead

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=SettingsRead)
def read_settings(
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_user),
) -> SettingsRead:
    return SettingsRead(
        app_name=settings.app_name,
        environment=settings.environment,
        ai_provider=settings.ai_provider,
        ai_model=settings.ai_model,
        openai_configured=bool(settings.openai_api_key),
        default_scan_interval_minutes=settings.default_scan_interval_minutes,
        max_upload_mb=settings.max_upload_mb,
    )


@router.get("/openai-key", response_model=ApiKeyStatus)
def openai_key_status(
    settings: Settings = Depends(get_settings),
    _: User = Depends(get_current_user),
) -> ApiKeyStatus:
    return ApiKeyStatus(configured=bool(settings.openai_api_key))
