import json
import os

import pytest

from src.answer import REFUSAL, Reply, answer, check_citations


def reply(text, cites, grounded=True):
    return Reply(answer=text, citations=cites, grounded=grounded)


def model_says(text, cites, grounded=True):
    def fake(prompt, schema=None):
        fake.prompt = prompt
        return {"answer": text, "citations": cites, "grounded": grounded}

    return fake


def no_model(prompt, schema=None):
    raise AssertionError("the model must not be called")


def test_valid_citations_pass():
    assert check_citations(reply("File the HR form [1]. Your manager approves it [2].", [1, 2]), 5) is None


def test_answer_without_markers_is_rejected():
    assert check_citations(reply("File the HR form.", [1]), 5) == "answer has no citations"


def test_citation_to_a_source_never_retrieved_is_rejected():
    problem = check_citations(reply("It costs 20 GEL [7].", [7]), 5)
    assert problem is not None
    assert "never retrieved" in problem and "7" in problem


def test_markers_and_list_must_agree():
    assert "disagree" in check_citations(reply("File the HR form [1].", [1, 2]), 5)


def test_every_sentence_needs_a_citation():
    problem = check_citations(reply("File the HR form [1]. You will love it.", [1]), 5)
    assert problem is not None
    assert problem.startswith("uncited sentence")


def test_refuses_without_calling_the_model_when_nothing_is_relevant(index):
    result = answer(index, "What is the guest cafeteria menu on Friday?", llm=no_model)
    assert result.status == "refused" and result.text == REFUSAL
    assert "below threshold" in result.reason


def test_refuses_when_the_model_says_the_sources_do_not_answer(index):
    result = answer(index, "How do I request time off?", llm=model_says("The sources do not say.", [], False))
    assert result.status == "refused" and result.reason.startswith("model:")


def test_refuses_an_invented_citation(index):
    result = answer(index, "How do I request time off?", llm=model_says("It costs 20 GEL [7].", [7]))
    assert result.status == "refused"
    assert "never retrieved" in result.reason


def test_answered_sources_map_numbers_to_documents(index):
    fake = model_says("File a request in the HR form [1].", [1])
    result = answer(index, "How do I request time off?", llm=fake)
    assert result.status == "answered"
    assert result.sources[0]["n"] == 1
    assert result.sources[0]["doc_id"] == "time-off"
    assert "[1] Time off" in fake.prompt


def test_every_answer_writes_one_log_line(index):
    log = os.environ["MENTOR_ANSWER_LOG"]
    before = sum(1 for _ in open(log, encoding="utf-8")) if os.path.exists(log) else 0
    answer(index, "How do I request time off?", llm=model_says("File the HR form [1].", [1]))
    lines = open(log, encoding="utf-8").read().splitlines()
    assert len(lines) == before + 1
    last = json.loads(lines[-1])
    assert {"question", "status", "best_score", "retrieved", "cited"} <= set(last)


def test_reply_schema_forbids_extra_fields():
    with pytest.raises(Exception):
        Reply.model_validate({"answer": "x [1].", "citations": [1], "grounded": True, "confidence": 0.9})
    assert Reply.model_json_schema()["additionalProperties"] is False
