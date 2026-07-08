import sqlite3
import hashlib
from datetime import datetime, timezone
from config import DB_PATH


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posted (
            id TEXT PRIMARY KEY,
            title TEXT,
            posted_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS channel_posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            link TEXT,
            description TEXT,
            category TEXT,
            pub_date TEXT
        )
    """)
    return conn


def make_id(title: str, source: str = "") -> str:
    return hashlib.sha256(f"{title}|{source}".encode("utf-8")).hexdigest()


def already_posted(item_id: str) -> bool:
    conn = _connect()
    cur = conn.execute("SELECT 1 FROM posted WHERE id = ?", (item_id,))
    result = cur.fetchone() is not None
    conn.close()
    return result


def mark_posted(item_id: str, title: str):
    conn = _connect()
    conn.execute("INSERT OR IGNORE INTO posted (id, title) VALUES (?, ?)", (item_id, title))
    conn.commit()
    conn.close()


def add_channel_post(item_id: str, title: str, link: str, description: str, category: str):
    """Record a post so it can be re-published in our own RSS feed (feed.xml)."""
    conn = _connect()
    conn.execute(
        "INSERT OR IGNORE INTO channel_posts (id, title, link, description, category, pub_date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (item_id, title, link, description, category, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()


def get_last_post_time(category: str):
    """Last time this category actually posted something (not just checked)."""
    conn = _connect()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS category_state (category TEXT PRIMARY KEY, last_posted_at TEXT)"
    )
    cur = conn.execute("SELECT last_posted_at FROM category_state WHERE category = ?", (category,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    try:
        return datetime.fromisoformat(row[0])
    except Exception:
        return None


def set_last_post_time(category: str, dt: datetime):
    conn = _connect()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS category_state (category TEXT PRIMARY KEY, last_posted_at TEXT)"
    )
    conn.execute(
        "INSERT INTO category_state (category, last_posted_at) VALUES (?, ?) "
        "ON CONFLICT(category) DO UPDATE SET last_posted_at = excluded.last_posted_at",
        (category, dt.isoformat()),
    )
    conn.commit()
    conn.close()


def get_recent_channel_posts(limit: int = 100):
    conn = _connect()
    cur = conn.execute(
        "SELECT title, link, description, category, pub_date FROM channel_posts "
        "ORDER BY pub_date DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"title": r[0], "link": r[1], "description": r[2], "category": r[3], "pub_date": r[4]}
        for r in rows
    ]
