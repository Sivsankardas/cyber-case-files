"""
Live malware / threat-actor spotlight.

Primary source: MITRE ATT&CK's public Enterprise ATT&CK STIX bundle
(no API key, no signup). We pull "intrusion-set" objects (APT/threat-actor
groups) and "malware" objects straight from MITRE's own GitHub-hosted data.

Secondary/optional source: AlienVault OTX pulses, used only if OTX_API_KEY
is set (free account required, https://otx.alienvault.com/api).
"""
import requests
import random
from storage import make_id, already_posted
from config import OTX_API_KEY
from freshness import parse_iso, humanize_age

MITRE_ATTACK_URL = (
    "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/"
    "enterprise-attack/enterprise-attack.json"
)
OTX_PULSES_URL = "https://otx.alienvault.com/api/v1/pulses/subscribed"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}

_cache = {"objects": None}


def _load_mitre_objects():
    if _cache["objects"] is not None:
        return _cache["objects"]
    try:
        resp = requests.get(MITRE_ATTACK_URL, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        bundle = resp.json()
        objects = [
            o for o in bundle.get("objects", [])
            if o.get("type") == "intrusion-set" and not o.get("revoked") and not o.get("x_mitre_deprecated")
        ]
        _cache["objects"] = objects
        return objects
    except Exception as e:
        print(f"[MITRE ATT&CK fetch error] {e}")
        return []


def _from_mitre():
    groups = _load_mitre_objects()
    if not groups:
        return None
    random.shuffle(groups)
    for g in groups:
        name = g.get("name", "").strip()
        if not name:
            continue
        item_id = make_id(name, "mitre-attack")
        if already_posted(item_id):
            continue
        description = (g.get("description") or "").strip().split("\n")[0][:600]
        aliases = g.get("aliases", []) or []
        ext_refs = g.get("external_references", []) or []
        link = next((r.get("url") for r in ext_refs if r.get("source_name") == "mitre-attack"), None)
        if not link:
            attack_id = next((r.get("external_id") for r in ext_refs if r.get("source_name") == "mitre-attack"), None)
            link = f"https://attack.mitre.org/groups/{attack_id}/" if attack_id else "https://attack.mitre.org/groups/"
        return {
            "id": item_id,
            "name": name,
            "aliases": aliases,
            "description": description or "No public description available.",
            "link": link,
            "source": "MITRE ATT&CK",
            "freshness": humanize_age(parse_iso(g.get("modified", g.get("created", "")))),
            "freshness_label": "Profile last updated",
        }
    return None


def _from_otx():
    if not OTX_API_KEY:
        return None
    try:
        resp = requests.get(
            OTX_PULSES_URL,
            headers={**HEADERS, "X-OTX-API-KEY": OTX_API_KEY},
            params={"limit": 20},
            timeout=30,
        )
        resp.raise_for_status()
        pulses = resp.json().get("results", [])
    except Exception as e:
        print(f"[OTX fetch error] {e}")
        return None
    random.shuffle(pulses)
    for p in pulses:
        name = (p.get("name") or "").strip()
        if not name:
            continue
        item_id = make_id(name, "otx")
        if already_posted(item_id):
            continue
        return {
            "id": item_id,
            "name": name,
            "aliases": p.get("tags", [])[:5],
            "description": (p.get("description") or "No description provided.")[:600],
            "link": f"https://otx.alienvault.com/pulse/{p.get('id', '')}",
            "source": "AlienVault OTX",
            "freshness": humanize_age(parse_iso(p.get("created", p.get("modified", "")))),
            "freshness_label": "Pulse published",
        }
    return None


def fetch_threat_actor_spotlight():
    return _from_mitre() or _from_otx()
