import json

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()


class RecommendationPlan(BaseModel):
    match_summary: str = Field(description="A short explanation of the candidate's job match.")
    top_strengths: list[str] = Field(description="The candidate's strongest relevant qualifications.")
    priority_skill_gaps: list[str] = Field(description="The most important missing skills to learn.")
    resume_improvements: list[str] = Field(description="Honest improvements that can be made to the résumé.")
    learning_plan: list[str] = Field(description="A practical step-by-step learning plan.")
    interview_questions: list[str] = Field(description="Likely interview questions based on the job.")
    next_action: str = Field(description="The most important action the candidate should take next.")


def generate_recommendations(resume_text, job_data, match_result):
    """Generate a personalised job-improvement plan."""
    client = genai.Client()
    job_json = json.dumps(job_data, separators=(",", ":"))
    match_json = json.dumps(match_result, separators=(",", ":"))

    prompt = f"""
You are the CareerPilot AI Recommendation Agent.

Your goal is to help a Computer Science fresher prepare for the given job honestly and practically.

RESUME:
{resume_text[:6000]}

JOB ANALYSIS:
{job_json}

MATCH RESULT:
{match_json}

Rules:
1. Do not invent experience, projects or skills.
2. Do not recommend adding an unlearned skill as an existing skill.
3. Prioritise missing required skills before preferred skills.
4. Keep every recommendation concise and actionable.
5. Suggest beginner-friendly learning steps.
6. Generate no more than five interview questions.
7. Clearly explain what the candidate should do next.
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": RecommendationPlan.model_json_schema(),
        },
        store=False,
    )

    recommendation = RecommendationPlan.model_validate_json(interaction.output_text)
    return recommendation, interaction.usage
