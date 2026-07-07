"""
Pulls real, live bug bounty and vulnerability research coverage from
PortSwigger's "The Daily Swig" — a security news outlet that actively covers
bug bounty disclosures, researcher write-ups, and web security findings.

(Note: HackerOne's public Hacktivity RSS feed was deprecated and no longer
returns live data, so this replaced it as a more reliable live source.)
"""
import feedparser
import random
import re
from storage import make_id, already_posted

BOUNTY_FEEDS = [
    "https://portswigger.net/daily-swig/rss",
]


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def fetch_recent_disclosure():
    entries_pool = []

    for feed_url in BOUNTY_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
            entries_pool.extend(parsed.entries[:30])
        except Exception as e:
            print(f"[Bounty feed error] {feed_url}: {e}")
            continue

    random.shuffle(entries_pool)

    for entry in entries_pool:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        summary = _strip_html(entry.get("summary", "") or entry.get("description", ""))[:500]

        if not title or not link:
            continue

        relevant_keywords = ["bounty", "bug", "vulnerab", "disclos", "exploit",
                             "hacker", "researcher", "flaw", "cve", "patch"]
        text_to_check = (title + " " + summary).lower()
        is_relevant = any(kw in text_to_check for kw in relevant_keywords)
        if not is_relevant:
            continue

        item_id = make_id(title, link)
        if already_posted(item_id):
            continue

        return {
            "id": item_id,
            "title": title,
            "link": link,
            "summary": summary,
        }

    return None
