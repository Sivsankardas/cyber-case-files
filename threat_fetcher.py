"""
Live malware family / APT (threat actor) spotlight, pulled from AlienVault
OTX's pulse feed. Requires a free OTX_API_KEY (sign up at
https://otx.alienvault.com/api -- Settings -> API Integration).

If no key is configured, this returns None so main.py's fallback logic
kicks in instead of crashing the run.
"""
import requests
import random
from storage import make_id, already_posted
from config import OTX_API_KEY

OTX_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"

def fetch_threat_spotlight():
    if not OTX_API_KEY:
        print("[Threat fetch] OTX_API_KEY not set -- skipping. "
              "Get a free key at https://otx.alienvault.com/api")
        return None

    headers = {"X-OTX-API-KEY": OTX_API_KEY, "User-Agent": "CyberCaseFiles-Bot/1.0"}
    try:
        resp = requests.get(OTX_URL, headers=headers, params={"limit": 30}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[Threat fetch error] {e}")
        return None

    pulses = data.get("results", [])
    random.shuffle(pulses)
    for pulse in pulses:
        name = (pulse.get("name") or "").strip()
        pulse_id = pulse.get("id", "")
        if not name or not pulse_id:
            continue
        item_id = make_id(name, pulse_id)
        if already_posted(item_id):
            continue

        tags = pulse.get("tags", []) or []
        malware_families = pulse.get("malware_families", []) or []
        adversary = pulse.get("adversary", "") or "Unknown / unattributed"
        description = (pulse.get("description") or "").strip()[:500]

        return {
            "id": item_id,
            "name": name,
            "adversary": adversary,
            "malware_families": ", ".join(malware_families) if malware_families else "Not specified",
            "tags": ", ".join(tags[:6]) if tags else "N/A",
            "description": description or "No description provided by source.",
            "link": f"https://otx.alienvault.com/pulse/{pulse_id}",
        }
    print("[Threat fetch] No new (undeduped) pulses right now.")
    return None
