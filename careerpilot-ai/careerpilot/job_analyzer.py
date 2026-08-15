from typing import Optional

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()


class JobAnalysis(BaseModel):
    role_title: str = Field(description="The job title mentioned in the description.")
    company_name: Optional[str] = Field(description="The company name, or null when it is not mentioned.")
    required_skills: list[str] = Field(description="Skills that the candidate must have.")
    preferred_skills: list[str] = Field(description="Skills that are useful but not compulsory.")
    experience_required: str = Field(description="Required experience or fresher eligibility.")
    education_required: list[str] = Field(description="Accepted degrees or education requirements.")
    responsibilities: list[str] = Field(description="The main responsibilities of the role.")
    ats_keywords: list[str] = Field(description="Important technical keywords suitable for résumé matching.")


def analyze_job_description(job_description):
    """Use Gemini to extract structured information from a job description."""
    if not job_description.strip():
        raise ValueError("The job description cannot be empty.")

    client = genai.Client()
    prompt = f"""
Extract factual hiring information from the job description below.

Rules:
1. Do not invent skills or requirements.
2. Separate required and preferred skills.
3. Mention whether freshers can apply.
4. Keep every list short and relevant.

JOB DESCRIPTION:
{job_description}
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": JobAnalysis.model_json_schema(),
        },
        store=False,
    )

    analysis = JobAnalysis.model_validate_json(interaction.output_text)
    return analysis, interaction.usage
