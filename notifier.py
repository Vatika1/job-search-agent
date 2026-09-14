import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()
USER = os.environ["GMAIL_USER"]
PASSWORD = os.environ["GMAIL_APP_PASSWORD"]


def send(subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = USER
    msg["To"] = USER
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(USER, PASSWORD)
        s.send_message(msg)


def format_jobs(ranked: list[tuple[dict, dict]]) -> str:
    lines = []
    for job, r in ranked:
        lines.append(f"[{r['score']}] {job['title']} — {job['company']} ({job['location']})")
        lines.append(f"    {r['seniority_fit']} | {r['reason']}")
        lines.append(f"    {job['url']}\n")
    return "\n".join(lines)