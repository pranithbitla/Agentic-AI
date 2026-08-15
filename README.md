# Agentic AI & Python Portfolio

A project-based repository showing my progression from Python fundamentals to practical Agentic AI applications.

The main portfolio project is **CareerPilot AI**, an agentic résumé and job-match analyzer. The repository also contains foundational Python projects that demonstrate core programming concepts and problem-solving practice.

## ⭐ Featured Project — CareerPilot AI

[`careerpilot-ai/`](careerpilot-ai/)

CareerPilot AI analyzes a résumé against a job description and produces a structured job-match report.

**Highlights**

- Agent workflow built with LangGraph
- Google Gemini for structured job analysis and recommendations
- Deterministic skill-match scoring instead of an LLM-generated percentage
- Required vs. preferred skill weighting
- Résumé skill-gap analysis and learning recommendations
- Streamlit user interface
- PDF résumé parsing
- Pydantic structured outputs
- Caching to reduce repeated LLM calls
- Automated tests with pytest
- GitHub Actions CI for CareerPilot tests

**Tech stack:** Python · LangGraph · Google Gemini · Pydantic · Streamlit · pypdf · pytest

➡️ [View the complete CareerPilot documentation](careerpilot-ai/README.md)

## 📁 Repository Structure

```text
Agentic-AI/
├── .github/
│   └── workflows/
│       └── careerpilot-tests.yml
├── careerpilot-ai/          # Featured Agentic AI project
├── python-projects/         # Python foundation projects
├── .gitignore
└── README.md
```

## 🧩 Project Index

| Project | Focus | Level |
|---|---|---|
| [CareerPilot AI](careerpilot-ai/) | Agentic AI, LangGraph, Gemini, Streamlit | Featured |
| [Chat Analyzer](python-projects/chat_analyzer.py) | Functions, strings, collections, modular Python | Foundational |
| [ATM Simulator](python-projects/atm_simulator.py) | Loops, conditions, state, user input | Foundational |
| [MovieMate](python-projects/movie_recommender.py) | Lists, conditions, dates, user interaction | Foundational |

## 🛠 Engineering Practices Demonstrated

- Clear project separation and documentation
- Modular Python package structure in CareerPilot
- Environment-variable based secret handling
- `.env.example` instead of committed API keys
- Unit tests with pytest
- Automated CI with GitHub Actions
- Git/GitHub based version control

## 🚀 Quick Start

Clone the repository:

```bash
git clone https://github.com/pranithbitla/Agentic-AI.git
cd Agentic-AI
```

### Run CareerPilot AI

```bash
cd careerpilot-ai
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

Before running CareerPilot, copy `.env.example` to `.env` and add your Gemini API key.

### Explore the Python projects

```bash
cd python-projects
python atm_simulator.py
```

See [`python-projects/README.md`](python-projects/README.md) for details.

## 🎯 Current Direction

This repository documents a learning path from Python programming fundamentals toward AI engineering and Agentic AI. Future work will focus on stronger UI/UX, deployment, semantic matching, additional automated tests, and production-oriented AI workflows.

## 👨‍💻 Author

**Pranith Bitla**  
GitHub: [@pranithbitla](https://github.com/pranithbitla)
