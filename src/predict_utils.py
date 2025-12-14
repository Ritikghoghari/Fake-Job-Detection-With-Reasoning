# src/predict_utils.py
import os
import joblib
import pandas as pd
from scipy.sparse import hstack
from sentence_transformers import SentenceTransformer

from data_processing import prepare_features
from explain_with_openai import openai_realism_and_reasoning
from fake_keywords import find_fake_keywords
from generation_checks import boilerplate_score, perplexity, generation_score_from_perplexity, most_similar_template
from structure_validation import validate_structure
from web_verification import verify_job_online_safe
from email_check_openai import enhanced_email_check
from integrity_check import assess_tamper

PATH_TFIDF = os.path.join(os.path.dirname(__file__), "../model_artifacts/lightgbm_pipeline.joblib")
PATH_ISO = os.path.join(os.path.dirname(__file__), "../model_artifacts/iso_forest.joblib")

_embedder = SentenceTransformer("all-MiniLM-L6-v2")

def _load_tfidf():
    if os.path.exists(PATH_TFIDF):
        d = joblib.load(PATH_TFIDF)
        return d.get("model"), d.get("tf")
    return None, None

def _load_iso():
    if os.path.exists(PATH_ISO):
        return joblib.load(PATH_ISO)
    return None

def _local_embed(text: str):
    try:
        return _embedder.encode([text])[0].tolist()
    except Exception:
        return [0.0]

def predict_single(job_dict: dict):
    df = pd.DataFrame([job_dict])
    df = prepare_features(df)
    text = df["combined"].iloc[0]

    # ML model (optional)
    model_tfidf, tf = _load_tfidf()
    scam_prob_model = 0.5
    if model_tfidf and tf:
        try:
            X_text = tf.transform([text])
            meta = df[["company_present","has_salary","location_present"]].values
            X = hstack([X_text, meta])
            scam_prob_model = float(model_tfidf.predict_proba(X)[:,1][0])
        except Exception:
            scam_prob_model = 0.5

    # Document-level OpenAI realism
    openai_doc = openai_realism_and_reasoning(text, scam_prob_model)
    realism_score = float(openai_doc.get("realism_score", 0.6))
    doc_category = openai_doc.get("category", "real")
    doc_explanation = openai_doc.get("explanation", "")

    # Anomaly (optional)
    iso = _load_iso()
    anomaly_score = None
    if iso:
        try:
            emb = _local_embed(text)
            d = iso.decision_function([emb])[0]
            anomaly_score = 1.0 - (d + 0.5)
        except Exception:
            anomaly_score = None

    # Structure & generation checks
    structure = validate_structure(text)
    gen_ppl = perplexity(text)
    gen_score = generation_score_from_perplexity(gen_ppl)
    gen_info = {"boilerplate_score": boilerplate_score(text), "perplexity": gen_ppl, "generation_score": gen_score, "most_similar_template": most_similar_template(text)}

    fake_keywords = find_fake_keywords(text)

    # Web verification (SAFE)
    web = verify_job_online_safe(text)
    web_verdict = web.get("web_verdict", "uncertain")
    web_conf = float(web.get("confidence", 0.5))
    company_name = web.get("company_detected", "Unknown")

    # Email checks
    emails_checked = enhanced_email_check(text, company=company_name)
    email_invalid = any(e.get("status") == "invalid" for e in emails_checked)

    # Integrity / Tamper check (HYBRID)
    integrity = assess_tamper(text, company=company_name)
    tamper_score = float(integrity.get("tamper_score", 0.0))
    suspicious_spans = integrity.get("suspicious_spans", [])
    tamper_expl = integrity.get("explanation", "")

    # FINAL SAFE-MODE DECISION (with tamper rules)
    final_label = "REAL"  # default

    # 1) If web says real -> keep real
    if web_verdict in ("real", "likely_real") and web_conf >= 0.55:
        final_label = "REAL"

    # 2) If web says likely_fake/fake -> Trust it more (updated logic)
    if web_verdict in ("likely_fake", "fake"):
        # High confidence web result is enough on its own
        if web_conf >= 0.70:
            final_label = "FAKE_SCAM"
        else:
            # Moderate confidence: require 1 corroboration (was 2)
            supports = 0
            if email_invalid:
                supports += 1
            if scam_prob_model > 0.70: # lowered from 0.80
                supports += 1
            if len(fake_keywords) >= 1: # lowered from 3
                supports += 1
            
            if supports >= 1:
                final_label = "FAKE_SCAM"
            else:
                # If explicitly "fake" (stronger than likely), lean to caution
                if web_verdict == "fake":
                    final_label = "FAKE_SCAM"
                else:
                    final_label = "REAL"

    # 3) Tamper override for recognized brands: if tamper_score high -> FAKE_MODIFIED
    safe_brands = {"mercedes", "mercedes-benz", "bmw", "google", "amazon", "siemens", "bosch", "meta", "microsoft", "apple", "dhl", "picnic"}
    brand_detected = any(b in text.lower() for b in safe_brands) or (company_name and any(b in str(company_name).lower() for b in safe_brands))
    if brand_detected and tamper_score >= 0.65:
        final_label = "FAKE_MODIFIED"

    # 4) Auto-generated detection (only if realism low)
    if gen_score > 0.9 and realism_score < 0.4:
        final_label = "AUTO_GENERATED"

    # 5) Final protective strong-flag rule (require multiple strong signals)
    strong_flags = 0
    if scam_prob_model > 0.85:
        strong_flags += 1
    if email_invalid:
        strong_flags += 1
    if len(fake_keywords) >= 3:
        strong_flags += 1
    if web_verdict in ("fake", "likely_fake") and web_conf > 0.75:
        strong_flags += 1
    if strong_flags >= 2:
        final_label = "FAKE_SCAM"

    return {
        "final_label": final_label,
        "scores": {"scam_prob_model": round(scam_prob_model, 3), "realism_score": round(realism_score, 3), "anomaly_score": None if anomaly_score is None else round(anomaly_score, 3)},
        "gemini": {"explanation": doc_explanation, "realism_score": realism_score, "category": doc_category},
        "web_verification": web,
        "emails_checked": emails_checked,
        "fake_keywords": fake_keywords,
        "structure": structure,
        "generation_checks": gen_info,
        "integrity": integrity,
        "raw": {"openai_doc_category": doc_category}
    }
