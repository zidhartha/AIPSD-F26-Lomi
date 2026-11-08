"""Pure route for a notice extraction. No model, no clock, no files."""
from __future__ import annotations

from dataclasses import dataclass, field

from .extract import Extraction

REQUIRED = ("title", "action", "timing")
KNOWN_TIMING = {
    "at least 5 working days ahead",
    "the same day",
    "day one",
    "before the change reaches main",
}
KNOWN_CONTACTS = {"office manager", "your manager", "manager", "hr"}
NOT_NOTICE = ("lunch", "menu", "concert", "birthday")

REASON_TEXT = {
    "missing": "{F}: not found on the image",
    "no_evidence": "{F}: we could not find the text this came from",
    "low_confidence": "{F}: we are not sure we read this correctly",
    "unrecognized_timing": "{F}: this timing is not a rule we know",
    "unknown_contact": "{F}: this person is not on the notice list",
}


@dataclass
class Decision:
    route: str
    flags: list[tuple[str, str]]
    hard: set[str] = field(default_factory=set)

    def reasons(self) -> list[str]:
        return [REASON_TEXT.get(kind, "{F}: " + kind).format(F=name.capitalize()) for kind, name in self.flags]


def looks_like_notice(extraction: Extraction) -> bool:
    if all(getattr(extraction, name).value is None for name in REQUIRED):
        return False
    evidence = (extraction.title.evidence or "").lower()
    return not any(word in evidence for word in NOT_NOTICE)


def decide(extraction: Extraction) -> Decision:
    flags: list[tuple[str, str]] = []
    for name in REQUIRED:
        item = getattr(extraction, name)
        if item.value is None:
            flags.append(("missing", name))
        elif item.evidence is None:
            flags.append(("no_evidence", name))
        elif item.confidence < 0.6:
            flags.append(("low_confidence", name))
    timing = extraction.timing.value
    if timing and timing.strip().lower() not in KNOWN_TIMING:
        flags.append(("unrecognized_timing", "timing"))
    contact = extraction.contact.value
    if contact and contact.strip().lower() not in KNOWN_CONTACTS:
        flags.append(("unknown_contact", "contact"))

    if not looks_like_notice(extraction):
        return Decision("rejected", flags)
    hard = {name for kind, name in flags if kind in ("missing", "no_evidence")}
    if hard:
        return Decision("review", flags, hard=hard)
    if flags:
        return Decision("confirm", flags)
    return Decision("accepted", flags)
