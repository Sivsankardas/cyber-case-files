# Cyber Case Files — Live-Only, Free, Always-On Telegram Bot

Every post is fetched fresh, live, at the moment it posts. Nothing is
pre-written or example content anymore.

## What it posts (rotates by day)

- **News Flash** — a real, current story pulled from live RSS feeds
  (The Hacker News, BleepingComputer, Krebs on Security, Dark Reading, CISA)
- **Live CVE Alert** — a real vulnerability disclosed in the last 7 days,
  pulled directly from NVD's (National Vulnerability Database) public API,
  with actual CVSS severity/score
- **Live Bug Bounty Disclosure** — a real, publicly disclosed report from
  HackerOne's Hacktivity feed — actual researchers, actual programs, actual bugs

If today's primary source has nothing new or is temporarily unreachable,
it automatically tries the other two live sources before giving up — it
will only skip a run if all three live feeds fail at once (rare).

## Why some text stays in English

CVE descriptions, bug bounty report titles, and news headlines are live,
factual, technical text. Auto-translating that unattended risks silently
distorting a number, a vendor name, or a technical detail — which matters
when it's real vulnerability data. So the labels/headers are bilingual,
but the live content itself stays exactly as published, with the source
link included so anyone can verify directly.

## Setup

Same as before — nothing changes in the setup process:

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHANNEL_ID="@WH04M1Intel"
python main.py
```

For automatic daily posting, this runs via GitHub Actions
(`.github/workflows/post.yml`) on the same free schedule as before —
no server, no cost.

## Files

- `main.py` — orchestrates the daily rotation and fallback logic
- `news_fetcher.py` — live RSS fetching
- `cve_fetcher.py` — live NVD CVE API fetching
- `bounty_fetcher.py` — live HackerOne Hacktivity feed fetching
- `content_generator.py` — pure formatting templates (no invented content)
- `storage.py` — dedup tracking so the same story/CVE/report never repeats
- `telegram_poster.py` — posts the final message to your channel

## Notes

- NVD's API occasionally rate-limits unauthenticated requests during high
  traffic. If a run shows a CVE fetch error in the Actions log, it's usually
  temporary — the fallback to news/bounty sources covers this automatically.
- HackerOne's Hacktivity feed only includes reports that were disclosed
  *with the program's permission* — this is intentionally public educational
  content, not a leak of anything private.
