import sqlite3
from datetime import datetime, timezone

DB_PATH = "jobs.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen (
            id TEXT PRIMARY KEY,
            first_seen TEXT NOT NULL
        )
    """)
    return conn


def is_seen(conn, job_id: str) -> bool:
    row = conn.execute("SELECT 1 FROM seen WHERE id = ?", (job_id,)).fetchone()
    return row is not None


def mark_seen(conn, job_id: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO seen (id, first_seen) VALUES (?, ?)",
        (job_id, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()