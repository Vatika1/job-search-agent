import re
import html
import requests

BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"


def strip_html(text: str) -> str:
    text = html.unescape(text or "")
    return re.sub(r"<[^>]+>", " ", text).strip()


def fetch(company_slug: str) -> list[dict]:
    url = BASE_URL.format(slug=company_slug)
    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        print(f"[warn] {company_slug}: HTTP {resp.status_code}")
        return []

    jobs = []
    for job in resp.json().get("jobs", []):
        jobs.append({
            "id": f"gh-{job['id']}",
            "title": job["title"],
            "company": company_slug,
            "location": job.get("location", {}).get("name", ""),
            "url": job["absolute_url"],
            "posted_at": job["updated_at"],
            "description": strip_html(job.get("content", "")),
        })
    return jobs