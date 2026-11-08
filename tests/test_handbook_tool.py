"""The function-calling door: valid calls run, bad calls do not, identity stays out."""
import json

from src.act import call_tool
from src.contracts import HandbookLookup
from src.tools import TOOLS, Tool, lookup_handbook, tools_for


def _call(arguments, caller=None, name="lookup_handbook", allowed=None):
    call = {"id": "t", "name": name, "arguments": json.dumps(arguments)}
    return call_tool(call, tools_for(caller) if allowed is None else allowed, caller)


def test_a_handbook_question_returns_the_document_name():
    result = lookup_handbook(HandbookLookup(question="How do I request time off?"))
    assert result.doc == "time-off"
    assert result.title == "Time off"
    assert "HR form" in result.passage
    assert "\\" not in result.doc and ".md" not in result.doc


def test_invalid_arguments_never_reach_the_tool(monkeypatch):
    def boom(args):
        raise AssertionError("tool ran")

    monkeypatch.setitem(TOOLS, "lookup_handbook", Tool("lookup_handbook", HandbookLookup, boom))
    out = _call({"question": "../../.env"})
    assert out["ok"] is False
    assert "invalid arguments" in out["error"]
    assert "question" in out["error"]


def test_a_tool_that_was_not_offered_does_not_run():
    out = _call({"question": "How do I request time off?"}, name="delete_handbook", allowed={})
    assert out["ok"] is False
    assert "delete_handbook" in out["error"]


def test_an_identity_field_is_refused():
    out = _call({"question": "How do I request time off?", "user_id": "s999"}, caller="s123")
    assert out["ok"] is False
    assert "user_id" in out["error"]
    assert "s123" not in json.dumps(out)


def test_a_number_outside_its_bounds_is_refused():
    out = _call({"question": "How do I request time off?", "max_chars": 5000})
    assert out["ok"] is False
    assert "max_chars" in out["error"]


def test_one_log_line_per_call_and_no_caller():
    import os
    from pathlib import Path

    path = Path(os.environ["MENTOR_TOOL_LOG"])
    before = path.read_text(encoding="utf-8").count("\n") if path.exists() else 0
    out = _call({"question": "How do I request time off?"}, caller="s123")
    lines = path.read_text(encoding="utf-8").splitlines()[before:]
    assert out["ok"] is True
    assert len(lines) == 1
    assert "s123" not in lines[0]
