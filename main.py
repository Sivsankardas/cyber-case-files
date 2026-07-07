"""
Cyber Case Files -- live-only poster.
Usage:
    python main.py news         -> real-time single news item (only if fresh)
    python main.py cve          -> posts up to 3 live CVE alerts
    python main.py bounty       -> posts up to 3 live bug bounty disclosures
    python main.py breach       -> posts up to 3 live claimed breach disclosures
    python main.py phishing     -> posts 1 live phishing/scam alert
    python main.py threat       -> posts 1 live malware/APT spotlight
    python main.py patchtuesday -> posts Microsoft's latest patch summary (no-op if already posted this month)
    python main.py leakedcreds  -> posts 1 confirmed breach (HaveIBeenPwned)
    python main.py quiz         -> posts an interactive poll built from a live CVE
"""
import sys
import datetime

from news_fetcher import fetch_fresh_news_item
from cve_fetcher import fetch_recent_cve
from bounty_fetcher import fetch_recent_disclosure
from breach_fetcher import fetch_recent_breach_claim
from phishing_fetcher import fetch_phishing_alert
from threat_fetcher import fetch_threat_spotlight
from patch_tuesday_fetcher import fetch_latest_patch_tuesday
from leaked_creds_fetcher import fetch_confirmed_breach

from content_generator import (
    generate_news_flash_post,
    generate_cve_alert_post,
    generate_bounty_disclosure_post,
    generate_breach_claim_post,
    generate_phishing_alert_post,
    generate_threat_spotlight_post,
    generate_patch_tuesday_post,
    generate_leaked_creds_post,
)
from telegram_poster import post_to_telegram
from storage import mark_posted
from rss_generator import generate_rss
from quiz_generator import post_daily_quiz

import time

ITEMS_PER_RUN = 3
DELAY_BETWEEN_POSTS_SECONDS = 5


def post_news_realtime():
    item = fetch_fresh_news_item()
    if not item:
        print("No live/fresh news right now -- skipping this run.")
        return 0
    mark_posted(item["id"], item["title"], item["link"], item.get("summary", ""))
    post_to_telegram(generate_news_flash_post(item))
    print(f"✅ Posted live news: {item['title']} ({item['age_minutes']:.1f} min old)")
    return 1


def post_cve_batch(count=ITEMS_PER_RUN):
    posted, attempts = 0, 0
    while posted < count and attempts < count * 4:
        attempts += 1
        cve = fetch_recent_cve()
        if not cve:
            print("No more fresh CVEs available right now.")
            break
        mark_posted(cve["id"], cve["cve_id"], cve["link"], cve.get("description", ""))
        post_to_telegram(generate_cve_alert_post(cve))
        posted += 1
        print(f"✅ Posted CVE {posted}/{count}: {cve['cve_id']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


def post_bounty_batch(count=ITEMS_PER_RUN):
    posted, attempts = 0, 0
    while posted < count and attempts < count * 4:
        attempts += 1
        report = fetch_recent_disclosure()
        if not report:
            print("No more fresh bug bounty disclosures available right now.")
            break
        mark_posted(report["id"], report["title"], report["link"], report.get("summary", ""))
        post_to_telegram(generate_bounty_disclosure_post(report))
        posted += 1
        print(f"✅ Posted bounty disclosure {posted}/{count}: {report['title']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


def post_breach_batch(count=ITEMS_PER_RUN):
    posted, attempts = 0, 0
    while posted < count and attempts < count * 4:
        attempts += 1
        item = fetch_recent_breach_claim()
        if not item:
            print("No more fresh breach claims available right now.")
            break
        mark_posted(item["id"], item["victim"], item["link"], item.get("sector", ""))
        post_to_telegram(generate_breach_claim_post(item))
        posted += 1
        print(f"✅ Posted breach claim {posted}/{count}: {item['victim']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


def post_phishing_alert():
    item = fetch_phishing_alert()
    if not item:
        print("No fresh phishing alert available right now.")
        return 0
    mark_posted(item["id"], item["domain"], item["defanged_url"], item.get("source", ""))
    post_to_telegram(generate_phishing_alert_post(item))
    print(f"✅ Posted phishing alert: {item['domain']}")
    return 1


def post_threat_spotlight():
    item = fetch_threat_spotlight()
    if not item:
        print("No fresh threat spotlight available right now.")
        return 0
    mark_posted(item["id"], item["name"], item["link"], item.get("description", ""))
    post_to_telegram(generate_threat_spotlight_post(item))
    print(f"✅ Posted threat spotlight: {item['name']}")
    return 1


def post_patch_tuesday():
    item = fetch_latest_patch_tuesday()
    if not item:
        print("No new Patch Tuesday release to post (or already posted this cycle).")
        return 0
    mark_posted(item["id"], item["title"], item["link"], f"{item['cve_count']} CVEs")
    post_to_telegram(generate_patch_tuesday_post(item))
    print(f"✅ Posted Patch Tuesday: {item['title']}")
    return 1


def post_leaked_creds():
    item = fetch_confirmed_breach()
    if not item:
        print("No new confirmed breach available right now.")
        return 0
    mark_posted(item["id"], item["title"], item["link"], item.get("description", ""))
    post_to_telegram(generate_leaked_creds_post(item))
    print(f"✅ Posted confirmed breach: {item['title']}")
    return 1


def post_quiz():
    return 1 if post_daily_quiz() else 0


MODES = {
    "news": post_news_realtime,
    "cve": post_cve_batch,
    "bounty": post_bounty_batch,
    "breach": post_breach_batch,
    "phishing": post_phishing_alert,
    "threat": post_threat_spotlight,
    "patchtuesday": post_patch_tuesday,
    "leakedcreds": post_leaked_creds,
    "quiz": post_quiz,
}


def run_once():
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        print(f"Usage: python main.py [{'|'.join(MODES.keys())}]")
        sys.exit(1)

    mode = sys.argv[1]
    print(f"[{datetime.datetime.now()}] Running mode: {mode}")
    posted_count = MODES[mode]()
    print(f"Done. Posted {posted_count} item(s) in '{mode}' mode.")

    # Keep the public RSS feed in sync with whatever just got posted.
    try:
        generate_rss()
    except Exception as e:
        print(f"[RSS] Failed to regenerate feed: {e}")


if __name__ == "__main__":
    run_once()
