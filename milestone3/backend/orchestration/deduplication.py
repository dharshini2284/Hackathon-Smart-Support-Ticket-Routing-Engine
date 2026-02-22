import time
from typing import List, Dict
import numpy as np

from ml.embeddings import get_embedding

# --------------------------------------------
# Configuration
# --------------------------------------------

SIMILARITY_THRESHOLD = 0.9
TIME_WINDOW_SECONDS = 300
FLOOD_THRESHOLD = 10


# --------------------------------------------
# Utility
# --------------------------------------------

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    if vec1 is None or vec2 is None:
        return 0.0

    denom = (
        np.linalg.norm(vec1)
        * np.linalg.norm(vec2)
    )

    if denom == 0:
        return 0.0

    return float(np.dot(vec1, vec2) / denom)


# --------------------------------------------
# Deduplicator Class
# --------------------------------------------

class Deduplicator:

    def __init__(self):
        self.recent_tickets: List[Dict] = []

    # --------------------------------------------
    # Clean Old Tickets
    # --------------------------------------------

    def _cleanup(self):
        current_time = time.time()

        self.recent_tickets = [
            t for t in self.recent_tickets
            if current_time - t["timestamp"] <= TIME_WINDOW_SECONDS
        ]

    # --------------------------------------------
    # Process Ticket
    # --------------------------------------------

    def process_ticket(self, text: str) -> Dict:
        """
        Returns:
        {
            "is_duplicate": bool,
            "duplicate_count": int,
            "incident": bool
        }
        """

        self._cleanup()

        embedding = get_embedding(text)

        duplicate_count = 0

        for ticket in self.recent_tickets:
            similarity = cosine_similarity(
                embedding,
                ticket["embedding"]
            )

            if similarity >= SIMILARITY_THRESHOLD:
                duplicate_count += 1

        is_duplicate = duplicate_count > 0
        incident_flag = duplicate_count >= FLOOD_THRESHOLD

        # Store current ticket
        self.recent_tickets.append({
            "embedding": embedding,
            "timestamp": time.time()
        })

        return {
            "is_duplicate": is_duplicate,
            "duplicate_count": duplicate_count,
            "incident": incident_flag
        }

def get_flood_metrics(deduplicator: Deduplicator) -> Dict:
    current_rate = len(deduplicator.recent_tickets)
    threshold = 10
    window_seconds = 300

    status = "surge" if current_rate >= threshold else "normal"

    return {
        "current_rate": current_rate,
        "threshold": threshold,
        "status": status,
        "window_seconds": window_seconds
    }

    def get_flood_metrics(deduplicator):
        current_rate = len(deduplicator.recent_tickets)
        threshold = 10
        window_seconds = 300

        status = "surge" if current_rate >= threshold else "normal"

        return {
            "current_rate": current_rate,
            "threshold": threshold,
            "status": status,
            "window_seconds": window_seconds
        }