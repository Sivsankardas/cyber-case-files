"""
Live phishing/scam alert of the day, from OpenPhish's free community feed
(no API key required, updated roughly every 15 minutes).
https://openphish.com/feed.txt
"""
import requests
import random
from urllib.parse import urlparse
from storage import make_id, already_posted

FEED_URL = "https://openphish.com/feed.txt"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}

def _defang(url: str) -> str:
    """
    Never post a live, clickable phishing link. Defanging (hxxp / [.]) is
    the standard threat-intel practice: humans can still read it, but it
    won't render as a clickable link and can't be copy-pasted into a
    browser by accident.
    """
    defanged = url.replace("https://", "hxxps://").replace("http://", "hxxp://")
    defanged = defanged.replace(".", "[.]")
    return defanged

def fetch_phishing_alert():
    try:
        resp = requests.get(FEED_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"[Phishing feed error] {e}")
        return None

    lines = [l.strip() for l in resp.text.splitlines() if l.strip()]
    if not lines:
        print("[Phishing fetch] Feed returned no entries.")
        return None

    random.shuffle(lines)
    for url in lines:
        item_id = make_id(url, "openphish")
        if already_posted(item_id):
            continue
        try:
            domain = urlparse(url).netloc or "unknown"
        except Exception:
            domain = "unknown"
        return {
            "id": item_id,
            "url": url,
            "domain": domain,
            "defanged_url": _defang(url),
            "source": "OpenPhish",
        }
    print("[Phishing fetch] No new (undeduped) entries right now.")
    return None
