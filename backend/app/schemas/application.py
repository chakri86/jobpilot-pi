from datetime import datetime

from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    job_id: int
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    status: str | None = None
    cover_letter: str | None = None
    resume_suggestions: str | None = None
    answer_draft: str | None = None
    notes: str | None = None


class ApplicationRead(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    cover_letter: str | None = None
    resume_suggestions: str | None = None
    answer_draft: str | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AssistantRequest(BaseModel):
    application_id: int | None = None
    job_id: int
    question: str | None = None


class AssistantResponse(BaseModel):
    cover_letter: str
    resume_suggestions: str
    answer_draft: str
