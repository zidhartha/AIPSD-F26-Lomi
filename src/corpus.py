import re
from dataclasses import dataclass
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parents[1] / "data" / "corpus"


@dataclass(frozen=True)
class Chunk:
    id: str
    doc: str
    heading: str
    text: str


def slug(heading):
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def split_document(name, markdown):
    chunks = []
    heading, lines = None, []
    for line in markdown.splitlines():
        if line.startswith("## "):
            if heading and "".join(lines).strip():
                chunks.append(Chunk(f"{name}#{slug(heading)}", name, heading, " ".join(lines).strip()))
            heading, lines = line[3:].strip(), []
        elif heading is not None and not line.startswith("# "):
            lines.append(line.strip())
    if heading and "".join(lines).strip():
        chunks.append(Chunk(f"{name}#{slug(heading)}", name, heading, " ".join(lines).strip()))
    return chunks


def load_chunks(corpus_dir=CORPUS_DIR):
    chunks = []
    for path in sorted(Path(corpus_dir).glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        chunks.extend(split_document(path.name, path.read_text(encoding="utf-8")))
    return chunks
