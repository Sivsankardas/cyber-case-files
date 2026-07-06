import re
from config import HASHTAGS, CHANNEL_HANDLE


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def generate_news_flash_post(news_item: dict) -> str:
    title = news_item.get("title", "").strip()
    link = news_item.get("link", "").strip()
    summary = _strip_html(news_item.get("summary", ""))[:500]

    return f"""🚨 *CYBER NEWS FLASH* / *साइबर न्यूज़ फ्लैश*

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

    return f"""🛑 *LIVE CVE ALERT* / *लाइव CVE अलर्ट*

🆔 {cve['cve_id']}
{severity_emoji} Severity: {cve['severity']} (CVSS {cve['score']})

📋 {cve['description']}

🔗 {cve['link']}

{HASHTAGS} #CVE #Vulnerability {CHANNEL_HANDLE}"""


def generate_bounty_disclosure_post(report: dict) -> str:
    return f"""🐞 *LIVE BUG BOUNTY DISCLOSURE* / *लाइव बग बाउंटी डिस्क्लोज़र*

*{report['title']}*
{report['summary']}

🔗 {report['link']}

⚠️ Real disclosed report from a public bug bounty program — for learning, not replication without authorization.

{HASHTAGS} #BugBounty #EthicalHacking {CHANNEL_HANDLE}"""
