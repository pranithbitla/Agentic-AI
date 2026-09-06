# Development Guide

This guide explains how CareerPilot is organized and how to extend it without mixing deterministic matching logic with LLM responsibilities.

## Module responsibilities

### `careerpilot/resume_reader.py`
Reads PDF or plain-text résumés and enforces size, page, format, and extracted-text limits.

### `careerpilot/config.py`
Centralizes input limits, Gemini model selection, and user-facing configuration errors.

### `careerpilot/prompts.py`
Builds prompts with explicit trust boundaries around untrusted résumé and job-description content.

### `careerpilot/job_analyzer.py`
Uses Gemini structured output and a Pydantic schema to convert an unstructured job description into fields such as required skills, preferred skills, experience, responsibilities, and ATS keywords.

### `careerpilot/skill_matcher.py`
Contains deterministic matching logic. It normalizes text, resolves aliases in both directions,
deduplicates equivalent skills, and calculates required, preferred, and ATS keyword coverage.

### `careerpilot/recommendation_agent.py`
Uses the résumé, structured job analysis, and deterministic match result to generate grounded recommendations. Its prompt explicitly prevents invented experience or skills.

### `careerpilot/cache.py`
Builds a SHA-256 hash from the résumé text and job description. Persistent reuse is opt-in through
`CAREERPILOT_ENABLE_DISK_CACHE=true` because reports may contain résumé-derived data.

### `careerpilot/graph.py`
Defines the LangGraph state and workflow nodes. Conditional routing decides whether to return a cached result or execute a fresh analysis.

### `app.py`
Provides the Streamlit user interface and manages temporary uploaded files.

## Development workflow

1. Create and activate a virtual environment.
2. Install runtime and development dependencies.
3. Copy `.env.example` to `.env` and configure `GEMINI_API_KEY`.
4. Make changes in the appropriate module.
5. Run tests before committing.
6. Run Streamlit locally for end-to-end validation.

```bash
pip install -r requirements-dev.txt
python -m ruff check .
python -m pytest -q
streamlit run app.py
```

## Adding a new skill alias

Add aliases only when they clearly represent the same skill and add or update a test whenever matching behavior changes.

## Testing strategy

Tests do not require an API key. Inject fake AI clients for integration boundaries and mock individual
workflow functions when testing LangGraph nodes. CI runs Ruff and enforces at least 80% package
coverage on Python 3.11 and 3.12.

## Design principles

- Keep numeric scoring deterministic and explainable.
- Use the LLM for language understanding, not arbitrary scoring.
- Validate LLM output with Pydantic.
- Never invent candidate experience or skills.
- Keep secrets and personal résumé files out of Git.
- Prefer small modules with one clear responsibility.
