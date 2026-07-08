"""
Cyber Case Files -- live-only poster with images.

Usage:
    python main.py news      -> real-time: posts ONE news item (image + text)
    python main.py cve       -> posts 3 live CVE alerts
    python main.py bounty    -> posts 3 live bug bounty disclosures
    python main.py breach    -> posts 3 live claimed breach disclosures
    python main.py phishing  -> posts 1 live active phishing alert
    python main.py threat    -> posts 1 live threat actor spotlight (needs OTX_API_KEY)
    python main.py patch     -> posts Patch Tuesday summary (only once it happens)
    python main.py hibp      -> posts 1 live CONFIRMED breach (HaveIBeenPwned)
"""
import sys
import time
import datetime

from news_fetcher import fetch_fresh_news_item
from cve_fetcher import fetch_recent_cve
from bounty_fetcher import fetch_recent_disclosure
from breach_fetcher import fetch_recent_breach_claim
from phishing_fetcher import fetch_active_phishing
from threat_actor_fetcher import fetch_threat_actor_spotlight
from patch_tuesday_fetcher import fetch_patch_tuesday_summary
from hibp_fetcher import fetch_confirmed_breach
from content_generator import (
    generate_news_flash_post,
    generate_cve_alert_post,
    generate_bounty_disclosure_post,
    generate_breach_claim_post,
    generate_phishing_alert_post,
    generate_threat_actor_post,
    generate_patch_tuesday_post,
    generate_confirmed_breach_post,
)
from telegram_poster import send_post
from storage import mark_posted
from image_helper import resolve_image

ITEMS_PER_RUN = 3
DELAY_BETWEEN_POSTS_SECONDS = 5


def post_news_realtime():
    item = fetch_fresh_news_item()
    if not item:
        print("No live/fresh news right now -- skipping this run.")
        return 0
    mark_posted(item["id"], item["title"])
    image = resolve_image(url=item.get("link"))
    send_post(generate_news_flash_post(item), image_url=image)
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
        send_post(generate_cve_alert_post(cve))
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
        image = resolve_image(url=report.get("link"))
        send_post(generate_bounty_disclosure_post(report), image_url=image)
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
        image = resolve_image(url=item.get("link"))
        send_post(generate_breach_claim_post(item), image_url=image)
        posted += 1
        print(f"✅ Posted breach claim {posted}/{count}: {item['victim']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


def post_phishing_single():
    item = fetch_active_phishing()
    if not item:
        print("No new active phishing alerts available right now.")
        return 0
    mark_posted(item["id"], item["domain"])
    send_post(generate_phishing_alert_post(item))
    print(f"✅ Posted phishing alert: {item['domain']}")
    return 1


def post_threat_actor_single():
    item = fetch_threat_actor_spotlight()
    if not item:
        print("No new threat actor spotlight available right now.")
        return 0
    mark_posted(item["id"], item["name"])
    send_post(generate_threat_actor_post(item))
    print(f"✅ Posted threat actor spotlight: {item['name']}")
    return 1


def post_patch_tuesday_single():
    item = fetch_patch_tuesday_summary()
    if not item:
        print("No new Patch Tuesday summary to post right now.")
        return 0
    mark_posted(item["id"], item["title"])
    send_post(generate_patch_tuesday_post(item))
    print(f"✅ Posted Patch Tuesday summary: {item['title']}")
    return 1


def post_hibp_single():
    item = fetch_confirmed_breach()
    if not item:
        print("No new confirmed breach available right now.")
        return 0
    mark_posted(item["id"], item["title"])
    send_post(generate_confirmed_breach_post(item))
    print(f"✅ Posted confirmed breach: {item['title']}")
    return 1


MODES = {
    "news": post_news_realtime,
    "cve": post_cve_batch,
    "bounty": post_bounty_batch,
    "breach": post_breach_batch,
    "phishing": post_phishing_single,
    "threat": post_threat_actor_single,
    "patch": post_patch_tuesday_single,
    "hibp": post_hibp_single,
}


def run_once():
    if len(sys.argv) < 2 or sys.argv[1] not in MODES:
        print(f"Usage: python main.py [{'|'.join(MODES.keys())}]")
        sys.exit(1)

    mode = sys.argv[1]
    print(f"[{datetime.datetime.now()}] Running mode: {mode}")
    posted_count = MODES[mode]()
    print(f"Done. Posted {posted_count} item(s) in '{mode}' mode.")


if __name__ == "__main__":
    run_once()
