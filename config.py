"""
Configuration for Cyber Case Files bot.
Fill these in via environment variables (recommended) or directly here.
NEVER commit real tokens to a public repo / GitHub.
"""
import os

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@your_channel_username")

# --- Optional API keys (free tiers) ---
# NVD: raises rate limit from ~5/30s to ~50/30s. Get one free at
#      https://nvd.nist.gov/developers/request-an-api-key
NVD_API_KEY = os.environ.get("NVD_API_KEY", "")
# AlienVault OTX: required for the threat-actor/malware spotlight feature.
#      Free account + key at https://otx.alienvault.com/api
OTX_API_KEY = os.environ.get("OTX_API_KEY", "")

# --- Posting schedule (legacy reference; real-time news uses cron interval) ---
POST_TIMES = ["09:00", "14:00", "19:00"]
TIMEZONE = "Asia/Kolkata"

# --- Real-time news freshness window ---
FRESHNESS_WINDOW_MINUTES = 60

# --- Storage ---
DB_PATH = "posted_history.db"

# --- RSS output (your own channel as a subscribable feed) ---
RSS_FEED_PATH = "docs/feed.xml"
RSS_FEED_TITLE = "Cyber Case Files — Live Threat Intel"
RSS_FEED_LINK = "https://t.me/WH04M1Intel"
RSS_FEED_DESCRIPTION = "Live CVEs, phishing alerts, breach claims, malware/APT spotlights and more."
RSS_MAX_ITEMS = 60

# --- Brand ---
CHANNEL_HANDLE = "@WH04M1Intel"
BRAND_TAG = "TEAM WH04M1"
HASHTAGS = "#CyberSecurity #CyberCrime #InfoSec #StaySafeOnline"
ENGAGEMENT_CTA = "💬 React & forward if this helped you stay safe!"
