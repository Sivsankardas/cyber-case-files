"""
Live RSS news sources. This is the only "source list" left in the project —
CVEs come from NVD's live API (cve_fetcher.py) and bug bounty disclosures
come from HackerOne's live Hacktivity feed (bounty_fetcher.py). No static
or pre-written content exists anywhere in this project anymore.
"""

RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://www.darkreading.com/rss.xml",
    "https://www.cisa.gov/cybersecurity-advisories/all.xml",
]
