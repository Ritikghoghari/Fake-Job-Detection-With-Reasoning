# src/explain_with_openai.py
import os, json
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception:
    client = None

def openai_realism_and_reasoning(text: str, model_score: float):
    # returns: realism_score (0..1), category, explanation
    if client is None:
        return {"realism_score": 0.6, "category":"real", "explanation":"OpenAI not available; using fallback."}
    prompt = f"""
You are an expert judge for job postings. Given this job text, return JSON:
- realism_score: 0..1 (1=very realistic)
- category: "real"|"fictional"|"other"
- explanation: short reasoning (1-3 sentences)

Job text:
\"\"\"{text}\"\"\"
"""
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"You judge job posting realism."},{"role":"user","content":prompt}],
            response_format={"type":"json_object"},
            temperature=0.1
        )
        raw = res.choices[0].message.content.strip()
        data = json.loads(raw)
        return {"realism_score": float(data.get("realism_score",0.6)), "category": data.get("category","real"), "explanation": data.get("explanation","")}
    except Exception as e:
        return {"realism_score":0.6, "category":"real", "explanation": f"OpenAI error: {e}"}
