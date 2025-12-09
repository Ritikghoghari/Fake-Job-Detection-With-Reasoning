# src/structure_validation.py
import re

def validate_structure(text: str):
    # returns completeness_score (0..1) and missing fields list
    flags = {
        "title": False,
        "company": False,
        "location": False,
        "salary": False,
        "description": False,
        "apply_info": False
    }
    lower = text.lower()
    if len(text.strip()) > 50:
        flags["description"] = True
    if re.search(r"\b(company|company:)\b", lower):
        flags["company"] = True
    if re.search(r"\b(location|city|remote|hybrid)\b", lower):
        flags["location"] = True
    if re.search(r"\b\d{1,3}[.,]?\d{0,3}\s*(€|eur|\$|£)\b", text):
        flags["salary"] = True
    if re.search(r"\bapply\b|\bsubmit\b|\bemail\b|\bapply here\b", lower):
        flags["apply_info"] = True
    completeness = sum(1 for v in flags.values() if v) / max(1, len(flags))
    missing = [k for k, v in flags.items() if not v]
    return {"completeness_score": round(completeness, 3), "missing_fields": missing, "completeness_flags": flags}
