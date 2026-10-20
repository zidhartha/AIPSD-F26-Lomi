import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from src import llm, offline
from src.answer import answer_with_trace
from src.retrieve import K, THRESHOLD

ROOT = Path(__file__).resolve().parent
GOLDEN = ROOT / "golden.yaml"
RESULTS = ROOT / "results"


def load_golden(path=GOLDEN):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def check(case, reply):
    if case["expect"] == "refusal":
        return reply.get("grounded") is False, "refused" if reply.get("grounded") is False else "answered instead of refusing"
    if reply.get("grounded") is not True:
        return False, "refused instead of answering"
    if case["source"] not in reply["citations"]:
        return False, f"expected source {case['source']} not cited"
    missing = [m for m in case.get("must_mention", []) if m.lower() not in reply["answer"].lower()]
    if missing:
        return False, f"answer does not mention {missing}"
    return True, "answered from the expected source"


def run(golden, *, chat, mode, k=K, threshold=THRESHOLD):
    rows = []
    for case in golden["questions"]:
        reply, trace = answer_with_trace(case["question"], k=k, threshold=threshold, chat=chat)
        passed, why = check(case, reply)
        rows.append({"id": case["id"], "kind": case["kind"], "question": case["question"], "passed": passed,
                     "why": why, "reply": reply, "trace": trace})
    passed = sum(r["passed"] for r in rows)
    return {
        "run_at": datetime.now().isoformat(timespec="minutes"),
        "mode": mode,
        "model": offline.MODEL if mode == "offline" else llm.model_name(),
        "k": k,
        "retrieval_threshold": threshold,
        "pass_threshold": golden["threshold"],
        "passed": passed,
        "total": len(rows),
        "pass_rate": round(passed / len(rows), 2),
        "gate": "pass" if passed / len(rows) >= golden["threshold"] else "fail",
        "results": rows,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the golden set and save the result in evals/results/.")
    parser.add_argument("--offline", action="store_true", help="use the offline stand-in instead of the model")
    parser.add_argument("--k", type=int, default=K)
    args = parser.parse_args(argv)
    mode = "offline" if args.offline else "live"
    try:
        report = run(load_golden(), chat=offline.chat if args.offline else llm.chat, mode=mode, k=args.k)
    except llm.MissingKey as err:
        print(json.dumps({"error": "missing_key", "detail": str(err)}))
        return 2
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"{datetime.now():%Y-%m-%d-%H%M}-{mode}-k{args.k}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in report["results"]:
        print(f"{row['id']} {row['kind']:<9} {'PASS' if row['passed'] else 'FAIL'}  {row['why']}")
    print(f"{report['passed']}/{report['total']} ({report['pass_rate']}) gate {report['gate']} -> {out.relative_to(ROOT.parent)}")
    return 0 if report["gate"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
