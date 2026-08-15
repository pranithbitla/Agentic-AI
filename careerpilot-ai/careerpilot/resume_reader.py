from pathlib import Path
from pypdf import PdfReader


def extract_resume_text(pdf_path):
    """Extract and return text from a text-based PDF résumé."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    reader = PdfReader(str(path))
    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        cleaned_text = page_text.strip()
        if cleaned_text:
            extracted_pages.append(cleaned_text)
        else:
            print(f"Warning: Page {page_number} has no readable text.")

    if not extracted_pages:
        raise ValueError("No readable text was found in the PDF.")

    return "\n".join(extracted_pages)
