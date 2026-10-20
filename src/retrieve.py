import math
import re
from collections import Counter
from dataclasses import dataclass

from src.corpus import Chunk, load_chunks

K = 5
THRESHOLD = 3.5

STOPWORDS = set(
    """a an and are as at be but by can could do does for from get go got has have how i if in into is it
    its me my of on or our should so than that the their them then there they this to us was we what when
    where which who why will with would you your am been being did doing just need much many any""".split()
)


def tokenize(text):
    tokens = []
    for word in re.findall(r"\w+", text.lower()):
        if word in STOPWORDS:
            continue
        if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
            word = word[:-1]
        tokens.append(word)
    return tokens


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


class Index:
    def __init__(self, chunks, k1=1.5, b=0.75):
        self.chunks = list(chunks)
        self.k1, self.b = k1, b
        self.docs = [Counter(tokenize(c.heading + " " + c.text)) for c in self.chunks]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg_len = sum(self.lengths) / len(self.lengths)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def score(self, terms, i):
        doc, length, total = self.docs[i], self.lengths[i], 0.0
        for t in terms:
            f = doc.get(t, 0)
            if f:
                norm = f + self.k1 * (1 - self.b + self.b * length / self.avg_len)
                total += self.idf[t] * f * (self.k1 + 1) / norm
        return total

    def search(self, question, k=K):
        terms = set(tokenize(question))
        hits = [Hit(c, self.score(terms, i)) for i, c in enumerate(self.chunks)]
        hits = [h for h in hits if h.score > 0]
        hits.sort(key=lambda h: (-h.score, h.chunk.id))
        return hits[:k]


_default = None


def default_index():
    global _default
    if _default is None:
        _default = Index(load_chunks())
    return _default
