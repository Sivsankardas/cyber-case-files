"""
Pulls real, live bug bounty write-ups and disclosed vulnerability research
from multiple active sources. Attaches real publish-age from each feed
entry's own timestamp (same approach as news_fetcher.py).
"""
import feedparser
import random
import re
from calendar import timegm
from datetime import datetime, timezone
from storage import make_id, already_posted
from freshness import humanize_age

BOUNTY_FEEDS = [
    "https://infosecwriteups.com/feed",
    "https://medium.com/feed/tag/bug-bounty",
    "https://medium.com/feed/tag/bugbounty",
    "https://medium.com/feed/tag/penetration-testing",
    "https://portswigger.net/daily-swig/rss",
]


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _entry_datetime(entry):
    parsed_time = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed_time:
        return None
    return datetime.fromtimestamp(timegm(parsed_time), tz=timezone.utc)


def fetch_recent_disclosure():
    feeds = BOUNTY_FEEDS[:]
    random.shuffle(feeds)
    for feed_url in feeds:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"[Bounty feed error] {feed_url}: {e}")
            continue
        entries = parsed.entries[:20]
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
            print(f"[Bounty fetch] Found item from {feed_url}: {title}")
            return {
                "id": item_id,
                "title": title,
                "link": link,
                "summary": summary,
                "freshness": humanize_age(_entry_datetime(entry)),
            }
        print(f"[Bounty fetch] No new items in {feed_url} (all posted already or empty).")
    return None
