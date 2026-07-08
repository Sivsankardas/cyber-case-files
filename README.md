# Cyber Case Files — Live-Only, Free, Always-On Telegram Bot

Every post is fetched fresh, live, at the moment it posts. Nothing is
pre-written or example content (the one exception is a small rotating
awareness-quiz bank used purely for engagement polls — clearly separate
from the threat-intel content).

## Check frequency: everything, every 5 minutes

A single GitHub Actions cron (`*/5 * * * *`) runs `python main.py auto`
every 5 minutes. That one run checks **every** source below in the same
cycle. Nothing waits longer than one 5-minute check to be picked up once
it's genuinely new.

To stop that from flooding your channel — some sources (bounty writeups,
CVEs) almost always have *something* "new" available — each category has
its own minimum gap between actual posts. The check still runs every 5
min regardless; the gap only limits how often a category is *allowed* to
publish again:

| Mode            | Checked every | Min. gap between posts | Source |
|------------------|---------------|--------------------------|--------|
| `news`          | 5 min | 5 min (already freshness-gated on its own) | The Hacker News, BleepingComputer, Krebs, Dark Reading, CISA |
| `phishing`      | 5 min | 10 min | OpenPhish free feed |
| `breach`        | 5 min | 10 min | ransomware.live public API |
| `bounty`        | 5 min | 10 min | infosecwriteups, Medium tags, PortSwigger |
| `cve`           | 5 min | 20 min | NVD public API |
| `leaked_creds`  | 5 min | 20 min | HaveIBeenPwned public `/breaches` |
| `threat_actor`  | 5 min | 20 min | MITRE ATT&CK (keyless) / OTX (optional key) |
| `patch_tuesday` | 5 min, only on the 8th–14th of the month | 60 min | MSRC CVRF API |
| `quiz`          | 5 min | 24 hr | Local rotating question bank (engagement only) |

If a source has nothing genuinely new, or is temporarily unreachable, that
category is simply skipped this cycle and re-checked in 5 minutes.

Tune any gap yourself via `CATEGORY_CONFIG` in `main.py`. One rule to keep
in mind: an `interval_minutes` value below the cron interval (currently 5)
has no extra effect, since the whole script can't run more often than the
cron fires anyway.

⚠️ Running every 5 min uses roughly 2x the GitHub Actions minutes and
upstream API calls compared to every 10 min. Fine on the free tier for
public repos; worth knowing if your repo is private (Actions minutes are
metered there).

## What it posts

| Mode            | What it is |
|------------------|------------|
| `news`          | Fresh news, real-time only |
| `cve`           | Live CVE with real CVSS score + dynamic vendor/product hashtags |
| `bounty`        | Real disclosed bug bounty writeups |
| `breach`        | Unverified ransomware-group leak-site claims |
| `phishing`      | Active phishing URL (defanged before posting) |
| `threat_actor`  | APT group / malware spotlight |
| `patch_tuesday` | Monthly patch summary, auto-fires on the 2nd Tuesday |
| `leaked_creds`  | **Confirmed** breaches (distinct from the ransomware-claim feed) |
| `quiz`          | Telegram quiz poll for engagement |

If a given source has nothing new or is temporarily unreachable, that
category is simply skipped this cycle and re-checked in 5 minutes.

## What changed in this pass

**Bug fixes**
- Replaced the old multi-cron, wall-clock-guessing schedule with a single
  `*/10 * * * *` trigger running `python main.py auto`, which checks every
  category itself and paces posts via `CATEGORY_CONFIG` — this eliminates
  the original bug entirely (mode selection silently falling back to `news`
  whenever a scheduled run was delayed a few minutes), since there's no
  longer any time-based mode guessing to get wrong.
- Added `concurrency: cancel-in-progress: false` so overlapping runs queue
  instead of racing each other on `posted_history.db`.
- Added `git pull --rebase` before `git push` as a second safety net against
  non-fast-forward push failures.
- `NVD_API_KEY` support (optional secret) to raise the NVD rate limit from
  5/30s to 50/30s.
- `breach_fetcher.py`'s fallback link now URL-encodes the group name so it
  doesn't produce a broken link for groups with spaces/special characters.

**Freshness tags on every post type**
Every post now shows how old the underlying data actually is, using each
source's own real timestamp (via `freshness.py`):
- `cve` — NVD's `published` date ("📅 Published: 3 hr ago")
- `bounty` — each RSS entry's own publish timestamp
- `breach` — ransomware.live's `attackdate`/`discovered` field
- `leaked_creds` — HIBP's `AddedDate` (when HIBP verified/loaded it — shown
  alongside the original historical `BreachDate`)
