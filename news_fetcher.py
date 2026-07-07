"""
Live, real-time news fetcher. Checks the ACTUAL publish timestamp on every
entry and only returns items published within FRESHNESS_WINDOW_MINUTES.
If nothing genuinely new has been published recently, returns None instead
of posting stale filler.
"""
import feedparser
from datetime import datetime, timezone
from calendar import timegm

from sources import RSS_FEEDS
from storage import make_id, already_posted
from config import FRESHNESS_WINDOW_MINUTES


def _entry_age_minutes(entry) -> float:
    parsed_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed_time:
        return float("inf")
    published = datetime.fromtimestamp(timegm(parsed_time), tz=timezone.utc)
    age = datetime.now(timezone.utc) - published
    return age.total_seconds() / 60


def fetch_fresh_news_item():
    candidates = []

    for feed_url in RSS_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"[News feed error] {feed_url}: {e}")
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
                continue

            summary = entry.get("summary", "") or entry.get("description", "")
            candidates.append({
                "id": item_id,
                "title": title,
                "link": link,
                "summary": summary,
                "source": feed_url,
                "age_minutes": age,
            })

    if not candidates:
        print(f"[News fetch] No items published in the last {FRESHNESS_WINDOW_MINUTES} min.")
        return None

    candidates.sort(key=lambda c: c["age_minutes"])
    newest = candidates[0]
    print(f"[News fetch] Newest live item: '{newest['title']}' ({newest['age_minutes']:.1f} min old)")
    return newest
