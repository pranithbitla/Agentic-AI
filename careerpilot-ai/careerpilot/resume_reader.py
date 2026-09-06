from pathlib import Path

from pypdf import PdfReader

from careerpilot.config import (
    MAX_RESUME_CHARS,
    MAX_RESUME_FILE_BYTES,
    MAX_RESUME_PAGES,
    InputValidationError,
)


def extract_resume_text(pdf_path):
    """Extract résumé text from a supported PDF or plain-text file."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if path.stat().st_size > MAX_RESUME_FILE_BYTES:
        raise InputValidationError("The résumé file is larger than the 5 MB limit.")

    if path.suffix.lower() == ".txt":
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise InputValidationError("The pasted résumé text is empty.")
        if len(text) > MAX_RESUME_CHARS:
            raise InputValidationError(
                f"The résumé is too long. Keep it under {MAX_RESUME_CHARS:,} characters."
            )
        return text

    if path.suffix.lower() != ".pdf":
        raise InputValidationError("Only PDF and plain-text résumés are supported.")

    reader = PdfReader(str(path))
    if len(reader.pages) > MAX_RESUME_PAGES:
        raise InputValidationError(f"The résumé exceeds the {MAX_RESUME_PAGES}-page limit.")

    extracted_pages = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        cleaned_text = page_text.strip()
        if cleaned_text:
            extracted_pages.append(cleaned_text)

    if not extracted_pages:
        raise InputValidationError(
            "No readable text was found. Use a text-based PDF or paste the résumé text."
        )

    result = "\n".join(extracted_pages)
    if len(result) > MAX_RESUME_CHARS:
        raise InputValidationError(
            f"The extracted résumé is too long. Keep it under {MAX_RESUME_CHARS:,} characters."
        )
    return result
