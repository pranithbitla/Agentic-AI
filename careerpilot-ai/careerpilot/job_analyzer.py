from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

from careerpilot.config import get_api_key, get_model_name, validate_job_description
from careerpilot.prompts import build_job_analysis_prompt

load_dotenv()


class JobAnalysis(BaseModel):
    role_title: str = Field(description="The job title mentioned in the description.")
    company_name: str | None = Field(
        description="The company name, or null when it is not mentioned."
    )
    required_skills: list[str] = Field(
        description="Skills that the candidate must have.", max_length=20
    )
    preferred_skills: list[str] = Field(
        description="Skills that are useful but not compulsory.", max_length=20
    )
    experience_required: str = Field(description="Required experience or fresher eligibility.")
    education_required: list[str] = Field(
        description="Accepted degrees or education requirements.", max_length=10
    )
    responsibilities: list[str] = Field(
        description="The main responsibilities of the role.", max_length=15
    )
    ats_keywords: list[str] = Field(
        description="Important technical keywords suitable for résumé matching.", max_length=25
    )


def analyze_job_description(job_description: str, client=None):
    """Use Gemini to extract structured information from a job description."""
    validated_description = validate_job_description(job_description)
    ai_client = client or genai.Client(api_key=get_api_key())

    interaction = ai_client.interactions.create(
        model=get_model_name(),
        input=build_job_analysis_prompt(validated_description),
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": JobAnalysis.model_json_schema(),
        },
        store=False,
    )

    analysis = JobAnalysis.model_validate_json(interaction.output_text)
    return analysis, interaction.usage
