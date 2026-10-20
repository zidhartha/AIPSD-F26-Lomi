# AI Mentor · Spec v1

## Goal

A junior developer in their first two weeks at a 30-person company has no onboarding team. AI Mentor answers their question from the company's own documents, or says the documents do not contain the answer.

## Users

That junior developer. They know the question and not which document answers it.

## Acceptance criteria

- AC1 A question whose best passage scores at or above 0.5 returns `{answer, citations, grounded: true}`. `answer` is that passage. Every citation is a file just retrieved.
- AC2 A question whose best score is below 0.5 returns `{answer: "That is not in the company documents.", citations: [], grounded: false}` and does not call a model.
- AC3 An empty or whitespace-only question returns `{error: "invalid_question", detail: "Question is empty."}`.
- AC4 On the seed corpus, AC1 and AC2 finish in under 50 ms.
- AC5 A citation that was not retrieved is refused with the AC2 sentence. The employee never sees the invented answer.

## Context the agent needs

`data/corpus/*.md` · `docs/spec.md` · `AGENTS.md`. The refusal sentence is the one in AC2. Do not invent another.

## Constraints

Python 3.11. No new dependency in this slice. Tests never call a model or the network. Seed documents are fictional.

## Out of scope

Company signup, subscription plans, employee accounts, progress tracking, quizzes, photo upload, and a model paraphrasing the passage.

## Verification

`python -m pytest -q tests` is green locally and in GitHub Actions. No API key. Three commands in `evals/golden.md` match the stdout written there.

## First slice (Lab 2)

Criteria: AC1, AC2, AC3
Done when: `tests/test_ask.py` passes locally and in CI
Not in this slice: AC5 is tested here because it is a pure check, but a model that writes the answer is later. Photos, accounts, and billing are later.

## Napkin math

This slice calls no model, so cost is $0 per question. The later answer call, at about 1,650 input tokens and 150 output tokens on `google/gemini-3.8-flash` ($0.75 / $3.75 per million, promo price checked 13 October 2026), is about $0.0018 per question. 50 questions/day × $0.0018 × 30 = $2.70 / month.
