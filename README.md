# AI Mentor

**Answers a new employee's question from the company's own documents, or says the documents do not contain the answer.**
CS6920 capstone · Fall 2026 · Lomi · Davit Jincharadze, Irakli Giguashvili, Elene Kifiani, Sandro Paikidze

> Status: Lab 4 · a question is answered from a retrieved handbook chunk and cited, or refused. A notice photo is still routed by `decide()`.

## The problem
A junior developer in their first two weeks at a 30-person company has no onboarding team. The rules live in handbooks, so they ask the same senior colleague the same basic questions.

## Demo
[2-minute narrated video, YouTube Unlisted: link] · [backup demo video, Week 14] · [deployed URL, from Week 12]

## Run it
```
copy .env.example .env
pip install -r requirements.txt
python -m src.ask "How do I request time off?"
python -m pytest -q tests
```

The passage lookup does not read `.env`. The notice command does, when `OPENROUTER_API_KEY` is set in the shell. Do not commit `.env`.

```
python -m src.extract tests/images/clean.jpg
```

Grounded answer. Rebuild the index when the embedding model changes. `MENTOR_OFFLINE=1` runs this with no key and does not measure a live model.

```
python -m src.index
python -m src.answer "How do I request time off?"
python -m evals.run_golden
```

## How it works
A question is embedded, mixed with a keyword score, and refused before any chat model when the best cosine is under the threshold. Otherwise the model must cite a retrieved chunk. A notice photo is downscaled, read into value / evidence / confidence, and routed by `decide()`.
Key decisions: [docs/decisions/](docs/decisions/)

## Does it work? (evidence)
| What we measure | Result | Where |
|---|---|---|
| Unit tests | Lab 2, notice, and grounding tests, no API key | `tests/` |
| Clean notice, live | four fields, each with evidence, 2026-10-20 | `logs/usage.jsonl` |
| Degraded notice, live | route `review`, hard field `action` | same log |
| Golden set | 5/5 live, pass rate 1.00, threshold 0.70 | `evals/results/2026-10-20-1734-live-k5.json` |
| Cost per notice | $0.002447 and $0.002702 | `logs/usage.jsonl` |

## Case study
[docs/case-study.md: what we built, what we delegated, what we measured, what we would change · from Week 13]

## Team and how we work
[Names and roles] · Team rules: [docs/TEAM-REPO.md](docs/TEAM-REPO.md) · Spec: [docs/spec.md](docs/spec.md) · Delegation log: [docs/delegation-log.md](docs/delegation-log.md) · Journals: [docs/journal/](docs/journal/) · Team contract: [TEAM-CONTRACT.md](TEAM-CONTRACT.md)
