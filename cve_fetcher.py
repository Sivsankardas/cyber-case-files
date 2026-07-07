import requests
import random
from datetime import datetime, timedelta, timezone
from storage import make_id, already_posted

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0 (+https://t.me/WH04M1Intel)"}


def fetch_recent_cve():
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)
    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": 50,
    }
    try:
        resp = requests.get(NVD_API_URL, params=params, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[NVD fetch error] {e}")
        return None

    vulns = data.get("vulnerabilities", [])
    random.shuffle(vulns)

    for item in vulns:
        cve = item.get("cve", {})
        cve_id = cve.get("id", "")
        if not cve_id:
            continue

        item_id = make_id(cve_id, "nvd")
        if already_posted(item_id):
            continue

        descriptions = cve.get("descriptions", [])
        description = next((d["value"] for d in descriptions if d.get("lang") == "en"), "")
        if not description:
            continue

        metrics = cve.get("metrics", {})
        severity, score = "Unknown", "N/A"
        for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if key in metrics and metrics[key]:
                cvss = metrics[key][0].get("cvssData", {})
                score = cvss.get("baseScore", "N/A")
                severity = metrics[key][0].get("baseSeverity", cvss.get("baseSeverity", "Unknown"))
                break

        return {
            "id": item_id,
            "cve_id": cve_id,
            "description": description,
            "severity": severity,
            "score": score,
            "link": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
        }
    return None
