"""
Live Microsoft "Patch Tuesday" summary fetcher, using MSRC's free public
CVRF API (no auth required). Only returns a summary once the current
month's Patch Tuesday has actually happened.
"""
import calendar
import requests
from datetime import datetime, timezone
from storage import make_id, already_posted

MSRC_UPDATES_URL = "https://api.msrc.microsoft.com/cvrf/v3.0/updates"
MSRC_CVRF_URL = "https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/{id}"
HEADERS = {"Accept": "application/json", "User-Agent": "CyberCaseFiles-Bot/1.0"}


def _second_tuesday(year: int, month: int) -> int:
    cal = calendar.monthcalendar(year, month)
    tuesdays = [week[calendar.TUESDAY] for week in cal if week[calendar.TUESDAY] != 0]
    return tuesdays[1]


def fetch_patch_tuesday_summary():
    now = datetime.now(timezone.utc)
    patch_day = _second_tuesday(now.year, now.month)

    if now.day < patch_day:
        print("[Patch Tuesday] Hasn't happened yet this month -- skipping.")
        return None

    id_slug = now.strftime("%Y-%b")
    item_id = make_id(id_slug, "msrc")
    if already_posted(item_id):
        return None

    try:
        resp = requests.get(MSRC_UPDATES_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[MSRC fetch error] {e}")
        return None

    matches = [v for v in data.get("value", []) if v.get("ID", "").startswith(id_slug)]
    if not matches:
        print(f"[Patch Tuesday] No MSRC release found yet for {id_slug}.")
        return None

    release = matches[0]
    release_id = release.get("ID", id_slug)

    try:
        detail_resp = requests.get(MSRC_CVRF_URL.format(id=release_id), headers=HEADERS, timeout=30)
        detail_resp.raise_for_status()
        detail = detail_resp.json()
        vuln_count = len(detail.get("Vulnerability", []))
    except Exception as e:
        print(f"[MSRC detail fetch error] {e}")
        vuln_count = "Unknown"

    return {
        "id": item_id,
        "title": release.get("DocumentTitle", f"{id_slug} Security Update"),
        "vuln_count": vuln_count,
        "link": f"https://msrc.microsoft.com/update-guide/releaseNote/{release_id}",
    }
