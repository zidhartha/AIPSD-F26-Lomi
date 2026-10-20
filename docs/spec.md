# Spec v0 · AI Mentor

*Team Lomi. One page. This is the capstone, not HW1.*

## Problem

A junior developer in their first two weeks at a 30-person company has no onboarding team. The rules live in handbooks and policy docs, so they ask the same senior colleague the same basic questions.

## Users

That junior developer. They know the question ("how do I request time off?") and not which document answers it. HR and the senior colleague are the people who stop being interrupted.

## Success criteria

1. A question the handbook answers comes back with the answer and the source document. Measured by a golden question that checks the citation.
2. A question the handbook does not answer is refused in one fixed sentence. It never invents a policy. Measured by a refusal golden question.
3. Median cost per question stays under $0.005 on `google/gemini-3.8-flash`. Measured from `logs/usage.jsonl`.

## Core feature (Weeks 2 to 4 scope)

**Handbook Q&A.** The employee asks one question. The service retrieves the relevant passages from that company's uploaded documents, answers from those passages, and cites them. If nothing scores above the threshold, it refuses before calling the model. A citation that was not retrieved is also a refusal. Week 3 adds one path for a photo of a policy page: extract the text only when the evidence is good enough, otherwise send it to a human. Accounts, billing, and progress charts are not this feature.

## Context list

- The question the employee typed.
- The company's documents, as text, in `data/corpus/` for the first slice. Later, the files an admin uploaded for that workspace.
- The retrieved chunks and their scores. The model sees those chunks, not the whole corpus.
- The refusal sentence, written in this spec, not invented per question.

## Acceptance criteria

1. A question whose best chunk scores at or above the threshold returns `{answer, citations, grounded: true}`, and every citation is one of the chunks just retrieved.
2. A question whose best score is below the threshold returns the refusal sentence, `grounded: false`, and does not call the chat model.
3. An answer that cites a document that was not retrieved is refused. The employee never sees it.

## Napkin math

Retrieval, not the whole handbook: about 1,650 input tokens and 150 output tokens. At the 13 October 2026 OpenRouter promo price for `google/gemini-3.8-flash` ($0.75 / $3.75 per million), that is about $0.0018 per question. 50 questions/day × $0.0018 × 30 = **$2.70 / month**. The standard price doubles it to about $5.40. Putting an 180,000-token handbook into every prompt would be about $0.14 per question instead.

## Risks and safety

- The model states a policy that is not in the documents. Mitigation: refuse when retrieval misses, and check every citation in code.
- One company's handbook is shown to another company's employee. Mitigation: later, documents are scoped to a workspace. The first slice uses one corpus and no shared tenants.
- Someone pastes a real employee's name or review into a test document. Mitigation: seed data is fictional. No real HR files in `data/`.

## Out of scope (for now)

Company signup, subscription plans, employee accounts, progress tracking, quizzes, and editing the handbook from the chat.
