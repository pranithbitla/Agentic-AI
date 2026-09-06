from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

from careerpilot.config import get_api_key, get_model_name
from careerpilot.prompts import build_recommendation_prompt

load_dotenv()


class RecommendationPlan(BaseModel):
    match_summary: str = Field(description="A short explanation of the candidate's job match.")
    top_strengths: list[str] = Field(
        description="The candidate's strongest relevant qualifications."
    )
    priority_skill_gaps: list[str] = Field(
        description="The most important missing skills to learn."
    )
    resume_improvements: list[str] = Field(
        description="Honest improvements that can be made to the résumé."
    )
    learning_plan: list[str] = Field(description="A practical step-by-step learning plan.")
    interview_questions: list[str] = Field(
        description="Likely interview questions based on the job."
    )
    next_action: str = Field(
        description="The most important action the candidate should take next."
    )


def generate_recommendations(resume_text: str, job_data: dict, match_result: dict, client=None):
    """Generate a personalised job-improvement plan."""
    ai_client = client or genai.Client(api_key=get_api_key())

    interaction = ai_client.interactions.create(
        model=get_model_name(),
        input=build_recommendation_prompt(resume_text, job_data, match_result),
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": RecommendationPlan.model_json_schema(),
        },
        store=False,
    )

    recommendation = RecommendationPlan.model_validate_json(interaction.output_text)
    return recommendation, interaction.usage
