"""
Cyber Case Files — single-run poster.

Designed to be triggered by GitHub Actions on a cron schedule (100% free for
public repos, and free for private repos within the monthly minutes quota).
Each run posts exactly ONE message, then exits.

Format alternates by calendar day:
  - even days -> "case_file" (bilingual historical dossier)
  - odd days  -> "news_flash" (fresh RSS news + bilingual tip)
Falls back to a historical case if RSS feeds are unreachable/dry.
"""
import datetime

from sources import HISTORICAL_CASES, SECURITY_TIPS, BUG_BOUNTY_TIPS
from news_fetcher import fetch_fresh_news_item
from content_generator import generate_case_file_post, generate_news_flash_post, generate_bounty_tip_post
from telegram_poster import post_to_telegram
from storage import mark_posted, next_counter_value


def pick_historical_case():
    idx = next_counter_value("case_file_index")
    case_number = idx + 1
    return HISTORICAL_CASES[idx % len(HISTORICAL_CASES)], case_number


def pick_tip():
    idx = next_counter_value("tip_index")
    return SECURITY_TIPS[idx % len(SECURITY_TIPS)]


def pick_bounty_tip():
    idx = next_counter_value("bounty_tip_index")
    return BUG_BOUNTY_TIPS[idx % len(BUG_BOUNTY_TIPS)]


def run_once():
    # 3-way rotation: day 0 -> case file, day 1 -> news flash, day 2 -> bounty tip
    day_of_year = datetime.date.today().timetuple().tm_yday
    fmt = ["case_file", "news_flash", "bounty_tip"][day_of_year % 3]
    print(f"[{datetime.datetime.now()}] Running — format: {fmt}")

    if fmt == "case_file":
        case, case_number = pick_historical_case()
        post_text = generate_case_file_post(case, case_number)
    elif fmt == "bounty_tip":
        tip = pick_bounty_tip()
        post_text = generate_bounty_tip_post(tip)
    else:
        news = fetch_fresh_news_item()
        tip = pick_tip()
        if news:
            post_text = generate_news_flash_post(news, tip)
            mark_posted(news["id"], news["title"])
        else:
            print("No fresh news available, falling back to historical case.")
            case, case_number = pick_historical_case()
            post_text = generate_case_file_post(case, case_number)

    post_to_telegram(post_text)
    print("✅ Posted successfully.")


if __name__ == "__main__":
    run_once()
