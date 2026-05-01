from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class JobSourceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    url: HttpUrl
    source_type: str = "mock"
    enabled: bool = True
    scan_interval_minutes: int = Field(default=5, ge=5, le=1440)


class JobSourceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    url: HttpUrl | None = None
    source_type: str | None = None
    enabled: bool | None = None
    scan_interval_minutes: int | None = Field(default=None, ge=5, le=1440)


class JobSourceRead(BaseModel):
    id: int
    user_id: int
    name: str
    url: str
    source_type: str
    enabled: bool
    scan_interval_minutes: int
    last_scanned_at: datetime | None = None

    model_config = {"from_attributes": True}


class SourceScanResponse(BaseModel):
    source_id: int
    discovered: int
    created: int
    updated: int
