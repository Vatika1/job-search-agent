from datetime import datetime, timedelta, timezone
from fetchers.greenhouse import fetch
from storage import get_conn, is_seen, mark_seen
from filters import title_ok, java_hits, MIN_JAVA_HITS, location_ok
from scorer import score
from notifier import send, format_jobs

TOP_N = 15
SLUGS = ["behavox", "workleap", "lyft"]
MAX_AGE_DAYS = 4


def is_fresh(posted_at: str) -> bool:
    posted = datetime.fromisoformat(posted_at)
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    return posted >= cutoff


if __name__ == "__main__":
    conn = get_conn()
    results = []
    for slug in SLUGS:
        for job in fetch(slug):
            if not is_fresh(job["posted_at"]):
                continue
            if not title_ok(job["title"]):
                continue
            if not location_ok(job["location"]):
                continue
            if java_hits(job["description"]) < MIN_JAVA_HITS:
                continue
            if is_seen(conn, job["id"]):
                continue
            results.append((job, score(job)))
            mark_seen(conn, job["id"])
    results.sort(key=lambda x: x[1]["score"], reverse=True)
    top = results[:TOP_N]
    body = format_jobs(top) if top else "No new jobs today."
    print(body)
    if top:
        send(f"Job agent: {len(top)} new matches", body)
    print(f"\n{len(results)} new jobs, emailed top {len(top)}")