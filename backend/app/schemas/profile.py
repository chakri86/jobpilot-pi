from pydantic import BaseModel, Field


class ProfileBase(BaseModel):
    name: str = Field(default="Default Profile", min_length=2, max_length=255)
    full_name: str | None = None
    target_role: str | None = None
    location: str | None = None
    experience_years: int = Field(default=0, ge=0, le=70)
    skills: list[str] = Field(default_factory=list)
    preferences: dict = Field(default_factory=dict)


class ProfileUpdate(ProfileBase):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    full_name: str | None = None
    target_role: str | None = None
    location: str | None = None
    experience_years: int | None = Field(default=None, ge=0, le=70)
    skills: list[str] | None = None
    preferences: dict | None = None


class ProfileRead(ProfileBase):
    id: int
    user_id: int
    is_active: bool
    resume_filename: str | None = None
    resume_text: str | None = None

    model_config = {"from_attributes": True}


class ProfileCreate(ProfileBase):
    pass


class ResumeUploadResponse(BaseModel):
    filename: str
    extracted_preview: str
