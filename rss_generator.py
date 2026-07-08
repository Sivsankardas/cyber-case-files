"""
Turns our own posting history into a standard RSS 2.0 feed (feed.xml) so
anyone can subscribe to Cyber Case Files outside of Telegram.

Committed to the repo by the workflow alongside posted_history.db. To make
it publicly browsable as a real feed URL, either:
  1) enable GitHub Pages on the repo (Settings -> Pages -> serve from
     branch root), then subscribe to https://<user>.github.io/<repo>/feed.xml, or
  2) point readers at the raw file: https://raw.githubusercontent.com/<user>/<repo>/main/feed.xml
Set RSS_SELF_URL in config.py to whichever you use.
"""
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape
from storage import get_recent_channel_posts
from config import RSS_OUTPUT_PATH, RSS_TITLE, RSS_DESCRIPTION, RSS_SELF_URL, RSS_MAX_ITEMS, CHANNEL_HANDLE


def _rfc822(dt_str: str) -> str:
    try:
        dt = datetime.fromisoformat(dt_str)
    except Exception:
        dt = datetime.now(timezone.utc)
    return format_datetime(dt)


def regenerate_feed():
    posts = get_recent_channel_posts(RSS_MAX_ITEMS)
    items_xml = []
    for p in posts:
        items_xml.append(f"""
    <item>
      <title>{escape(p['title'])}</title>
      <link>{escape(p['link'] or '')}</link>
      <guid isPermaLink="false">{escape(p['link'] or p['title'])}</guid>
      <category>{escape(p['category'])}</category>
      <pubDate>{_rfc822(p['pub_date'])}</pubDate>
      <description>{escape(p['description'] or '')}</description>
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(RSS_TITLE)}</title>
    <link>https://t.me/{CHANNEL_HANDLE.lstrip('@')}</link>
    <atom:link href="{escape(RSS_SELF_URL)}" rel="self" type="application/rss+xml" />
    <description>{escape(RSS_DESCRIPTION)}</description>
    <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>{''.join(items_xml)}
  </channel>
</rss>
"""
    with open(RSS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(feed)
    print(f"[RSS] Regenerated {RSS_OUTPUT_PATH} with {len(posts)} items.")
