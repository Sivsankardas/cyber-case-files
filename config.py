"""
Configuration for Cyber Case Files bot.
Fill these in via environment variables (recommended) or directly here.
NEVER commit real tokens to a public repo / GitHub.
"""
import os

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@your_channel_username")

# --- Posting schedule (legacy reference; real-time news uses cron interval) ---
POST_TIMES = ["09:00", "14:00", "19:00"]
TIMEZONE = "Asia/Kolkata"

# --- Real-time news freshness window ---
FRESHNESS_WINDOW_MINUTES = 60

# --- Storage ---
DB_PATH = "posted_history.db"

# --- Brand ---
CHANNEL_HANDLE = "@WH04M1Intel"
BRAND_TAG = "TEAM WH04M1"
HASHTAGS = "#CyberSecurity #CyberCrime #InfoSec #StaySafeOnline"
