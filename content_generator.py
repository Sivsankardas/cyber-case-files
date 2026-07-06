"""
Zero-cost content generator — pure Python string templates, NO API calls, NO cost.

Historical cases: fully bilingual, pre-written (see sources.py) -> just formatted.
Fresh RSS news: title/summary come from the feed in English. Full free machine
translation isn't reliable enough to trust unattended for factual news text, so
the dynamic news portion stays in English; the wrapper text and the tip are
bilingual (pre-written). This keeps everything 100% free with zero hallucination risk.
"""
import re
from config import HASHTAGS, CHANNEL_HANDLE


def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def generate_case_file_post(case: dict, case_number: int) -> str:
    en, hi = case["en"], case["hi"]
    return f"""🗂 *CASE FILE #{case_number:03d}*
🎯 CASE: {case['title']}
📅 YEAR: {case['year']}

🔍 *What Happened*
{en['what']}

⚙️ *The Method*
{en['method']}

💥 *The Impact*
{en['impact']}

🛡 *The Lesson*
{en['lesson']}

———

🔍 *क्या हुआ*
{hi['what']}

⚙️ *तरीका*
{hi['method']}

💥 *असर*
{hi['impact']}

🛡 *सबक*
{hi['lesson']}

{HASHTAGS} {CHANNEL_HANDLE}"""


def generate_news_flash_post(news_item: dict, tip: dict) -> str:
    title = news_item.get("title", "").strip()
    link = news_item.get("link", "").strip()
    summary = _strip_html(news_item.get("summary", ""))[:400]

    return f"""🚨 *CYBER NEWS FLASH*

*{title}*
{summary}

🔗 {link}

💡 *Security Tip of the Day:*
{tip['en']}

———

🚨 *साइबर न्यूज़ फ्लैश*

*{title}*
(अंग्रेज़ी सोर्स से — नीचे लिंक देखें)

🔗 {link}

💡 *आज की सुरक्षा टिप:*
{tip['hi']}

{HASHTAGS} {CHANNEL_HANDLE}"""
