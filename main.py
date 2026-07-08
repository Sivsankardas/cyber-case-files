"""
Cyber Case Files -- live-only poster.

Usage:
    python main.py auto          -> (default, used by the 10-min cron) checks
                                     EVERY category and posts whichever ones
                                     are both due (per their pacing interval
                                     below) and have genuinely new content.
    python main.py news          -> force a single real-time news check
    python main.py cve           -> force a CVE batch
    python main.py bounty        -> force a bug bounty batch
    python main.py breach        -> force a ransomware-claim batch
    python main.py phishing      -> force a phishing/scam alert check
    python main.py threat_actor  -> force a threat-actor spotlight check
    python main.py patch_tuesday -> force a Patch Tuesday check
    python main.py leaked_creds  -> force a HIBP confirmed-breach check
    python main.py quiz          -> force an engagement quiz poll

Forced single-mode runs (anything but `auto`) ignore the pacing interval --
that's what workflow_dispatch uses so you can always trigger something
manually regardless of when it last posted.
"""
import sys
import time
import datetime as dt

from news_fetcher import fetch_fresh_news_item
from cve_fetcher import fetch_recent_cve
from bounty_fetcher import fetch_recent_disclosure
from breach_fetcher import fetch_recent_breach_claim
from phishing_fetcher import fetch_active_phishing_url
from threat_actor_fetcher import fetch_threat_actor_spotlight
from patch_tuesday_fetcher import fetch_current_patch_tuesday
from hibp_fetcher import fetch_confirmed_breach

from content_generator import (
    generate_news_flash_post,
    generate_cve_alert_post,
    generate_bounty_disclosure_post,
    generate_breach_claim_post,
    generate_phishing_alert_post,
    generate_threat_actor_post,
    generate_patch_tuesday_post,
    generate_hibp_breach_post,
)
from telegram_poster import post_to_telegram
from storage import mark_posted, add_channel_post, get_last_post_time, set_last_post_time
from rss_generator import regenerate_feed
from engagement import post_engagement_quiz

ITEMS_PER_RUN = 3
DELAY_BETWEEN_POSTS_SECONDS = 5


def _record(item_id, title, link, description, category):
    mark_posted(item_id, title)
    add_channel_post(item_id, title, link, description, category)


def post_news_realtime():
    item = fetch_fresh_news_item()
    if not item:
        print("No live/fresh news right now -- skipping this run.")
        return 0
    _record(item["id"], item["title"], item["link"], item.get("summary", ""), "news")
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
        _record(cve["id"], cve["cve_id"], cve["link"], cve["description"], "cve")
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
        _record(report["id"], report["title"], report["link"], report["summary"], "bounty")
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
        _record(item["id"], item["victim"], item["link"], f"Claimed by {item['group']}", "breach_claim")
        post_to_telegram(generate_breach_claim_post(item))
        posted += 1
        print(f"✅ Posted breach claim {posted}/{count}: {item['victim']}")
        if posted < count:
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)
    return posted


def post_phishing_alert():
    item = fetch_active_phishing_url()
    if not item:
        print("No new active phishing URLs right now.")
        return 0
    _record(item["id"], item["domain"], item["link"], f"Impersonates: {item['impersonates']}", "phishing")
    post_to_telegram(generate_phishing_alert_post(item))
    print(f"✅ Posted phishing alert: {item['domain']}")
    return 1


def post_threat_actor_spotlight():
    actor = fetch_threat_actor_spotlight()
    if not actor:
        print("No new threat-actor profiles available right now.")
        return 0
    _record(actor["id"], actor["name"], actor["link"], actor["description"], "threat_actor")
    post_to_telegram(generate_threat_actor_post(actor))
    print(f"✅ Posted threat actor spotlight: {actor['name']}")
    return 1


