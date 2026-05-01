from app.models.job import Job
from app.models.profile import Profile
from app.models.qa_memory import QAMemory


class LocalFallbackProvider:
    def generate_application_pack(
        self,
        profile: Profile | None,
        job: Job,
        qa_items: list[QAMemory],
        question: str | None = None,
    ) -> dict[str, str]:
        name = profile.full_name if profile and profile.full_name else "I"
        skills = ", ".join(profile.skills[:8]) if profile and profile.skills else "relevant experience"
        company = job.company or "your team"
        role = job.title
        reusable = "\n".join(f"- {item.question}: {item.answer}" for item in qa_items[:3])

        cover_letter = (
            f"Dear {company} hiring team,\n\n"
            f"{name} is excited to apply for the {role} role. My background in {skills} "
            f"aligns with the needs described in the posting, especially around "
            f"{', '.join(job.required_skills[:4]) or 'the core responsibilities'}.\n\n"
            "I would welcome the chance to discuss how I can contribute to this role.\n"
        )
        resume_suggestions = (
            "Resume suggestions:\n"
            "- Mirror the job title and top required skills where truthful.\n"
            "- Add a concise impact bullet for each matching skill.\n"
            "- Include Raspberry Pi, Docker, FastAPI, PostgreSQL, and React work if relevant."
        )
        answer_draft = (
            "Answer draft:\n"
            f"{question or 'Tell us why you are a fit for this role.'}\n\n"
            f"I would connect my experience in {skills} to the role's requirements. "
            "I would keep the answer specific, measurable, and tied to the employer's needs."
        )
        if reusable:
            answer_draft += f"\n\nRelevant saved Q&A:\n{reusable}"

        return {
            "cover_letter": cover_letter,
            "resume_suggestions": resume_suggestions,
            "answer_draft": answer_draft,
        }
