"""
Live phishing/scam alert fetcher.

Primary source: OpenPhish's free community feed (https://openphish.com/feed.txt),
a plain-text list of currently active phishing URLs, no API key required.

Note: the free OpenPhish feed gives URLs only (no metadata like target brand),
so we derive a human-readable "impersonates" guess from the domain itself where
possible, and are upfront in the post that this is an automated feed entry.
"""
import requests
import re
from urllib.parse import urlparse
from storage import make_id, already_posted
from freshness import humanize_age

OPENPHISH_FEED_URL = "https://openphish.com/feed.txt"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}


def _guess_target(url: str) -> str:
    host = urlparse(url).netloc.lower()
    brands = [
        "paypal", "amazon", "apple", "microsoft", "google", "facebook", "instagram",
        "netflix", "bankofamerica", "wellsfargo", "chase", "irs", "dhl", "fedex",
        "usps", "coinbase", "binance", "outlook", "office365", "linkedin", "whatsapp",
    ]
    for b in brands:
        if b in host:
            return b.capitalize()
    return "Unknown / unbranded"


def fetch_active_phishing_url():
    try:
        resp = requests.get(OPENPHISH_FEED_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        lines = [l.strip() for l in resp.text.splitlines() if l.strip().startswith("http")]
    except Exception as e:
        print(f"[Phishing fetch error] {e}")
        return None

    for url in lines:
        item_id = make_id(url, "openphish")
        if already_posted(item_id):
            continue
        domain = urlparse(url).netloc
        return {
            "id": item_id,
            "url": url,
            "domain": domain,
            "impersonates": _guess_target(url),
            "link": url,
            "freshness": humanize_age(None),  # OpenPhish's free feed doesn't expose a per-URL timestamp
        }
    return None
