from types import SimpleNamespace

from careerpilot import graph


def test_convert_usage_to_dict():
    usage = SimpleNamespace(total_input_tokens=10, total_output_tokens=5, total_tokens=15)
    assert graph.convert_usage_to_dict(usage) == {
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
    }


def test_read_inputs_node_reads_and_hashes_inputs(tmp_path):
    resume_path = tmp_path / "resume.txt"
    job_path = tmp_path / "job.txt"
    resume_path.write_text("Python and Git", encoding="utf-8")
    job_path.write_text(
        "AI Intern role requiring Python, Git, testing, communication, and documentation. "
        "Fresh graduates with practical projects may apply.",
        encoding="utf-8",
    )

    result = graph.read_inputs_node(
        {"resume_path": str(resume_path), "job_path": str(job_path)}
    )

    assert result["resume_text"] == "Python and Git"
    assert result["job_description"].startswith("AI Intern")
    assert len(result["input_hash"]) == 64


def test_cache_nodes_and_routing(monkeypatch):
    report = {"match_result": {"match_score": 80}}
    monkeypatch.setattr(graph, "load_cached_report", lambda input_hash: report)

    assert graph.check_cache_node({"input_hash": "abc"}) == {"cached_report": report}
    assert graph.choose_cache_route({"cached_report": report}) == "use_cache"
    assert graph.choose_cache_route({"cached_report": None}) == "analyze_job"
    assert graph.use_cache_node({"cached_report": report}) == {
        "final_report": report,
        "used_cache": True,
    }


def test_analysis_matching_and_recommendation_nodes(monkeypatch):
    usage = SimpleNamespace(total_input_tokens=10, total_output_tokens=5, total_tokens=15)
    job_model = SimpleNamespace(model_dump=lambda: {"required_skills": ["Python"]})
    recommendation_model = SimpleNamespace(model_dump=lambda: {"next_action": "Apply"})

    monkeypatch.setattr(graph, "analyze_job_description", lambda description: (job_model, usage))
    monkeypatch.setattr(
        graph,
        "calculate_job_match",
        lambda resume, job: {"match_score": 100, "matched_required_skills": ["Python"]},
    )
    monkeypatch.setattr(
        graph,
        "generate_recommendations",
        lambda resume, job, match: (recommendation_model, usage),
    )

    analyzed = graph.analyze_job_node({"job_description": "Python role"})
    matched = graph.match_resume_node(
        {"resume_text": "Python", "job_analysis": analyzed["job_analysis"]}
    )
    recommended = graph.recommendation_node(
        {
            "resume_text": "Python",
            "job_analysis": analyzed["job_analysis"],
            "match_result": matched["match_result"],
        }
    )

    assert analyzed["job_usage"]["total_tokens"] == 15
    assert matched["match_result"]["match_score"] == 100
    assert recommended["recommendations"]["next_action"] == "Apply"


def test_build_report_sums_usage_and_saves(monkeypatch):
    saved_reports = []
    monkeypatch.setattr(graph, "save_report", saved_reports.append)
    state = {
        "input_hash": "abc",
        "job_analysis": {"role_title": "AI Intern"},
        "match_result": {"match_score": 70},
        "recommendations": {"next_action": "Practice"},
        "job_usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
        "recommendation_usage": {
            "input_tokens": 20,
            "output_tokens": 10,
            "total_tokens": 30,
        },
    }

    result = graph.build_report_node(state)

    assert result["final_report"]["token_usage"] == {
        "input_tokens": 30,
        "output_tokens": 15,
        "total_tokens": 45,
    }
    assert saved_reports == [result["final_report"]]
    assert result["used_cache"] is False


def test_graph_factory_compiles_workflow():
    assert graph.create_careerpilot_graph() is not None
