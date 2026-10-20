from evals.run import check, load_golden, run
from src import offline


def test_golden_set_has_the_lab4_shape():
    golden = load_golden()
    kinds = [q["kind"] for q in golden["questions"]]
    assert golden["threshold"] == 0.70
    assert len(kinds) == 5 and kinds.count("refusal") >= 1
    for q in golden["questions"]:
        assert q["expect"] == "refusal" or (q["source"] and q["must_mention"])


def test_check_fails_an_answer_from_the_wrong_source():
    case = {"expect": "answer", "source": "a.md#x", "must_mention": ["24"]}
    assert check(case, {"answer": "24 days", "citations": ["b.md#y"], "grounded": True})[0] is False
    assert check(case, {"answer": "24 days", "citations": ["a.md#x"], "grounded": True})[0] is True


def test_check_fails_a_refusal_question_that_was_answered():
    assert check({"expect": "refusal"}, {"answer": "Yes", "citations": ["a.md#x"], "grounded": True})[0] is False


def test_offline_run_reports_a_pass_rate(monkeypatch, tmp_path):
    monkeypatch.setattr(offline, "LOG_PATH", tmp_path / "usage-offline.jsonl")
    report = run(load_golden(), chat=offline.chat, mode="offline")
    assert report["total"] == 5
    assert report["pass_rate"] == round(report["passed"] / 5, 2)
    by_id = {r["id"]: r for r in report["results"]}
    assert by_id["g5"]["passed"] and by_id["g5"]["trace"]["model_called"] is False
