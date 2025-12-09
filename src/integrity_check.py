# src/integrity_check.py
"""
Hybrid tamper / integrity detection:
- Fast heuristics detect obvious injections (emails changed, money patterns, date edits, new URLs).
- LLM (OpenAI) compares posting style to typical corporate style and highlights suspicious spans.
- Combines heuristic_score (0..1) and llm_score (0..1) into tamper_score = 0.4*heur + 0.6*llm.
Returns dict with tamper_score, heuristics, llm_result, suspicious_spans, explanation.
"""

import os
import re
import json
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Try import client (openai package)
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception:
    openai_client = None

# Heuristic checks (fast)
def _heuristic_checks(text: str):
    text_lower = text.lower()
    heur = {}
    # new/different emails (heuristic: many different domains or generic domains)
    emails = list(set(re.findall(r"[A-Za-z0-9\.\-_+]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}", text)))
    heur['email_count'] = len(emails)
    heur['emails'] = emails
    heur['many_domains'] = len(set([e.split("@")[-1].lower() for e in emails])) > 1 if emails else False

    # money patterns injected
    heur['money_patterns'] = bool(re.search(r"\b(?:€|eur|\$|£|usd|€\s?\d+|\$\s?\d+)\b", text))

    # suspicious quick-hire keywords (including your supplied list)
    suspicious_list = ["quickhire", "instant-onboard", "wire-transfer-ready", "pay-per-task",
                       "earn-instant", "no-interview-hire", "provide-bank-details", "activation-fee",
                       "recruiter-bonus-referral", "send money", "western union", "bitcoin", "crypto"]
    found = [k for k in suspicious_list if k in text_lower]
    heur['suspicious_keywords'] = found

    # dates/future-year anomalies (e.g., 2100- or odd dates)
    heur['weird_dates'] = bool(re.search(r"\b20[5-9]\d\b|\b21\d{2}\b", text))  # years >= 2050 or 2100s
    # abrupt short sections or many short lines (possible pasted segments)
    heur['short_lines_ratio'] = sum(1 for s in text.splitlines() if len(s.strip())<40) / max(1, len(text.splitlines()))
    # uppercase spammy blocks
    heur['uppercase_blocks'] = bool(re.search(r"\n[A-Z\s]{8,}\n", text))

    # basic heuristic score aggregation (0..1)
    score = 0.0
    if heur['many_domains']:
        score += 0.25
    if heur['money_patterns']:
        score += 0.20
    if len(found) >= 1:
        score += min(0.30, 0.10 * len(found))
    if heur['weird_dates']:
        score += 0.15
    if heur['short_lines_ratio'] > 0.25:
        score += 0.10
    if heur['uppercase_blocks']:
        score += 0.10

    heur['heuristic_score'] = round(min(1.0, score), 3)
    return heur

# LLM check: compare posting vs typical company style / detect inserted spans
def _llm_integrity_check(text: str, company: str = "Unknown Company"):
    """
    Calls OpenAI to produce:
    - llm_score: 0..1 (1 = highly inconsistent / tampered)
    - suspicious_spans: list of short excerpts flagged suspicious
    - explanation: short text
    """
    if openai_client is None:
        return {"llm_score": 0.5, "suspicious_spans": [], "explanation": "OpenAI client not available (fallback)."}
    prompt = f"""
You are an expert at spotting edited or tampered job postings. Given a job posting and the company name,
answer with ONLY a JSON object with keys:
- llm_score: 0..1 (1.0 means highly likely the posting has been edited/tampered)
- suspicious_spans: list of short text excerpts (max 6) from the posting that look injected, altered, or inconsistent
- explanation: 1-2 sentence rationale

Job posting:
\"\"\"{text}\"\"\"

Company (guessed): {company}

Consider style consistency, corporate tone, suspicious injections (money, payments, non-company emails),
odd dates, unnatural phrasing, and AI-generated paste fragments.
If the post seems genuine and consistent, return llm_score near 0 and an empty suspicious_spans array.
"""
    try:
        res = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You detect tampering in job postings."},{"role":"user","content":prompt}],
            response_format={"type":"json_object"},
            temperature=0.0,
            max_tokens=600,
        )
        raw = res.choices[0].message.content.strip()
        data = json.loads(raw)
        # sanitize
        return {
            "llm_score": float(data.get("llm_score", 0.5)),
            "suspicious_spans": data.get("suspicious_spans", [])[:6],
            "explanation": data.get("explanation", "") or ""
        }
    except Exception as e:
        return {"llm_score": 0.5, "suspicious_spans": [], "explanation": f"OpenAI error: {e}"}

def assess_tamper(text: str, company: str = "Unknown Company"):
    heur = _heuristic_checks(text)
    llm = _llm_integrity_check(text, company=company)

    # Combine scores: weight LLM heavier (0.6) and heuristics 0.4
    heur_score = float(heur.get("heuristic_score", 0.5))
    llm_score = float(llm.get("llm_score", 0.5))
    tamper_score = round(min(1.0, 0.4 * heur_score + 0.6 * llm_score), 3)

    # assemble suspicious spans: union of LLM spans + heuristic hints (emails/money)
    spans = list(llm.get("suspicious_spans", []) or [])
    # add suspicious emails and money patterns if not in spans
    for e in heur.get("emails", []):
        if e not in spans and heur['many_domains']:
            spans.append(e)
    if heur.get("money_patterns") and "money_pattern" not in spans:
        spans.append("money_pattern")
    spans = spans[:6]

    return {
        "tamper_score": tamper_score,
        "heuristic": heur,
        "llm": llm,
        "suspicious_spans": spans,
        "explanation": llm.get("explanation", "") or ""
    }
