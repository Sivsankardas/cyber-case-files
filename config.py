"""
Configuration for Cyber Case Files bot.
Fill these in via environment variables (recommended) or directly here.
NEVER commit real tokens to a public repo / GitHub.
"""
import os

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@your_channel_username")

# --- Optional keys (free tiers) ---
# NVD: https://nvd.nist.gov/developers/request-an-api-key  (raises rate limit 5/30s -> 50/30s)
NVD_API_KEY = os.environ.get("NVD_API_KEY", "")
# AlienVault OTX: https://otx.alienvault.com/api  (free account, used only as an optional
# secondary source for the threat-actor spotlight; MITRE ATT&CK is the primary, keyless source)
OTX_API_KEY = os.environ.get("OTX_API_KEY", "")

# --- Posting schedule (legacy reference; real-time news uses cron interval) ---
POST_TIMES = ["09:00", "14:00", "19:00"]
TIMEZONE = "Asia/Kolkata"

# --- Real-time news freshness window ---
FRESHNESS_WINDOW_MINUTES = 60

# --- Storage ---
DB_PATH = "posted_history.db"

# --- RSS output (your own channel, re-published as a feed others can subscribe to) ---
RSS_OUTPUT_PATH = "feed.xml"
RSS_TITLE = "Cyber Case Files — Live Threat Intel"
RSS_DESCRIPTION = "Live CVEs, breach claims, phishing alerts, malware/APT spotlights and more, auto-posted from public sources."
RSS_SELF_URL = os.environ.get("RSS_SELF_URL", "https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/feed.xml")
RSS_MAX_ITEMS = 100

# --- Brand ---
CHANNEL_HANDLE = os.environ.get("CHANNEL_HANDLE", "@your_channel_username")
BRAND_TAG = os.environ.get("BRAND_TAG", "Cyber Case Files")
HASHTAGS = os.environ.get(
    "HASHTAGS",
    "#CyberSecurity #CyberCrime #InfoSec #StaySafeOnline"
)
