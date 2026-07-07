"""
Live-only content generator. Every post is built from data fetched at
run time -- no pre-written cases, no static examples.
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
    return f"""🛑 *LIVE CVE ALERT* / *लाइव CVE अलर्ट*

🆔 {cve['cve_id']}
{severity_emoji} Severity: {cve['severity']} (CVSS {cve['score']})

📋 {description}

🔗 {cve['link']}

{HASHTAGS} #CVE #Vulnerability {CHANNEL_HANDLE}"""


def generate_bounty_disclosure_post(report: dict) -> str:
    title = _sanitize_md(report.get("title", ""))
    summary = _sanitize_md(report.get("summary", ""))
    return f"""🐞 *LIVE BUG BOUNTY DISCLOSURE* / *लाइव बग बाउंटी डिस्क्लोज़र*

*{title}*

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
    return f"""🚩 *CLAIMED DATA BREACH* / *दावा किया गया डेटा ब्रीच*

Threat actor: {group}
Target: {victim}
Sector: {sector}
Country: {country}
Observed: {observed}
Status: ⚠️ Claimed by threat actor -- pending verification

🔗 {item['link']}

⚠️ This is an unverified claim from a leak-site monitor, not a confirmed breach. Included for awareness only.

{HASHTAGS} #DataBreach #ThreatIntel {CHANNEL_HANDLE}"""


def generate_cve_severity_poll(cve: dict):
    real_severity = str(cve.get("severity", "")).upper()
    levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    if real_severity not in levels:
        return None
    question = f"🎯 Guess the CVSS severity: {cve['cve_id']}"
    correct_index = levels.index(real_severity)
    return question, levels, correct_index
