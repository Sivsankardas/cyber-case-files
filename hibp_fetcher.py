"""
Live CONFIRMED breach fetcher using HaveIBeenPwned's public breach list
(no API key needed for this endpoint). Distinct from breach_fetcher.py,
which tracks CLAIMED leak-site posts (unverified). This only lists
breaches HIBP has verified as involving real credential data.
"""
import requests
from storage import make_id, already_posted

HIBP_URL = "https://haveibeenpwned.com/api/v3/breaches"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}


def fetch_confirmed_breach():
    try:
        resp = requests.get(HIBP_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        breaches = resp.json()
    except Exception as e:
        print(f"[HIBP fetch error] {e}")
        return None

    breaches.sort(key=lambda b: b.get("AddedDate", ""), reverse=True)

    for b in breaches[:30]:
        name = (b.get("Name") or "").strip()
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
            "data_classes": ", ".join(b.get("DataClasses", [])) or "Not specified",
            "is_verified": b.get("IsVerified", False),
            "link": f"https://haveibeenpwned.com/PwnedWebsites#{name}",
        }
    return None
