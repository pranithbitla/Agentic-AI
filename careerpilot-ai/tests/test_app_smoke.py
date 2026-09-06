from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).parents[1] / "app.py"


def test_app_starts_without_api_key():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=15)
    assert not app.exception
    assert app.title[0].value == "CareerPilot AI"


def test_example_report_renders_without_api_call():
    app = AppTest.from_file(str(APP_PATH)).run(timeout=15)
    app.sidebar.button[0].click().run(timeout=15)

    assert not app.exception
    assert any(header.value == "Career Match Report" for header in app.header)
    assert any(info.value.startswith("Example report") for info in app.info)
