import json
import re

from src import llm
from src.retrieve import K, THRESHOLD, default_index

REFUSAL = "I could not find this in the company documents, so I will not guess. Please ask HR or your team lead."

SYSTEM = """You are AI Mentor, answering a new employee's question from their company's documents.
Use only the numbered sources below. Never add a rule, number or date that is not in them.
Quote money and durations exactly as the source writes them.
Answer in the language of the question, in at most three sentences.
Reply with one JSON object and nothing else:
{"answer": "<text>", "citations": [<source numbers you used>], "grounded": true}
If the sources do not answer the question, reply {"answer": "", "citations": [], "grounded": false}."""


def refusal():
    return {"answer": REFUSAL, "citations": [], "grounded": False}


def build_messages(question, hits):
    sources = "\n\n".join(
        f"[{n}] ({hit.chunk.id}) {hit.chunk.heading}: {hit.chunk.text}" for n, hit in enumerate(hits, 1)
    )
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Sources:\n{sources}\n\nQuestion: {question}"},
    ]


def parse_reply(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        reply = json.loads(text)
    except json.JSONDecodeError:
        return None
    return reply if isinstance(reply, dict) else None


def check_citations(reply, hits):
    citations = reply.get("citations")
    if not isinstance(citations, list) or not citations:
        return None
    ids = []
    for n in citations:
        if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= len(hits):
            return None
        ids.append(hits[n - 1].chunk.id)
    return list(dict.fromkeys(ids))


def answer_with_trace(question, *, index=None, k=K, threshold=THRESHOLD, chat=llm.chat):
    if not isinstance(question, str) or not question.strip():
        return {"error": "invalid_question", "detail": "question must be a non-empty string"}, {"stage": "input"}
    hits = (index or default_index()).search(question, k=k)
    trace = {"retrieved": [(h.chunk.id, round(h.score, 2)) for h in hits], "model_called": False}
    if not hits or hits[0].score < threshold:
        return refusal(), {**trace, "stage": "retrieval_below_threshold"}
    result = chat(build_messages(question, hits), feature="ask")
    trace.update(model_called=True, cost_usd=result.get("cost_usd"), latency_ms=result.get("latency_ms"))
    reply = parse_reply(result["text"])
    if reply is None:
        return refusal(), {**trace, "stage": "unparseable_reply"}
    if reply.get("grounded") is not True or not str(reply.get("answer", "")).strip():
        return refusal(), {**trace, "stage": "model_refused"}
    cited = check_citations(reply, hits)
    if cited is None:
        return refusal(), {**trace, "stage": "citation_not_retrieved"}
    return {"answer": reply["answer"].strip(), "citations": cited, "grounded": True}, {**trace, "stage": "answered"}


def ask(question, **kwargs):
    return answer_with_trace(question, **kwargs)[0]
