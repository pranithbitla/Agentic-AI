import json

from careerpilot.cache import create_input_hash, load_cached_report, save_report


def test_cache_is_disabled_by_default(monkeypatch, tmp_path):
    report_path = tmp_path / "report.json"
    monkeypatch.delenv("CAREERPILOT_ENABLE_DISK_CACHE", raising=False)
    monkeypatch.setenv("CAREERPILOT_CACHE_PATH", str(report_path))

    assert save_report({"input_hash": "abc"}) is False
    assert not report_path.exists()
    assert load_cached_report("abc") is None


def test_opt_in_cache_round_trip(monkeypatch, tmp_path):
    report_path = tmp_path / "nested" / "report.json"
    monkeypatch.setenv("CAREERPILOT_ENABLE_DISK_CACHE", "true")
    monkeypatch.setenv("CAREERPILOT_CACHE_PATH", str(report_path))
    report = {"input_hash": "abc", "match_result": {"match_score": 75}}

    assert save_report(report) is True
    assert json.loads(report_path.read_text(encoding="utf-8")) == report
    assert load_cached_report("abc") == report
    assert load_cached_report("different") is None


def test_corrupt_cache_is_ignored(monkeypatch, tmp_path):
    report_path = tmp_path / "report.json"
    report_path.write_text("not-json", encoding="utf-8")
    monkeypatch.setenv("CAREERPILOT_ENABLE_DISK_CACHE", "yes")
    monkeypatch.setenv("CAREERPILOT_CACHE_PATH", str(report_path))
    assert load_cached_report("abc") is None


def test_input_hash_is_deterministic_and_input_sensitive():
    assert create_input_hash("resume", "job") == create_input_hash("resume", "job")
    assert create_input_hash("resume", "job") != create_input_hash("other", "job")
