import logging

from app.ai.fallback import LocalFallbackProvider
from app.ai.openai_provider import OpenAIProvider
from app.config import get_settings
from app.models.job import Job
from app.models.profile import Profile
from app.models.qa_memory import QAMemory

logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.provider = (
            OpenAIProvider(settings.openai_api_key, settings.ai_model)
            if settings.ai_provider == "openai" and settings.openai_api_key
            else LocalFallbackProvider()
        )

    def generate_application_pack(
        self,
        profile: Profile | None,
        job: Job,
        qa_items: list[QAMemory],
        question: str | None = None,
    ) -> dict[str, str]:
        try:
            return self.provider.generate_application_pack(profile, job, qa_items, question)
        except Exception:
            logger.exception("AI provider failed; using local fallback")
            return LocalFallbackProvider().generate_application_pack(profile, job, qa_items, question)
