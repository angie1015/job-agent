"""Logs every job to your Google Sheet."""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

HEADERS = ["Date", "Company", "Role", "Location",
           "Job URL", "Match Score", "Why It Matches", "Gaps", "Status", "Notes"]

def get_sheet():
    creds = Credentials.from_service_account_file("google_credentials.json", scopes=SCOPES)
    gc = gspread.authorize(creds)
    sheet_name = os.environ.get("GOOGLE_SHEET_NAME", "Job Applications Tracker")

    try:
        sheet = gc.open(sheet_name).sheet1
    except gspread.SpreadsheetNotFound:
        # Create the sheet if it doesn't exist yet
        spreadsheet = gc.create(sheet_name)
        sheet = spreadsheet.sheet1
        sheet.append_row(HEADERS)
        # Make it accessible to you
        spreadsheet.share(None, perm_type="anyone", role="writer")
        print(f"✓ Created new Google Sheet: {sheet_name}")

    return sheet


def log_to_sheets(job: dict, score: dict, status: str = "Applied"):
    sheet = get_sheet()
    sheet.append_row([
        datetime.today().strftime("%Y-%m-%d"),
        job.get("company", ""),
        job.get("title", ""),
        job.get("location", ""),
        job.get("link", ""),
        score.get("score", ""),
        ", ".join(score.get("reasons", [])),
        ", ".join(score.get("gaps", [])),
        status,
        "",  # Notes column — fill in manually
    ])