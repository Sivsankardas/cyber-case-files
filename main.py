"""
Cyber Case Files — live-only poster, multi-item mode.

Usage:
    python main.py cve      -> posts 3 live CVE alerts
    python main.py news     -> posts 3 live news flashes
    python main.py bounty   -> posts 3 live bug bounty disclosures

Designed to be triggered by GitHub Actions at three different times of day,
each with a different mode, so the channel gets a themed batch per time slot
instead of one random pick per day.
"""
import sys
import time
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

ITEMS_PER_RUN = 3
DELAY_BETWEEN_POSTS_SECONDS = 5  # be gentle on Telegram's rate limits


def post_news_batch(count=ITEMS_PER_RUN):
    posted = 0
    attempts = 0
    while posted < count and attempts < count * 4:
        attempts += 1
        item = fetch_fresh_news_item()
        if not item:
            print("No more fresh news items available right now.")
            break
        mark_posted(item["id"], item["title"])
        post_to_telegram(generate_news_flash_post(item))
        posted += 1
        print(f"✅ Posted news {posted}/{count}: {item['title']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


def post_cve_batch(count=ITEMS_PER_RUN):
    posted = 0
    attempts = 0
    while posted < count and attempts < count * 4:
        attempts += 1
        cve = fetch_recent_cve()
        if not cve:
            print("No more fresh CVEs available right now.")
            break
        mark_posted(cve["id"], cve["cve_id"])
        post_to_telegram(generate_cve_alert_post(cve))
        posted += 1
        print(f"✅ Posted CVE {posted}/{count}: {cve['cve_id']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


def post_bounty_batch(count=ITEMS_PER_RUN):
    posted = 0
    attempts = 0
    while posted < count and attempts < count * 4:
        attempts += 1
        report = fetch_recent_disclosure()
        if not report:
            print("No more fresh bug bounty disclosures available right now.")
            break
        mark_posted(report["id"], report["title"])
        post_to_telegram(generate_bounty_disclosure_post(report))
        posted += 1
        print(f"✅ Posted bounty disclosure {posted}/{count}: {report['title']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


MODES = {
    "news": post_news_batch,
    "cve": post_cve_batch,
    "bounty": post_bounty_batch,
}


def run_once():
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        print("Usage: python main.py [news|cve|bounty]")
        sys.exit(1)

    mode = sys.argv[1]
    print(f"[{datetime.datetime.now()}] Running mode: {mode}")
    posted_count = MODES[mode]()
    print(f"Done. Posted {posted_count} item(s) in '{mode}' mode.")


if __name__ == "__main__":
    run_once()
