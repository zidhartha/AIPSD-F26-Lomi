from src.checks import decide
from src.extract import Field


def test_clean_notice_is_accepted(clean):
    decision = decide(clean)
    assert decision.route == "accepted"
    assert decision.flags == []
    assert decision.hard == set()


def test_degraded_notice_goes_to_review_with_hard_action(degraded):
    decision = decide(degraded)
    assert decision.route == "review"
    assert ("missing", "action") in decision.flags
    assert decision.hard == {"action"}
    assert "Action: not found on the image" in decision.reasons()


def test_ambiguous_timing_asks_for_confirmation(ambiguous):
    decision = decide(ambiguous)
    assert decision.route == "confirm"
    assert ("low_confidence", "timing") in decision.flags
    assert ("unrecognized_timing", "timing") in decision.flags
    assert decision.hard == set()


def test_lunch_menu_is_rejected(not_applicable):
    assert decide(not_applicable).route == "rejected"


def test_value_without_evidence_is_hard_and_not_prefilled(clean):
    clean.action = Field(value="File a request in the HR form", evidence=None, confidence=0.99)
    decision = decide(clean)
    assert decision.route == "review"
    assert ("no_evidence", "action") in decision.flags
    assert "action" in decision.hard
    assert ("low_confidence", "action") not in decision.flags


def test_unknown_contact_alone_is_confirm(clean):
    clean.contact = Field(value="the intern", evidence="the intern", confidence=0.9)
    decision = decide(clean)
    assert decision.route == "confirm"
    assert ("unknown_contact", "contact") in decision.flags
    assert decision.hard == set()
