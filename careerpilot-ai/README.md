# 🚀 CareerPilot AI

**CareerPilot AI** is an agentic résumé and job-match analyzer built with **Python, LangGraph, Google Gemini, Pydantic, and Streamlit**. It compares a candidate's résumé against a job description, calculates a deterministic skill-match score, identifies gaps, and generates practical career recommendations.

## ✨ Key features

- Upload a text-based PDF résumé
- Paste any job description
- Extract structured hiring requirements with Gemini
- Separate required and preferred skills
- Calculate a deterministic résumé-to-job match score
- Match common aliases such as `GitHub → Git` and `AWS → cloud deployment`
- Generate strengths, skill gaps, résumé improvements, and a learning roadmap
- Generate role-specific interview questions
- Cache identical analyses to reduce unnecessary LLM calls
- Download the complete result as JSON
- Delete temporary uploaded files after analysis

## 🧠 Workflow

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
     │   Deterministic Matcher
     │          │
     │          ▼
     │   Recommendation Agent
     │          │
     └──────► Final Report
                │
                ▼
          Streamlit Dashboard
```

For the detailed graph and design decisions, see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

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
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT.md
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

| Area | Technology |
|---|---|
| Language | Python |
| Agent workflow | LangGraph |
| LLM | Google Gemini (`google-genai`) |
| Structured output | Pydantic |
| UI | Streamlit |
| PDF parsing | pypdf |
| Testing | pytest |

## ⚙️ Setup

### 1. Clone this branch

```bash
git clone --branch careerpilot-ai --single-branch https://github.com/pranithbitla/Agentic-AI.git
cd Agentic-AI/careerpilot-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit the real `.env` file.

### 5. Run the application

```bash
streamlit run app.py
```

## 🧪 Run tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

Current tests verify skill-alias matching, false-positive prevention, and the 70/30 required-vs-preferred weighting logic.

## 🎯 Match-score design

CareerPilot deliberately does **not** ask the LLM to invent an ATS percentage. The numeric score is calculated in Python:

- Required skills: **70%** of the final score
- Preferred skills: **30%** of the final score

Gemini is used where language understanding is useful: extracting job requirements and generating grounded recommendations.

## 🔒 Privacy and repository hygiene

The repository ignores `.env`, Streamlit secrets, uploaded résumé PDFs, generated JSON reports, Python caches, virtual environments, and editor files. Uploaded files are handled as temporary files by the Streamlit UI and removed after processing.

## 📚 Additional documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — graph flow, component responsibilities, and design decisions
- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) — development workflow, testing, module guide, and extension ideas
- [`examples/sample_job_description.txt`](examples/sample_job_description.txt) — safe sample input for testing

## 🔮 Future improvements

- Semantic skill matching using embeddings
- More complete ATS keyword normalization
- DOCX résumé support
- Better visual dashboards and charts
- Exportable PDF report
- Persistent database-backed caching
- Streamlit Community Cloud deployment
- Additional tests for agent and graph behavior

## 👨‍💻 Author

**Pranith Bitla**  
GitHub: [@pranithbitla](https://github.com/pranithbitla)
