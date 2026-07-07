"""
Confirmed (not claimed) data breach tracker -- pulled from Have I Been
Pwned's public breach list API. This endpoint requires no API key. This
is intentionally distinct from breach_fetcher.py (ransomware.live), which
tracks *unverified* threat-actor claims -- HIBP only lists breaches that
have been added after some verification by their team.
https://haveibeenpwned.com/API/v3#AllBreaches
"""
import requests
import re
from storage import make_id, already_posted

HIBP_URL = "https://haveibeenpwned.com/api/v3/breaches"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0 (+https://t.me/WH04M1Intel)"}

def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()

def fetch_confirmed_breach():
    try:
        resp = requests.get(HIBP_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        breaches = resp.json()
    except Exception as e:
        print(f"[HIBP fetch error] {e}")
        return None

    # Most recently added first
    breaches.sort(key=lambda b: b.get("AddedDate", ""), reverse=True)

    for b in breaches:
        name = b.get("Name", "")
        if not name:
            continue
        item_id = make_id(name, "hibp")
        if already_posted(item_id):
            continue

        return {
            "id": item_id,
            "title": b.get("Title", name),
            "domain": b.get("Domain", "N/A"),
            "breach_date": b.get("BreachDate", "N/A"),
            "added_date": b.get("AddedDate", "N/A"),
            "pwn_count": b.get("PwnCount", 0),
            "data_classes": ", ".join(b.get("DataClasses", []) or []) or "Not specified",
            "description": _strip_html(b.get("Description", ""))[:500],
            "link": f"https://haveibeenpwned.com/PwnedWebsites#{name}",
        }
    print("[HIBP fetch] No new (undeduped) breaches right now.")
    return None
