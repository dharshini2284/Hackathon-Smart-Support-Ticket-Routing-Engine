import re
from typing import Dict

# --------------------------------------------
# Lightweight Category Rules
# --------------------------------------------

CATEGORY_KEYWORDS = {
    "Technical": [
        "error", "bug", "crash", "down", "outage",
        "not working", "failed", "issue", "server",
        "latency", "timeout", "broken", "database"
    ],
    "Billing": [
        "invoice", "refund", "charge", "billing",
        "payment", "subscription", "price",
        "credit card", "double charged"
    ],
    "Legal": [
        "contract", "compliance", "gdpr", "lawsuit",
        "legal", "policy", "privacy", "terms"
    ]
}

# --------------------------------------------
# Urgency Keywords
# --------------------------------------------

CRITICAL = [
    "critical", "production down", "data loss",
    "security breach", "outage"
]

HIGH = [
    "urgent", "asap", "immediately",
    "major", "high priority"
]

MEDIUM = [
    "problem", "issue", "error", "delay"
]


# --------------------------------------------
# Helper Functions
# --------------------------------------------

def _clean_text(text: str) -> str:
    if text is None:
        return ""
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


# --------------------------------------------
# Category Classification
# --------------------------------------------

def lightweight_classify(text: str) -> str:
    """
    Fast keyword-based classifier.
    Never throws error.
    """

    text = _clean_text(text)

    if not text:
        return "Technical"

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for word in keywords:
            if word in text:
                score += 1
        scores[category] = score

    # If all zero → default Technical
    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "Technical"

    return best_category


# --------------------------------------------
# Lightweight Urgency Score
# --------------------------------------------

def lightweight_urgency(text: str) -> float:
    """
    Returns urgency score between 0 and 1.
    Deterministic and ultra-fast.
    """

    text = _clean_text(text)

    if not text:
        return 0.1

    for word in CRITICAL:
        if word in text:
            return 0.95

    for word in HIGH:
        if word in text:
            return 0.8

    for word in MEDIUM:
        if word in text:
            return 0.6

    # Default low urgency
    return 0.2


# --------------------------------------------
# Category Vector (For Skill Routing)
# --------------------------------------------

CATEGORY_VECTORS: Dict[str, Dict[str, float]] = {
    "Technical": {"Technical": 1.0, "Billing": 0.0, "Legal": 0.0},
    "Billing": {"Technical": 0.0, "Billing": 1.0, "Legal": 0.0},
    "Legal": {"Technical": 0.0, "Billing": 0.0, "Legal": 1.0}
}


def get_category_vector(category: str) -> Dict[str, float]:
    """
    Returns skill vector for routing optimization.
    """

    if category not in CATEGORY_VECTORS:
        return CATEGORY_VECTORS["Technical"]

    return CATEGORY_VECTORS[category]