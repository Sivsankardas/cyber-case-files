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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS counters (
            name TEXT PRIMARY KEY,
            value INTEGER NOT NULL DEFAULT 0
        )
    """)
    return conn


def next_counter_value(name: str) -> int:
    """
    Returns the next value for a named counter (starting at 0, incrementing
    every call) and persists it. Used to rotate through historical cases and
    tips in order, without repeats, regardless of how many times the script
    runs in a day (manual test runs included).
    """
    conn = _connect()
    cur = conn.execute("SELECT value FROM counters WHERE name = ?", (name,))
    row = cur.fetchone()
    current = row[0] if row else 0
    conn.execute(
        "INSERT INTO counters (name, value) VALUES (?, ?) "
        "ON CONFLICT(name) DO UPDATE SET value = ?",
        (name, current + 1, current + 1),
    )
    conn.commit()
    conn.close()
    return current


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
