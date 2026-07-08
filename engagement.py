"""
Engagement extras. These are the one deliberately-static piece of content
in the bot -- a small rotating bank of general cybersecurity-awareness quiz
questions (NOT threat data, NOT case files) posted as Telegram quiz polls
to drive interaction. Everything else in the bot remains 100% live-fetched.
"""
import random
from telegram_poster import send_poll

QUIZ_BANK = [
    {
        "question": "You get an SMS saying your bank account is 'locked' with a link to unlock it. Best move?",
        "options": ["Click the link and log in", "Ignore the link, open your bank app/site directly", "Reply STOP"],
        "correct": 1,
    },
    {
        "question": "Which of these makes a password hardest to crack?",
        "options": ["Length + randomness (passphrase)", "Adding '123!' to a word", "Using your pet's name"],
        "correct": 0,
    },
    {
        "question": "A CVE has a CVSS score of 9.8. That severity is generally considered:",
        "options": ["Low", "Medium", "Critical"],
        "correct": 2,
    },
    {
        "question": "What should you enable on every important account to stop most account-takeovers?",
        "options": ["Two-factor authentication (2FA)", "A longer username", "Auto-fill passwords"],
        "correct": 0,
    },
    {
        "question": "You find a USB drive in a parking lot. Best practice is to:",
        "options": ["Plug it in to see who it belongs to", "Hand it to IT/security or discard it", "Plug it into a personal laptop only"],
        "correct": 1,
    },
    {
        "question": "In bug bounty terms, 'responsible disclosure' means:",
        "options": ["Posting the exploit publicly first", "Reporting privately to the vendor before going public", "Selling it to the highest bidder"],
        "correct": 1,
    },
]


def post_engagement_quiz():
    quiz = random.choice(QUIZ_BANK)
    send_poll(
        question=f"🧠 Quick Security IQ Check: {quiz['question']}",
        options=quiz["options"],
        correct_option_id=quiz["correct"],
    )
    print(f"✅ Posted engagement quiz: {quiz['question']}")
    return 1
