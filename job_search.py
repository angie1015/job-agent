"""Searches Google Jobs via SerpAPI for matching roles."""

import requests
import os
from dotenv import load_dotenv
load_dotenv()

def search_jobs(title: str, location: str, remote: str) -> list[dict]:
    query = f"{title} {remote} jobs {location}"
    params = {
        "engine": "google_jobs",
        "q": query,
        "api_key": os.environ["SERPAPI_KEY"],
        "num": 10,
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json().get("jobs_results", [])

    jobs = []
    for j in results:
        # Get the direct application link if available
        links = j.get("related_links", [])
        link = links[0].get("link", "") if links else j.get("share_link", "")

        jobs.append({
            "title":       j.get("title", ""),
            "company":     j.get("company_name", ""),
            "location":    j.get("location", ""),
            "link":        link,
            "description": j.get("description", ""),
            "posted":      j.get("detected_extensions", {}).get("posted_at", ""),
        })

    return jobs