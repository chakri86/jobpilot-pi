import logging

from sqlalchemy.orm import Session

from app.config import Settings
from app.models.user import User
from app.security.passwords import hash_password, verify_password

logger = logging.getLogger(__name__)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def bootstrap_admin(db: Session, settings: Settings) -> None:
    if not settings.bootstrap_admin_password:
        logger.warning("BOOTSTRAP_ADMIN_PASSWORD is not set; admin bootstrap skipped")
        return

    email = settings.bootstrap_admin_email.lower()
    existing = get_user_by_email(db, email)
    if existing:
        return

    user = User(
        email=email,
        password_hash=hash_password(settings.bootstrap_admin_password),
        is_admin=True,
        must_change_password=settings.bootstrap_admin_force_password_change,
    )
    db.add(user)
    db.commit()
    logger.info("Bootstrap admin created for %s", email)


def change_password(db: Session, user: User, current_password: str, new_password: str) -> bool:
    if not verify_password(current_password, user.password_hash):
        return False
    user.password_hash = hash_password(new_password)
    user.must_change_password = False
    db.add(user)
    db.commit()
    return True
