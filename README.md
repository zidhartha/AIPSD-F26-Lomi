# AI Mentor

**Answers a new employee's question from the company's own documents, or says the documents do not contain the answer.**
CS6920 capstone · Fall 2026 · Lomi · Davit Jincharadze, Irakli Giguashvili, Elene Kifiani, Sandro Paikidze

> Status: Lab 2 · a question returns the matching handbook passage and its filename, or a refusal. No model call yet.

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

This slice does not read `.env`. The file is there for the later model call. Leave `OPENROUTER_API_KEY` empty. Do not commit `.env`.

## How it works
[Architecture diagram or a short list: components, which model does what, where data lives.]
Key decisions: [docs/decisions/](docs/decisions/)

## Does it work? (evidence)
| What we measure | Result | Where |
|---|---|---|
| Unit tests | [passing in CI] | [link to latest CI run] |
| Golden set | [x / 5 in Week 4 · x / 10 at threshold 0.70 from Week 11] | evals/ |
| Cost per request | [$] | [log or dashboard] |
| p95 latency | [s] | [log or dashboard] |

## Case study
[docs/case-study.md: what we built, what we delegated, what we measured, what we would change · from Week 13]

## Team and how we work
[Names and roles] · Team rules: [docs/TEAM-REPO.md](docs/TEAM-REPO.md) · Spec: [docs/spec.md](docs/spec.md) · Delegation log: [docs/delegation-log.md](docs/delegation-log.md) · Journals: [docs/journal/](docs/journal/) · Team contract: [TEAM-CONTRACT.md](TEAM-CONTRACT.md)
