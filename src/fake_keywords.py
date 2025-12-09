# src/fake_keywords.py
FAKE_KEYWORDS = [
    "wire-transfer-ready", "pay-per-task", "earn-instant", "no-interview-hire",
    "provide-bank-details", "activation-fee", "recruiter-bonus-referral",
    "quickhire", "instant-onboard", "earn-instantly", "work-from-home and pay",
    "send money", "investment opportunity", "bitcoin", "crypto-wallet", "western union"
]

def find_fake_keywords(text: str):
    textl = text.lower()
    found = [k for k in FAKE_KEYWORDS if k in textl]
    # also detect money patterns
    import re
    if re.search(r"\$\s?\d+", text):
        found.append("money_pattern")
    return found
