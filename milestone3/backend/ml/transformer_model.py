import time
import logging
from typing import Dict

import torch
from transformers import pipeline

# --------------------------------------------
# Model Configuration
# --------------------------------------------

MODEL_NAME = "facebook/bart-large-mnli"

CANDIDATE_LABELS = [
    "Technical",
    "Billing",
    "Legal"
]

# --------------------------------------------
# Load Model (Lazy Singleton)
# --------------------------------------------

_classifier = None


def _get_model():
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "zero-shot-classification",
            model=MODEL_NAME,
            device=0 if torch.cuda.is_available() else -1
        )
    return _classifier


# --------------------------------------------
# Main Classification Function
# --------------------------------------------

def classify_ticket(text: str) -> str:
    """
    Uses transformer zero-shot classification.
    Returns category label.
    """

    if not text or not text.strip():
        return "Technical"

    model = _get_model()

    result = model(
        text,
        candidate_labels=CANDIDATE_LABELS
    )

    return result["labels"][0]


# --------------------------------------------
# Urgency Scoring
# --------------------------------------------

def get_urgency_score(text: str) -> float:
    """
    Predicts urgency level between 0 and 1.
    Uses semantic classification.
    """

    if not text or not text.strip():
        return 0.1

    urgency_labels = [
        "critical production issue",
        "urgent problem",
        "normal request"
    ]

    model = _get_model()

    result = model(
        text,
        candidate_labels=urgency_labels
    )

    top_label = result["labels"][0]

    if top_label == "critical production issue":
        return 0.95
    elif top_label == "urgent problem":
        return 0.8
    else:
        return 0.4