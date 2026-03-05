"""
main.py — Run this every morning: python main.py
"""

import asyncio
from resume_parser import parse_resume
from job_search import search_jobs
from job_matcher import score_job
from telegram_approval import send_job_summary
from sheets_tracker import log_to_sheets

# ── Edit these to match your job search ──────────────────────────────────────
PREFERENCES = {
    "job_titles":  ["Software Engineer", "Salesforce Engineer", "Application Engineer", "Solutions Engineer", "Associate Product Manager", "Product Manager Intern", "Product Manager"],
    "location":    "Bangalore",
    "remote":      "remote",
    "min_score":   65,    # Skip anything below this
    "max_applies": 100,    # Max jobs to send you per day
}

RESUME_PATH = "resume.pdf"


async def run():
    print("\n🤖 Job Agent starting...\n")

    # Step 1: Parse resume
    print("📄 Step 1/5: Parsing your resume...")
    resume = parse_resume(RESUME_PATH)
    print(f"   ✓ {resume['name']} | {resume['years_experience']} yrs exp | {len(resume['skills'])} skills\n")

    # Step 2: Search for jobs
    print("🔍 Step 2/5: Searching for jobs...")
    all_jobs = []
    for title in PREFERENCES["job_titles"]:
        jobs = search_jobs(title, PREFERENCES["location"], PREFERENCES["remote"])
        all_jobs.extend(jobs)
    seen = set()
    unique_jobs = []
    for j in all_jobs:
        key = (j["company"], j["title"])
        if key not in seen:
            seen.add(key)
            unique_jobs.append(j)
    print(f"   ✓ Found {len(unique_jobs)} unique listings\n")

    # Step 3: Score jobs in parallel
    print("🤖 Step 3/5: Scoring jobs with AI (parallel)...")

    async def score_one(job):
        loop = asyncio.get_event_loop()
        score = await loop.run_in_executor(None, score_job, resume, job)
        print(f"   Scored: {job['company']} — {score['score']}/100")
        return {"job": job, "score": score, "cover_letter": ""}

    results = await asyncio.gather(*[score_one(job) for job in unique_jobs])
    candidates = [r for r in results if r["score"]["score"] >= PREFERENCES["min_score"]]
    candidates.sort(key=lambda x: x["score"]["score"], reverse=True)
    candidates = candidates[:PREFERENCES["max_applies"]]
    print(f"   ✓ {len(candidates)} jobs above score {PREFERENCES['min_score']}\n")

    if not candidates:
        print("😔 No strong matches today. Try lowering min_score in PREFERENCES.")
        return

    # Step 4: Send summary to Telegram
    print("📱 Step 4/5: Sending job summary to Telegram...")
    await send_job_summary(candidates)
    print(f"   ✓ Sent {len(candidates)} jobs to Telegram\n")

    # Step 5: Log all matches to Google Sheets
    print("📊 Step 5/5: Logging to Google Sheets...")
    for c in candidates:
        log_to_sheets(c["job"], c["score"], status="To Apply")
        print(f"   ✓ {c['job']['title']} at {c['job']['company']}")

    print(f"\n🎉 Done! Check Telegram for your matches and apply at your own pace.")


if __name__ == "__main__":
    asyncio.run(run())