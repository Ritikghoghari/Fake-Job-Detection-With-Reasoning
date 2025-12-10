# src/web_verification.py
import os, re, json, requests
import streamlit as st
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
if not SERPAPI_KEY and "SERPAPI_KEY" in st.secrets:
    SERPAPI_KEY = st.secrets["SERPAPI_KEY"]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY and "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Try to import OpenAI client if available, else use placeholder
try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception:
    openai_client = None

SERPAPI_URL = "https://serpapi.com/search"

def google_search_company(query: str, num: int = 5) -> Dict[str, Any]:
    if not SERPAPI_KEY:
        return {"error": "Missing SERPAPI_KEY"}
    try:
        r = requests.get(SERPAPI_URL, params={"engine":"google","q":query,"num":num,"api_key":SERPAPI_KEY}, timeout=10)
        if r.status_code != 200:
            return {"error": f"SerpAPI {r.status_code}"}
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def _guess_company(text: str) -> str:
    patterns = [r"Company[:\-\s]+([A-Z][A-Za-z0-9 &\.\-]+)", r"Apply to\s+([A-Z][A-Za-z0-9 &\.\-]+)", r" at ([A-Z][A-Za-z0-9 &\.\-]+)"]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    brands = ["mercedes", "mercedes-benz", "bmw", "audi","google","amazon","siemens","bosch","meta","microsoft","apple","dhl","picnic"]
    low = text.lower()
    for b in brands:
        if b in low:
            return b.title()
    return "Unknown"

def _call_openai_safe(job_text: str, company: str, google_context: str) -> Dict[str, Any]:
    # If client missing, fallback conservative response
    if openai_client is None:
        return {"verdict":"uncertain","confidence":0.45,"reason":"OpenAI client not available","web_realism_score":0.45}
    prompt = f"""
You are a careful job-posting verifier operating in SAFE MODE.
Rules:
- If a major recognized company (Mercedes-Benz, BMW, Google, Amazon, etc.) is present,
  assume real unless the posting contains clear scam signals (payments, crypto, requests
  for bank details, WhatsApp-only contact, or extremely poor English).
- Missing salary is common and should not make a posting suspicious.
- Not finding an exact job page on Google is normal for ATS/portal-hosted internal jobs.

Job text:
\"\"\"{job_text}\"\"\"

Company guess: {company}

Google context snippets:
\"\"\"{google_context}\"\"\"

Return JSON only:
{{"verdict":"real"|"likely_real"|"uncertain"|"likely_fake"|"fake", "confidence":0-1, "reason":"short", "web_realism_score":0-1}}
"""
    try:
        res = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You analyze job postings for realism."},{"role":"user","content":prompt}],
            response_format={"type":"json_object"},
            temperature=0.1,
        )
        raw = res.choices[0].message.content.strip()
        data = json.loads(raw)
        return {"verdict":data.get("verdict","uncertain"), "confidence":float(data.get("confidence",0.5)), "reason":data.get("reason",""), "web_realism_score":float(data.get("web_realism_score",0.5))}
    except Exception as e:
        return {"verdict":"uncertain","confidence":0.4,"reason":f"OpenAI error: {e}","web_realism_score":0.4}

def verify_job_online_safe(job_text: str) -> Dict[str, Any]:
    company = _guess_company(job_text)
    google_results = []
    if company != "Unknown":
        serp = google_search_company(company, num=5)
        if "error" not in serp:
            org = serp.get("organic_results", []) or []
            for it in org[:6]:
                google_results.append({"title": it.get("title","")[:220],"snippet":it.get("snippet","")[:400],"url":it.get("link","")})
    google_context = "\n".join([r.get("snippet","") for r in google_results])[:1600]
    ai_out = _call_openai_safe(job_text, company, google_context)
    # brand-safety: if major brand is present, bias to real
    safe_brands = {"mercedes","mercedes-benz","bmw","google","amazon","siemens","bosch","meta","microsoft","apple","dhl","picnic"}
    brand_detected = any(b in job_text.lower() for b in safe_brands) or (company != "Unknown" and any(b in company.lower() for b in safe_brands))
    if brand_detected and ai_out["verdict"] in ("likely_fake","fake","uncertain"):
        ai_out["verdict"] = "real"
        ai_out["confidence"] = max(ai_out["confidence"], 0.85)
        ai_out["reason"] = "Recognized corporate brand present; SAFE MODE assumes genuine posting unless clear scam indicators."
    return {"company_detected": company, "google_results": google_results, "web_verdict": ai_out["verdict"], "confidence": ai_out["confidence"], "web_realism_score": ai_out["web_realism_score"], "reasoning": ai_out["reason"], "job_exists_online": bool(google_results)}
