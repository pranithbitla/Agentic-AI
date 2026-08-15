import re

SKILL_ALIASES = {
    "python": ["python"],
    "problem solving": ["problem solving", "analytical thinking"],
    "communication": ["communication", "written communication", "verbal communication"],
    "basic ai ml knowledge": ["ai ml", "machine learning", "artificial intelligence", "ai engineering"],
    "generative ai": ["generative ai", "genai"],
    "ai agents": ["ai agents", "agentic ai", "intelligent agents"],
    "llms": ["llm", "llms", "large language model", "large language models"],
    "rag": ["rag", "retrieval augmented generation"],
    "langchain": ["langchain"],
    "git": ["git", "github"],
    "cloud deployment": ["cloud deployment", "aws", "azure", "gcp", "google cloud"],
}


def normalize_text(text):
    """Convert text into a consistent format for comparison."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def contains_phrase(text, phrase):
    """Check whether a complete word or phrase exists in the text."""
    normalized_phrase = normalize_text(phrase)
    pattern = r"\b" + re.escape(normalized_phrase).replace(r"\ ", r"\s+") + r"\b"
    return re.search(pattern, text) is not None


def resume_has_skill(resume_text, skill):
    """Check a skill and all its possible aliases."""
    normalized_resume = normalize_text(resume_text)
    normalized_skill = normalize_text(skill)
    possible_names = SKILL_ALIASES.get(normalized_skill, [normalized_skill])
    return any(contains_phrase(normalized_resume, name) for name in possible_names)


def separate_skills(resume_text, job_skills):
    matched = []
    missing = []
    for skill in job_skills:
        if resume_has_skill(resume_text, skill):
            matched.append(skill)
        else:
            missing.append(skill)
    return matched, missing


def calculate_percentage(matched_skills, total_skills):
    if len(total_skills) == 0:
        return 100
    return round(len(matched_skills) / len(total_skills) * 100)


def calculate_job_match(resume_text, job_data):
    required_skills = job_data.get("required_skills", [])
    preferred_skills = job_data.get("preferred_skills", [])

    matched_required, missing_required = separate_skills(resume_text, required_skills)
    matched_preferred, missing_preferred = separate_skills(resume_text, preferred_skills)

    required_score = calculate_percentage(matched_required, required_skills)
    preferred_score = calculate_percentage(matched_preferred, preferred_skills)
    overall_score = round(required_score * 0.70 + preferred_score * 0.30)

    return {
        "role_title": job_data.get("role_title", "Unknown role"),
        "company_name": job_data.get("company_name", "Unknown company"),
        "match_score": overall_score,
        "required_skill_score": required_score,
        "preferred_skill_score": preferred_score,
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
    }
