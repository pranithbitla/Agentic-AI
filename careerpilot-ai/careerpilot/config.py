import os

DEFAULT_MODEL = "gemini-3.5-flash-lite"
MAX_JOB_DESCRIPTION_CHARS = 20_000
MIN_JOB_DESCRIPTION_CHARS = 80
MAX_RESUME_CHARS = 15_000
MAX_RESUME_FILE_BYTES = 5 * 1024 * 1024
MAX_RESUME_PAGES = 10


class ConfigurationError(RuntimeError):
    """Raised when the application is not configured correctly."""


class InputValidationError(ValueError):
    """Raised when user-provided content cannot be safely processed."""


def get_api_key() -> str:
    """Return the configured Gemini API key or a user-friendly error."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ConfigurationError(
            "Gemini is not configured. Add GEMINI_API_KEY to a local .env file, "
            "then restart the app."
        )
    return api_key


def get_model_name() -> str:
    """Allow model changes without editing source code."""
    return os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def validate_job_description(job_description: str) -> str:
    """Validate and normalize a pasted job description."""
    normalized = job_description.strip()
    if len(normalized) < MIN_JOB_DESCRIPTION_CHARS:
        raise InputValidationError(
            "The job description is too short. "
            f"Add at least {MIN_JOB_DESCRIPTION_CHARS} characters."
        )
    if len(normalized) > MAX_JOB_DESCRIPTION_CHARS:
        raise InputValidationError(
            "The job description is too long. "
            f"Keep it under {MAX_JOB_DESCRIPTION_CHARS:,} characters."
        )
    return normalized
