from dataclasses import dataclass

from app.connectors.base import JobListing
from app.models.job import Job
from app.models.profile import Profile


@dataclass(frozen=True)
class MatchResult:
    score: int
    explanation: str
    missing_skills: list[str]


def _normalize(values: list[str] | None) -> set[str]:
    return {value.strip().lower() for value in values or [] if value.strip()}


def score_listing(profile: Profile | None, listing: JobListing | Job) -> MatchResult:
    if not profile:
        return MatchResult(
            score=35,
            explanation="Create a profile with target role and skills to improve matching.",
            missing_skills=list(getattr(listing, "required_skills", []) or []),
        )

    profile_skills = _normalize(profile.skills)
    required_skills = _normalize(getattr(listing, "required_skills", []))
    title = getattr(listing, "title", "") or ""
    description = getattr(listing, "description", "") or ""
    target_role = (profile.target_role or "").lower()

    skill_matches = profile_skills.intersection(required_skills)
    skill_score = int((len(skill_matches) / max(len(required_skills), 1)) * 55)
    role_score = 20 if target_role and target_role in title.lower() else 0
    text_score = 15 if any(skill in description.lower() for skill in profile_skills) else 0
    experience_score = 10 if profile.experience_years >= 1 else 0
    score = min(100, skill_score + role_score + text_score + experience_score)

    missing = sorted(required_skills.difference(profile_skills))
    matched = sorted(skill_matches)
    explanation = (
        f"Matched {len(matched)} required skills"
        + (f" ({', '.join(matched)})" if matched else "")
        + "."
    )
    if role_score:
        explanation += " Target role appears in the job title."
    if missing:
        explanation += f" Missing skills to review: {', '.join(missing)}."

    return MatchResult(score=score, explanation=explanation, missing_skills=missing)
