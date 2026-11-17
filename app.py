import json
import streamlit as st
from pypdf import PdfReader
from workflow import run_careerpilot

st.set_page_config(page_title="CareerPilot AI", page_icon="🎯", layout="wide")
st.title("🎯 CareerPilot AI")
st.caption("Resume intelligence and job-fit analysis powered by Gemini + LangGraph")

with st.sidebar:
    st.subheader("Setup")
    api_key = st.text_input("Gemini API key", type="password")
    st.info("Your resume is processed for this analysis. Do not upload sensitive documents to a demo app.")

resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste the job description", height=240)

if st.button("Analyze my fit", type="primary", use_container_width=True):
    if not api_key:
        st.error("Enter your Gemini API key.")
    elif not resume_file or not job_description.strip():
        st.error("Upload a PDF and paste a job description.")
    else:
        try:
            reader = PdfReader(resume_file)
            resume_text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
            if not resume_text:
                st.error("No readable text found. Use a text-based PDF rather than a scanned image.")
            else:
                with st.spinner("CareerPilot is analyzing the role and your resume..."):
                    result = run_careerpilot(resume_text, job_description, api_key)
                st.success("Analysis completed.")
                score = result["match"]["overall_score"]
                st.metric("Estimated job match", f"{score:.1f}%")
                left, right = st.columns(2)
                with left:
                    st.subheader("Skills found")
                    st.write(result["match"]["matched_required"])
                    st.subheader("Missing required skills")
                    st.write(result["match"]["missing_required"])
                with right:
                    st.subheader("Role analysis")
                    st.json(result["job_analysis"])
                st.subheader("Career coach recommendations")
                st.json(result["recommendations"])
                st.download_button("Download report (JSON)", json.dumps(result, indent=2),
                                   file_name="careerpilot_report.json", mime="application/json")
        except Exception as exc:
            st.error(f"Could not complete analysis: {exc}")
