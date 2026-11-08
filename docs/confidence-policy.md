# Confidence policy · Notice photo

`src/checks.py` `decide()` implements this table. Evidence is checked before the model's own confidence number.

## 1 · Routes

| Route | What it means | What the user sees | What gets created |
|---|---|---|---|
| `accepted` | title, action, and timing are present, evidenced, and consistent | the notice as fact, with the line it came from | a draft the employee can file |
| `confirm` | soft flags only | the value, highlighted, with one question | a draft until the employee confirms |
| `review` | a required field is missing or has no evidence | those fields empty, the photo beside them | a draft a person fills in |
| `rejected` | not a company notice | what it looks like, and a pointer back to the handbook question box | nothing |

## 2 · Signals, per required field

| Field | Signal | Condition | Flag | Hard or soft |
|---|---|---|---|---|
| title, action, timing | value present | `value is None` | `missing` | hard |
| title, action, timing | evidence present | `evidence is None` | `no_evidence` | hard |
| title, action, timing | self-rated confidence | `confidence < 0.6`, and value and evidence both exist | `low_confidence` | soft |
| timing | format is a known rule | value not in the four handbook timings | `unrecognized_timing` | soft |
| contact | known role | value not in office manager, your manager, manager, HR | `unknown_contact` | soft |

Known timings: "at least 5 working days ahead", "the same day", "day one", "before the change reaches main".

## 3 · From flags to a route

```
title evidence is a lunch menu, concert, or birthday, or all required values are null  → rejected
any hard flag                                                                          → review
any soft flag, no hard flag                                                            → confirm
no flags                                                                               → accepted
```

A hard field is shown empty. `decide()` does not copy a guessed value into it.

## 4 · The reason text

| Flag | On screen |
|---|---|
| `missing` | "[Field]: not found on the image" |
| `no_evidence` | "[Field]: we could not find the text this came from" |
| `low_confidence` | "[Field]: we are not sure we read this correctly" |
| `unrecognized_timing` | "Timing: this timing is not a rule we know" |
| `unknown_contact` | "Contact: this person is not on the notice list" |

## 5 · Tests

In `tests/test_checks.py`, hand-written extractions, no API call:

1. Clean time-off card → `accepted`, no flags.
2. Degraded card, action missing → `review`, `action` in `hard`.
3. Timing "sometime next week" at confidence 0.42 → `confirm`.
4. Title evidence "Friday lunch menu" → `rejected`.
5. A value with no evidence → `review`, and low confidence is not the flag.

## 6 · What we measure once it runs

- Share of real photos per route. If most land in review, the photos or the 0.6 line are wrong.
- Wrong accepts are the expensive mistake. Wrong reviews are the annoying one.
- Revisit 0.6 after the first twenty real photos and write a decision record.
