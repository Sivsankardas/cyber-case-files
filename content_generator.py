"""
Clean, minimal content generator. Telegram auto-generates the big preview
card (image, description, Instant View) from the article's own metadata
the moment a real link is present in the message -- so the caption only
needs to be one short line. No banners, no hashtag blocks.
"""
import re
from urllib.parse import urlparse
from config import CHANNEL_HANDLE


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _sanitize_md(text: str) -> str:
    if not text:
        return text
    for ch in ("*", "_", "`", "[", "]", "(", ")"):
        text = text.replace(ch, "")
    return text


def _domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc
        return netloc.replace("www.", "")
    except Exception:
        return url


def generate_news_flash_post(news_item: dict) -> str:
    title = _sanitize_md(news_item.get("title", "").strip())
    link = news_item.get("link", "").strip()
    domain = _domain(link)
    return f"{title} – [{domain}]({link})"


def generate_cve_alert_post(cve: dict) -> str:
    severity_emoji = {
        "CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢",
    }.get(str(cve.get("severity", "")).upper(), "⚪")
    return f"{severity_emoji} {cve['cve_id']} — {cve['severity']} (CVSS {cve['score']}) – [nvd.nist.gov]({cve['link']})"


def generate_bounty_disclosure_post(report: dict) -> str:
    title = _sanitize_md(report.get("title", ""))
    link = report.get("link", "").strip()
    domain = _domain(link)
    return f"🐞 {title} – [{domain}]({link})"


def generate_breach_claim_post(item: dict) -> str:
    victim = _sanitize_md(item.get("victim", ""))
    group = _sanitize_md(item.get("group", ""))
    link = item.get("link", "").strip()
    domain = _domain(link)
    return f"🚩 {victim} allegedly breached by {group} (claimed, unverified) – [{domain}]({link})"


def generate_phishing_alert_post(item: dict) -> str:
    # Domain shown as inline code, NOT a hyperlink -- don't make an active
    # phishing site one tap away.
    domain = _sanitize_md(item.get("domain", ""))
    impersonates = _sanitize_md(str(item.get("impersonates", "Unknown brand")))
    return f"🎣 Active phishing domain impersonating {impersonates}: `{domain}` — do not visit or enter credentials"


def generate_threat_actor_post(item: dict) -> str:
    name = _sanitize_md(item.get("name", ""))
    link = item.get("link", "").strip()
    domain = _domain(link)
    return f"🕵️ {name} – [{domain}]({link})"


def generate_patch_tuesday_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    link = item.get("link", "").strip()
    return f"🪟 {title} — {item.get('vuln_count', 'Unknown')} vulnerabilities patched – [msrc.microsoft.com]({link})"


def generate_confirmed_breach_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    link = item.get("link", "").strip()
    pwn_count = item.get("pwn_count", 0)
    return f"🔓 {title} breach confirmed — {pwn_count:,} accounts affected – [haveibeenpwned.com]({link})"


# Alias for compatibility with main.py's existing import name
generate_hibp_breach_post = generate_confirmed_breach_post
