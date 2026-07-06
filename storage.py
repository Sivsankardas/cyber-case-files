import sqlite3
import hashlib
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
