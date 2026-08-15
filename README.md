# Agentic AI & Python Projects

A hands-on learning repository for Python fundamentals, automation, and Agentic AI applications.

## 📁 Repository Structure

```text
Agentic-AI/
├── README.md
├── python-projects/
│   ├── ATM.py
│   ├── email_automation.py
│   ├── main.py
│   ├── movie_recommendations (1).py
│   └── my_programs.py
└── careerpilot-ai/
    ├── app.py
    ├── careerpilot/
    ├── docs/
    ├── examples/
    ├── tests/
    ├── requirements.txt
    ├── requirements-dev.txt
    ├── .env.example
    ├── .gitignore
    └── README.md
```

## 🚀 Featured Project — CareerPilot AI

**CareerPilot AI** is an agentic résumé and job-match analyzer built with Python, LangGraph, Google Gemini, Pydantic, and Streamlit.

It can:

- Read a text-based PDF résumé
- Analyze a pasted job description
- Extract required and preferred skills
- Calculate a deterministic résumé-to-job match score
- Identify missing skills and strengths
- Generate résumé improvements and a learning roadmap
- Create role-specific interview questions
- Cache repeated analyses to reduce unnecessary LLM calls
- Present the result in a Streamlit dashboard

CareerPilot uses a LangGraph workflow to coordinate analysis steps while keeping the actual match percentage deterministic in Python instead of asking the LLM to invent a score.

For full setup instructions, architecture details, testing, and documentation, see [`careerpilot-ai/README.md`](careerpilot-ai/README.md).

### CareerPilot Tech Stack

| Area | Technology |
|---|---|
| Language | Python |
| Agent workflow | LangGraph |
| LLM | Google Gemini |
| Structured output | Pydantic |
| UI | Streamlit |
| PDF parsing | pypdf |
| Testing | pytest |

### Run CareerPilot

```bash
cd careerpilot-ai
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Add your Gemini API key using `.env.example`, then run:

```bash
streamlit run app.py
```

## 🐍 Python Practice Projects

The `python-projects/` folder contains smaller projects and exercises created while strengthening Python fundamentals.

| File | Description |
|---|---|
| `ATM.py` | ATM operations and user-interaction practice project. |
| `movie_recommendations (1).py` | Movie recommendation project using Python logic and user input. |
| `my_programs.py` | Collection of Python practice programs and programming exercises. |
| `main.py` | General Python experimentation and practice script. |
| `email_automation.py` | Email automation experimentation module. |

## 🎯 Learning Goals

- Strengthen Python programming fundamentals
- Build real-world automation projects
- Understand AI-agent workflows
- Learn LangGraph and LLM integration
- Build practical Streamlit applications
- Practice testing and structured project organization
- Maintain clean projects using Git and GitHub

## 🛠️ Technologies Used Across This Repository

- Python
- LangGraph
- Google Gemini
- Pydantic
- Streamlit
- pypdf
- pytest
- Git
- GitHub

## 📌 Repository Status

This repository documents my progression from Python fundamentals to structured Agentic AI applications. CareerPilot AI is the main end-to-end project, while `python-projects/` contains smaller practice programs and experiments.
