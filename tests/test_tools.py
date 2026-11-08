"""search_handbook, called directly with validated contracts, plus the locks that must hold.

No model and no key: these run in CI like every other test in tests/.
"""
import pytest

from src import tools
from src.contracts import SearchHandbook


def search(query, **kw):
    return tools.search_handbook(SearchHandbook(query=query, **kw))


def test_finds_the_right_document():
    r = search("how do I request paid time off?")
    assert r.grounded and r.top_doc == "time-off.md" and r.count >= 1


def test_a_different_question_finds_a_different_document():
    assert search("what is the remote work policy?").top_doc == "remote-work.md"


def test_top_k_bounds_the_number_of_passages():
    assert search("company account password portal", top_k=1).count == 1


def test_a_question_the_handbook_does_not_cover_is_refused():
    with pytest.raises(tools.ToolFailure, match="does not cover"):
        search("who won the football match yesterday?")


def test_the_error_names_the_next_step_and_leaks_no_path():
    try:
        search("who won the football match yesterday?")
    except tools.ToolFailure as e:
        assert "human" in str(e).lower()
        assert "corpus" not in str(e).lower() and "/" not in str(e)


def test_no_tool_writes_or_deletes():
    assert not any(t.writes for t in tools.TOOLS.values())
    assert not any(w in name for name in tools.TOOLS for w in ("delete", "remove", "update", "write"))


def test_the_tool_is_offered_to_a_visitor_because_it_reads_only():
    assert "search_handbook" in tools.tools_for(None)


# ---- both doors read the same contract (contracts.py is the single source of truth) ----

def test_schema_comes_from_the_contract_and_forbids_extra_fields():
    s = tools.TOOLS["search_handbook"].schema()["function"]["parameters"]
    assert s["additionalProperties"] is False                       # extra="forbid"
    assert "pattern" in s["properties"]["query"]                    # a pattern on the string
    assert s["properties"]["top_k"]["maximum"] == 5                 # bounds on the number


def test_contract_has_no_identity_field():
    assert "student" not in SearchHandbook.model_fields
    assert "user" not in SearchHandbook.model_fields