- `patch_tuesday` — MSRC's `InitialReleaseDate`
- `threat_actor` — MITRE's `modified` date, labeled "Profile last updated"
  (not framed as news, since ATT&CK group profiles are maintained reference
  data, updated on MITRE's own cadence, not breaking intel)
- `phishing` — **honest exception**: OpenPhish's free feed doesn't expose a
  per-URL timestamp, so the post says so explicitly rather than faking a
  freshness figure
- `news` — already had this from the start (freshness-gated, not just tagged)

**New features**
- **Phishing/scam alerts** (OpenPhish) — active URLs are defanged
  (`hxxps://`, `[.]`) before posting so they're not clickable.
- **Threat actor / malware spotlight** (MITRE ATT&CK, keyless primary source;
  AlienVault OTX as an optional secondary source if you set `OTX_API_KEY`).
- **Patch Tuesday tracker** (MSRC), auto-fires only in the 8th–14th-of-the-month
  Tuesday window.
- **Confirmed leaked credentials alerts** (HaveIBeenPwned `/breaches`) —
  separate from the ransomware.live *claims* feed; these are breaches HIBP
  has verified and loaded.
- **Dynamic hashtags** — CVE posts now pull vendor/product from the NVD
  CPE match data and append hashtags like `#Microsoft #Windows10` automatically.
- **RSS output** — every post is recorded to a `channel_posts` table and
  `feed.xml` is regenerated after each run, so your channel is also a
  subscribable RSS feed. See "Publishing your RSS feed" below.
- **Engagement quiz polls** — a daily Telegram quiz poll (using the
  previously-unused `send_poll` function) to drive interaction; the
  question bank is local and general-awareness only, not live threat data.

## Publishing your RSS feed

`feed.xml` is committed to the repo after every run. To make it a real,
subscribable URL:

1. **Easiest**: point readers at
   `https://raw.githubusercontent.com/<you>/<repo>/main/feed.xml`
2. **Nicer URL**: enable GitHub Pages (Settings → Pages → serve from the
   `main` branch root), then use `https://<you>.github.io/<repo>/feed.xml`

Set `RSS_SELF_URL` in `config.py` to whichever URL you use.

## Setup

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHANNEL_ID="@WH04M1Intel"
python main.py auto   # checks all categories once, same as the 5-min cron does
# or force a single category regardless of pacing: python main.py news
```

Optional secrets (repo Settings → Secrets → Actions):
- `NVD_API_KEY` — free at https://nvd.nist.gov/developers/request-an-api-key
- `OTX_API_KEY` — free at https://otx.alienvault.com/api (only used as a
  secondary source for `threat_actor`; MITRE ATT&CK works with no key at all)

Automatic posting runs via GitHub Actions
(`.github/workflows/post.yml`) — no server, no cost.

## Files

- `main.py` — orchestrates rotation, fallback logic, and RSS regeneration
- `news_fetcher.py` / `cve_fetcher.py` / `bounty_fetcher.py` / `breach_fetcher.py`
  / `phishing_fetcher.py` / `threat_actor_fetcher.py` / `patch_tuesday_fetcher.py`
  / `hibp_fetcher.py` — live fetchers, one per source
- `content_generator.py` — pure formatting templates (no invented content)
- `engagement.py` — the one static, clearly-labeled quiz bank
- `storage.py` — dedup tracking + channel-post history for RSS
- `rss_generator.py` — builds `feed.xml` from that history
- `telegram_poster.py` — posts messages and polls to your channel

## Notes

- NVD's API occasionally rate-limits unauthenticated requests during high
  traffic — set `NVD_API_KEY` to raise the limit; the fallback to other
  sources covers this in the meantime.
- HackerOne-style bounty writeups here come from public security blogs, not
  HackerOne's Hacktivity API directly (that endpoint requires auth to query
  broadly) — infosecwriteups/Medium/PortSwigger are all freely accessible
  and cover the same disclosed-report space.
- The `breach` mode surfaces **unverified** ransomware-group claims; the
  new `leaked_creds` mode surfaces **confirmed** breaches from HIBP. Post
  copy makes this distinction explicit both times.
- Phishing URLs are always shown defanged. Never re-fang them for clicking.
