"""
Live-only content generator. Every post is built from data fetched at
run time -- no pre-written cases, no static examples.
"""
import re
from config import HASHTAGS, CHANNEL_HANDLE, ENGAGEMENT_CTA

def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()

def _sanitize_md(text: str) -> str:
    if not text:
        return text
    for ch in ("*", "_", "`", "[", "]"):
        text = text.replace(ch, "")
    return text

def generate_news_flash_post(news_item: dict) -> str:
    title = _sanitize_md(news_item.get("title", "").strip())
    link = news_item.get("link", "").strip()
    summary = _sanitize_md(_strip_html(news_item.get("summary", ""))[:500])
    age = news_item.get("age_minutes")
    freshness_tag = f"⚡ Published {int(age)} min ago" if age is not None else ""
    return f"""🚨 *CYBER NEWS FLASH* / *साइबर न्यूज़ फ्लैश*
{freshness_tag}
*{title}*
{summary}
🔗 {link}
{ENGAGEMENT_CTA}
{HASHTAGS} {CHANNEL_HANDLE}"""

def generate_cve_alert_post(cve: dict) -> str:
    severity_emoji = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢",
    }.get(str(cve.get("severity", "")).upper(), "⚪")
    description = _sanitize_md(cve.get("description", ""))
    dynamic_tags = cve.get("hashtags", "#CVE #Vulnerability")
    return f"""🛑 *LIVE CVE ALERT* / *लाइव CVE अलर्ट*
🆔 {cve['cve_id']}
{severity_emoji} Severity: {cve['severity']} (CVSS {cve['score']})
📋 {description}
🔗 {cve['link']}
{ENGAGEMENT_CTA}
{HASHTAGS} #CVE {dynamic_tags} {CHANNEL_HANDLE}"""

def generate_bounty_disclosure_post(report: dict) -> str:
    title = _sanitize_md(report.get("title", ""))
    summary = _sanitize_md(report.get("summary", ""))
    return f"""🐞 *LIVE BUG BOUNTY DISCLOSURE* / *लाइव बग बाउंटी डिस्क्लोज़र*
*{title}*
{summary}
🔗 {report['link']}
⚠️ Real disclosed report from a public bug bounty program -- for learning, not replication without authorization.
{ENGAGEMENT_CTA}
{HASHTAGS} #BugBounty #EthicalHacking {CHANNEL_HANDLE}"""

def generate_breach_claim_post(item: dict) -> str:
    victim = _sanitize_md(item.get("victim", ""))
    group = _sanitize_md(item.get("group", ""))
    sector = _sanitize_md(str(item.get("sector", "Not disclosed")))
    country = item.get("country", "N/A")
    observed = item.get("observed", "N/A")
    return f"""🚩 *CLAIMED DATA BREACH* / *दावा किया गया डेटा ब्रीच*
Threat actor: {group}
Target: {victim}
Sector: {sector}
Country: {country}
Observed: {observed}
Status: ⚠️ Claimed by threat actor -- pending verification
🔗 {item['link']}
⚠️ This is an unverified claim from a leak-site monitor, not a confirmed breach. Included for awareness only.
{ENGAGEMENT_CTA}
{HASHTAGS} #DataBreach #ThreatIntel {CHANNEL_HANDLE}"""

def generate_phishing_alert_post(item: dict) -> str:
    domain = _sanitize_md(item.get("domain", "unknown"))
    defanged = item.get("defanged_url", "")
    return f"""🎣 *PHISHING / SCAM ALERT* / *फ़िशिंग चेतावनी*
An active phishing site has been detected impersonating or targeting users via:
🌐 Domain: {domain}
🔗 (defanged, do NOT visit): {defanged}
🛑 If you receive a link like this, do not click, do not enter credentials, and report it to your email/browser provider.
Source: {item.get('source', 'OpenPhish')}
{ENGAGEMENT_CTA}
{HASHTAGS} #Phishing #ScamAlert {CHANNEL_HANDLE}"""

def generate_threat_spotlight_post(item: dict) -> str:
    name = _sanitize_md(item.get("name", ""))
    adversary = _sanitize_md(item.get("adversary", "Unknown / unattributed"))
    families = _sanitize_md(item.get("malware_families", "Not specified"))
    tags = _sanitize_md(item.get("tags", "N/A"))
    description = _sanitize_md(item.get("description", ""))
    return f"""🕵️ *THREAT ACTOR / MALWARE SPOTLIGHT* / *खतरा स्पॉटलाइट*
*{name}*
👤 Attributed actor: {adversary}
🦠 Malware families: {families}
🏷️ Tags: {tags}
📋 {description}
🔗 {item['link']}
{ENGAGEMENT_CTA}
{HASHTAGS} #ThreatIntel #Malware #APT {CHANNEL_HANDLE}"""

def generate_patch_tuesday_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    return f"""🧩 *PATCH TUESDAY TRACKER* / *पैच ट्यूज़डे ट्रैकर*
*{title}*
📦 CVEs addressed this cycle: {item.get('cve_count', 'Unknown')}
🔗 {item['link']}
Patch your systems as soon as possible -- attackers often reverse-engineer patches within hours of release.
{ENGAGEMENT_CTA}
{HASHTAGS} #PatchTuesday #Microsoft {CHANNEL_HANDLE}"""

def generate_leaked_creds_post(item: dict) -> str:
    title = _sanitize_md(item.get("title", ""))
    domain = _sanitize_md(item.get("domain", "N/A"))
    return f"""🔓 *CONFIRMED BREACH — LEAKED CREDENTIALS* / *पुष्ट डेटा ब्रीच*
*{title}*
🌐 Domain: {domain}
📅 Breach date: {item.get('breach_date', 'N/A')}  |  Added: {item.get('added_date', 'N/A')}
👥 Accounts affected: {(f"{item['pwn_count']:,}" if isinstance(item.get('pwn_count'), int) else item.get('pwn_count', 'Unknown'))}
🗃️ Data exposed: {item.get('data_classes', 'Not specified')}
🔗 {item['link']}
✅ Confirmed by HaveIBeenPwned -- check if you're affected at haveibeenpwned.com
{ENGAGEMENT_CTA}
{HASHTAGS} #DataBreach #HIBP {CHANNEL_HANDLE}"""
