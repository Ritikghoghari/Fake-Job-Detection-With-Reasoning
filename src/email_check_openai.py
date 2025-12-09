# src/email_check_openai.py
import os, re, json, requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    from openai import OpenAI
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
except Exception:
    openai_client = None

EMAIL_REGEX = r"[A-Za-z0-9\.\-_+]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}"

def extract_emails(text: str):
    return list(dict.fromkeys(re.findall(EMAIL_REGEX, text)))

def _mx_lookup(domain: str) -> bool:
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX")
        return len(answers) > 0
    except Exception:
        return False

def google_email_search(email: str, company: str = None, num=3):
    if not SERPAPI_KEY:
        return []
    queries = [f'"{email}"', f'"{email}" scam', f'"{email}" hiring']
    if company:
        queries.append(f'"{company}" "{email}"')
    hits = []
    for q in queries[:4]:
        try:
            r = requests.get("https://serpapi.com/search", params={"api_key":SERPAPI_KEY,"engine":"google","q":q,"num":3}, timeout=8)
            if r.status_code != 200:
                continue
            data = r.json()
            org = data.get("organic_results", []) or []
            for it in org[:3]:
                hits.append({"title": it.get("title","")[:160], "snippet": it.get("snippet","")[:300], "url": it.get("link",""), "domain": urlparse(it.get("link","") or "").netloc})
        except Exception:
            continue
    return hits[:8]

def _call_openai_email(email, domain, mx_valid, google_hits, company):
    if openai_client is None:
        return {"email_legitimacy_score":0.5,"email_verdict":"suspicious","match_company":False,"domain_reputation":"unknown","explanation":"OpenAI not available"}
    prompt = f"""
You are an email legitimacy analyst.
Given:
email: {email}
domain: {domain}
mx_valid: {mx_valid}
company: {company}
google_hits: {json.dumps(google_hits)[:1000]}

Return ONLY JSON with:
email_legitimacy_score: 0..1
email_verdict: "valid"|"suspicious"|"invalid"
match_company: true/false
domain_reputation: "good"|"unknown"|"bad"
explanation: short reason
"""
    try:
        res = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You evaluate email legitimacy in recruitment contexts."},{"role":"user","content":prompt}],
            response_format={"type":"json_object"},
            temperature=0.0,
        )
        raw = res.choices[0].message.content.strip()
        data = json.loads(raw)
        return {
            "email_legitimacy_score": float(data.get("email_legitimacy_score",0.5)),
            "email_verdict": data.get("email_verdict","suspicious"),
            "match_company": bool(data.get("match_company",False)),
            "domain_reputation": data.get("domain_reputation","unknown"),
            "explanation": data.get("explanation","")
        }
    except Exception as e:
        return {"email_legitimacy_score":0.45,"email_verdict":"suspicious","match_company":False,"domain_reputation":"unknown","explanation":f"OpenAI error: {e}"}

def enhanced_email_check(text: str, company: str = None):
    emails = extract_emails(text)
    out = []
    for email in emails:
        domain = email.split("@")[-1].lower()
        mx = _mx_lookup(domain)
        hits = google_email_search(email, company)
        ai = _call_openai_email(email, domain, mx, hits, company or "")
        status = ai.get("email_verdict","suspicious")
        out.append({"email":email,"domain":domain,"mx_valid":mx,"google_hits":hits,"openai":ai,"status":status,"explanation":ai.get("explanation","")})
    return out
