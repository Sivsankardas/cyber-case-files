import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID


def post_to_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    if len(text) > 4090:
        text = text[:4080] + "\n…(trimmed)"

    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code != 200:
        print(f"[Telegram error] {resp.status_code}: {resp.text}")
    resp.raise_for_status()
    return resp.json()
