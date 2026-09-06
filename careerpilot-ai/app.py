import json
import logging
import tempfile
from pathlib import Path

import streamlit as st

from careerpilot.config import ConfigurationError, InputValidationError
from careerpilot.graph import careerpilot_agent

APP_ROOT = Path(__file__).parent
EXAMPLE_REPORT_PATH = APP_ROOT / "examples" / "sample_report.json"
LOGGER = logging.getLogger(__name__)

st.set_page_config(
    page_title="CareerPilot AI — Explainable Job Matching",
    page_icon="🚀",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px;}
    .stButton > button {width: 100%; border-radius: 10px; height: 3rem; font-weight: 600;}
    [data-testid="stMetric"] {
        padding: 18px;
        border: 1px solid rgba(128,128,128,.2);
        border-radius: 12px;
    }
    button[data-baseweb="tab"] {font-size: 16px; font-weight: 600;}
    .trust-note {
        padding: .8rem 1rem;
        border-left: 4px solid #4f46e5;
        background: rgba(79,70,229,.08);
        border-radius: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def display_list(items, empty_message):
    if not items:
        st.info(empty_message)
        return
    for item in items:
        st.markdown(f"- {item}")


def score_label(score, item_count):
    return f"{score}%" if item_count else "Not listed"


def load_example_report():
    return json.loads(EXAMPLE_REPORT_PATH.read_text(encoding="utf-8"))


def render_report(report, used_cache=False, report_mode="analysis"):
    job = report["job_analysis"]
    match = report["match_result"]
    recommendations = report["recommendations"]

    st.divider()
    st.header("Career Match Report")
    st.subheader(f"{job['role_title']} at {job.get('company_name') or 'Unknown Company'}")

    if report_mode == "example":
        st.info("Example report — uses fictional data and makes no API call.")
    elif used_cache:
        st.info("Loaded from the optional local cache. No new Gemini tokens were used.")

    score_column, required_column, preferred_column, keyword_column = st.columns(4)
    score_column.metric("Skill Match", f"{match['match_score']}%")
    required_column.metric(
        "Required Skills",
        score_label(match["required_skill_score"], match.get("required_skill_count", 0)),
    )
    preferred_column.metric(
        "Preferred Skills",
        score_label(match["preferred_skill_score"], match.get("preferred_skill_count", 0)),
    )
    keyword_column.metric(
        "Keyword Coverage",
        score_label(match.get("ats_keyword_score", 0), match.get("ats_keyword_count", 0)),
    )
    st.progress(match["match_score"] / 100)
    st.caption(
        "This score is deterministic skill coverage, not a hiring probability or guarantee. "
        "Required skills carry 70% weight when both skill groups are present."
    )

    match_tab, improve_tab, roadmap_tab, interview_tab, job_tab = st.tabs(
        ["🎯 Match", "📈 Improvements", "🗺 Roadmap", "🎤 Interview", "💼 Job Details"]
    )

    with match_tab:
        st.subheader("Match Summary")
        st.write(recommendations["match_summary"])
        matched_column, missing_column = st.columns(2)
        with matched_column:
            st.subheader("✅ Matched Skills")
            display_list(
                match["matched_required_skills"] + match["matched_preferred_skills"],
                "No matching skills were detected.",
            )
        with missing_column:
            st.subheader("⚠️ Missing Skills")
            display_list(
                match["missing_required_skills"] + match["missing_preferred_skills"],
                "No missing skills were detected.",
            )

        with st.expander("ATS keyword evidence"):
            keyword_match_column, keyword_gap_column = st.columns(2)
            with keyword_match_column:
                st.markdown("**Present in résumé**")
                display_list(match.get("matched_ats_keywords", []), "No keywords matched.")
            with keyword_gap_column:
                st.markdown("**Not detected**")
                display_list(match.get("missing_ats_keywords", []), "No keyword gaps detected.")

    with improve_tab:
        strengths_column, gaps_column = st.columns(2)
        with strengths_column:
            st.subheader("Top Strengths")
            display_list(recommendations["top_strengths"], "No strengths were generated.")
        with gaps_column:
            st.subheader("Priority Skill Gaps")
            display_list(recommendations["priority_skill_gaps"], "No priority gaps were generated.")
        st.subheader("Résumé Improvements")
        display_list(recommendations["resume_improvements"], "No improvements were generated.")

    with roadmap_tab:
        st.subheader("Practical Learning Roadmap")
        for number, learning_step in enumerate(recommendations["learning_plan"], start=1):
            st.markdown(f"**{number}.** {learning_step}")
        st.subheader("Recommended Next Action")
        st.success(recommendations["next_action"])

    with interview_tab:
        st.subheader("Role-Specific Interview Questions")
        for number, question in enumerate(recommendations["interview_questions"], start=1):
            st.markdown(f"**Q{number}.** {question}")

    with job_tab:
        st.markdown(f"**Experience:** {job['experience_required']}")
        st.markdown("**Education**")
        display_list(job["education_required"], "No education requirement was listed.")
        st.markdown("**Responsibilities**")
        display_list(job["responsibilities"], "No responsibilities were extracted.")
        with st.expander("Structured analysis"):
            st.json(job)
            if report_mode == "analysis" and not used_cache:
                st.write(f"Tokens used: {report['token_usage']['total_tokens']}")

    st.download_button(
        label="📥 Download JSON Report",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name="careerpilot_report.json",
        mime="application/json",
        width="stretch",
    )


for key, default_value in {
    "final_report": None,
    "used_cache": False,
    "report_mode": "analysis",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

with st.sidebar:
    st.title("🚀 CareerPilot AI")
    st.markdown("**Explainable résumé-to-job matching**")
    st.markdown(
        "- Structured job extraction\n"
        "- Deterministic skill scoring\n"
        "- Grounded AI recommendations\n"
        "- Actionable learning roadmap"
    )
    st.divider()
    if st.button("Preview Example Report"):
        st.session_state.final_report = load_example_report()
        st.session_state.used_cache = False
        st.session_state.report_mode = "example"
    st.caption("Python · LangGraph · Gemini · Pydantic · Streamlit")

st.title("CareerPilot AI")
st.markdown("### Turn a job description into an honest, actionable preparation plan")
st.write(
    "CareerPilot separates AI interpretation from deterministic scoring so every percentage "
    "can be traced to detected skills."
)
st.markdown(
    '<div class="trust-note">🔒 Uploaded files use temporary storage and are deleted after '
    "analysis. Persistent disk caching is disabled by default.</div>",
    unsafe_allow_html=True,
)

with st.expander("How the agent workflow works"):
    st.write(
        "LangGraph routes the inputs through validation, optional cache lookup, structured job "
        "analysis, deterministic skill matching, and grounded recommendation generation."
    )

st.divider()
resume_column, job_column = st.columns(2)
with resume_column:
    st.subheader("1. Add résumé")
    resume_mode = st.radio(
        "Résumé format", ["Upload PDF", "Paste text"], horizontal=True, label_visibility="collapsed"
    )
    if resume_mode == "Upload PDF":
        uploaded_resume = st.file_uploader(
            "Upload a PDF résumé",
            type=["pdf"],
            help="Text-based PDFs up to 5 MB and 10 pages are supported.",
        )
        pasted_resume = ""
    else:
        uploaded_resume = None
        pasted_resume = st.text_area(
            "Résumé text",
            height=280,
            placeholder="Paste résumé text here...",
        )

with job_column:
    st.subheader("2. Add job description")
    job_description = st.text_area(
        "Job description",
        height=280,
        placeholder="Paste the complete job description here...",
    )

resume_ready = uploaded_resume is not None or bool(pasted_resume.strip())
inputs_ready = resume_ready and bool(job_description.strip())

if st.button("✨ Analyze Match", type="primary", disabled=not inputs_ready, width="stretch"):
    temporary_resume_path = None
    temporary_job_path = None
    try:
        with st.spinner("CareerPilot agents are analyzing the match..."):
            if uploaded_resume is not None:
                with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as file:
                    file.write(uploaded_resume.getvalue())
                    temporary_resume_path = file.name
            else:
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".txt", encoding="utf-8", delete=False
                ) as file:
                    file.write(pasted_resume)
                    temporary_resume_path = file.name

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", encoding="utf-8", delete=False
            ) as file:
                file.write(job_description)
                temporary_job_path = file.name

            result = careerpilot_agent.invoke(
                {"resume_path": temporary_resume_path, "job_path": temporary_job_path}
            )
            st.session_state.final_report = result["final_report"]
            st.session_state.used_cache = result.get("used_cache", False)
            st.session_state.report_mode = "analysis"
        st.success("Analysis completed successfully.")
    except (ConfigurationError, InputValidationError, FileNotFoundError) as error:
        st.error(str(error))
    except Exception:
        LOGGER.exception("CareerPilot analysis failed")
        st.error("The analysis could not be completed. Check the API configuration and try again.")
    finally:
        for temporary_path in (temporary_resume_path, temporary_job_path):
            if temporary_path:
                Path(temporary_path).unlink(missing_ok=True)

if st.session_state.final_report:
    render_report(
        st.session_state.final_report,
        used_cache=st.session_state.used_cache,
        report_mode=st.session_state.report_mode,
    )
