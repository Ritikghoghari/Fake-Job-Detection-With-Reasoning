# src/generation_checks.py
import math, re

def boilerplate_score(text: str) -> float:
    # crude heuristic: ratio of repeated short phrases
    phrases = re.findall(r'\b(?:the|and|to|for|with|our|we)\b', text.lower())
    if not text:
        return 0.0
    ratio = min(1.0, len(phrases) / max(10, len(text.split())/10))
    return round(ratio, 3)

def perplexity(text: str) -> float:
    # stub: return heuristic based on average word repetition and length
    words = text.split()
    if not words:
        return 999.0
    uniq = len(set(words))
    p = max(10.0, min(200.0, (len(words) / uniq) * 20.0))
    return round(p, 2)

def generation_score_from_perplexity(ppl: float) -> float:
    # map perplexity to 0..1 where low ppl -> templated (lower=more template-like)
    if ppl is None:
        return 0.5
    s = max(0.0, min(1.0, 1.0 - (ppl - 10) / 190.0))
    return round(s, 3)

def most_similar_template(text: str):
    # stub - return None usually
    return None
