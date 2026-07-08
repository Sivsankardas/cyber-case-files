"""
Confirmed (not claimed) data breach fetcher.

Source: HaveIBeenPwned's public /breaches endpoint, which lists breaches
HIBP has verified and loaded -- no API key required for this endpoint
(only the per-email breach search requires a paid key). This is distinct
from breach_fetcher.py, which tracks unverified ransomware-group claims.
"""
import requests
from storage import make_id, already_posted
from freshness import parse_iso, humanize_age

HIBP_BREACHES_URL = "https://haveibeenpwned.com/api/v3/breaches"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}


def fetch_confirmed_breach():
    try:
        resp = requests.get(HIBP_BREACHES_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        breaches = resp.json()
    except Exception as e:
        print(f"[HIBP fetch error] {e}")
        return None

    # Most recently *added* to HIBP first (not necessarily most recently occurred),
    # so the freshest confirmed entries surface first.
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
            "data_classes": b.get("DataClasses", []),
            "is_sensitive": b.get("IsSensitive", False),
            "verified": b.get("IsVerified", False),
            "link": f"https://haveibeenpwned.com/PwnedWebsites#{name}",
            "freshness": humanize_age(parse_iso(b.get("AddedDate", ""))),
        }
    return None
