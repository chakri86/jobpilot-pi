from dataclasses import dataclass, field


@dataclass(frozen=True)
class JobListing:
    external_id: str
    title: str
    company: str
    location: str
    url: str
    description: str
    required_skills: list[str] = field(default_factory=list)
    employment_type: str | None = None
    salary: str | None = None
    remote: bool = False


class BaseJobConnector:
    def fetch(self, source_url: str) -> list[JobListing]:
        raise NotImplementedError
