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
import random
import datetime

from sources import HISTORICAL_CASES, SECURITY_TIPS
from news_fetcher import fetch_fresh_news_item
from content_generator import generate_case_file_post, generate_news_flash_post
from telegram_poster import post_to_telegram
from storage import mark_posted


def pick_historical_case():
    # Rotate deterministically through the pool based on day-of-year so it
    # cycles predictably instead of repeating randomly.
    day_index = datetime.date.today().timetuple().tm_yday
    return HISTORICAL_CASES[day_index % len(HISTORICAL_CASES)]


def run_once():
    today_is_even = datetime.date.today().day % 2 == 0
    fmt = "case_file" if today_is_even else "news_flash"
    print(f"[{datetime.datetime.now()}] Running — format: {fmt}")

    if fmt == "case_file":
        case = pick_historical_case()
        post_text = generate_case_file_post(case)
    else:
        news = fetch_fresh_news_item()
        tip = random.choice(SECURITY_TIPS)
        if news:
            post_text = generate_news_flash_post(news, tip)
            mark_posted(news["id"], news["title"])
        else:
            print("No fresh news available, falling back to historical case.")
            case = pick_historical_case()
            post_text = generate_case_file_post(case)

    post_to_telegram(post_text)
    print("✅ Posted successfully.")


if __name__ == "__main__":
    run_once()
