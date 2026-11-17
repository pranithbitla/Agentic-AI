import json
import re
from typing import TypedDict, Any
from google import genai
from langgraph.graph import StateGraph, START, END

class CareerState(TypedDict, total=False):
    resume_text: str
    job_description: str
    api_key: str
    job_analysis: dict
    match: dict
    recommendations: dict

def ask_gemini(api_key: str, prompt: str) -> dict:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    raw = response.text or "{}"
    # Remove markdown fences if the model adds them.
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.I)
    return json.loads(raw)

def analyze_job(state: CareerState):
    prompt = f"""
Extract job requirements from the job description. Return ONLY JSON with keys:
role_title, company, required_skills (array), preferred_skills (array),
responsibilities (array), fresher_eligible (boolean or null).
Do not invent details.
JOB DESCRIPTION:
{state['job_description']}
"""
    return {"job_analysis": ask_gemini(state["api_key"], prompt)}

def match_resume(state: CareerState):
    job = state["job_analysis"]
    required = [str(x).lower() for x in job.get("required_skills", [])]
    preferred = [str(x).lower() for x in job.get("preferred_skills", [])]
    resume = state["resume_text"].lower()
    matched_req = [s for s in required if s in resume]
    missing_req = [s for s in required if s not in resume]
    matched_pref = [s for s in preferred if s in resume]
    req_score = 100 * len(matched_req) / len(required) if required else 100
    pref_score = 100 * len(matched_pref) / len(preferred) if preferred else 100
    overall = 0.7 * req_score + 0.3 * pref_score
    return {"match": {
        "overall_score": round(overall, 1),
        "required_score": round(req_score, 1),
        "preferred_score": round(pref_score, 1),
        "matched_required": matched_req,
        "missing_required": missing_req,
        "matched_preferred": matched_pref
    }}

def recommend(state: CareerState):
    prompt = f"""
Act as a practical career coach. Use only evidence in the resume and job details.
Never invent experience, projects, certificates, or skills. Identify gaps honestly.
Return ONLY JSON with keys: strengths (array), priority_gaps (array),
resume_improvements (array), 7_day_learning_plan (array), interview_questions (array).
RESUME:
{state['resume_text'][:7000]}
JOB:
{json.dumps(state['job_analysis'])}
MATCH:
{json.dumps(state['match'])}
"""
    return {"recommendations": ask_gemini(state["api_key"], prompt)}

def build_graph():
    graph = StateGraph(CareerState)
    graph.add_node("analyze_job", analyze_job)
    graph.add_node("match_resume", match_resume)
    graph.add_node("recommend", recommend)
    graph.add_edge(START, "analyze_job")
    graph.add_edge("analyze_job", "match_resume")
    graph.add_edge("match_resume", "recommend")
    graph.add_edge("recommend", END)
    return graph.compile()

def run_careerpilot(resume_text: str, job_description: str, api_key: str):
    result = build_graph().invoke({
        "resume_text": resume_text,
        "job_description": job_description,
        "api_key": api_key
    })
    return {
        "job_analysis": result["job_analysis"],
        "match": result["match"],
        "recommendations": result["recommendations"]
    }
