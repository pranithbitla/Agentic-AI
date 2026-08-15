from careerpilot.skill_matcher import calculate_job_match, resume_has_skill


def test_skill_aliases_are_detected():
    resume = "Built agentic AI projects using GitHub and AWS."
    assert resume_has_skill(resume, "AI agents")
    assert resume_has_skill(resume, "Git")
    assert resume_has_skill(resume, "cloud deployment")


def test_unrelated_skill_does_not_match():
    assert not resume_has_skill("Java developer", "Python")


def test_required_skills_have_higher_weight():
    job = {
        "role_title": "AI Intern",
        "company_name": "Example",
        "required_skills": ["Python", "communication"],
        "preferred_skills": ["RAG", "LangChain"],
    }
    result = calculate_job_match("Python developer with strong communication.", job)
    assert result["required_skill_score"] == 100
    assert result["preferred_skill_score"] == 0
    assert result["match_score"] == 70
