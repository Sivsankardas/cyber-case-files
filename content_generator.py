"""
Bold, detailed, "attention-grabbing" content generator. Uses Telegram
Markdown (*bold*, _italic_) heavily, section dividers, and more fields
per post than the earlier minimal version. Pairs with telegram_poster's
send_post(), which attaches a real image pulled from the source (see
image_helper.py) so every post has a visual, not just a text card.
"""
import re
from urllib.parse import urlparse
from config import HASHTAGS, CHANNEL_HANDLE

DIVIDER = "━━━━━━━━━━━━━━━━━━━"

VENDOR_HASHTAG_MAP = {
    "microsoft": "#Microsoft", "windows": "#Windows", "azure": "#Azure",
    "apple": "#Apple", "ios": "#iOS", "macos": "#macOS",
    "google": "#Google", "chrome": "#Chrome", "android": "#Android",
    "linux": "#Linux", "ubuntu": "#Ubuntu",
    "wordpress": "#WordPress", "cisco": "#Cisco", "adobe": "#Adobe",
    "vmware": "#VMware", "oracle": "#Oracle", "fortinet": "#Fortinet",
    "sap": "#SAP", "ibm": "#IBM", "citrix": "#Citrix", "juniper": "#Juniper",
    "docker": "#Docker", "kubernetes": "#Kubernetes",
}


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _sanitize_md(text: str) -> str:
    """Strips markdown-breaking chars from LIVE/untrusted text only."""
    if not text:
        return text
    for ch in ("*", "_", "`", "[", "]"):
        text = text.replace(ch, "")
    return text


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return url


def _vendor_hashtags(text: str) -> str:
    lowered = (text or "").lower()
    found = []
    for keyword, tag in VENDOR_HASHTAG_MAP.items():
        if keyword in lowered and tag not in found:
            found.append(tag)
        if len(found) >= 3:
            break
    return " ".join(found)


def generate_news_flash_post(news_item: dict) -> str:
    title = _sanitize_md(news_item.get("title", "").strip())
    link = news_item.get("link", "").strip()
    domain = _domain(link)
    summary = _sanitize_md(_strip_html(news_item.get("summary", ""))[:350])
    age = news_item.get("age_minutes")
    freshness = f"🕒 Published *{int(age)} min ago*" if age is not None else "🕒 *Just published*"
    return f"""🚨 *BREAKING CYBER NEWS* 🚨
{DIVIDER}
*{title}*

{summary}

📰 Source: *{domain}*
{freshness}
📡 Status: 🟢 *LIVE*
{DIVIDER}
🔗 [Read Full Story]({link})

{HASHTAGS} #CyberNews {CHANNEL_HANDLE}"""


def generate_cve_alert_post(cve: dict) -> str:
    severity = str(cve.get("severity", "UNKNOWN")).upper()
    severity_emoji = {
        "CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢",
    }.get(severity, "⚪")
    description = _sanitize_md(cve.get("description", ""))[:400]
    vendor_tags = _vendor_hashtags(cve.get("description", ""))
    return f"""🛑 *CRITICAL VULNERABILITY DISCLOSED* 🛑
{DIVIDER}
🆔 *{cve['cve_id']}*
{severity_emoji} Severity: *{severity}*
📊 CVSS Score: *{cve['score']}/10*
📅 Disclosed: last 7 days (NVD)

📋 *Technical Summary:*
_{description}_
{DIVIDER}
🔗 [Full NVD Report]({cve['link']})

{HASHTAGS} #CVE #Vulnerability {vendor_tags} {CHANNEL_HANDLE}"""


def generate_bounty_disclosure_post(report: dict) -> str:
    title = _sanitize_md(report.get("title", ""))
    summary = _sanitize_md(report.get("summary", ""))[:350]
    link = report.get("link", "").strip()
    domain = _domain(link)
    return f"""🐞 *BUG BOUNTY DISCLOSURE* 🐞
{DIVIDER}
*{title}*

{summary}

📰 Source: *{domain}*
{DIVIDER}
⚠️ _Public, disclosed research — for learning, not replication without authorization._

🔗 [Read Full Writeup]({link})

{HASHTAGS} #BugBounty #EthicalHacking {CHANNEL_HANDLE}"""


