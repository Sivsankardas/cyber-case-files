"""
Microsoft "Patch Tuesday" tracker -- pulled live from Microsoft's own
MSRC CVRF API (free, no key required). Auto-detects the latest monthly
security update release and only posts once per month (dedup by release ID).
"""
import requests
from storage import make_id, already_posted

UPDATES_URL = "https://api.msrc.microsoft.com/cvrf/v3.0/updates"
DETAIL_URL = "https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/{id}"
HEADERS = {"Accept": "application/json", "User-Agent": "CyberCaseFiles-Bot/1.0"}

def fetch_latest_patch_tuesday():
    try:
        resp = requests.get(UPDATES_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[Patch Tuesday fetch error] {e}")
        return None

    values = data.get("value", [])
    if not values:
        return None

    # Most recent release is last in the list
    latest = values[-1]
    release_id = latest.get("ID", "")
    title = latest.get("DocumentTitle", "").strip()
    if not release_id:
        return None

    item_id = make_id(release_id, "msrc")
    if already_posted(item_id):
        print(f"[Patch Tuesday] {release_id} already posted this cycle.")
        return None

    cve_count = "Unknown"
    try:
        detail_resp = requests.get(DETAIL_URL.format(id=release_id), headers=HEADERS, timeout=30)
        detail_resp.raise_for_status()
        detail = detail_resp.json()
        vulns = detail.get("Vulnerability", [])
        cve_count = len(vulns)
    except Exception as e:
        print(f"[Patch Tuesday detail fetch error] {e}")

    return {
        "id": item_id,
        "release_id": release_id,
        "title": title or f"Microsoft Security Update Release {release_id}",
        "cve_count": cve_count,
        "link": f"https://msrc.microsoft.com/update-guide/releaseNote/{release_id}",
    }
