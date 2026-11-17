# CareerPilot AI — Resume & Job-Fit Agent

## What it does
1. Reads a text-based PDF resume.
2. Uses Gemini to extract structured job requirements from a pasted job description.
3. Runs a transparent Python keyword match (70% required skills + 30% preferred skills).
4. Uses Gemini to produce evidence-aware strengths, gaps, resume suggestions and interview questions.
5. Uses LangGraph to orchestrate the steps and pass shared state between nodes.

## Run
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Enter your Gemini API key in the sidebar.

## Honest limitations
- The match score is a keyword baseline, not a measure of actual skill proficiency.
- A skill can be missed if it is described using different wording.
- Scanned PDFs need OCR, which this version does not include.
- The system provides decision support; it does not make hiring decisions.
- Test with sample resumes and job descriptions before putting it on a public portfolio.
