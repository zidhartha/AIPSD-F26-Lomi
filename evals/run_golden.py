"""Run the golden set and save the result.

    python -m src.index
    python -m evals.run_golden
    MENTOR_OFFLINE=1 python -m evals.run_golden
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from src.answer import answer
from src.index import load
from src.llm import CHAT_MODEL, OFFLINE, embed_model_name

GOLDEN = Path("evals/golden.yaml")
RESULTS = Path("evals/results")


def score(item: dict, result) -> tuple[bool, list[str]]:
    why = []
    if result.status != item["expect"]:
        why.append(f"expected {item['expect']}, got {result.status} ({result.reason or 'no reason'})")
    if item["expect"] == "answered":
        cited = {source["doc_id"] for source in result.sources}
        why += [f"did not cite {doc}" for doc in item.get("must_cite", []) if doc not in cited]
        text = result.text.lower()
        why += [f"did not mention '{phrase}'" for phrase in item.get("must_mention", []) if phrase.lower() not in text]
    return (not why), why


def run(k: int = 5) -> dict:
    spec = yaml.safe_load(GOLDEN.read_text(encoding="utf-8"))
    index = load()
    rows = []
    for item in spec["items"]:
        result = answer(index, item["question"], k=k)
        ok, why = score(item, result)
        rows.append(
            {
                "id": item["id"],
                "type": item["type"],
                "pass": ok,
                "why": why,
                "status": result.status,
                "answer": result.text,
                "cited": [source["doc_id"] for source in result.sources],
            }
        )
        print(f"{'PASS' if ok else 'FAIL'}  {item['id']}  {item['type']:<9}  {item['question']}")
        for line in why:
            print(f"        {line}")
    passed = sum(row["pass"] for row in rows)
    report = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": "offline" if OFFLINE else "live",
        "chat_model": "offline/extractive" if OFFLINE else CHAT_MODEL,
        "embed_model": embed_model_name(),
        "k": k,
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 2),
        "threshold": spec["threshold"],
        "items": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    (RESULTS / f"{stamp}-{report['mode']}-k{k}.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"\n{passed}/{len(rows)} passed · pass rate {report['pass_rate']:.2f} · threshold {spec['threshold']}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=5)
    report = run(k=parser.parse_args().k)
    sys.exit(0 if report["pass_rate"] >= report["threshold"] else 1)
