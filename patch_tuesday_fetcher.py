"""
Live "Patch Tuesday" tracker.

Source: Microsoft's public MSRC CVRF API (https://api.msrc.microsoft.com),
no API key required for read access to monthly security update summaries.
We only want this to actually post something on/after the second Tuesday
of the month (when Patch Tuesday happens), which the workflow's cron
schedule handles -- this module just fetches and summarizes whatever the
current month's document contains.
"""
import requests
from datetime import datetime, timezone
from storage import make_id, already_posted
from freshness import parse_iso, humanize_age

MSRC_BASE = "https://api.msrc.microsoft.com/cvrf/v2.0"
HEADERS = {"Accept": "application/json", "User-Agent": "CyberCaseFiles-Bot/1.0"}


def fetch_current_patch_tuesday():
    now = datetime.now(timezone.utc)
    period = now.strftime("%Y-%b")  # e.g. "2026-Jul"
    url = f"{MSRC_BASE}/document/{period}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        doc = resp.json()
    except Exception as e:
        print(f"[MSRC fetch error] {e}")
        return None

    item_id = make_id(period, "msrc-patch-tuesday")
    if already_posted(item_id):
        return None

    vulnerabilities = doc.get("Vulnerability", []) or []
    total_cves = len(vulnerabilities)

    severity_counts = {"Critical": 0, "Important": 0, "Moderate": 0, "Low": 0}
    for v in vulnerabilities:
        for threat in v.get("Threats", []):
            desc = (threat.get("Description", {}) or {}).get("Value", "")
            if desc in severity_counts:
                severity_counts[desc] += 1

    exploited = 0
    for v in vulnerabilities:
        for threat in v.get("Threats", []):
            if threat.get("Type") == 1:  # Exploit Status
                desc = (threat.get("Description", {}) or {}).get("Value", "") or ""
                if "Exploited:Yes" in desc:
                    exploited += 1
                    break

    title = (doc.get("DocumentTitle", {}) or {}).get("Value", f"Security Updates {period}")
    tracking = doc.get("DocumentTracking", {}) or {}
    initial_release = (tracking.get("InitialReleaseDate") or "")

    return {
        "id": item_id,
        "period": period,
        "title": title,
        "total_cves": total_cves,
        "critical": severity_counts["Critical"],
        "important": severity_counts["Important"],
        "moderate": severity_counts["Moderate"],
        "low": severity_counts["Low"],
        "exploited_in_wild": exploited,
        "link": "https://msrc.microsoft.com/update-guide/",
        "freshness": humanize_age(parse_iso(initial_release)),
    }
