# AI Baby Product Advisor

## Problem Statement
Parents need quick, trustworthy, and age-appropriate baby product recommendations without spending hours researching.

## Solution
This Streamlit app uses an LLM to generate curated baby product recommendations, safety tips, and an Arabic translation for each result.

## How to Run
1. Create and activate a virtual environment.
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Set `GROQ_API_KEY` as an environment variable.
4. Run the app:
	```bash
	streamlit run app.py
	```

## Environment Variables
- `GROQ_API_KEY` (required)
- `GROQ_MODEL` (optional)

## Notes
Set `GROQ_API_KEY` as an environment variable before running the app.
