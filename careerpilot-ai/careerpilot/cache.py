import hashlib
import json
import os
from pathlib import Path

DEFAULT_REPORT_FILE = Path(".careerpilot-cache/report.json")


def is_cache_enabled() -> bool:
    """Disk caching is opt-in because reports may contain résumé-derived data."""
    return os.getenv("CAREERPILOT_ENABLE_DISK_CACHE", "false").lower() in {"1", "true", "yes"}


def get_report_file() -> Path:
    configured_path = os.getenv("CAREERPILOT_CACHE_PATH", "").strip()
    return Path(configured_path) if configured_path else DEFAULT_REPORT_FILE


def create_input_hash(resume_text, job_description):
    """Create a unique identifier for the current inputs."""
    combined_input = resume_text + "\n" + job_description
    return hashlib.sha256(combined_input.encode("utf-8")).hexdigest()


def load_cached_report(input_hash):
    """Return a saved report when the inputs have not changed."""
    if not is_cache_enabled():
        return None

    report_file = get_report_file()
    if not report_file.exists():
        return None
    try:
        saved_report = json.loads(report_file.read_text(encoding="utf-8"))
        if saved_report.get("input_hash") == input_hash:
            return saved_report
    except (json.JSONDecodeError, OSError):
        return None
    return None


def save_report(report):
    """Save the completed CareerPilot report."""
    if not is_cache_enabled():
        return False

    report_file = get_report_file()
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return True
