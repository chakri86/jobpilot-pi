from datetime import timedelta

from sqlalchemy.orm import Session

from app.connectors.registry import get_connector
from app.models.common import utc_now
from app.models.job import Job
from app.models.job_source import JobSource
from app.models.profile import Profile
from app.services.matching import score_listing


class ScanResult(dict):
    source_id: int
    discovered: int
    created: int
    updated: int


def scan_source(db: Session, source: JobSource) -> dict[str, int]:
    connector = get_connector(source.source_type)
    listings = connector.fetch(source.url)
    profile = db.query(Profile).filter(Profile.user_id == source.user_id).first()

    created = 0
    updated = 0
    for listing in listings:
        match = score_listing(profile, listing)
        existing = (
            db.query(Job)
            .filter(Job.source_id == source.id, Job.external_id == listing.external_id)
            .first()
        )
        if existing:
            job = existing
            updated += 1
        else:
            job = Job(user_id=source.user_id, source_id=source.id, external_id=listing.external_id)
            created += 1

        job.title = listing.title
        job.company = listing.company
        job.location = listing.location
        job.url = listing.url
        job.description = listing.description
        job.required_skills = listing.required_skills
        job.employment_type = listing.employment_type
        job.salary = listing.salary
        job.remote = listing.remote
        job.source_name = source.name
        job.score = match.score
        job.match_explanation = match.explanation
        job.missing_skills = match.missing_skills
        job.last_seen_at = utc_now()
        db.add(job)

    source.last_scanned_at = utc_now()
    db.add(source)
    db.commit()
    return {"source_id": source.id, "discovered": len(listings), "created": created, "updated": updated}


def scan_due_sources(db: Session) -> list[dict[str, int]]:
    now = utc_now()
    sources = db.query(JobSource).filter(JobSource.enabled.is_(True)).all()
    results: list[dict[str, int]] = []
    for source in sources:
        if source.last_scanned_at is None or source.last_scanned_at + timedelta(
            minutes=source.scan_interval_minutes
        ) <= now:
            results.append(scan_source(db, source))
    return results
