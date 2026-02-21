from transformers import pipeline
import time
import re

# Zero-shot classifier
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

CATEGORIES = ["Billing", "Technical", "Legal"]

def classify_ticket(text: str):
    result = classifier(text, CATEGORIES)
    
    return result["labels"][0]  # highest confidence label


sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

CRITICAL_KEYWORDS = [
    "down", "outage", "critical", "breach", "crashed",
    "not working", "failure", "broken", "data loss"
]

HIGH_KEYWORDS = [
    "urgent", "asap", "immediately", "losing customers",
    "production", "security", "major"
]

MEDIUM_KEYWORDS = [
    "error", "issue", "problem", "failed", "delay"
]


def get_urgency_score(text: str):
    text_lower = text.lower()

    # Base score from sentiment (normalized)
    sentiment = sentiment_pipeline(text)[0]

    if sentiment["label"] == "NEGATIVE":
        base_score = sentiment["score"] * 0.4
    else:
        base_score = 0.1

    keyword_score = 0

    for word in CRITICAL_KEYWORDS:
        if word in text_lower:
            keyword_score = 0.9
            break

    if keyword_score == 0:
        for word in HIGH_KEYWORDS:
            if word in text_lower:
                keyword_score = 0.75
                break

    if keyword_score == 0:
        for word in MEDIUM_KEYWORDS:
            if word in text_lower:
                keyword_score = 0.5
                break

    urgency = max(base_score, keyword_score)

    return round(min(urgency, 1.0), 2)