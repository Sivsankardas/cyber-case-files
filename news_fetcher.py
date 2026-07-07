# news_fetcher.py
import feedparser
from datetime import datetime, timezone, timedelta
from calendar import timegm
from sources import RSS_FEEDS
from storage import make_id, already_posted

FRESHNESS_WINDOW_MINUTES = 60  # only post things published in the last hour

def _entry_age_minutes(entry) -> float:
    parsed_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed_time:
        return 9999  # unknown age -> treat as stale, skip
    published = datetime.fromtimestamp(timegm(parsed_time), tz=timezone.utc)
    age = datetime.now(timezone.utc) - published
    return age.total_seconds() / 60

def fetch_fresh_news_item():
    candidates = []
    for feed_url in RSS_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception:
            continue
        for entry in parsed.entries[:15]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            if not title or not link:
                continue
            item_id = make_id(title, link)
            if already_posted(item_id):
                continue
            age = _entry_age_minutes(entry)
            if age > FRESHNESS_WINDOW_MINUTES:
                continue  # not actually breaking news, skip it
            candidates.append({
                "id": item_id,
                "title": title,
                "link": link,
                "summary": entry.get("summary", "") or entry.get("description", ""),
                "source": feed_url,
                "age_minutes": age,
            })
    if not candidates:
        return None
    candidates.sort(key=lambda c: c["age_minutes"])  # newest first
    return candidates[0]
