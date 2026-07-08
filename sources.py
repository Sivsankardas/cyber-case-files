"""
Live RSS news sources. CVEs come from NVD's live API (cve_fetcher.py),
bug bounty writeups from security blog feeds (bounty_fetcher.py), breach
claims from ransomware.live's live API (breach_fetcher.py), phishing URLs
from OpenPhish (phishing_fetcher.py), threat-actor profiles from MITRE
ATT&CK (threat_actor_fetcher.py), Patch Tuesday data from MSRC
(patch_tuesday_fetcher.py), and confirmed breaches from HIBP (hibp_fetcher.py).
"""
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.cisa.gov/cybersecurity-advisories/all.xml",
]

