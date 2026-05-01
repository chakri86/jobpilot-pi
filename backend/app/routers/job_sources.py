from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.job_source import JobSource
from app.models.user import User
from app.schemas.job_source import JobSourceCreate, JobSourceRead, JobSourceUpdate, SourceScanResponse
from app.services.job_collector import scan_source

router = APIRouter(prefix="/sources", tags=["job sources"])


@router.get("", response_model=list[JobSourceRead])
def list_sources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[JobSource]:
    return (
        db.query(JobSource)
        .filter(JobSource.user_id == current_user.id)
        .order_by(JobSource.created_at.desc())
        .all()
    )


@router.post("", response_model=JobSourceRead, status_code=status.HTTP_201_CREATED)
def create_source(
    payload: JobSourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobSource:
    source = JobSource(
        user_id=current_user.id,
        name=payload.name,
        url=str(payload.url),
        source_type=payload.source_type,
        enabled=payload.enabled,
        scan_interval_minutes=payload.scan_interval_minutes,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.put("/{source_id}", response_model=JobSourceRead)
def update_source(
    source_id: int,
    payload: JobSourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobSource:
    source = (
        db.query(JobSource)
        .filter(JobSource.id == source_id, JobSource.user_id == current_user.id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(source, field, str(value) if field == "url" else value)
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    source = (
        db.query(JobSource)
        .filter(JobSource.id == source_id, JobSource.user_id == current_user.id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    db.delete(source)
    db.commit()


@router.post("/{source_id}/scan", response_model=SourceScanResponse)
def scan_source_now(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, int]:
    source = (
        db.query(JobSource)
        .filter(JobSource.id == source_id, JobSource.user_id == current_user.id)
        .first()
    )
    if not source:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return scan_source(db, source)
