"""
Live RSS news sources. CVEs come from NVD's live API (cve_fetcher.py),
bug bounty writeups from security blog feeds (bounty_fetcher.py), breach
claims from ransomware.live (breach_fetcher.py), confirmed breaches from
HIBP (leaked_creds_fetcher.py), phishing domains from OpenPhish
(phishing_fetcher.py), and malware/APT pulses from AlienVault OTX
(threat_fetcher.py).
"""
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.cisa.gov/cybersecurity-advisories/all.xml",
]
