from sqlalchemy.orm import Session

from app.ai import AIClient
from app.models.application import Application
from app.models.job import Job
from app.models.profile import Profile
from app.models.qa_memory import QAMemory
from app.models.user import User


def generate_application_pack(
    db: Session,
    user: User,
    job: Job,
    question: str | None = None,
    application: Application | None = None,
) -> dict[str, str]:
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    qa_items = (
        db.query(QAMemory)
        .filter(QAMemory.user_id == user.id)
        .order_by(QAMemory.updated_at.desc())
        .all()
    )
    pack = AIClient().generate_application_pack(profile, job, qa_items, question)

    if application:
        application.cover_letter = pack["cover_letter"]
        application.resume_suggestions = pack["resume_suggestions"]
        application.answer_draft = pack["answer_draft"]
        db.add(application)
        db.commit()
        db.refresh(application)

    for item in qa_items[:3]:
        item.usage_count += 1
        db.add(item)
    db.commit()

    return pack
