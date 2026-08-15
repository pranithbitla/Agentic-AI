# 🚀 CareerPilot AI

**CareerPilot AI** is an agentic résumé and job-match analyzer built with Python, LangGraph, Gemini, and Streamlit. It compares a candidate's résumé with a job description, calculates a deterministic match score, identifies skill gaps, and generates practical career recommendations.

## ✨ Features

- Upload a text-based PDF résumé
- Paste any job description
- Extract structured job requirements with Gemini
- Calculate required and preferred skill-match scores
- Detect skill aliases such as `GitHub → Git` and `AWS → cloud deployment`
- Generate strengths, skill gaps, résumé improvements, and a learning plan
- Generate role-specific interview questions
- Cache identical analyses to avoid unnecessary LLM calls
- Download the complete analysis report as JSON

## 🧠 How it works

```text
Resume + Job Description
          │
          ▼
      Read Inputs
          │
          ▼
      Check Cache
       /       \
   cached      new
     │          │
     │          ▼
     │    Job Analyzer Agent
     │          │
     │          ▼
     │     Skill Matcher
     │          │
     │          ▼
     │   Recommendation Agent
     │          │
     └──────► Final Report
                │
                ▼
          Streamlit Dashboard
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the detailed workflow.

## 📁 Project structure

```text
careerpilot-ai/
├── app.py
├── careerpilot/
│   ├── __init__.py
│   ├── cache.py
│   ├── graph.py
│   ├── job_analyzer.py
│   ├── recommendation_agent.py
│   ├── resume_reader.py
│   └── skill_matcher.py
├── docs/
│   └── ARCHITECTURE.md
├── examples/
│   └── sample_job_description.txt
├── tests/
│   └── test_skill_matcher.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## 🛠 Tech stack

Python · LangGraph · Google Gemini · Pydantic · Streamlit · pypdf · pytest

## ⚙️ Setup

```bash
git clone https://github.com/pranithbitla/Agentic-AI.git
cd Agentic-AI/careerpilot-ai
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, add your Gemini API key, then run:

```bash
streamlit run app.py
```

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## 🔒 Privacy

Personal résumé PDFs, API keys, generated reports, Python caches, and virtual environments are excluded through `.gitignore`. Temporary uploaded files are removed after analysis.

## 🎯 Why this project is agentic

CareerPilot uses LangGraph to coordinate job analysis, deterministic résumé matching, personalized recommendation generation, and conditional cache routing. The workflow has explicit state, nodes, routing, and specialized responsibilities rather than relying on one LLM prompt.

## 🔮 Future improvements

- Semantic skill matching with embeddings
- Better ATS keyword normalization
- DOCX résumé support
- Exportable PDF report
- Streamlit Community Cloud deployment

## 👨‍💻 Author

**Pranith Bitla** — [@pranithbitla](https://github.com/pranithbitla)
