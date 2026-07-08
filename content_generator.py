"""
Live-only content generator. Every post is built from data fetched at
run time -- no pre-written cases, no static examples (the only exception
is the rotating engagement quiz bank in engagement.py, which is clearly
labeled as a general-awareness quiz, not threat data).
"""
import re
from config import HASHTAGS, CHANNEL_HANDLE


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _sanitize_md(text: str) -> str:
    if not text:
        return text
    for ch in ("*", "_", "`", "[", "]"):
        text = text.replace(ch, "")
    return text


def _defang(url: str) -> str:
    """Make an active malicious URL non-clickable/safe to display."""
    if not url:
        return url
    return url.replace("http://", "hxxp://").replace("https://", "hxxps://").replace(".", "[.]")


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
{HASHTAGS} {CHANNEL_HANDLE}"""


def generate_cve_alert_post(cve: dict) -> str:
    severity_emoji = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🟢",
    }.get(str(cve.get("severity", "")).upper(), "⚪")
    description = _sanitize_md(cve.get("description", ""))
    vendor_tags = " ".join(cve.get("vendor_tags", []) or [])
    extra_tags = f" {vendor_tags}" if vendor_tags else ""
    freshness = cve.get("freshness", "")
    freshness_line = f"📅 Published: {freshness}\n" if freshness else ""
    return f"""🛑 *LIVE CVE ALERT* / *लाइव CVE अलर्ट*
🆔 {cve['cve_id']}
{freshness_line}{severity_emoji} Severity: {cve['severity']} (CVSS {cve['score']})
📋 {description}
🔗 {cve['link']}
{HASHTAGS} #CVE #Vulnerability{extra_tags} {CHANNEL_HANDLE}"""


def generate_bounty_disclosure_post(report: dict) -> str:
    title = _sanitize_md(report.get("title", ""))
    summary = _sanitize_md(report.get("summary", ""))
    freshness = report.get("freshness", "")
    freshness_line = f"📅 Published: {freshness}\n" if freshness else ""
    return f"""🐞 *LIVE BUG BOUNTY DISCLOSURE* / *लाइव बग बाउंटी डिस्क्लोज़र*
{freshness_line}*{title}*
{summary}
🔗 {report['link']}
⚠️ Real disclosed report from a public bug bounty program -- for learning, not replication without authorization.
{HASHTAGS} #BugBounty #EthicalHacking {CHANNEL_HANDLE}"""


def generate_breach_claim_post(item: dict) -> str:
    victim = _sanitize_md(item.get("victim", ""))
    group = _sanitize_md(item.get("group", ""))
    sector = _sanitize_md(str(item.get("sector", "Not disclosed")))
    country = item.get("country", "N/A")
    observed = item.get("observed", "N/A")
    freshness = item.get("freshness", "")
    freshness_suffix = f" ({freshness})" if freshness else ""
    return f"""🚩 *CLAIMED DATA BREACH* / *दावा किया गया डेटा ब्रीच*
Threat actor: {group}
Target: {victim}
Sector: {sector}
Country: {country}
Observed: {observed}{freshness_suffix}
Status: ⚠️ Claimed by threat actor -- pending verification
🔗 {item['link']}
⚠️ This is an unverified claim from a leak-site monitor, not a confirmed breach. Included for awareness only.
{HASHTAGS} #DataBreach #ThreatIntel {CHANNEL_HANDLE}"""


def generate_phishing_alert_post(item: dict) -> str:
    domain = _sanitize_md(item.get("domain", ""))
    impersonates = _sanitize_md(item.get("impersonates", "Unknown"))
    safe_url = _defang(item.get("url", ""))
    freshness = item.get("freshness", "")
    if freshness and "not provided" not in freshness:
        status_line = f"Status: Currently listed active by OpenPhish, detected {freshness}"
    else:
        status_line = "Status: Currently listed active by OpenPhish (exact detection time not provided by this feed)"
    return f"""🎣 *PHISHING/SCAM ALERT* / *फिशिंग चेतावनी*
{status_line}
Active phishing domain detected: `{domain}`
Impersonating: {impersonates}
🔗 Defanged for safety (do NOT visit): {safe_url}
⚠️ Do not enter credentials, OTPs, or card details on this domain. Report and block it.
{HASHTAGS} #Phishing #ScamAlert {CHANNEL_HANDLE}"""


def generate_threat_actor_post(actor: dict) -> str:
    name = _sanitize_md(actor.get("name", ""))
    aliases = ", ".join(actor.get("aliases", [])[:5]) or "None listed"
    description = _sanitize_md(actor.get("description", ""))[:600]
    source = actor.get("source", "MITRE ATT&CK")
    freshness = actor.get("freshness", "")
    freshness_label = actor.get("freshness_label", "Last updated")
    freshness_line = f"🕓 {freshness_label}: {freshness}\n" if freshness else ""
    return f"""🕵️ *THREAT ACTOR SPOTLIGHT* / *थ्रेट एक्टर स्पॉटलाइट*
Group: *{name}*
Aliases: {aliases}
{freshness_line}{description}
📚 Source: {source}
ℹ️ This is reference profile data, not breaking news -- it describes a known group's known TTPs.
🔗 {actor['link']}
{HASHTAGS} #ThreatActor #APT #MalwareAnalysis {CHANNEL_HANDLE}"""


def generate_patch_tuesday_post(patch: dict) -> str:
    freshness = patch.get("freshness", "")
    freshness_line = f"📅 Released: {freshness}\n" if freshness else ""
    return f"""🪟 *PATCH TUESDAY TRACKER* / *पैच मंगलवार ट्रैकर*
{freshness_line}{_sanitize_md(patch.get('title', ''))} ({patch.get('period', '')})
🔢 Total CVEs patched: {patch.get('total_cves', 0)}
🔴 Critical: {patch.get('critical', 0)}   🟠 Important: {patch.get('important', 0)}
🟡 Moderate: {patch.get('moderate', 0)}   🟢 Low: {patch.get('low', 0)}
🎯 Actively exploited in the wild: {patch.get('exploited_in_wild', 0)}
🔗 {patch['link']}
⚠️ Patch as soon as possible, especially anything actively exploited.
{HASHTAGS} #PatchTuesday #Microsoft #WindowsUpdate {CHANNEL_HANDLE}"""


def generate_hibp_breach_post(item: dict) -> str:
    classes = ", ".join(item.get("data_classes", [])[:8]) or "Not specified"
    verified = "✅ Verified" if item.get("verified") else "⚠️ Unverified"
    sensitive = " 🔞 Sensitive breach" if item.get("is_sensitive") else ""
    freshness = item.get("freshness", "")
    freshness_suffix = f" ({freshness})" if freshness else ""
    return f"""🔓 *CONFIRMED LEAKED CREDENTIALS ALERT* / *पुष्टि की गई डेटा लीक चेतावनी*
Breach: *{_sanitize_md(item.get('title', ''))}*
Domain: {item.get('domain', 'N/A')}
Breach date: {item.get('breach_date', 'N/A')} | Added to HIBP: {item.get('added_date', 'N/A')}{freshness_suffix}
Accounts affected: {item.get('pwn_count', 0):,}
Data exposed: {classes}
Status: {verified}{sensitive}
🔗 {item['link']}
💡 Check haveibeenpwned.com to see if your own email was included, and change reused passwords.
{HASHTAGS} #DataBreach #HaveIBeenPwned #PasswordSecurity {CHANNEL_HANDLE}"""
