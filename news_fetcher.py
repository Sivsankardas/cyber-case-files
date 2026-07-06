import feedparser
import random
from sources import RSS_FEEDS
from storage import make_id, already_posted


def fetch_fresh_news_item():
    """
    Pull a random unposted entry from the configured RSS feeds.
    Returns dict {title, link, summary, source} or None if nothing new found.
    """
    feeds = RSS_FEEDS[:]
    random.shuffle(feeds)

    for feed_url in feeds:
        try:
            parsed = feedparser.parse(feed_url)
        except Exception:
            continue

        entries = parsed.entries[:15]
        random.shuffle(entries)

        for entry in entries:
            title = entry.get("title", "").strip()
            link = entry.get("link", "").strip()
            summary = entry.get("summary", "") or entry.get("description", "")
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
                "source": feed_url,
            }

    return None
