from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.qa_memory import QAMemory
from app.models.user import User
from app.schemas.qa_memory import QAMemoryCreate, QAMemoryRead, QAMemoryUpdate

router = APIRouter(prefix="/qa-memory", tags=["qa memory"])


@router.get("", response_model=list[QAMemoryRead])
def list_memory(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[QAMemory]:
    return (
        db.query(QAMemory)
        .filter(QAMemory.user_id == current_user.id)
        .order_by(QAMemory.updated_at.desc())
        .all()
    )


@router.post("", response_model=QAMemoryRead, status_code=status.HTTP_201_CREATED)
def create_memory(
    payload: QAMemoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QAMemory:
    item = QAMemory(user_id=current_user.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=QAMemoryRead)
def update_memory(
    item_id: int,
    payload: QAMemoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QAMemory:
    item = db.query(QAMemory).filter(QAMemory.id == item_id, QAMemory.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Q&A item not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    item = db.query(QAMemory).filter(QAMemory.id == item_id, QAMemory.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Q&A item not found")
    db.delete(item)
    db.commit()
