from app.models.job import Job
from app.models.profile import Profile
from app.models.qa_memory import QAMemory


class OpenAIProvider:
    def __init__(self, api_key: str | None, model: str) -> None:
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_application_pack(
        self,
        profile: Profile | None,
        job: Job,
        qa_items: list[QAMemory],
        question: str | None = None,
    ) -> dict[str, str]:
        profile_text = {
            "name": profile.full_name if profile else None,
            "target_role": profile.target_role if profile else None,
            "skills": profile.skills if profile else [],
            "experience_years": profile.experience_years if profile else 0,
        }
        qa_text = [{"question": item.question, "answer": item.answer} for item in qa_items[:10]]
        prompt = (
            "Create a concise application assistance pack. Return three sections with headings: "
            "Cover Letter, Resume Suggestions, Answer Draft.\n\n"
            f"Profile: {profile_text}\n"
            f"Job: title={job.title}, company={job.company}, description={job.description}, "
            f"required_skills={job.required_skills}\n"
            f"Reusable Q&A: {qa_text}\n"
            f"Specific question: {question or 'None'}"
        )
        response = self.client.responses.create(model=self.model, input=prompt)
        text = response.output_text
        return _split_sections(text)


def _split_sections(text: str) -> dict[str, str]:
    lower = text.lower()
    cover_idx = lower.find("cover letter")
    resume_idx = lower.find("resume suggestions")
    answer_idx = lower.find("answer draft")

    if cover_idx == -1 or resume_idx == -1 or answer_idx == -1:
        return {
            "cover_letter": text.strip(),
            "resume_suggestions": "Review the job requirements and tune truthful resume bullets.",
            "answer_draft": "Draft an answer using your saved Q&A memory and the job description.",
        }

    return {
        "cover_letter": text[cover_idx:resume_idx].strip(),
        "resume_suggestions": text[resume_idx:answer_idx].strip(),
        "answer_draft": text[answer_idx:].strip(),
    }
