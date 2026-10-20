"""BM25 keyword scores. No extra dependency."""
from __future__ import annotations

import math
import re
from collections import Counter


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(tokens(doc)) for doc in docs]
        self.length = [sum(counts.values()) for counts in self.tf]
        self.avg = sum(self.length) / max(1, len(self.length))
        document_frequency = Counter(token for counts in self.tf for token in counts)
        count = len(docs)
        self.idf = {
            token: math.log(1 + (count - freq + 0.5) / (freq + 0.5))
            for token, freq in document_frequency.items()
        }

    def scores(self, query: str) -> list[float]:
        query_tokens = tokens(query)
        scored = []
        for counts, length in zip(self.tf, self.length):
            score = 0.0
            for token in query_tokens:
                if token in counts:
                    freq = counts[token]
                    score += self.idf[token] * freq * (self.k1 + 1) / (
                        freq + self.k1 * (1 - self.b + self.b * length / self.avg)
                    )
            scored.append(score)
        return scored
