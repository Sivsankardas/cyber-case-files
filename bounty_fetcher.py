"""
Pulls real, live bug bounty write-ups and disclosed vulnerability research
from multiple active sources.
"""
import feedparser
import random
import re
from storage import make_id, already_posted

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
            }

        print(f"[Bounty fetch] No new items in {feed_url} (all posted already or empty).")
    return None
