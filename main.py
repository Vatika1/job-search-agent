from datetime import datetime, timedelta, timezone
from fetchers.greenhouse import fetch
from storage import get_conn, is_seen, mark_seen
from filters import title_ok, java_hits, MIN_JAVA_HITS

SLUGS = ["behavox", "workleap", "lyft"]
MAX_AGE_DAYS = 3


def is_fresh(posted_at: str) -> bool:
    posted = datetime.fromisoformat(posted_at)
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    return posted >= cutoff


if __name__ == "__main__":
    conn = get_conn()
    new_count = 0
    for slug in SLUGS:
        for job in fetch(slug):
            if not is_fresh(job["posted_at"]):
                continue
            if not title_ok(job["title"]):
                continue
            if java_hits(job["description"]) < MIN_JAVA_HITS:
                continue
            if is_seen(conn, job["id"]):
                continue
            print(f"{job['title']} | {job['company']} | {job['location']} | {job['posted_at']} | {job['url']}")
            mark_seen(conn, job["id"])
            new_count += 1
    print(f"\n{new_count} new jobs")