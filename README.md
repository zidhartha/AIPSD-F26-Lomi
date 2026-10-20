# AI Mentor

AI Mentor is an AI-powered employee onboarding and training platform that helps companies turn their internal documentation into an interactive, personalized learning experience.

Instead of searching through lengthy documents or repeatedly asking colleagues for help, employees can interact with an AI mentor that answers questions, explains company policies, and guides them through their onboarding journey using the company’s own knowledge base.

## Overview

Every company has its own guidelines, workflows, policies, and procedures. AI Mentor brings this information together in one place and makes it accessible through an intelligent, conversational assistant.

Companies can create a workspace, subscribe to a plan, upload their documentation, and register employees individually. Each employee receives access to a mentor that helps them understand company-specific information and learn how to perform their role effectively.

## Key Features

### 📚 Company Knowledge Base

* Upload company documentation, handbooks, policies, and guidelines.
* Organize internal knowledge in one centralized location.
* Make company-specific information accessible to authorized employees.

### 💬 AI-Powered Q&A

* Ask questions in natural language.
* Receive answers based on the company’s uploaded documentation.
* Get relevant explanations and references to source documents when available.
* Receive a clear response when the available documentation does not contain the answer.

### 🎓 Personalized Training

* Learn company procedures step by step.
* Explore complex guidelines through simplified explanations.
* Practice with examples and interactive knowledge checks.
* Reinforce understanding through follow-up questions and exercises.

### 👥 Employee Management

* Create individual employee accounts.
* Connect employees to their respective company workspaces.
* Provide employees with access to relevant onboarding materials.
* Support a more personalized training experience.

### 🏢 Company Subscriptions

* Allow companies to subscribe to the platform.
* Provide a dedicated workspace for each organization.
* Support centralized management of documentation and employee access.

### 📈 Training Progress

* Track employee learning progress.
* Identify topics that require additional attention.
* Help managers and HR teams understand onboarding progress.

## How It Works

1. **Create a company workspace** — The company registers and chooses a subscription plan.
2. **Upload documentation** — Administrators add internal guidelines, policies, and training materials.
3. **Register employees** — Each employee receives an individual account.
4. **Start learning** — Employees ask questions or follow guided training activities.
5. **Learn and improve** — The AI mentor explains procedures, answers questions using company resources, and helps employees check their understanding.

## Target Audience

* Companies onboarding new employees
* HR and people operations teams
* Managers and team leaders
* Employees learning new roles and responsibilities
* Organizations seeking to centralize internal knowledge

## Core Principles

* **Accuracy:** Answers should be grounded in the company’s available documentation.
* **Transparency:** The AI should acknowledge when information is unavailable rather than inventing policies.
* **Personalization:** Employees should receive guidance suited to their learning needs.
* **Security:** Company documentation and employee information should be protected through appropriate access controls.
* **Efficiency:** Reduce repetitive questions and make internal knowledge easier to access.

## Vision

Our vision is to make AI Mentor a reliable virtual workplace mentor that helps every employee learn, adapt, and grow while enabling companies to deliver consistent and scalable onboarding and training.

AI Mentor brings company knowledge closer to the people who need it — whenever they need it.

---

## The capstone today

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
