"""One chunk per markdown section. The title and heading are part of the embedded text."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

MAX_CHARS = 1200
OVERLAP_PARAS = 1


@dataclass
class Chunk:
    id: str
    doc_id: str
    title: str
    section: str
    text: str

    def embed_text(self) -> str:
        return f"{self.title} · {self.section}\n{self.text}"

    def to_dict(self) -> dict:
        return asdict(self)


def _split_long(text: str) -> list[str]:
    if len(text) <= MAX_CHARS:
        return [text]
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    pieces: list[str] = []
    current: list[str] = []
    for paragraph in paragraphs:
        if current and len("\n\n".join(current + [paragraph])) > MAX_CHARS:
            pieces.append("\n\n".join(current))
            current = current[-OVERLAP_PARAS:] if OVERLAP_PARAS else []
        current.append(paragraph)
    if current:
        pieces.append("\n\n".join(current))
    return pieces


def chunk_markdown(doc_id: str, markdown: str) -> list[Chunk]:
    lines = markdown.strip().splitlines()
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else doc_id
    sections: list[tuple[str, list[str]]] = []
    for line in lines[1:]:
        if line.startswith("## "):
            sections.append((line[3:].strip(), []))
        elif sections:
            sections[-1][1].append(line)
        elif line.strip():
            sections.append(("Overview", [line]))
    chunks: list[Chunk] = []
    for section, body in sections:
        text = "\n".join(body).strip()
        if not text:
            continue
        for piece in _split_long(text):
            chunks.append(Chunk(f"{doc_id}#{len(chunks) + 1}", doc_id, title, section, piece))
    return chunks


def load_corpus(root: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(root.rglob("*.md")):
        doc_id = path.relative_to(root).with_suffix("").as_posix()
        chunks.extend(chunk_markdown(doc_id, path.read_text(encoding="utf-8")))
    return chunks
