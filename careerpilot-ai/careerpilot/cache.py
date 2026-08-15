import hashlib
import json
from pathlib import Path


REPORT_FILE = Path("careerpilot_report.json")


def create_input_hash(resume_text, job_description):
    """Create a stable identifier for the current résumé and job description."""
    combined_input = resume_text + "\n" + job_description
    return hashlib.sha256(combined_input.encode("utf-8")).hexdigest()


def load_cached_report(input_hash):
    """Return a saved report when the inputs have not changed."""
    if not REPORT_FILE.exists():
        return None

    try:
        saved_report = json.loads(REPORT_FILE.read_text(encoding="utf-8"))
        if saved_report.get("input_hash") == input_hash:
            return saved_report
    except (json.JSONDecodeError, OSError):
        return None

    return None


def save_report(report):
    """Save the completed CareerPilot report for reuse."""
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
