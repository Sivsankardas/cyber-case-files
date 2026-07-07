"""
Turns your own channel's post history into a standard RSS 2.0 feed
(docs/feed.xml) so anyone can subscribe in Feedly, Inoreader, etc.
Enable free hosting by turning on GitHub Pages for the /docs folder
in your repo settings -> Pages -> Source: main branch /docs.
Your feed will then be live at:
  https://<username>.github.io/<repo>/feed.xml
"""
import html
from datetime import datetime, timezone
from email.utils import format_datetime
from storage import recent_posts
from config import RSS_FEED_PATH, RSS_FEED_TITLE, RSS_FEED_LINK, RSS_FEED_DESCRIPTION, RSS_MAX_ITEMS

def _rfc822(dt_str: str) -> str:
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
    except Exception:
        dt = datetime.now(timezone.utc)
    return format_datetime(dt)

def generate_rss():
    items = recent_posts(RSS_MAX_ITEMS)
    now = format_datetime(datetime.now(timezone.utc))

    item_xml = []
    for it in items:
        title = html.escape(it["title"] or "Untitled")
        link = html.escape(it["link"] or RSS_FEED_LINK)
        desc = html.escape((it["summary"] or "")[:500])
        pub_date = _rfc822(it["posted_at"])
        item_xml.append(f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="false">{it['id']}</guid>
      <pubDate>{pub_date}</pubDate>
      <description>{desc}</description>
    </item>""")

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{html.escape(RSS_FEED_TITLE)}</title>
    <link>{html.escape(RSS_FEED_LINK)}</link>
    <description>{html.escape(RSS_FEED_DESCRIPTION)}</description>
    <lastBuildDate>{now}</lastBuildDate>
{chr(10).join(item_xml)}
  </channel>
</rss>
"""
    with open(RSS_FEED_PATH, "w", encoding="utf-8") as f:
        f.write(feed)
    print(f"[RSS] Wrote {len(items)} items to {RSS_FEED_PATH}")
