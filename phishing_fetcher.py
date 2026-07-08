"""
Live active-phishing fetcher. Primary source is phishunt.io's free public
API (no auth), which enriches raw phishing URLs with the impersonated
company, hosting IP/org, and detection source. Falls back to OpenPhish's
free feed.txt (bare URL list, no metadata) if phishunt is unreachable.
"""
import requests
from storage import make_id, already_posted

PHISHUNT_URL = "https://phishunt.io/api/v1/domains"
OPENPHISH_URL = "https://openphish.com/feed.txt"
HEADERS = {"User-Agent": "CyberCaseFiles-Bot/1.0"}


def _from_phishunt():
    resp = requests.get(PHISHUNT_URL, headers=HEADERS, params={"limit": 30}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    for site in data.get("results", []):
        url = (site.get("url") or "").strip()
        domain = (site.get("domain") or "").strip()
        if not url or not domain:
            continue
        item_id = make_id(domain, "phishunt")
        if already_posted(item_id):
            continue
        return {
            "id": item_id,
            "domain": domain,
            "impersonates": site.get("company") or "Unknown brand",
            "first_seen": site.get("first_seen", "N/A"),
            "country": site.get("country", "N/A"),
            "org": site.get("org", "N/A"),
            "link": url,
        }
    return None


def _from_openphish():
    resp = requests.get(OPENPHISH_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    urls = [u.strip() for u in resp.text.splitlines() if u.strip()]
    for url in urls[:30]:
        try:
            domain = url.split("/")[2]
        except IndexError:
            continue
        item_id = make_id(domain, "openphish")
        if already_posted(item_id):
            continue
        return {
            "id": item_id,
            "domain": domain,
            "impersonates": "Not specified by source",
            "first_seen": "N/A",
            "country": "N/A",
            "org": "N/A",
            "link": url,
        }
    return None


def fetch_active_phishing():
    try:
        result = _from_phishunt()
        if result:
            return result
    except Exception as e:
        print(f"[Phishunt fetch error] {e}")

    try:
        result = _from_openphish()
        if result:
            return result
    except Exception as e:
        print(f"[OpenPhish fetch error] {e}")

    return None
