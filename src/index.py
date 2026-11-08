"""NumPy index of handbook chunks. Refuses to load vectors from another embedding model."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .bm25 import BM25
from .chunk import Chunk, load_corpus
from .llm import embed, embed_model_name

CORPUS = Path("data/corpus")
INDEX_DIR = Path("data/index")
BATCH = 64


class IndexMismatch(RuntimeError):
    """The saved vectors were built with a different embedding model."""


@dataclass
class Index:
    chunks: list[Chunk]
    vectors: np.ndarray
    model: str
    bm25: BM25 | None = None

    def __post_init__(self):
        if self.bm25 is None:
            self.bm25 = BM25([chunk.embed_text() for chunk in self.chunks])


def build(chunks: list[Chunk]) -> Index:
    texts = [chunk.embed_text() for chunk in chunks]
    parts = [embed(texts[start : start + BATCH]) for start in range(0, len(texts), BATCH)]
    return Index(chunks, np.vstack(parts).astype(np.float32), embed_model_name())


def save(index: Index, out: Path = INDEX_DIR) -> None:
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "vectors.npy", index.vectors)
    (out / "chunks.json").write_text(
        json.dumps([chunk.to_dict() for chunk in index.chunks], indent=1),
        encoding="utf-8",
    )
    meta = {
        "embed_model": index.model,
        "dims": int(index.vectors.shape[1]),
        "chunks": len(index.chunks),
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


def load(src: Path = INDEX_DIR) -> Index:
    meta = json.loads((src / "meta.json").read_text(encoding="utf-8"))
    if meta["embed_model"] != embed_model_name():
        raise IndexMismatch(
            f"index built with {meta['embed_model']}, queries use {embed_model_name()}. "
            "Vectors from different models are not comparable: rebuild with python -m src.index"
        )
    chunks = [Chunk(**row) for row in json.loads((src / "chunks.json").read_text(encoding="utf-8"))]
    return Index(chunks, np.load(src / "vectors.npy"), meta["embed_model"])


if __name__ == "__main__":
    built = build(load_corpus(CORPUS))
    save(built)
    print(f"indexed {len(built.chunks)} chunks from {CORPUS} with {built.model} -> {INDEX_DIR}", file=sys.stderr)
