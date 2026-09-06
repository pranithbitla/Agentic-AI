# Recruiter Walkthrough

Use this two-minute path to evaluate CareerPilot without reading the whole repository.

## 1. Preview the product

Run `streamlit run app.py` and select **Preview Example Report**. The fictional report demonstrates
the complete results interface without an API key or personal résumé.

## 2. Inspect the engineering decision

Open [`careerpilot/graph.py`](../careerpilot/graph.py). LangGraph coordinates validation, optional
cache routing, job analysis, skill matching, recommendation generation, and report assembly.

The main design choice is deliberate separation:

- Gemini extracts structured requirements and produces natural-language guidance.
- Python calculates the numeric score from visible matched and missing skills.
- Pydantic validates AI responses before downstream code uses them.

## 3. Check responsible AI behavior

Open [`careerpilot/prompts.py`](../careerpilot/prompts.py). Résumé and job-description text is
explicitly marked as untrusted data. The model is told not to follow instructions inside those
inputs and not to invent candidate experience.

Persistent caching is opt-in because generated reports can contain résumé-derived information.
Uploaded temporary files are deleted after every attempt, including failed analyses.

## 4. Verify quality

```bash
python -m ruff check .
python -m pytest -q
```

CI repeats these checks on Python 3.11 and 3.12 and enforces a package coverage threshold.

## Strong interview discussion points

1. Why deterministic scores are more trustworthy than LLM-generated percentages.
2. How conditional LangGraph routing avoids repeat model calls when private caching is enabled.
3. How dependency injection tests AI integrations without spending tokens.
4. Why input limits and prompt trust boundaries matter in LLM applications.
5. What would be added for production: authentication, encrypted storage, evaluation datasets,
   observability, rate limiting, and OCR.