def generate_breach_claim_post(item: dict) -> str:
    victim = _sanitize_md(item.get("victim", ""))
    group = _sanitize_md(item.get("group", ""))
    sector = _sanitize_md(str(item.get("sector", "Not disclosed")))
    country = item.get("country", "N/A")
    observed = item.get("observed", "N/A")
    link = item.get("link", "").strip()
    return f"""🚩 *CLAIMED DATA BREACH* 🚩
{DIVIDER}
🎯 Target: *{victim}*
👤 Threat Actor: *{group}*
🏢 Sector: *{sector}*
🌍 Country: *{country}*
📅 Observed: *{observed}*
🔎 Status: ⚠️ *Claimed — pending verification*
{DIVIDER}
⚠️ _Unverified leak-site claim. Included for awareness only, not confirmation._

🔗 [Source]({link})

{HASHTAGS} #DataBreach #ThreatIntel {CHANNEL_HANDLE}"""


def generate_phishing_alert_post(item: dict) -> str:
    domain = _sanitize_md(item.get("domain", ""))
    impersonates = _sanitize_md(str(item.get("impersonates", "Unknown brand")))
    return f"""🎣 *ACTIVE PHISHING ALERT* 🎣
{DIVIDER}
🏷️ Impersonating: *{impersonates}*
🌐 Malicious domain: `{domain}`
🕒 First seen: *{item.get('first_seen', 'N/A')}*
🖥️ Hosting: *{item.get('org', 'N/A')}* ({item.get('country', 'N/A')})
{DIVIDER}
🚫 *DO NOT* click, visit, or enter any credentials on this domain.

{HASHTAGS} #Phishing #ScamAlert {CHANNEL_HANDLE}"""


def generate_threat_actor_post(item: dict) -> str:
    name = _sanitize_md(item.get("name", ""))
    description = _sanitize_md(item.get("description", ""))[:350]
    link = item.get("link", "").strip()
    return f"""🕵️ *THREAT ACTOR / MALWARE SPOTLIGHT* 🕵️
{DIVIDER}
📛 Campaign: *{name}*
👤 Attributed to: *{item.get('adversary', 'Not attributed')}*
🦠 Malware families: *{item.get('malware_families', 'Not specified')}*
🏭 Targeted industries: *{item.get('industries', 'Not specified')}*
🌍 Targeted countries: *{item.get('targeted_countries', 'Not specified')}*
📊 Indicators tracked: *{item.get('indicator_count', 0)}*

📋 _{description}_
{DIVIDER}
🔗 [Full Threat Pulse]({link})

{HASHTAGS} #ThreatIntel #Malware {CHANNEL_HANDLE}"""


def generate_patch_tuesday_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    link = item.get("link", "").strip()
    return f"""🪟 *PATCH TUESDAY SUMMARY* 🪟
{DIVIDER}
{title}

🔧 Vulnerabilities patched: *{item.get('vuln_count', 'Unknown')}*
{DIVIDER}
⚠️ _Delaying patch deployment is one of the most common ways known vulnerabilities get exploited. Update as soon as your environment allows._

🔗 [Full Release Notes]({link})

{HASHTAGS} #PatchTuesday #Microsoft {CHANNEL_HANDLE}"""


def generate_confirmed_breach_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    link = item.get("link", "").strip()
    pwn_count = item.get("pwn_count", 0)
    verified_tag = "✅ *Verified*" if item.get("is_verified") else "⚠️ *Unverified*"
    return f"""🔓 *CONFIRMED DATA BREACH* 🔓
{DIVIDER}
{title}

🌐 Domain: *{item.get('domain', 'N/A')}*
📅 Breach date: *{item.get('breach_date', 'N/A')}*
📥 Added to database: *{item.get('added_date', 'N/A')}*
🔎 Status: {verified_tag}
👥 Accounts affected: *{pwn_count:,}*
📦 Data exposed: *{item.get('data_classes', 'Not specified')}*
{DIVIDER}
⚠️ _If you may have an account with this service, change your password and enable 2FA._

🔗 [Full Details]({link})

{HASHTAGS} #DataBreach #ConfirmedBreach {CHANNEL_HANDLE}"""


# Alias for compatibility with main.py's existing import name
generate_hibp_breach_post = generate_confirmed_breach_post
