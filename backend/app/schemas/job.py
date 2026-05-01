from datetime import datetime

from pydantic import BaseModel


class JobRead(BaseModel):
    id: int
    title: str
    company: str | None = None
    location: str | None = None
    url: str
    description: str | None = None
    required_skills: list[str]
    employment_type: str | None = None
    salary: str | None = None
    remote: bool
    source_name: str | None = None
    score: int
    match_explanation: str | None = None
    missing_skills: list[str]
    status: str
    first_seen_at: datetime
    last_seen_at: datetime

    model_config = {"from_attributes": True}


class JobStatusUpdate(BaseModel):
    status: str
