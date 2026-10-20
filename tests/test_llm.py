import json

import pytest

from src import llm


def reply(usage):
    return lambda body: {"model": body["model"], "choices": [{"message": {"content": "{}"}}], "usage": usage}


def test_every_call_appends_one_usage_line(tmp_path):
    log = tmp_path / "usage.jsonl"
    llm.chat([{"role": "user", "content": "hi"}], feature="ask", model="google/gemini-3.8-flash",
             transport=reply({"prompt_tokens": 1650, "completion_tokens": 150, "cost": 0.0018}), log_path=log)
    llm.chat([{"role": "user", "content": "hi"}], feature="ask", model="google/gemini-3.8-flash",
             transport=reply({"prompt_tokens": 10, "completion_tokens": 5, "cost": 0.00001}), log_path=log)
    lines = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == 2
    first = lines[0]
    assert first["model"] == "google/gemini-3.8-flash"
    assert (first["tokens_in"], first["tokens_out"], first["cost_usd"]) == (1650, 150, 0.0018)
    assert first["cost_source"] == "provider"
    assert isinstance(first["latency_ms"], int)
    assert first["feature"] == "ask"


def test_cost_falls_back_to_price_table(tmp_path):
    result = llm.chat([], feature="ask", model="google/gemini-3.8-flash",
                      transport=reply({"prompt_tokens": 1_000_000, "completion_tokens": 0}),
                      log_path=tmp_path / "u.jsonl")
    assert result["cost_usd"] == pytest.approx(0.75)
    assert result["cost_source"] == "price_table"


def test_model_comes_from_env_with_default(monkeypatch):
    monkeypatch.delenv("MODEL", raising=False)
    assert llm.model_name() == "google/gemini-3.8-flash"
    monkeypatch.setenv("MODEL", "other/model")
    assert llm.model_name() == "other/model"


def test_missing_key_raises_before_any_request(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(llm.MissingKey):
        llm.http_transport({"model": "x", "messages": []})
