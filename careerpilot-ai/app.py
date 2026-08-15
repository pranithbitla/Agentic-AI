import json
import tempfile
from pathlib import Path

import streamlit as st

from careerpilot.graph import careerpilot_agent

st.set_page_config(page_title="CareerPilot AI", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px;}
.stButton > button {width: 100%; border-radius: 10px; height: 3rem; font-weight: 600;}
[data-testid="stMetric"] {padding: 18px; border: 1px solid rgba(128,128,128,0.2); border-radius: 12px;}
button[data-baseweb="tab"] {font-size: 16px; font-weight: 600;}
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
    st.markdown("**AI-powered résumé and job-match analyzer**")
    st.markdown("- 📄 Résumé analysis\n- 🎯 Job match score\n- ⚠️ Skill gaps\n- 🗺 Learning roadmap\n- 🎤 Interview preparation")
    st.divider()
    st.caption("Python • LangGraph • Gemini • Streamlit")

st.title("🚀 CareerPilot AI")
st.markdown("### AI-Powered Résumé & Job Match Analyzer")
st.write("Upload your résumé and paste a job description to discover your match score, missing skills, learning roadmap, and interview preparation.")
st.divider()

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("1. Upload résumé")
    uploaded_resume = st.file_uploader("Upload a PDF résumé", type=["pdf"], help="Only text-based PDF résumés are supported.")
with right_column:
    st.subheader("2. Paste job description")
    job_description = st.text_area("Job description", height=250, placeholder="Paste the complete job description here...")

inputs_ready = uploaded_resume is not None and bool(job_description.strip())

if st.button("✨ Analyze Resume", type="primary", disabled=not inputs_ready, width="stretch"):
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
    with score_column:
        st.metric("Overall Match", f"{match['match_score']}%")
    with required_column:
        st.metric("Required Skills", f"{match['required_skill_score']}%")
    with preferred_column:
        st.metric("Preferred Skills", f"{match['preferred_skill_score']}%")
    st.progress(match["match_score"] / 100)

    match_tab, improve_tab, roadmap_tab, interview_tab = st.tabs([
        "🎯 Match", "📈 Improvements", "🗺 Learning Roadmap", "🎤 Interview Prep"
    ])

    with match_tab:
        st.subheader("Match Summary")
        st.write(recommendations["match_summary"])
        matched_column, missing_column = st.columns(2)
        with matched_column:
            st.subheader("✅ Matched Skills")
            display_list(match["matched_required_skills"] + match["matched_preferred_skills"], "No matching skills were detected.")
        with missing_column:
            st.subheader("⚠️ Missing Skills")
            display_list(match["missing_required_skills"] + match["missing_preferred_skills"], "No missing skills were detected.")

    with improve_tab:
        strengths_column, gaps_column = st.columns(2)
        with strengths_column:
            st.subheader("Top Strengths")
            display_list(recommendations["top_strengths"], "No strengths were generated.")
        with gaps_column:
            st.subheader("Priority Skill Gaps")
            display_list(recommendations["priority_skill_gaps"], "No priority gaps were generated.")
        st.subheader("Résumé Improvements")
        display_list(recommendations["resume_improvements"], "No résumé improvements were generated.")

    with roadmap_tab:
        st.subheader("Your Learning Roadmap")
        for number, learning_step in enumerate(recommendations["learning_plan"], start=1):
            st.markdown(f"**{number}.** {learning_step}")
        st.subheader("Recommended Next Action")
        st.success(recommendations["next_action"])

    with interview_tab:
        st.subheader("Interview Preparation")
        for number, question in enumerate(recommendations["interview_questions"], start=1):
            st.markdown(f"**Q{number}.** {question}")

    with st.expander("⚙️ Technical Details"):
        st.json(job)
        if not st.session_state.used_cache:
            st.write(f"Tokens used: {report['token_usage']['total_tokens']}")

    st.download_button(
        label="📥 Download Complete Report",
        data=json.dumps(report, indent=2),
        file_name="careerpilot_report.json",
        mime="application/json",
        width="stretch",
    )
