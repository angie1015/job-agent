# 🤖 AI Job Application Agent

A personal AI agent that finds relevant job listings every day, scores them against your resume, and sends the best matches to your Telegram — so you can apply at your own pace.

Built entirely through conversation with Claude, no prior API experience needed.

---

## What it does

- 📄 Parses your resume and extracts your skills, experience, and profile
- 🔍 Searches job boards daily for roles matching your target titles and location
- 🤖 Scores every listing against your profile using AI (0–100 match score with reasons)
- 📱 Sends top matches to Telegram every morning with direct apply links
- 📊 Logs everything to a Google Sheet — company, role, score, and status

---

## Tech stack

| Component | Tool |
|---|---|
| Resume parsing | pdfplumber + OpenRouter |
| Job search | SerpAPI (Google Jobs) |
| AI scoring | OpenRouter (stepfun/step-3.5-flash) |
| Notifications | python-telegram-bot |
| Tracking | gspread + Google Sheets API |
| Orchestration | Python async |

---

## Project structure
```
job-agent/
├── main.py                  # Main pipeline — run this every morning
├── resume_parser.py         # Extracts structured profile from your PDF
├── job_search.py            # Searches job boards via SerpAPI
├── job_matcher.py           # Scores jobs against your resume using AI
├── telegram_approval.py     # Sends job summaries to Telegram
├── sheets_tracker.py        # Logs results to Google Sheets
├── .env.example             # Template for your API keys
├── requirements.txt         # Python dependencies
└── screenshots/             # Screenshots folder (gitignored)
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/job-agent.git
cd job-agent
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up your API keys

Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

You'll need:
- **OpenRouter API key** — [openrouter.ai](https://openrouter.ai) → Keys → Create Key (free)
- **SerpAPI key** — [serpapi.com](https://serpapi.com) → Dashboard (100 free searches/month)
- **Telegram bot token + chat ID** — message [@BotFather](https://t.me/botfather) on Telegram → `/newbot`
- **Google credentials** — Google Cloud Console → Create Service Account → download JSON → rename to `google_credentials.json` and place in project folder

### 4. Add your resume
Place your resume PDF in the project folder and name it `resume.pdf`.

### 5. Set your preferences
Edit the `PREFERENCES` block at the top of `main.py`:
```python
PREFERENCES = {
    "job_titles":  ["Software Engineer", "Product Manager"],
    "location":    "Bangalore",
    "remote":      "remote",
    "min_score":   65,
    "max_applies": 10,
}
```

### 6. Run it
```bash
python3 main.py
```

---

## Run it automatically every morning
```bash
crontab -e
```
Add this line (runs at 8am daily):
```
0 8 * * * cd ~/job-agent && source venv/bin/activate && python3 main.py >> logs/agent.log 2>&1
```

---

## Sample Telegram output
```
🟢 87/100 — Senior Product Manager
🏢 Stripe | 📍 Remote
📅 2 days ago

Why you match:
- 3+ years PM experience
- Fintech domain knowledge
- Strong cross-functional experience

🔗 Apply Here
```

---

## Contributing

Found a bug or want to add a feature? PRs welcome!
Ideas for future improvements:
- [ ] Auto-apply via Playwright
- [ ] Cover letter generation per role
- [ ] Duplicate detection across runs
- [ ] Slack notifications support

---

## License

MIT
