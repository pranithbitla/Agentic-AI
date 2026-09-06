import pytest

from careerpilot.skill_matcher import (
    calculate_job_match,
    canonicalize_skill,
    deduplicate_skills,
    resume_has_skill,
)


@pytest.mark.parametrize(
    ("resume", "job_skill"),
    [
        ("Built agentic AI workflows.", "AI agents"),
        ("Deployed an app on AWS.", "cloud deployment"),
        ("Used PostgreSQL for persistence.", "SQL"),
        ("Created a RESTful API.", "REST APIs"),
        ("Built retrieval-augmented generation.", "RAG"),
    ],
)
def test_skill_aliases_are_detected_in_both_directions(resume, job_skill):
    assert resume_has_skill(resume, job_skill)


def test_unrelated_or_partial_words_do_not_match():
    assert not resume_has_skill("Java developer", "Python")
    assert not resume_has_skill("Worked on a campaign", "AI")


def test_aliases_are_canonicalized_and_deduplicated():
    assert canonicalize_skill("GitHub") == "git"
    assert deduplicate_skills(["Git", "GitHub", "  Python ", "python programming", ""] ) == [
        "Git",
        "Python",
    ]


def test_required_skills_have_higher_weight_when_both_groups_exist():
    job = {
        "role_title": "AI Intern",
        "company_name": "Example",
        "required_skills": ["Python", "communication"],
        "preferred_skills": ["RAG", "LangChain"],
        "ats_keywords": ["Python", "Git"],
    }
    result = calculate_job_match("Python developer with strong communication.", job)
    assert result["required_skill_score"] == 100
    assert result["preferred_skill_score"] == 0
    assert result["match_score"] == 70
    assert result["ats_keyword_score"] == 50


def test_missing_preferred_group_does_not_inflate_score():
    job = {"required_skills": ["Python", "Git"], "preferred_skills": []}
    result = calculate_job_match("Python", job)
    assert result["required_skill_score"] == 50
    assert result["match_score"] == 50


def test_no_listed_skills_returns_zero_instead_of_false_perfect_score():
    result = calculate_job_match("Python", {"required_skills": [], "preferred_skills": []})
    assert result["match_score"] == 0
    assert result["required_skill_count"] == 0
    assert result["preferred_skill_count"] == 0
