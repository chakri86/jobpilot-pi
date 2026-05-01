from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    full_name: str | None = None
    target_role: str | None = None
    location: str | None = None
    experience_years: int = Field(default=0, ge=0, le=70)
    skills: list[str] = Field(default_factory=list)
    preferences: dict = Field(default_factory=dict)


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: int
    user_id: int
    resume_filename: str | None = None
    resume_text: str | None = None

    model_config = {"from_attributes": True}


class ResumeUploadResponse(BaseModel):
    filename: str
    extracted_preview: str
