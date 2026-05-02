from hashlib import sha256
from urllib.parse import unquote, urlparse

from app.connectors.base import BaseJobConnector, JobListing


class MockJobConnector(BaseJobConnector):
    """Safe connector that creates deterministic sample jobs from configured source text."""

    def fetch(self, source_url: str, source_name: str | None = None) -> list[JobListing]:
        source_text = _source_text(source_url, source_name)
        seed = sha256(f"{source_name or ''}:{source_url}".encode()).hexdigest()[:10]
        if "product" in source_text or "manager" in source_text:
            return _product_manager_jobs(seed, source_url)
        if "data" in source_text or "analyst" in source_text:
            return _data_jobs(seed, source_url)
        if "design" in source_text or "ux" in source_text:
            return _design_jobs(seed, source_url)
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


def _source_text(source_url: str, source_name: str | None) -> str:
    parsed = urlparse(source_url)
    parts = [
        source_name or "",
        parsed.path,
        parsed.query,
        unquote(source_url),
    ]
    return " ".join(parts).lower().replace("-", " ").replace("_", " ")


def _product_manager_jobs(seed: str, source_url: str) -> list[JobListing]:
    return [
        JobListing(
            external_id=f"{seed}-ai-product-manager",
            title="AI Product Manager",
            company="Northstar Labs",
            location="Remote",
            url=f"{source_url.rstrip('/')}/jobs/ai-product-manager",
            description=(
                "Lead roadmap planning, customer discovery, launch coordination, "
                "and AI product experiments for a growing software platform."
            ),
            required_skills=[
                "Product Strategy",
                "Roadmap",
                "User Research",
                "Analytics",
                "Stakeholder Management",
            ],
            employment_type="Full-time",
            salary="$125k-$160k",
            remote=True,
        ),
        JobListing(
            external_id=f"{seed}-technical-product-manager",
            title="Technical Product Manager",
            company="CloudBridge Systems",
            location="Hybrid",
            url=f"{source_url.rstrip('/')}/jobs/technical-product-manager",
            description=(
                "Work with engineering, design, and customer teams to prioritize "
                "API, workflow, and reporting features."
            ),
            required_skills=["Agile", "APIs", "SQL", "UX", "Prioritization"],
            employment_type="Full-time",
            salary="$115k-$150k",
            remote=False,
        ),
    ]


def _data_jobs(seed: str, source_url: str) -> list[JobListing]:
    return [
        JobListing(
            external_id=f"{seed}-data-analyst",
            title="Data Analyst",
            company="MetricWorks",
            location="Remote",
            url=f"{source_url.rstrip('/')}/jobs/data-analyst",
            description="Build dashboards, analyze product funnels, and turn data into decisions.",
            required_skills=["SQL", "Python", "Dashboards", "Analytics", "Communication"],
            employment_type="Full-time",
            salary="$85k-$115k",
            remote=True,
        ),
        JobListing(
            external_id=f"{seed}-business-intelligence-analyst",
            title="Business Intelligence Analyst",
            company="SignalPath",
            location="Hybrid",
            url=f"{source_url.rstrip('/')}/jobs/business-intelligence-analyst",
            description=(
                "Create reporting models, maintain metrics definitions, "
                "and support business reviews."
            ),
            required_skills=["SQL", "BI", "Data Modeling", "Stakeholder Management", "Excel"],
            employment_type="Full-time",
            salary="$90k-$120k",
            remote=False,
        ),
    ]


def _design_jobs(seed: str, source_url: str) -> list[JobListing]:
    return [
        JobListing(
            external_id=f"{seed}-product-designer",
            title="Product Designer",
            company="CanvasLine",
            location="Remote",
            url=f"{source_url.rstrip('/')}/jobs/product-designer",
            description="Design product flows, prototypes, and user-tested improvements for SaaS tools.",
            required_skills=["Figma", "UX", "Prototyping", "User Research", "Design Systems"],
            employment_type="Full-time",
            salary="$100k-$135k",
            remote=True,
        ),
        JobListing(
            external_id=f"{seed}-ux-researcher",
            title="UX Researcher",
            company="InsightLoop",
            location="Remote",
            url=f"{source_url.rstrip('/')}/jobs/ux-researcher",
            description="Plan research studies and synthesize customer insights for product teams.",
            required_skills=["User Research", "Interviews", "Analytics", "Synthesis", "Communication"],
            employment_type="Contract",
            salary="$70-$95/hr",
            remote=True,
        ),
    ]
