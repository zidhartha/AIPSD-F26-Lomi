from evals.usage import summarize


def line(cost, latency, feature="ask"):
    return {"feature": feature, "model": "m", "tokens_in": 1000, "tokens_out": 100, "cost_usd": cost,
            "latency_ms": latency}


def test_summary_reports_median_cost_and_p95_latency_per_feature():
    rows = [line(0.001, 100), line(0.002, 200), line(0.003, 3000), line(0.01, 900, feature="extract")]
    ask, extract = summarize(rows)
    assert (ask["feature"], ask["calls"], ask["median_cost_usd"], ask["median_latency_ms"]) == ("ask", 3, 0.002, 200)
    assert ask["p95_latency_ms"] == 3000
    assert extract["calls"] == 1


def test_summary_ignores_unknown_costs():
    assert summarize([line(None, 10), line(0.004, 20)])[0]["median_cost_usd"] == 0.004
