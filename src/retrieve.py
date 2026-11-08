"""Vector search, plus hybrid search with BM25."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .chunk import Chunk
from .index import Index
from .llm import embed

RRF_K = 60


@dataclass
class Hit:
    chunk: Chunk
    score: float


def search(index: Index, query: str, k: int = 5) -> list[Hit]:
    query_vector = embed([query])[0]
    scores = index.vectors @ query_vector
    top = np.argsort(-scores)[:k]
    return [Hit(index.chunks[int(position)], float(scores[position])) for position in top]


def rrf(rankings: list[list[int]], k: int = RRF_K) -> list[int]:
    fused: dict[int, float] = {}
    for ranking in rankings:
        for rank, position in enumerate(ranking, start=1):
            fused[position] = fused.get(position, 0.0) + 1.0 / (k + rank)
    return sorted(fused, key=lambda position: -fused[position])


def hybrid(index: Index, query: str, k: int = 5, pool: int = 20) -> list[Hit]:
    query_vector = embed([query])[0]
    cosine = index.vectors @ query_vector
    by_vector = [int(position) for position in np.argsort(-cosine)[:pool]]
    keyword_scores = np.array(index.bm25.scores(query))
    by_keyword = [int(position) for position in np.argsort(-keyword_scores)[:pool] if keyword_scores[position] > 0]
    return [Hit(index.chunks[position], float(cosine[position])) for position in rrf([by_vector, by_keyword])[:k]]
