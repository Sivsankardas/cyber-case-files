"""
Live malware / threat-actor "pulse" fetcher using AlienVault OTX (Open
Threat Exchange), a free community threat-intel platform. Requires a free
OTX_API_KEY (sign up at otx.alienvault.com, no payment). If the key isn't
set, this source is skipped -- it won't crash the bot.
"""
import os
import requests
from storage import make_id, already_posted

OTX_API_KEY = os.environ.get("OTX_API_KEY", "")
OTX_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}


def fetch_threat_actor_spotlight():
    if not OTX_API_KEY:
        print("[OTX] No OTX_API_KEY set -- skipping threat actor spotlight.")
        return None

    headers = {**HEADERS, "X-OTX-API-KEY": OTX_API_KEY}
    try:
        resp = requests.get(OTX_URL, headers=headers, params={"limit": 20}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[OTX fetch error] {e}")
        return None

    for pulse in data.get("results", []):
        name = (pulse.get("name") or "").strip()
        pulse_id = pulse.get("id", "")
        if not name or not pulse_id:
            continue

        item_id = make_id(name, pulse_id)
        if already_posted(item_id):
            continue

        malware_families = pulse.get("malware_families", []) or []
        adversary = pulse.get("adversary", "") or "Not attributed"
        industries = pulse.get("industries", []) or []
        countries = pulse.get("targeted_countries", []) or []
        description = (pulse.get("description", "") or "").strip()[:400]
        indicator_count = pulse.get("indicator_count", 0)

        return {
            "id": item_id,
            "name": name,
            "adversary": adversary,
            "malware_families": ", ".join(malware_families) if malware_families else "Not specified",
            "industries": ", ".join(industries) if industries else "Not specified",
            "targeted_countries": ", ".join(countries) if countries else "Not specified",
            "description": description,
            "indicator_count": indicator_count,
            "link": f"https://otx.alienvault.com/pulse/{pulse_id}",
        }
    return None
