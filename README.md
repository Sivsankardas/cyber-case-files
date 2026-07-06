# Cyber Case Files — 100% Free, Always-On Telegram Bot

Zero budget setup:
- No paid server (GitHub Actions runs it on a schedule, free)
- No AI API (all content is pre-written or template-generated, free)
- Only cost: your own time to set it up once

## What it posts

- **Even calendar days** → bilingual (English + Hindi) "Case File" dossier on a
  real historical cyber crime case (Mirai, WannaCry, Colonial Pipeline, etc.) — fully
  pre-written, rotates through 10 cases based on day-of-year, never repeats back-to-back.
- **Odd calendar days** → "News Flash": a fresh story pulled live from RSS
  (The Hacker News, BleepingComputer, Krebs on Security, Dark Reading, CISA) plus a
  bilingual security tip. If feeds are unreachable that day, it falls back to a case file.

## One-time setup (10-15 minutes)

### 1. Create your Telegram bot
1. Message `@BotFather` on Telegram → `/newbot` → follow prompts → copy the token.
2. Create your channel (public or private).
3. Add the bot to the channel as **Admin** with "Post Messages" permission.
4. Get your channel ID: if public, it's `@your_channel_username`. If private, forward
   any message from the channel to `@userinfobot` to get the numeric `-100...` id.

### 2. Put this code on GitHub (free)
1. Create a new **public** GitHub repo (public repos = unlimited free Actions minutes;
   private repos also work, just capped at ~2,000 free minutes/month which is more than enough
   for 3 posts/day).
2. Upload all these files to the repo, preserving the `.github/workflows/post.yml` path.

### 3. Add your secrets
In your repo: **Settings → Secrets and variables → Actions → New repository secret**
- `TELEGRAM_BOT_TOKEN` → your bot token
- `TELEGRAM_CHANNEL_ID` → your channel id/username

### 4. Done — it's live
The workflow in `.github/workflows/post.yml` runs automatically 3x/day
(~9am, 2pm, 7pm IST) forever, for free, even if your laptop is off.

To test immediately without waiting: go to your repo's **Actions** tab →
"Post to Cyber Case Files Telegram Channel" → **Run workflow** button.

## Local testing (optional, before pushing to GitHub)

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="123456:ABC-your-token"
export TELEGRAM_CHANNEL_ID="@your_channel"
python main.py
```

This posts ONE message immediately using today's format (even/odd day rule) — good
for checking formatting before relying on the schedule.

## Customizing (no cost impact)

- **Add more historical cases** → append bilingual entries to `HISTORICAL_CASES` in `sources.py`
- **Add more tips** → append to `SECURITY_TIPS` in `sources.py`
- **Add more RSS sources** → edit `RSS_FEEDS` in `sources.py`
- **Change posting times** → edit the `cron` lines in `.github/workflows/post.yml`
  (times are in UTC — IST is UTC+5:30)
- **Change hashtags/branding** → edit `config.py`

## Why the news isn't auto-translated to Hindi

Free machine translation (e.g. unofficial Google Translate wrappers) is unreliable
for factual news content — it can silently distort numbers, names, or claims, which
matters when you're reporting real cyber crime incidents. So: the historical case
files (finite, pre-written pool) are hand-translated and fully bilingual, while
live news headlines stay in English with the link included, and only the wrapper
text + security tip are bilingual. This keeps everything both free and accurate.
If you want full bilingual news later, the cheapest reliable path is a translation
API with a free tier (e.g. Google Cloud Translation free monthly quota) — that's an
easy drop-in addition to `content_generator.py` whenever you're ready.

## Limits of the free GitHub Actions approach

- Scheduled workflows can occasionally run a few minutes late during GitHub's peak
  load — not an issue for a 3x/day posting cadence.
- If a repo has zero activity for 60 days, GitHub may auto-disable scheduled
  workflows — just push any small commit or click "Run workflow" once to re-enable.
