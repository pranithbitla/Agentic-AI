import re
from collections.abc import Iterable

SKILL_ALIASES = {
    "ai agents": ("ai agents", "agentic ai", "intelligent agents"),
    "cloud deployment": ("cloud deployment", "aws", "azure", "gcp", "google cloud"),
    "communication": ("communication", "written communication", "verbal communication"),
    "data analysis": ("data analysis", "data analytics"),
    "docker": ("docker", "containerization", "containers"),
    "fastapi": ("fastapi",),
    "generative ai": ("generative ai", "genai"),
    "git": ("git", "github", "version control"),
    "langchain": ("langchain",),
    "langgraph": ("langgraph",),
    "llms": ("llm", "llms", "large language model", "large language models"),
    "machine learning": ("machine learning", "artificial intelligence", "ai ml", "ai/ml"),
    "pandas": ("pandas",),
    "problem solving": ("problem solving", "analytical thinking"),
    "python": ("python", "python programming"),
    "rag": ("rag", "retrieval augmented generation", "retrieval-augmented generation"),
    "rest apis": ("rest api", "rest apis", "restful api", "restful apis"),
    "sql": ("sql", "mysql", "postgresql", "sqlite"),
    "streamlit": ("streamlit",),
    "vector databases": ("vector database", "vector databases", "vector db", "vector store"),
}


def normalize_text(text: str) -> str:
    """Convert text into a consistent format for phrase comparison."""
    lowered = text.casefold()
    normalized = re.sub(r"[^a-z0-9+#]+", " ", lowered)
    return " ".join(normalized.split())


def contains_phrase(normalized_text: str, phrase: str) -> bool:
    """Check whether a complete word or phrase exists in normalized text."""
    normalized_phrase = normalize_text(phrase)
    pattern = r"(?<![a-z0-9])" + re.escape(normalized_phrase).replace(r"\ ", r"\s+")
    pattern += r"(?![a-z0-9])"
    return re.search(pattern, normalized_text) is not None


def canonicalize_skill(skill: str) -> str:
    """Map either a canonical skill or one of its aliases to a stable name."""
    normalized_skill = normalize_text(skill)
    for canonical_name, aliases in SKILL_ALIASES.items():
        normalized_aliases = {normalize_text(alias) for alias in aliases}
        if normalized_skill == canonical_name or normalized_skill in normalized_aliases:
            return canonical_name
    return normalized_skill


def aliases_for_skill(skill: str) -> tuple[str, ...]:
    canonical_name = canonicalize_skill(skill)
    return SKILL_ALIASES.get(canonical_name, (canonical_name,))


def resume_has_skill(resume_text: str, skill: str) -> bool:
    """Check a skill and all of its recognized aliases."""
    normalized_resume = normalize_text(resume_text)
    return any(contains_phrase(normalized_resume, alias) for alias in aliases_for_skill(skill))


def deduplicate_skills(skills: Iterable[str]) -> list[str]:
    """Remove empty and equivalent skills while preserving display order."""
    result = []
    seen = set()
    for skill in skills:
        cleaned_skill = skill.strip()
        canonical_name = canonicalize_skill(cleaned_skill)
        if cleaned_skill and canonical_name not in seen:
            result.append(cleaned_skill)
            seen.add(canonical_name)
    return result


def separate_skills(resume_text: str, job_skills: Iterable[str]) -> tuple[list[str], list[str]]:
    matched = []
    missing = []
    for skill in deduplicate_skills(job_skills):
        destination = matched if resume_has_skill(resume_text, skill) else missing
        destination.append(skill)
    return matched, missing


def calculate_percentage(matched_skills: list[str], total_skills: list[str]) -> int:
    if not total_skills:
        return 0
    return round(len(matched_skills) / len(total_skills) * 100)


def calculate_overall_score(
    required_score: int,
    preferred_score: int,
    required_skills: list[str],
    preferred_skills: list[str],
) -> int:
    """Apply 70/30 weighting only when both skill groups exist."""
    if required_skills and preferred_skills:
        return round(required_score * 0.70 + preferred_score * 0.30)
    if required_skills:
        return required_score
    if preferred_skills:
        return preferred_score
    return 0


def calculate_job_match(resume_text: str, job_data: dict) -> dict:
    required_skills = deduplicate_skills(job_data.get("required_skills", []))
    preferred_skills = deduplicate_skills(job_data.get("preferred_skills", []))
    ats_keywords = deduplicate_skills(job_data.get("ats_keywords", []))

    matched_required, missing_required = separate_skills(resume_text, required_skills)
    matched_preferred, missing_preferred = separate_skills(resume_text, preferred_skills)
    matched_keywords, missing_keywords = separate_skills(resume_text, ats_keywords)

    required_score = calculate_percentage(matched_required, required_skills)
    preferred_score = calculate_percentage(matched_preferred, preferred_skills)
    overall_score = calculate_overall_score(
        required_score, preferred_score, required_skills, preferred_skills
    )

    return {
        "role_title": job_data.get("role_title", "Unknown role"),
        "company_name": job_data.get("company_name") or "Unknown company",
        "match_score": overall_score,
        "required_skill_score": required_score,
        "preferred_skill_score": preferred_score,
        "ats_keyword_score": calculate_percentage(matched_keywords, ats_keywords),
        "required_skill_count": len(required_skills),
        "preferred_skill_count": len(preferred_skills),
        "ats_keyword_count": len(ats_keywords),
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "matched_preferred_skills": matched_preferred,
        "missing_preferred_skills": missing_preferred,
        "matched_ats_keywords": matched_keywords,
        "missing_ats_keywords": missing_keywords,
    }
