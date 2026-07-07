import sqlite3
import hashlib
from config import DB_PATH

def _connect():
    # A short busy_timeout means concurrent GH Actions runners waiting on
    # the sqlite file (rare, since we now serialize via concurrency: in
    # the workflow) fail fast instead of hanging.
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posted (
            id TEXT PRIMARY KEY,
            title TEXT,
            link TEXT,
            summary TEXT,
            posted_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Migration for DBs created before link/summary existed.
    existing_cols = {row[1] for row in conn.execute("PRAGMA table_info(posted)")}
    if "link" not in existing_cols:
        conn.execute("ALTER TABLE posted ADD COLUMN link TEXT")
    if "summary" not in existing_cols:
        conn.execute("ALTER TABLE posted ADD COLUMN summary TEXT")
    return conn

def make_id(title: str, source: str = "") -> str:
    return hashlib.sha256(f"{title}|{source}".encode("utf-8")).hexdigest()

def already_posted(item_id: str) -> bool:
    conn = _connect()
    cur = conn.execute("SELECT 1 FROM posted WHERE id = ?", (item_id,))
    result = cur.fetchone() is not None
    conn.close()
    return result

def mark_posted(item_id: str, title: str, link: str = "", summary: str = ""):
    conn = _connect()
    conn.execute(
        "INSERT OR IGNORE INTO posted (id, title, link, summary) VALUES (?, ?, ?, ?)",
        (item_id, title, link, summary),
    )
    conn.commit()
    conn.close()

def recent_posts(limit: int = 60):
    """Used by rss_generator.py to build the public feed."""
    conn = _connect()
    cur = conn.execute(
        "SELECT id, title, link, summary, posted_at FROM posted "
        "WHERE link IS NOT NULL AND link != '' "
        "ORDER BY posted_at DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"id": r[0], "title": r[1], "link": r[2], "summary": r[3] or "", "posted_at": r[4]}
        for r in rows
    ]
