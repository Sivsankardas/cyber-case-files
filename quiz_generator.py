"""
Daily engagement quiz -- a Telegram poll built from a live CVE, keeping
the channel interactive instead of pure one-way broadcasting.
"""
import random
from cve_fetcher import fetch_recent_cve
from telegram_poster import send_poll

def post_daily_quiz():
    cve = fetch_recent_cve()
    if not cve:
        print("[Quiz] No live CVE available to build a quiz from -- skipping.")
        return False

    real_severity = str(cve.get("severity", "Unknown")).upper()
    all_severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    if real_severity not in all_severities:
        print("[Quiz] CVE severity unknown -- skipping quiz this run.")
        return False

    options = all_severities[:]
    random.shuffle(options)
    correct_index = options.index(real_severity)

    question = f"🧠 Quiz: What severity is {cve['cve_id']}? (CVSS {cve['score']})"
    send_poll(question, options, correct_option_id=correct_index)
    print(f"✅ Posted daily quiz for {cve['cve_id']} (answer: {real_severity})")
    return True
