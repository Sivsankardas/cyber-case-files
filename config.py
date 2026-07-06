"""
Configuration for Cyber Case Files bot.
Fill these in via environment variables (recommended) or directly here.
NEVER commit real tokens to a public repo / GitHub.
"""
import os

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@your_channel_username")  # or numeric -100... id

# --- Posting schedule ---
POST_TIMES = ["09:00", "14:00", "19:00"]  # 24hr local time, 3 posts/day. Adjust as you like.
TIMEZONE = "Asia/Kolkata"

# --- Storage ---
DB_PATH = "posted_history.db"

# --- Brand ---
CHANNEL_HANDLE = "@YourChannelName"      # shown in footer
BRAND_TAG = "Team Cyronex"               # optional credit line
HASHTAGS = "#CyberSecurity #CyberCrime #InfoSec #StaySafeOnline"
