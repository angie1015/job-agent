"""Reads your resume PDF and extracts a structured profile using OpenRouter."""

import pdfplumber
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

def parse_resume(path: str) -> dict:
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "model": "stepfun/step-3.5-flash:free",
            "messages": [{
                "role": "user",
                "content": f"""Extract a profile from this resume and return ONLY valid JSON, nothing else.

Format:
{{
  "name": "...",
  "email": "...",
  "phone": "...",
  "skills": ["skill1", "skill2"],
  "job_titles": ["most recent title", "previous title"],
  "years_experience": 5,
  "education": "Degree, University",
  "summary": "2 sentence summary"
}}

Resume:
{text}"""
            }]
        }
    ).json()

    content = response["choices"][0]["message"]["content"]
    # Strip markdown code fences if model adds them
    content = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(content)