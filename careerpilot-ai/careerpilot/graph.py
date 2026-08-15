from pathlib import Path
from typing import Literal

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from careerpilot.cache import create_input_hash, load_cached_report, save_report
from careerpilot.job_analyzer import analyze_job_description
from careerpilot.recommendation_agent import generate_recommendations
from careerpilot.resume_reader import extract_resume_text
from careerpilot.skill_matcher import calculate_job_match


class CareerPilotState(TypedDict, total=False):
    resume_path: str
    job_path: str
    resume_text: str
    job_description: str
    input_hash: str
    cached_report: dict | None
    used_cache: bool
    job_analysis: dict
    job_usage: dict
    match_result: dict
    recommendations: dict
    recommendation_usage: dict
    final_report: dict


def convert_usage_to_dict(usage):
    return {
        "input_tokens": usage.total_input_tokens,
        "output_tokens": usage.total_output_tokens,
        "total_tokens": usage.total_tokens,
    }


def read_inputs_node(state: CareerPilotState):
    resume_text = extract_resume_text(state["resume_path"])
    job_description = Path(state["job_path"]).read_text(encoding="utf-8")
    if not job_description.strip():
        raise ValueError("The job description is empty.")
    input_hash = create_input_hash(resume_text, job_description)
    return {"resume_text": resume_text, "job_description": job_description, "input_hash": input_hash}


def check_cache_node(state: CareerPilotState):
    return {"cached_report": load_cached_report(state["input_hash"])}


def choose_cache_route(state: CareerPilotState) -> Literal["use_cache", "analyze_job"]:
    return "use_cache" if state.get("cached_report") else "analyze_job"


def use_cache_node(state: CareerPilotState):
    return {"final_report": state["cached_report"], "used_cache": True}


def analyze_job_node(state: CareerPilotState):
    job_analysis, usage = analyze_job_description(state["job_description"])
    return {"job_analysis": job_analysis.model_dump(), "job_usage": convert_usage_to_dict(usage)}


def match_resume_node(state: CareerPilotState):
    return {"match_result": calculate_job_match(state["resume_text"], state["job_analysis"])}


def recommendation_node(state: CareerPilotState):
    recommendations, usage = generate_recommendations(
        state["resume_text"], state["job_analysis"], state["match_result"]
    )
    return {
        "recommendations": recommendations.model_dump(),
        "recommendation_usage": convert_usage_to_dict(usage),
    }


def build_report_node(state: CareerPilotState):
    job_usage = state["job_usage"]
    recommendation_usage = state["recommendation_usage"]
    total_usage = {
        "input_tokens": job_usage["input_tokens"] + recommendation_usage["input_tokens"],
        "output_tokens": job_usage["output_tokens"] + recommendation_usage["output_tokens"],
        "total_tokens": job_usage["total_tokens"] + recommendation_usage["total_tokens"],
    }
    report = {
        "input_hash": state["input_hash"],
        "job_analysis": state["job_analysis"],
        "match_result": state["match_result"],
        "recommendations": state["recommendations"],
        "token_usage": total_usage,
    }
    save_report(report)
    return {"final_report": report, "used_cache": False}


def create_careerpilot_graph():
    builder = StateGraph(CareerPilotState)
    builder.add_node("read_inputs", read_inputs_node)
    builder.add_node("check_cache", check_cache_node)
    builder.add_node("use_cache", use_cache_node)
    builder.add_node("analyze_job", analyze_job_node)
    builder.add_node("match_resume", match_resume_node)
    builder.add_node("generate_recommendations", recommendation_node)
    builder.add_node("build_report", build_report_node)

    builder.add_edge(START, "read_inputs")
    builder.add_edge("read_inputs", "check_cache")
    builder.add_conditional_edges(
        "check_cache",
        choose_cache_route,
        {"use_cache": "use_cache", "analyze_job": "analyze_job"},
    )
    builder.add_edge("use_cache", END)
    builder.add_edge("analyze_job", "match_resume")
    builder.add_edge("match_resume", "generate_recommendations")
    builder.add_edge("generate_recommendations", "build_report")
    builder.add_edge("build_report", END)
    return builder.compile()


careerpilot_agent = create_careerpilot_graph()
