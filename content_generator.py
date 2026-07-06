"""
Live-only content generator. Every post is built from data fetched at
run time — no pre-written cases, no static examples. Templates below only
format the live data; they don't invent content.

Note on language: since the underlying data (CVE descriptions, news
headlines, bug bounty report titles) is fetched live and must stay factually
exact, it's kept in English with the source link included. Auto-translating
live technical text isn't reliable enough to trust unattended, so only the
wrapper labels are bilingual. This keeps the content 100% accurate to source.
"""
import re
from config import HASHTAGS, CHANNEL_HANDLE


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def _sanitize_md(text: str) -> str:
    """
    Live text (CVE descriptions, report titles, news headlines) can contain
    characters that break Telegram's legacy Markdown parser (*, _, `, [).
    Since we can't control what's in real-time source text, strip those
    characters so the message always sends successfully.
    """
    if not text:
        return text
    for ch in ("*", "_", "`", "[", "]"):
        text = text.replace(ch, "")
    return text


def generate_news_flash_post(news_item: dict) -> str:
    title = _sanitize_md(news_item.get("title", "").strip())
    link = news_item.get("link", "").strip()
    summary = _sanitize_md(_strip_html(news_item.get("summary", ""))[:500])

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

⚠️ Real disclosed report from a public bug bounty program — for learning, not replication without authorization.

{HASHTAGS} #BugBounty #EthicalHacking {CHANNEL_HANDLE}"""
