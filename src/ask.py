import json
import re
import sys
from pathlib import Path

REFUSAL = "That is not in the company documents."
THRESHOLD = 0.5
CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus"
STOP = {"a", "an", "the", "how", "do", "i", "to", "is", "what", "my", "of", "for", "in", "on"}


def tokens(text):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [word for word in words if word not in STOP and len(word) > 1]


def load_corpus(path=CORPUS):
    docs = []
    for file in sorted(path.glob("*.md")):
        docs.append({"id": file.name, "text": file.read_text(encoding="utf-8")})
    return docs


def retrieve(question, corpus):
    query = tokens(question)
    if not query:
        return []
    hits = []
    for doc in corpus:
        words = set(tokens(doc["text"]))
        score = len(set(query) & words) / len(set(query))
        hits.append({"id": doc["id"], "text": doc["text"], "score": score})
    hits.sort(key=lambda hit: hit["score"], reverse=True)
    return hits


def refusal():
    return {"answer": REFUSAL, "citations": [], "grounded": False}


def guard(citations, retrieved_ids, answer):
    if not citations or any(citation not in retrieved_ids for citation in citations):
        return refusal()
    return {"answer": answer, "citations": list(citations), "grounded": True}


def ask(question, corpus=None, complete=None):
    if not isinstance(question, str) or not question.strip():
        return {"error": "invalid_question", "detail": "Question is empty."}
    docs = load_corpus() if corpus is None else corpus
    hits = retrieve(question, docs)
    if not hits or hits[0]["score"] < THRESHOLD:
        return refusal()
    top = hits[0]
    return guard([top["id"]], [top["id"]], top["text"])


def main(argv=None):
    question = " ".join(sys.argv[1:] if argv is None else argv)
    print(json.dumps(ask(question)))


if __name__ == "__main__":
    main()
