"""
Hacker-terminal style content generator. Uses Telegram's monospace/code
formatting for that "terminal output" look, while keeping the actual
source link as a plain markdown link (not inside a code block) so
Telegram still auto-generates the big preview card from it.
"""
import re
from urllib.parse import urlparse
from config import CHANNEL_HANDLE

CURSOR = "▓"


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _sanitize_md(text: str) -> str:
    """Strips markdown-breaking chars from LIVE/untrusted text only."""
    if not text:
        return text
    for ch in ("*", "_", "`", "[", "]", "(", ")"):
        text = text.replace(ch, "")
    return text


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return url


def generate_news_flash_post(news_item: dict) -> str:
    title = _sanitize_md(news_item.get("title", "").strip())
    link = news_item.get("link", "").strip()
    domain = _domain(link)
    return f"""{CURSOR*3} NEWS_FLASH.exe {CURSOR*3}

> {title}

```
[SOURCE]  {domain}
[STATUS]  LIVE
```
🔗 [Read full story]({link})"""


def generate_cve_alert_post(cve: dict) -> str:
    severity = str(cve.get("severity", "UNKNOWN")).upper()
    severity_emoji = {
        "CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢",
    }.get(severity, "⚪")
    description = _sanitize_md(cve.get("description", ""))[:300]
    return f"""{CURSOR*3} CVE_ALERT.sh {CURSOR*3}

```
[ID]        {cve['cve_id']}
[SEVERITY]  {severity_emoji} {severity}
[CVSS]      {cve['score']}
```
> {description}

🔗 [Full disclosure]({cve['link']})"""


def generate_bounty_disclosure_post(report: dict) -> str:
    title = _sanitize_md(report.get("title", ""))
    link = report.get("link", "").strip()
    domain = _domain(link)
    return f"""{CURSOR*3} BOUNTY_LOG.txt {CURSOR*3}

> {title}

```
[SOURCE]  {domain}
[TYPE]    disclosed report
```
🔗 [Read writeup]({link})"""


def generate_breach_claim_post(item: dict) -> str:
    victim = _sanitize_md(item.get("victim", ""))
    group = _sanitize_md(item.get("group", ""))
    link = item.get("link", "").strip()
    return f"""{CURSOR*3} BREACH_CLAIM.log {CURSOR*3}

```
[TARGET]  {victim}
[ACTOR]   {group}
[STATUS]  ⚠ claimed / unverified
```
🔗 [Source]({link})"""


def generate_phishing_alert_post(item: dict) -> str:
    domain = _sanitize_md(item.get("domain", ""))
    impersonates = _sanitize_md(str(item.get("impersonates", "Unknown brand")))
    return f"""{CURSOR*3} PHISHING_ALERT.warn {CURSOR*3}

```
[TARGET]    {impersonates}
[DOMAIN]    {domain}
[ACTION]    DO NOT VISIT
```
⚠️ Active phishing site — no link provided intentionally."""


def generate_threat_actor_post(item: dict) -> str:
    name = _sanitize_md(item.get("name", ""))
    link = item.get("link", "").strip()
    domain = _domain(link)
    return f"""{CURSOR*3} THREAT_ACTOR.db {CURSOR*3}

> {name}

```
[ADVERSARY]  {item.get('adversary', 'Not attributed')}
[MALWARE]    {item.get('malware_families', 'N/A')}
[SOURCE]     {domain}
```
🔗 [Full pulse]({link})"""


def generate_patch_tuesday_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    link = item.get("link", "").strip()
    return f"""{CURSOR*3} PATCH_TUESDAY.update {CURSOR*3}

> {title}

```
[PATCHED]  {item.get('vuln_count', 'Unknown')} vulnerabilities
```
🔗 [Release notes]({link})"""


def generate_confirmed_breach_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    link = item.get("link", "").strip()
    pwn_count = item.get("pwn_count", 0)
    return f"""{CURSOR*3} CONFIRMED_BREACH.db {CURSOR*3}

> {title}

```
[STATUS]     ✅ confirmed
[ACCOUNTS]   {pwn_count:,}
```
🔗 [Details]({link})"""


# Alias for compatibility with main.py's existing import name
generate_hibp_breach_post = generate_confirmed_breach_post
