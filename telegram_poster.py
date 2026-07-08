import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID


def _send_message(text: str, parse_mode: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": False,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    return requests.post(url, json=payload, timeout=30)


def _send_photo(image_url: str, caption: str, parse_mode: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "photo": image_url,
        "caption": caption[:1024],
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    return requests.post(url, json=payload, timeout=30)


def post_to_telegram(text: str):
    """Plain text post, Markdown with automatic plain-text fallback."""
    if len(text) > 4090:
        text = text[:4080] + "\n…(trimmed)"
    resp = _send_message(text, "Markdown")
    if resp.status_code != 200:
        print(f"[Telegram Markdown error] {resp.status_code}: {resp.text}")
        plain_text = text.replace("*", "").replace("_", "").replace("`", "")
        resp = _send_message(plain_text, None)
    if resp.status_code != 200:
        print(f"[Telegram plain-text error] {resp.status_code}: {resp.text}")
    resp.raise_for_status()
    return resp.json()


def send_post(text: str, image_url: str = None):
    """
    Posts an image + the full rich text as one attractive post whenever an
    image is available: the image goes out first (no caption, since
    captions are capped at 1024 chars and our posts are longer/richer than
    that), immediately followed by the full formatted text message. Falls
    back to a text-only post if no image was found or the image fails to
    send (e.g. dead/blocked URL).
    """
    if image_url:
        try:
            photo_resp = _send_photo(image_url, "", None)
            if photo_resp.status_code != 200:
                print(f"[Telegram photo error] {photo_resp.status_code}: {photo_resp.text}")
        except Exception as e:
            print(f"[Telegram photo send failed] {e}")
    return post_to_telegram(text)


def send_poll(question: str, options: list, correct_option_id: int, is_anonymous: bool = True):
    """
    Posts a Telegram quiz-style poll (type='quiz'), which shows a correct
    answer and auto-explains once someone votes. Telegram limits: question
    <= 300 chars, each option <= 100 chars, 2-10 options per poll.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPoll"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "question": question[:300],
        "options": [str(opt)[:100] for opt in options],
        "type": "quiz",
        "correct_option_id": correct_option_id,
        "is_anonymous": is_anonymous,
    }
    resp = requests.post(url, json=payload, timeout=30)
    if resp.status_code != 200:
        print(f"[Telegram poll error] {resp.status_code}: {resp.text}")
    resp.raise_for_status()
    return resp.json()
