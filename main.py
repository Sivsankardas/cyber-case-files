"""
Cyber Case Files — LIVE-ONLY poster.

Every run fetches fresh, real data at that moment:
  - "news"   -> live RSS from cybersecurity news outlets
  - "cve"    -> live recently-published CVEs from NVD's public API
  - "bounty" -> live disclosed reports from HackerOne's public Hacktivity feed

No pre-written or example content is ever posted. Rotates by day-of-year,
and if the primary source for the day is unreachable or has nothing new,
falls back to trying the other two live sources in order — it will only
skip posting entirely if ALL THREE live sources fail (rare, but possible
if feeds are down or network issues occur).
"""
import datetime

from news_fetcher import fetch_fresh_news_item
from cve_fetcher import fetch_recent_cve
from bounty_fetcher import fetch_recent_disclosure
from content_generator import (
    generate_news_flash_post,
    generate_cve_alert_post,
    generate_bounty_disclosure_post,
)
from telegram_poster import post_to_telegram
from storage import mark_posted


def try_news():
    item = fetch_fresh_news_item()
    if not item:
        return None
    mark_posted(item["id"], item["title"])
    return generate_news_flash_post(item)


def try_cve():
    cve = fetch_recent_cve()
    if not cve:
        return None
    mark_posted(cve["id"], cve["cve_id"])
    return generate_cve_alert_post(cve)


def try_bounty():
    report = fetch_recent_disclosure()
    if not report:
        return None
    mark_posted(report["id"], report["title"])
    return generate_bounty_disclosure_post(report)


def run_once():
    day_of_year = datetime.date.today().timetuple().tm_yday
    order_variants = [
        [try_news, try_cve, try_bounty],
        [try_cve, try_bounty, try_news],
        [try_bounty, try_news, try_cve],
    ]
    order = order_variants[day_of_year % 3]
    names = {try_news: "news", try_cve: "cve", try_bounty: "bounty"}

    print(f"[{datetime.datetime.now()}] Today's primary source: {names[order[0]]}")

    for fn in order:
        post_text = fn()
        if post_text:
            post_to_telegram(post_text)
            print(f"✅ Posted successfully using live source: {names[fn]}")
            return

    print("⚠️ All three live sources returned nothing new or were unreachable. Skipping this run.")


if __name__ == "__main__":
    run_once()
