"""Uses OpenRouter to score each job against your resume."""

import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

def score_job(resume: dict, job: dict) -> dict:
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
                "content": f"""Score this job for this candidate. Return ONLY valid JSON, nothing else.

Format:
{{
  "score": 75,
  "reasons": ["reason 1", "reason 2", "reason 3"],
  "apply_recommended": true,
  "gaps": ["any missing skills or experience"]
}}

Candidate profile:
{json.dumps(resume, indent=2)}

Job:
Title: {job['title']}
Company: {job['company']}
Description: {job['description'][:1500]}"""
            }]
        }
    ).json()
    print("DEBUG:", response)  # ← add this line temporarily
    content = response["choices"][0]["message"]["content"]
    content = content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(content)