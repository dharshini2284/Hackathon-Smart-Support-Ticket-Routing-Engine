import numpy as np
import threading
import logging
from sentence_transformers import SentenceTransformer
from typing import List

# --------------------------------------------
# Configuration
# --------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"
NORMALIZE_EMBEDDINGS = True

logger = logging.getLogger(__name__)

# --------------------------------------------
# Thread-safe Lazy Loader
# --------------------------------------------

_model = None
_model_lock = threading.Lock()


def _load_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                logger.info("Loading SentenceTransformer model...")
                _model = SentenceTransformer(MODEL_NAME)
                logger.info("Embedding model loaded successfully.")
    return _model


# --------------------------------------------
# Embedding Functions
# --------------------------------------------

def get_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a single text.
    Handles:
    - Empty strings
    - None input
    - Extremely long input (truncates)
    """

    if text is None:
        text = ""

    text = text.strip()

    if len(text) == 0:
        # Return zero vector to avoid crashes
        return [0.0] * 384

    # Hard limit to avoid memory explosion
    if len(text) > 5000:
        text = text[:5000]

    model = _load_model()

    embedding = model.encode(
        text,
        normalize_embeddings=NORMALIZE_EMBEDDINGS
    )

    return embedding.tolist()


def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Batch embedding generation (more efficient)
    """

    if not texts:
        return []

    cleaned = []
    for t in texts:
        if t is None:
            cleaned.append("")
        else:
            cleaned.append(t[:5000])

    model = _load_model()

    embeddings = model.encode(
        cleaned,
        normalize_embeddings=NORMALIZE_EMBEDDINGS
    )

    return [e.tolist() for e in embeddings]


# --------------------------------------------
# Cosine Similarity
# --------------------------------------------

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Safe cosine similarity calculation
    Handles:
    - Zero vectors
    - Length mismatch
    - NaN values
    """

    if not vec1 or not vec2:
        return 0.0

    if len(vec1) != len(vec2):
        return 0.0

    v1 = np.array(vec1)
    v2 = np.array(vec2)

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = float(np.dot(v1, v2) / (norm1 * norm2))

    # Clamp to avoid floating overflow
    return max(min(similarity, 1.0), -1.0)


# --------------------------------------------
# Semantic Similarity Utility
# --------------------------------------------

def semantic_similarity(text1: str, text2: str) -> float:
    """
    Compute similarity directly between two texts
    """

    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)

    return cosine_similarity(emb1, emb2)