from datetime import datetime

from pydantic import BaseModel, Field


class QAMemoryCreate(BaseModel):
    question: str = Field(min_length=3)
    answer: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)


class QAMemoryUpdate(BaseModel):
    question: str | None = Field(default=None, min_length=3)
    answer: str | None = Field(default=None, min_length=1)
    tags: list[str] | None = None


class QAMemoryRead(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str
    tags: list[str]
    usage_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
