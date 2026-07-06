import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID


def _send(text: str, parse_mode: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": False,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    return requests.post(url, json=payload, timeout=30)


def post_to_telegram(text: str):
    if len(text) > 4090:
        text = text[:4080] + "\n…(trimmed)"

    resp = _send(text, "Markdown")

    if resp.status_code != 200:
        print(f"[Telegram Markdown error] {resp.status_code}: {resp.text}")
        print("Retrying as plain text so the post isn't lost...")
        plain_text = text.replace("*", "").replace("_", "").replace("`", "")
        resp = _send(plain_text, None)

    if resp.status_code != 200:
        print(f"[Telegram plain-text error] {resp.status_code}: {resp.text}")

    resp.raise_for_status()
    return resp.json()
