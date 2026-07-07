"""
Live ransomware/extortion group breach claims, pulled from ransomware.live's
public API. Tracks what groups themselves post publicly on their leak
sites -- does not host or distribute leaked data. Claims are unverified
by definition until the victim organization confirms.
"""
import requests
from storage import make_id, already_posted

API_URL = "https://api.ransomware.live/v2/recentvictims"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}


def fetch_recent_breach_claim():
    try:
        resp = requests.get(API_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        victims = resp.json()
    except Exception as e:
        print(f"[Breach fetch error] {e}")
        return None

    for v in victims:
        victim_name = (v.get("victim") or "").strip()
        group = (v.get("group") or "Unknown").strip()
        if not victim_name:
            continue

        item_id = make_id(f"{victim_name}|{group}", v.get("attackdate", ""))
        if already_posted(item_id):
            continue

        press = v.get("press") or []
        link = press[0] if press else f"https://www.ransomware.live/group/{group.lower()}"

        return {
            "id": item_id,
            "victim": victim_name,
            "group": group,
            "country": v.get("country", "N/A"),
            "sector": v.get("sector", "Not disclosed"),
            "observed": v.get("attackdate", v.get("discovered", "N/A")),
            "link": link,
        }
    return None
