import time

import pytest

from src.ask import REFUSAL, ask, guard

CALLED = False


def boom():
    global CALLED
    CALLED = True
    raise AssertionError("model was called")


def test_time_off_cites_the_handbook():
    result = ask("How do I request time off?", complete=boom)
    assert result["grounded"] is True
    assert result["citations"] == ["time-off.md"]
    assert "HR form" in result["answer"]
    assert CALLED is False


def test_unknown_question_refuses_without_a_model():
    result = ask("What is the office dog's name?", complete=boom)
    assert result == {"answer": REFUSAL, "citations": [], "grounded": False}
    assert CALLED is False


@pytest.mark.parametrize("question", ["", "   "])
def test_empty_question_is_an_error(question):
    assert ask(question) == {"error": "invalid_question", "detail": "Question is empty."}


def test_invented_citation_is_refused():
    result = guard(["secret-policy.md"], ["time-off.md"], "You get 40 extra days.")
    assert result["grounded"] is False
    assert result["answer"] == REFUSAL
    assert "40 extra days" not in result["answer"]


def test_lookup_is_under_50ms():
    start = time.perf_counter()
    ask("How do I request time off?")
    assert time.perf_counter() - start < 0.05
