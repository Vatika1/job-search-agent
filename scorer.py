import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-sonnet-5"
CV = (Path(__file__).parent / "cv.txt").read_text(encoding="utf-8")

PROMPT = """You are screening job postings for a candidate. Compare the CV and the job description.
Respond with JSON only, no prose, no markdown:
{{"score": <0-100 match>, "seniority_fit": "under"|"match"|"over", "missing_required": [<required skills the CV lacks>], "reason": "<one sentence>"}}

CV:
{cv}

JOB TITLE: {title}
JOB DESCRIPTION:
{description}"""


def score(job: dict) -> dict:
    prompt = PROMPT.format(cv=CV, title=job["title"], description=job["description"][:8000])
    resp = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    text = text.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"[warn] bad JSON for {job['id']}: {text[:80]}")
        return {"score": 0, "seniority_fit": "?", "missing_required": [], "reason": "parse error"}