"""
Cyber Case Files -- live-only poster (text only, no images).

Usage:
    python main.py auto      -> checks EVERY category, respecting each
                                 category's own minimum gap since it last
                                 actually posted (see CATEGORY_CONFIG below)
    python main.py news      -> real-time: posts ONE news item
    python main.py cve       -> posts 3 live CVE alerts
    python main.py bounty    -> posts 3 live bug bounty disclosures
    python main.py breach    -> posts 3 live claimed breach disclosures
    python main.py phishing  -> posts 1 live active phishing alert
    python main.py threat    -> posts 1 live threat actor spotlight
    python main.py patch     -> posts Patch Tuesday summary (only once it happens)
    python main.py hibp      -> posts 1 live CONFIRMED breach (HaveIBeenPwned)
    python main.py quiz      -> posts 1 engagement quiz poll

`auto` is meant to be called every 5 minutes by cron. It does NOT post
every category every time -- it checks every category every time, but each
category is only allowed to actually POST again once `gap_minutes` has
passed since IT last posted (tracked in storage.py's category_state table,
independent of the cron interval).
"""
import sys
import datetime
import time
from datetime import timezone

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
from telegram_poster import post_to_telegram
from storage import mark_posted, get_last_post_time, set_last_post_time
from engagement import post_engagement_quiz

ITEMS_PER_RUN = 3
DELAY_BETWEEN_POSTS_SECONDS = 5


# ---------------------------------------------------------------------------
# Individual mode functions -- each returns the number of items it posted.
# ---------------------------------------------------------------------------

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


def post_phishing_single():
    item = fetch_active_phishing()
    if not item:
        print("No new active phishing alerts available right now.")
        return 0
    mark_posted(item["id"], item["domain"])
    post_to_telegram(generate_phishing_alert_post(item))
    print(f"✅ Posted phishing alert: {item['domain']}")
    return 1


def post_threat_actor_single():
    item = fetch_threat_actor_spotlight()
    if not item:
        print("No new threat actor spotlight available right now.")
        return 0
    mark_posted(item["id"], item["name"])
    post_to_telegram(generate_threat_actor_post(item))
    print(f"✅ Posted threat actor spotlight: {item['name']}")
    return 1


def post_patch_tuesday_single():
    item = fetch_patch_tuesday_summary()
    if not item:
        print("No new Patch Tuesday summary to post right now.")
        return 0
    mark_posted(item["id"], item["title"])
    post_to_telegram(generate_patch_tuesday_post(item))
    print(f"✅ Posted Patch Tuesday summary: {item['title']}")
    return 1


def post_hibp_single():
    item = fetch_confirmed_breach()
    if not item:
        print("No new confirmed breach available right now.")
        return 0
    mark_posted(item["id"], item["title"])
    post_to_telegram(generate_confirmed_breach_post(item))
    print(f"✅ Posted confirmed breach: {item['title']}")
    return 1


def post_quiz():
    posted = post_engagement_quiz()
    return 1 if posted else 0


# ---------------------------------------------------------------------------
# CATEGORY_CONFIG -- single source of truth for auto mode.
#
# gap_minutes: minimum time since this category last ACTUALLY POSTED before
#              it's allowed to post again. The cron still checks every
#              category every 5 min regardless -- this only paces posting.
# day_check:   optional function(now) -> bool. If present and it returns
#              False, the category is skipped entirely this run (used for
#              Patch Tuesday's 8th-14th window).
# ---------------------------------------------------------------------------

CATEGORY_CONFIG = {
    "news":    {"func": post_news_realtime,       "gap_minutes": 5},
    "phishing":{"func": post_phishing_single,     "gap_minutes": 10},
    "breach":  {"func": post_breach_batch,        "gap_minutes": 10},
    "bounty":  {"func": post_bounty_batch,        "gap_minutes": 10},
    "cve":     {"func": post_cve_batch,           "gap_minutes": 20},
    "hibp":    {"func": post_hibp_single,         "gap_minutes": 20},
    "threat":  {"func": post_threat_actor_single, "gap_minutes": 20},
    "patch": {
        "func": post_patch_tuesday_single,
        "gap_minutes": 60,
        "day_check": lambda now: 8 <= now.day <= 14,
    },
    "quiz":    {"func": post_quiz,                "gap_minutes": 24 * 60},
}


def _category_due(name: str, cfg: dict, now: datetime.datetime) -> bool:
    day_check = cfg.get("day_check")
    if day_check and not day_check(now):
        return False
    last = get_last_post_time(name)
    if last is None:
        return True
    elapsed_minutes = (now - last).total_seconds() / 60
    return elapsed_minutes >= cfg["gap_minutes"]


def post_auto():
    """
    Auto mode: called every 5 minutes by cron. Checks EVERY category in
    CATEGORY_CONFIG every single run. A category only actually posts if
    it's "due" -- i.e. either it's never posted before, or at least
    gap_minutes have passed since it last posted successfully. Categories
    that aren't due, or whose source has nothing new, are silently skipped
    and re-checked on the next 5-minute run.
    """
    now = datetime.datetime.now(timezone.utc)
    total_posted = 0

    for name, cfg in CATEGORY_CONFIG.items():
        if not _category_due(name, cfg, now):
            continue

        print(f"[auto] Checking category '{name}'...")
        posted = cfg["func"]()

        if posted:
            set_last_post_time(name, now)
            total_posted += posted
        else:
            print(f"[auto] Nothing new for '{name}' this run.")

    if total_posted == 0:
        print("[auto] Nothing posted this cycle across any category.")

    return total_posted


MODES = {
    "news": post_news_realtime,
    "cve": post_cve_batch,
    "bounty": post_bounty_batch,
    "breach": post_breach_batch,
    "phishing": post_phishing_single,
    "threat": post_threat_actor_single,
    "patch": post_patch_tuesday_single,
    "hibp": post_hibp_single,
    "quiz": post_quiz,
    "auto": post_auto,
}

# Aliases so slightly different mode names (e.g. in the workflow file's
# workflow_dispatch dropdown) still resolve to the right mode.
MODE_ALIASES = {
    "threat_actor": "threat",
    "threatactor": "threat",
    "patch_tuesday": "patch",
    "patchtuesday": "patch",
    "hibp_breach": "hibp",
    "confirmed_breach": "hibp",
    "leaked_creds": "hibp",
    "breach_claim": "breach",
    "phish": "phishing",
    "bug_bounty": "bounty",
    "bugbounty": "bounty",
}


def run_once():
    if len(sys.argv) < 2:
        print(f"Usage: python main.py [{'|'.join(MODES.keys())}]")
        sys.exit(1)

    mode = sys.argv[1]
    mode = MODE_ALIASES.get(mode, mode)  # normalize alias -> real mode name

    if mode not in MODES:
        print(f"Usage: python main.py [{'|'.join(MODES.keys())}]")
        sys.exit(1)

    print(f"[{datetime.datetime.now()}] Running mode: {mode}")
    posted_count = MODES[mode]()
    print(f"Done. Posted {posted_count} item(s) in '{mode}' mode.")


if __name__ == "__main__":
    run_once()
