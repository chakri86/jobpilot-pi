from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate, ResumeUploadResponse
from app.services.profile_service import (
    create_profile,
    get_or_create_active_profile,
    get_profile_for_user,
    list_profiles,
    set_active_profile,
)
from app.services.resume_parser import extract_resume_text, validate_resume_upload

router = APIRouter(tags=["profiles"])


@router.get("/profile", response_model=ProfileRead)
def get_active_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    return get_or_create_active_profile(db, current_user)


@router.put("/profile", response_model=ProfileRead)
def update_active_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    profile = get_or_create_active_profile(db, current_user)
    return _update_profile(db, profile, payload)


@router.post("/profile/resume", response_model=ResumeUploadResponse)
async def upload_active_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeUploadResponse:
    profile = get_or_create_active_profile(db, current_user)
    return await _upload_resume(db, current_user, profile, resume)


@router.get("/profiles", response_model=list[ProfileRead])
def get_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Profile]:
    return list_profiles(db, current_user)


@router.post("/profiles", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
def add_profile(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    return create_profile(db, current_user, Profile(**payload.model_dump()))


@router.get("/profiles/{profile_id}", response_model=ProfileRead)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    profile = get_profile_for_user(db, current_user, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.put("/profiles/{profile_id}", response_model=ProfileRead)
def update_profile(
    profile_id: int,
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    profile = get_profile_for_user(db, current_user, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return _update_profile(db, profile, payload)


@router.post("/profiles/{profile_id}/activate", response_model=ProfileRead)
def activate_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Profile:
    try:
        return set_active_profile(db, current_user, profile_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found") from exc


@router.post("/profiles/{profile_id}/resume", response_model=ResumeUploadResponse)
async def upload_profile_resume(
    profile_id: int,
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeUploadResponse:
    profile = get_profile_for_user(db, current_user, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return await _upload_resume(db, current_user, profile, resume)


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    profiles = list_profiles(db, current_user)
    if len(profiles) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one profile is required",
        )
    profile = get_profile_for_user(db, current_user, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    was_active = profile.is_active
    db.delete(profile)
    db.commit()
    if was_active:
        remaining = list_profiles(db, current_user)[0]
        set_active_profile(db, current_user, remaining.id)


def _update_profile(db: Session, profile: Profile, payload: ProfileUpdate) -> Profile:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


async def _upload_resume(
    db: Session,
    current_user: User,
    profile: Profile,
    resume: UploadFile,
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

    safe_name = f"{uuid4().hex}{Path(resume.filename or 'resume').suffix.lower()}"
    upload_dir = Path(settings.upload_dir) / str(current_user.id) / str(profile.id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / safe_name).write_bytes(content)

    extracted = extract_resume_text(resume.filename or safe_name, content)
    profile.resume_filename = safe_name
    profile.resume_text = extracted
    db.add(profile)
    db.commit()

    return ResumeUploadResponse(filename=safe_name, extracted_preview=extracted[:500])
