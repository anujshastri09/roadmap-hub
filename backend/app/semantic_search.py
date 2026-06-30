"""
A small, dependency-free TF-IDF + cosine-similarity search engine.

Why not use embeddings/sentence-transformers? Those require downloading model
weights (hundreds of MB) and a heavier runtime footprint. TF-IDF is a classic,
well-understood IR technique that still meaningfully beats naive substring
search for this dataset size (a few hundred topics) — it matches on word
importance and overlap rather than requiring an exact keyword hit, e.g. a
query like "handle multiple requests at once" can surface the "asyncio" /
"concurrency" topic even without sharing an exact keyword.

For a production system at larger scale, swap this for a real embedding
model (OpenAI/Cohere embeddings or a local sentence-transformers model) and
a vector store (FAISS/Chroma/pgvector) — the index-building and query
interfaces below are designed to be a drop-in replacement target.
"""

import math
import re
from collections import Counter
from functools import lru_cache

from app.data import ALL_FIELDS

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "at", "by", "for", "with", "about", "and", "or",
    "this", "that", "it", "as", "from", "into", "your", "you", "how", "what",
}


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


class _Document:
    __slots__ = ("field_id", "field_name", "stage_id", "stage_title", "topic", "tokens", "tf")

    def __init__(self, field_id, field_name, stage_id, stage_title, topic):
        self.field_id = field_id
        self.field_name = field_name
        self.stage_id = stage_id
        self.stage_title = stage_title
        self.topic = topic
        text = " ".join(
            [topic["title"], topic["description"]] + [r["title"] for r in topic["resources"]]
        )
        self.tokens = _tokenize(text)
        self.tf = Counter(self.tokens)


@lru_cache(maxsize=1)
def _build_index():
    """Build the TF-IDF index once and cache it in memory for the process lifetime."""
    docs = []
    for field in ALL_FIELDS:
        for stage in field["stages"]:
            for topic in stage["topics"]:
                docs.append(_Document(field["id"], field["name"], stage["id"], stage["title"], topic))

    doc_freq = Counter()
    for doc in docs:
        for term in set(doc.tokens):
            doc_freq[term] += 1

    n_docs = len(docs)
    idf = {term: math.log((1 + n_docs) / (1 + df)) + 1 for term, df in doc_freq.items()}

    doc_vectors = []
    for doc in docs:
        vec = {term: tf * idf.get(term, 0) for term, tf in doc.tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        doc_vectors.append((doc, vec, norm))

    return doc_vectors, idf


def semantic_search(query: str, top_k: int = 8) -> list[dict]:
    """Rank topics by TF-IDF cosine similarity to the query. Returns [] if no terms match."""
    doc_vectors, idf = _build_index()
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    query_tf = Counter(query_tokens)
    query_vec = {term: tf * idf.get(term, 0) for term, tf in query_tf.items()}
    query_norm = math.sqrt(sum(v * v for v in query_vec.values())) or 1.0

    scored = []
    for doc, vec, norm in doc_vectors:
        dot = sum(query_vec.get(term, 0) * weight for term, weight in vec.items())
        if dot <= 0:
            continue
        similarity = dot / (norm * query_norm)
        scored.append((similarity, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {
            "field_id": doc.field_id,
            "field_name": doc.field_name,
            "stage_id": doc.stage_id,
            "stage_title": doc.stage_title,
            "topic": doc.topic,
            "relevance": round(score, 4),
        }
        for score, doc in scored[:top_k]
    ]
