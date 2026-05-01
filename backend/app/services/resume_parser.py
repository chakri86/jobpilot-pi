from pathlib import Path

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}
SUPPORTED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}


def validate_resume_upload(filename: str, content_type: str | None, size_bytes: int, max_mb: int) -> None:
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Resume must be a PDF, DOC, DOCX, or TXT file")
    if content_type and content_type not in SUPPORTED_CONTENT_TYPES:
        raise ValueError("Unsupported resume content type")
    if size_bytes > max_mb * 1024 * 1024:
        raise ValueError(f"Resume must be smaller than {max_mb} MB")


def extract_resume_text(filename: str, content: bytes) -> str:
    extension = Path(filename).suffix.lower()
    if extension == ".txt":
        return content.decode("utf-8", errors="ignore").strip()
    return (
        "Resume uploaded successfully. Full parsing for PDF and DOCX can be enabled "
        "with a document parser in a later release."
    )
