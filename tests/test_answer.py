import json

import pytest

from src.answer import REFUSAL, answer_with_trace, ask

TIME_OFF = "How do I request time off?"


def fake_chat(reply):
    calls = []

    def chat(messages, *, feature, **kwargs):
        calls.append(messages)
        text = reply if isinstance(reply, str) else json.dumps(reply)
        return {"text": text, "cost_usd": 0.0, "latency_ms": 1}

    chat.calls = calls
    return chat


def never_called(*args, **kwargs):
    raise AssertionError("the chat model must not be called")


def test_grounded_answer_cites_a_retrieved_chunk():
    chat = fake_chat({"answer": "Use the HR portal, 10 working days ahead.", "citations": [1], "grounded": True})
    reply = ask(TIME_OFF, chat=chat)
    assert reply == {
        "answer": "Use the HR portal, 10 working days ahead.",
        "citations": ["time-off.md#how-to-request-time-off"],
        "grounded": True,
    }
    assert "time-off.md#how-to-request-time-off" in chat.calls[0][1]["content"]


def test_below_threshold_refuses_without_calling_the_model():
    reply, trace = answer_with_trace("Does Brightpath pay for a gym membership?", chat=never_called)
    assert reply == {"answer": REFUSAL, "citations": [], "grounded": False}
    assert trace["stage"] == "retrieval_below_threshold"
    assert trace["model_called"] is False


@pytest.mark.parametrize("citations", [[9], [0], [], ["1"], [True], None])
def test_citation_that_was_not_retrieved_is_refused(citations):
    chat = fake_chat({"answer": "Ask your lead.", "citations": citations, "grounded": True})
    reply, trace = answer_with_trace(TIME_OFF, chat=chat)
    assert reply["grounded"] is False and reply["answer"] == REFUSAL
    assert trace["stage"] == "citation_not_retrieved"


def test_model_saying_not_grounded_becomes_the_fixed_refusal():
    chat = fake_chat({"answer": "", "citations": [], "grounded": False})
    reply, trace = answer_with_trace(TIME_OFF, chat=chat)
    assert reply["answer"] == REFUSAL
    assert trace["stage"] == "model_refused"


def test_unparseable_reply_is_refused_not_raised():
    reply, trace = answer_with_trace(TIME_OFF, chat=fake_chat("Sure! You get 24 days."))
    assert reply["answer"] == REFUSAL
    assert trace["stage"] == "unparseable_reply"


def test_fenced_json_reply_is_accepted():
    chat = fake_chat('```json\n{"answer": "Via the HR portal.", "citations": [1], "grounded": true}\n```')
    assert ask(TIME_OFF, chat=chat)["grounded"] is True


@pytest.mark.parametrize("question", ["", "   ", None])
def test_blank_question_is_a_request_error(question):
    reply = ask(question, chat=never_called)
    assert reply["error"] == "invalid_question"
    assert reply["detail"]
