"""
Cyber Case Files -- live-only poster.

Usage:
    python main.py news     -> real-time mode: posts ONE news item only if
                                something was published in the last
                                FRESHNESS_WINDOW_MINUTES.
    python main.py cve      -> posts 3 live CVE alerts
    python main.py bounty   -> posts 3 live bug bounty disclosures
    python main.py breach   -> posts 3 live claimed breach disclosures
"""
import sys
import time
import datetime

from news_fetcher import fetch_fresh_news_item
from cve_fetcher import fetch_recent_cve
from bounty_fetcher import fetch_recent_disclosure
from breach_fetcher import fetch_recent_breach_claim
from content_generator import (
    generate_news_flash_post,
    generate_cve_alert_post,
    generate_bounty_disclosure_post,
    generate_breach_claim_post,
)
from telegram_poster import post_to_telegram
from storage import mark_posted

ITEMS_PER_RUN = 3
DELAY_BETWEEN_POSTS_SECONDS = 5


def post_news_realtime():
    item = fetch_fresh_news_item()
    if not item:
        print("No live/fresh news right now -- skipping this run.")
        return 0
    mark_posted(item["id"], item["title"])
    post_to_telegram(generate_news_flash_post(item))
    print(f"✅ Posted live news: {item['title']} ({item['age_minutes']:.1f} min old)")
    return 1


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


def post_breach_batch(count=ITEMS_PER_RUN):
    posted = 0
    attempts = 0
    while posted < count and attempts < count * 4:
        attempts += 1
        item = fetch_recent_breach_claim()
        if not item:
            print("No more fresh breach claims available right now.")
            break
        mark_posted(item["id"], item["victim"])
        post_to_telegram(generate_breach_claim_post(item))
        posted += 1
        print(f"✅ Posted breach claim {posted}/{count}: {item['victim']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


MODES = {
    "news": post_news_realtime,
    "cve": post_cve_batch,
    "bounty": post_bounty_batch,
    "breach": post_breach_batch,
}


def run_once():
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        print("Usage: python main.py [news|cve|bounty|breach]")
        sys.exit(1)

    mode = sys.argv[1]
    print(f"[{datetime.datetime.now()}] Running mode: {mode}")
    posted_count = MODES[mode]()
    print(f"Done. Posted {posted_count} item(s) in '{mode}' mode.")


if __name__ == "__main__":
    run_once()
