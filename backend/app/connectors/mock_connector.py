from hashlib import sha256

from app.connectors.base import BaseJobConnector, JobListing


class MockJobConnector(BaseJobConnector):
    """Safe connector that creates deterministic sample jobs from a configured URL."""

    def fetch(self, source_url: str) -> list[JobListing]:
        seed = sha256(source_url.encode("utf-8")).hexdigest()[:10]
        return [
            JobListing(
                external_id=f"{seed}-fastapi",
                title="Full Stack Python Engineer",
                company="LocalTech Labs",
                location="Remote",
                url=f"{source_url.rstrip('/')}/jobs/full-stack-python-engineer",
                description=(
                    "Build FastAPI services, React dashboards, PostgreSQL models, "
                    "and AI-assisted workflows for a small product team."
                ),
                required_skills=["Python", "FastAPI", "React", "PostgreSQL", "Docker"],
                employment_type="Full-time",
                salary="$110k-$145k",
                remote=True,
            ),
            JobListing(
                external_id=f"{seed}-platform",
                title="DevOps Platform Engineer",
                company="EdgeOps Systems",
                location="Hybrid",
                url=f"{source_url.rstrip('/')}/jobs/devops-platform-engineer",
                description=(
                    "Own Docker Compose deployments, Linux services, monitoring, "
                    "and secure release workflows for edge devices."
                ),
                required_skills=["Docker", "Linux", "PostgreSQL", "GitHub Actions", "Security"],
                employment_type="Contract",
                salary="$80-$110/hr",
                remote=False,
            ),
        ]