def post_patch_tuesday():
    patch = fetch_current_patch_tuesday()
    if not patch:
        print("No new Patch Tuesday summary available (already posted this month, or not released yet).")
        return 0
    _record(patch["id"], patch["title"], patch["link"], f"{patch['total_cves']} CVEs patched", "patch_tuesday")
    post_to_telegram(generate_patch_tuesday_post(patch))
    print(f"✅ Posted Patch Tuesday summary: {patch['period']}")
    return 1


def post_leaked_creds():
    item = fetch_confirmed_breach()
    if not item:
        print("No new confirmed breaches available right now.")
        return 0
    _record(item["id"], item["title"], item["link"], f"{item['pwn_count']} accounts affected", "leaked_creds")
    post_to_telegram(generate_hibp_breach_post(item))
    print(f"✅ Posted confirmed breach: {item['title']}")
    return 1


def post_quiz():
    return post_engagement_quiz()


# Each category's minimum gap (in minutes) between posts, so a 10-min check
# cycle doesn't flood the channel just because a source always has *something*
# new. Every category is still CHECKED every 10 min -- this only paces how
# often a check is allowed to actually publish.
CATEGORY_CONFIG = {
    "news":          {"fn": post_news_realtime,          "interval_minutes": 10},
    "phishing":      {"fn": post_phishing_alert,          "interval_minutes": 20},
    "cve":           {"fn": post_cve_batch,               "interval_minutes": 30},
    "breach":        {"fn": post_breach_batch,            "interval_minutes": 30},
    "leaked_creds":  {"fn": post_leaked_creds,            "interval_minutes": 60},
    "bounty":        {"fn": post_bounty_batch,            "interval_minutes": 60},
    "patch_tuesday": {"fn": post_patch_tuesday,           "interval_minutes": 60, "day_window": (8, 14)},
    "threat_actor":  {"fn": post_threat_actor_spotlight,  "interval_minutes": 240},
    "quiz":          {"fn": post_quiz,                    "interval_minutes": 1440},
}

MODES = {
    "news": post_news_realtime,
    "cve": post_cve_batch,
    "bounty": post_bounty_batch,
    "breach": post_breach_batch,
    "phishing": post_phishing_alert,
    "threat_actor": post_threat_actor_spotlight,
    "patch_tuesday": post_patch_tuesday,
    "leaked_creds": post_leaked_creds,
    "quiz": post_quiz,
}


def run_auto():
    """Checked every 10 minutes. Walks every category; for each one that's
    past its pacing interval (and, for patch_tuesday, in its date window),
    attempts a fetch+post. Nothing here is ever more than one check-cycle
    (10 min) away from being picked up once it's due."""
    now = dt.datetime.now(dt.timezone.utc)
    total_posted = 0
    for category, cfg in CATEGORY_CONFIG.items():
        day_window = cfg.get("day_window")
        if day_window:
            lo, hi = day_window
            if not (lo <= now.day <= hi):
                continue

        last = get_last_post_time(category)
        interval = cfg["interval_minutes"]
        if last is not None:
            elapsed_minutes = (now - last).total_seconds() / 60
            if elapsed_minutes < interval:
                continue

        try:
            count = cfg["fn"]()
        except Exception as e:
            print(f"[{category}] error during auto check: {e}")
            count = 0

        if count:
            set_last_post_time(category, now)
            total_posted += count
            time.sleep(DELAY_BETWEEN_POSTS_SECONDS)

    return total_posted


def run_once():
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"

    if mode == "auto":
        print(f"[{dt.datetime.now()}] Running auto check across all categories")
        posted_count = run_auto()
    elif mode in MODES:
        print(f"[{dt.datetime.now()}] Forcing mode: {mode}")
        posted_count = MODES[mode]()
    else:
        print(f"Usage: python main.py [auto|{'|'.join(MODES.keys())}]")
        sys.exit(1)

    if posted_count:
        regenerate_feed()
    print(f"Done. Posted {posted_count} item(s) in '{mode}' mode.")


if __name__ == "__main__":
    run_once()
