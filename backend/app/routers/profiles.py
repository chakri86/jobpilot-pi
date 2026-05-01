from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileRead, ProfileUpdate, ResumeUploadResponse
from app.services.resume_parser import extract_resume_text, validate_resume_upload

router = APIRouter(prefix="/profile", tags=["profile"])


def _get_or_create_profile(db: Session, user_id: int) -> Profile:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        return profile
    profile = Profile(user_id=user_id)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("", response_model=ProfileRead)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    return _get_or_create_profile(db, current_user.id)


@router.put("", response_model=ProfileRead)
def update_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    profile = _get_or_create_profile(db, current_user.id)
    for field, value in payload.model_dump().items():
        setattr(profile, field, value)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/resume", response_model=ResumeUploadResponse)
async def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeUploadResponse:
    settings = get_settings()
    content = await resume.read()
    try:
        validate_resume_upload(
            resume.filename or "resume",
            resume.content_type,
            len(content),
            settings.max_upload_mb,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    profile = _get_or_create_profile(db, current_user.id)
    safe_name = f"{uuid4().hex}{Path(resume.filename or 'resume').suffix.lower()}"
    upload_dir = Path(settings.upload_dir) / str(current_user.id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / safe_name).write_bytes(content)

    extracted = extract_resume_text(resume.filename or safe_name, content)
    profile.resume_filename = safe_name
    profile.resume_text = extracted
    db.add(profile)
    db.commit()

    return ResumeUploadResponse(filename=safe_name, extracted_preview=extracted[:500])
