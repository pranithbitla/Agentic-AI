import pytest

from careerpilot import resume_reader
from careerpilot.config import MAX_RESUME_CHARS, InputValidationError
from careerpilot.resume_reader import extract_resume_text


def test_plain_text_resume_is_supported(tmp_path):
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("  Python developer with Git experience.  ", encoding="utf-8")
    assert extract_resume_text(resume_path) == "Python developer with Git experience."


def test_empty_plain_text_resume_is_rejected(tmp_path):
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("   ", encoding="utf-8")
    with pytest.raises(InputValidationError, match="empty"):
        extract_resume_text(resume_path)


def test_unsupported_resume_type_is_rejected(tmp_path):
    resume_path = tmp_path / "resume.docx"
    resume_path.write_text("content", encoding="utf-8")
    with pytest.raises(InputValidationError, match="Only PDF"):
        extract_resume_text(resume_path)


def test_oversized_resume_text_is_rejected(tmp_path):
    resume_path = tmp_path / "resume.txt"
    resume_path.write_text("x" * (MAX_RESUME_CHARS + 1), encoding="utf-8")
    with pytest.raises(InputValidationError, match="too long"):
        extract_resume_text(resume_path)


def test_missing_resume_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_resume_text(tmp_path / "missing.pdf")


def test_pdf_text_is_extracted(monkeypatch, tmp_path):
    resume_path = tmp_path / "resume.pdf"
    resume_path.write_bytes(b"small-test-file")
    pages = [
        SimplePage(" Python developer "),
        SimplePage("Git and LangGraph"),
    ]
    monkeypatch.setattr(resume_reader, "PdfReader", lambda path: FakeReader(pages))

    assert extract_resume_text(resume_path) == "Python developer\nGit and LangGraph"


def test_pdf_without_readable_text_is_rejected(monkeypatch, tmp_path):
    resume_path = tmp_path / "resume.pdf"
    resume_path.write_bytes(b"small-test-file")
    monkeypatch.setattr(resume_reader, "PdfReader", lambda path: FakeReader([SimplePage(None)]))

    with pytest.raises(InputValidationError, match="No readable text"):
        extract_resume_text(resume_path)


def test_pdf_page_limit_is_enforced(monkeypatch, tmp_path):
    resume_path = tmp_path / "resume.pdf"
    resume_path.write_bytes(b"small-test-file")
    monkeypatch.setattr(
        resume_reader,
        "PdfReader",
        lambda path: FakeReader([SimplePage("text")] * 11),
    )

    with pytest.raises(InputValidationError, match="10-page"):
        extract_resume_text(resume_path)


class SimplePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


class FakeReader:
    def __init__(self, pages):
        self.pages = pages
