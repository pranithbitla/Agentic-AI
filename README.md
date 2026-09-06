# Agentic AI & Python Portfolio

[![CareerPilot Tests](https://github.com/pranithbitla/Agentic-AI/actions/workflows/careerpilot-tests.yml/badge.svg)](https://github.com/pranithbitla/Agentic-AI/actions/workflows/careerpilot-tests.yml)

A project-based repository showing my progression from Python fundamentals to practical Agentic AI applications.

The main portfolio project is **CareerPilot AI**, an agentic résumé and job-match analyzer. The repository also contains foundational Python projects that demonstrate core programming concepts and problem-solving practice.

## ⭐ Featured Project — CareerPilot AI

[`careerpilot-ai/`](careerpilot-ai/)

CareerPilot AI analyzes a résumé against a job description and produces a structured job-match report.

**Highlights**

- Agent workflow built with LangGraph
- Google Gemini for structured job analysis and recommendations
- Deterministic skill-match scoring instead of an LLM-generated percentage
- Prompt-injection boundaries for untrusted résumé and job text
- Required vs. preferred skill weighting
- Separate ATS keyword coverage
- Résumé skill-gap analysis and learning recommendations
- Streamlit user interface
- PDF and pasted-text résumé input
- Pydantic structured outputs
- Privacy-first, opt-in disk caching
- Safe example report that works without an API key
- Ruff, pytest, coverage enforcement, and multi-version GitHub Actions CI

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
- Ruff linting and coverage-enforced tests
- Automated CI on Python 3.11 and 3.12
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

This repository documents a learning path from Python fundamentals toward AI engineering and Agentic AI. CareerPilot now emphasizes explainable scoring, responsible handling of untrusted inputs, privacy-aware defaults, automated quality checks, and honest product limitations.

## 👨‍💻 Author

**Pranith Bitla**  
GitHub: [@pranithbitla](https://github.com/pranithbitla)
