from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.models.user import User


def list_profiles(db: Session, user: User) -> list[Profile]:
    profiles = (
        db.query(Profile)
        .filter(Profile.user_id == user.id)
        .order_by(Profile.is_active.desc(), Profile.updated_at.desc())
        .all()
    )
    if profiles:
        return profiles
    return [create_profile(db, user, Profile(name="Default Profile", user_id=user.id, is_active=True))]


def create_profile(db: Session, user: User, profile: Profile) -> Profile:
    has_profiles = db.query(Profile).filter(Profile.user_id == user.id).first() is not None
    profile.user_id = user.id
    profile.is_active = not has_profiles if not profile.is_active else profile.is_active
    db.add(profile)
    db.commit()
    db.refresh(profile)
    if profile.is_active:
        set_active_profile(db, user, profile.id)
        db.refresh(profile)
    return profile


def get_profile_for_user(db: Session, user: User, profile_id: int) -> Profile | None:
    return db.query(Profile).filter(Profile.id == profile_id, Profile.user_id == user.id).first()


def get_active_profile(db: Session, user_id: int) -> Profile | None:
    profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id, Profile.is_active.is_(True))
        .order_by(Profile.updated_at.desc())
        .first()
    )
    if profile:
        return profile
    return db.query(Profile).filter(Profile.user_id == user_id).order_by(Profile.updated_at.desc()).first()


def get_or_create_active_profile(db: Session, user: User) -> Profile:
    profile = get_active_profile(db, user.id)
    if profile:
        if not profile.is_active:
            return set_active_profile(db, user, profile.id)
        return profile
    return create_profile(db, user, Profile(name="Default Profile", user_id=user.id, is_active=True))


def set_active_profile(db: Session, user: User, profile_id: int) -> Profile:
    profile = get_profile_for_user(db, user, profile_id)
    if not profile:
        raise ValueError("Profile not found")
    db.query(Profile).filter(Profile.user_id == user.id).update({Profile.is_active: False})
    profile.is_active = True
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
