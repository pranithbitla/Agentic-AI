import pytest

from careerpilot.config import (
    ConfigurationError,
    InputValidationError,
    get_api_key,
    get_model_name,
    validate_job_description,
)


def test_api_key_is_required(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ConfigurationError, match="GEMINI_API_KEY"):
        get_api_key()


def test_model_name_can_be_configured(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "custom-model")
    assert get_model_name() == "custom-model"


def test_api_key_and_default_model(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    assert get_api_key() == "test-key"
    assert get_model_name() == "gemini-3.5-flash-lite"


@pytest.mark.parametrize("description", ["", "too short"])
def test_job_description_rejects_short_input(description):
    with pytest.raises(InputValidationError, match="too short"):
        validate_job_description(description)


def test_job_description_is_trimmed():
    description = "  " + "Python developer role with API testing and documentation. " * 2 + "  "
    assert validate_job_description(description) == description.strip()


def test_job_description_rejects_oversized_input():
    with pytest.raises(InputValidationError, match="too long"):
        validate_job_description("x" * 20_001)
