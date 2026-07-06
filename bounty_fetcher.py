import feedparser
import random
import re
from storage import make_id, already_posted

HACKERONE_FEED = "https://hackerone.com/hacktivity.rss"


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def fetch_recent_disclosure():
    try:
        parsed = feedparser.parse(HACKERONE_FEED)
    except Exception as e:
        print(f"[HackerOne fetch error] {e}")
        return None

    entries = parsed.entries[:30]
    random.shuffle(entries)

    for entry in entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        summary = _strip_html(entry.get("summary", "") or entry.get("description", ""))[:500]

        if not title or not link:
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
