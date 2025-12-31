# Embeddings & KNN Reflection similarity Logic

import math
from .models import Reflection
from .state import USER_REFLECTIONS
import hashlib
from typing import List
from .config import USE_PINECONE, SIMILARITY_THRESHOLD
import re

# For the free version of embeddings, remove stopwords from hashing so that they don't dominate useful topic words. 
STOPWORDS = {
    "i", "me", "my", "myself",
    "we", "our", "ours",
    "you", "your", "yours",
    "he", "she", "it", "they",
    "is", "am", "are", "was", "were",
    "be", "been", "being",
    "a", "an", "the",
    "and", "or", "but",
    "about", "to", "of", "in", "on",
    "for", "with", "as",
    "at", "by", "from",
    "that", "this", "these", "those",
    "feel", "feels", "feeling"
}
# Use a slightly more sophisticated embedding - use the "hash trick" - every word goes into the same bucket & different words are statistically spread out
# Every embedding is a fixed length (dim param) so it is compatible with pinecone
# Can later replace this with more sophisticated embeddings such as SentenceTransformers (free, but I would need to upgrade my OS), or OpenAI/Claude (paid).
def embed_text(text: str, dim: int) -> list[float]:
    vec = [0.0] * dim

    tokens = re.findall(r"\b\w+\b", text.lower())

    for token in tokens:
        if token in STOPWORDS:
            continue

        idx = hash(token) % dim
        vec[idx] += 1.0

    return vec

# Better cosine similarity that that works with the hash trick vectors, or later real embeddings. 
# Use when PINECONE is not enabled
def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if len(v1) != len(v2):
        raise ValueError("Vectors must be same length")

    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)

# Free version to get relevant reflections when PINECONE is not enabled
def retrieve_relevant_reflections_local(user_id: str, current_reflection: Reflection, k: int = 3, threshold: float = SIMILARITY_THRESHOLD):
    past_reflections = USER_REFLECTIONS.get(user_id, [])

    # Similarity scoring
    scored = []
    for r in past_reflections:
        if r is current_reflection:
            continue
        score = cosine_similarity(
            current_reflection.embedding,
            r.embedding
        )
        # Only keep matches that pass the similarit threshold
        if(score >= SIMILARITY_THRESHOLD):
            scored.append((score, r))

    # rank and filter
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for score, r in scored[:k] if score > 0]

def retrieve_relevant_reflections(user_id: str, current_reflection: Reflection, k: int = 3):
    if USE_PINECONE:
        # Import here so that pinecone only initializes if the flag is on
        from .vector_store import retrieve_relevant_reflections_pinecone
        return retrieve_relevant_reflections_pinecone(
            user_id, current_reflection, k, SIMILARITY_THRESHOLD
        )
    else:
        return retrieve_relevant_reflections_local(
            user_id, current_reflection, k, SIMILARITY_THRESHOLD
        )
