"""Sends a summary of all matched jobs to Telegram in one message."""

import os
from telegram import Bot
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID   = os.environ["TELEGRAM_CHAT_ID"]


async def send_job_summary(candidates: list):
    bot = Bot(token=BOT_TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=f"🤖 *Job Agent — Daily Run*\nFound *{len(candidates)}* matches for you today 👇",
        parse_mode="Markdown",
    )

    for c in candidates:
        job   = c["job"]
        score = c["score"]
        emoji = "🟢" if score["score"] >= 80 else "🟡" if score["score"] >= 65 else "🔴"
        reasons = "\n".join(f"• {r}" for r in score["reasons"])

        await bot.send_message(
            chat_id=CHAT_ID,
            text=(
                f"{emoji} *{score['score']}/100* — {job['title']}\n"
                f"🏢 {job['company']} | 📍 {job['location']}\n"
                f"📅 {job.get('posted', 'recently')}\n\n"
                f"*Why you match:*\n{reasons}\n\n"
                f"🔗 [Apply Here]({job['link']})"
            ),
            parse_mode="Markdown",
            disable_web_page_preview=False,
        )

    await bot.send_message(
        chat_id=CHAT_ID,
        text="✅ That's all for today! Good luck Anagha 🍀",
        parse_mode="Markdown",
    )


async def notify_applied(job: dict):
    await Bot(token=BOT_TOKEN).send_message(
        chat_id=CHAT_ID,
        text=f"📨 Logged → *{job['title']}* at *{job['company']}*",
        parse_mode="Markdown",
    )

async def notify_error(job: dict, error: str):
    await Bot(token=BOT_TOKEN).send_message(
        chat_id=CHAT_ID,
        text=f"⚠️ Error with *{job['title']}* at *{job['company']}*\n`{error}`",
        parse_mode="Markdown",
    )