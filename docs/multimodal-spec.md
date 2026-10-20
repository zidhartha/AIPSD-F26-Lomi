# Multimodal spec · Notice photo

The input is a photo of one printed company notice. The handbook text already lives in `data/corpus/`. This slice only reads the card in the employee's hand.

## 1 · The input

- **What the user has in their hand:** a one-page company notice, such as the time-off card in the welcome packet.
- **How it reaches us:** a phone photo, JPEG.
- **Typical quality:** indoor light, sometimes a thumb or a crease across one line.
- **What we will never accept:** faces, ID documents, another person's personal data, or a photo that is not a company notice.

The four files in `tests/images/` are synthetic cards rendered from the handbook wording. They stand in for phone photos. The fields and the routes are the same.

## 2 · The fields

| Field | Type after normalisation | Required | Normalisation rule | Example value | Example evidence |
|---|---|---|---|---|---|
| title | string | yes | the notice name, as printed | Time off | Time off |
| action | string | yes | the thing the employee must do, as printed | File a request in the HR form | File a request in the HR form |
| timing | string | yes | one of the known rules, lowercased for the check, value kept as printed | at least 5 working days ahead | at least 5 working days ahead |
| contact | string | no | who handles it, as printed | your manager | your manager |

Every field returns `value`, `evidence`, `confidence`. `value` and `evidence` are `null` when the line cannot be read. A guess is never a value.

## 3 · The schema

The request sends `Extraction.model_json_schema()` from `src/extract.py`. The reply is checked with `Extraction.model_validate`.

```python
class Field(BaseModel):
    value: str | None
    evidence: str | None
    confidence: float  # 0..1

class Extraction(BaseModel):
    title: Field
    action: Field
    timing: Field
    contact: Field
```

## 4 · Acceptance criteria

1. Given `tests/images/clean.jpg`, a valid extraction of the clean card has a non-null value and evidence for title, action, and timing.
2. Given the degraded card's extraction (action unreadable), `decide()` returns `review`, and `action` is in `hard`. It is never accepted, and the missing action is not prefilled.
3. Given `tests/images/not-applicable.jpg`'s extraction (a lunch menu), the route is `rejected` and nothing is created.
4. The image is downscaled to a longest side of 1024 px before the model call. One notice call is expected under $0.01 and under 15 seconds. The logged call, not this sentence, is the measurement.
5. `decide()` makes no model call. `python -m pytest -q tests/test_checks.py tests/test_images.py` is green with no API key.

## 5 · Test images (in `tests/images/`)

| File | What it is | What we expect |
|---|---|---|
| `clean.jpg` | Time-off notice, every line readable | accepted |
| `degraded.jpg` | Same card, the action line covered | review, action flagged hard |
| `ambiguous.jpg` | Timing printed as "sometime next week??" | confirm, timing flagged |
| `not-applicable.jpg` | A Friday lunch menu | rejected |

## 6 · Model and budget

- Model: `google/gemini-3.8-flash` via OpenRouter, env `MODEL`. It is the course default for image input and JSON schema.
- Cost from `logs/usage.jsonl` on 2026-10-20: clean card $0.002447 (1813 in, 290 out, 5228 ms); degraded card $0.002702 (1813 in, 358 out, 10457 ms). Both under $0.01 and under 15 seconds.
- Expected volume: about 5 notice photos a day. At $0.0027 each, that is about $0.40 a month.

## 7 · Out of scope for this slice

- Multiple pages, batch upload, handwriting, and languages other than English.
- Creating the leave request. A human still files the HR form.

## 8 · Stretch

- Run the extraction twice and flag fields whose values disagree. Not in this slice.
