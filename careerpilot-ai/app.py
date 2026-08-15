import json
import tempfile
from pathlib import Path

import streamlit as st

from careerpilot.graph import careerpilot_agent


st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem;}
[data-testid="stMetric"] {padding: 16px; border: 1px solid rgba(128,128,128,.2); border-radius: 12px;}
.stButton > button {width: 100%; border-radius: 10px; height: 3rem; font-weight: 600;}
</style>
""", unsafe_allow_html=True)


def display_list(items, empty_message):
    if not items:
        st.info(empty_message)
        return
    for item in items:
        st.markdown(f"- {item}")


if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "used_cache" not in st.session_state:
    st.session_state.used_cache = False

with st.sidebar:
    st.title("🚀 CareerPilot AI")
    st.write("Agentic résumé and job-match analyzer")
    st.markdown("**Stack:** Python · LangGraph · Gemini · Streamlit")
    st.caption("Your uploaded résumé is processed through temporary files and removed after analysis.")

st.title("CareerPilot AI")
st.subheader("AI-Powered Resume & Job Match Analyzer")
st.write("Compare your résumé with a job description, understand your match, identify skill gaps, and get a practical learning roadmap.")
st.divider()

left_column, right_column = st.columns(2)
with left_column:
    uploaded_resume = st.file_uploader("1. Upload résumé", type=["pdf"], help="Text-based PDF résumés are supported.")
with right_column:
    job_description = st.text_area("2. Paste job description", height=250, placeholder="Paste the complete job description here...")

inputs_ready = uploaded_resume is not None and bool(job_description.strip())

if st.button("✨ Analyse My Résumé", type="primary", disabled=not inputs_ready, width="stretch"):
    temporary_resume_path = None
    temporary_job_path = None
    try:
        with st.spinner("CareerPilot agents are analysing your profile..."):
            with tempfile.NamedTemporaryFile(mode="wb", suffix=".pdf", delete=False) as resume_file:
                resume_file.write(uploaded_resume.getvalue())
                temporary_resume_path = resume_file.name

            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", encoding="utf-8", delete=False) as job_file:
                job_file.write(job_description)
                temporary_job_path = job_file.name

            result = careerpilot_agent.invoke({"resume_path": temporary_resume_path, "job_path": temporary_job_path})
            st.session_state.final_report = result["final_report"]
            st.session_state.used_cache = result.get("used_cache", False)
        st.success("Analysis completed successfully!")
    except Exception as error:
        st.error(f"Analysis failed: {error}")
    finally:
        for temporary_path in [temporary_resume_path, temporary_job_path]:
            if temporary_path:
                Path(temporary_path).unlink(missing_ok=True)

report = st.session_state.final_report
if report:
    st.divider()
    job = report["job_analysis"]
    match = report["match_result"]
    recommendations = report["recommendations"]
    st.header("Career Match Report")
    st.subheader(f"{job['role_title']} at {job.get('company_name') or 'Unknown Company'}")

    if st.session_state.used_cache:
        st.info("This report was loaded from cache. No new Gemini tokens were used.")

    score_column, required_column, preferred_column = st.columns(3)
    score_column.metric("Overall Match", f"{match['match_score']}%")
    required_column.metric("Required Skills", f"{match['required_skill_score']}%")
    preferred_column.metric("Preferred Skills", f"{match['preferred_skill_score']}%")
    st.progress(match["match_score"] / 100)

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Match", "📈 Improvements", "🗺 Learning Roadmap", "🎤 Interview Prep"])

    with tab1:
        st.subheader("Match Summary")
        st.write(recommendations["match_summary"])
        matched_column, missing_column = st.columns(2)
        with matched_column:
            st.subheader("✅ Matched Skills")
            display_list(match["matched_required_skills"] + match["matched_preferred_skills"], "No matching skills were detected.")
        with missing_column:
            st.subheader("⚠️ Missing Skills")
            display_list(match["missing_required_skills"] + match["missing_preferred_skills"], "No missing skills were detected.")

    with tab2:
        strengths_column, gaps_column = st.columns(2)
        with strengths_column:
            st.subheader("Top Strengths")
            display_list(recommendations["top_strengths"], "No strengths were generated.")
        with gaps_column:
            st.subheader("Priority Skill Gaps")
            display_list(recommendations["priority_skill_gaps"], "No priority gaps were generated.")
        st.subheader("Résumé Improvements")
        display_list(recommendations["resume_improvements"], "No résumé improvements were generated.")

    with tab3:
        for number, learning_step in enumerate(recommendations["learning_plan"], start=1):
            st.markdown(f"**{number}.** {learning_step}")
        st.success(recommendations["next_action"])

    with tab4:
        for number, question in enumerate(recommendations["interview_questions"], start=1):
            st.markdown(f"**Q{number}.** {question}")

    with st.expander("⚙️ Technical details"):
        new_tokens = 0 if st.session_state.used_cache else report["token_usage"]["total_tokens"]
        st.write(f"New tokens used: {new_tokens}")
        st.json(job)

    report_json = json.dumps(report, indent=2)
    st.download_button("📥 Download Complete Report", data=report_json, file_name="careerpilot_report.json", mime="application/json", width="stretch")
