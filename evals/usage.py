import argparse
import json
import statistics
import sys
from pathlib import Path

from src.llm import LOG_PATH


def summarize(lines):
    by_feature = {}
    for line in lines:
        by_feature.setdefault((line["feature"], line["model"]), []).append(line)
    summary = []
    for (feature, model), rows in sorted(by_feature.items()):
        costs = [r["cost_usd"] for r in rows if r["cost_usd"] is not None]
        latencies = sorted(r["latency_ms"] for r in rows)
        summary.append({
            "feature": feature,
            "model": model,
            "calls": len(rows),
            "median_tokens_in": statistics.median(r["tokens_in"] for r in rows),
            "median_tokens_out": statistics.median(r["tokens_out"] for r in rows),
            "median_cost_usd": statistics.median(costs) if costs else None,
            "median_latency_ms": statistics.median(latencies),
            "p95_latency_ms": latencies[min(len(latencies) - 1, round(0.95 * (len(latencies) - 1)))],
        })
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description="Median cost and latency per feature from a usage log.")
    parser.add_argument("log", nargs="?", default=str(LOG_PATH))
    args = parser.parse_args(argv)
    path = Path(args.log)
    if not path.is_file():
        print(json.dumps({"error": "log_not_found", "detail": str(path)}))
        return 2
    lines = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(json.dumps(summarize(lines), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
