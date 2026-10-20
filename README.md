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

## What runs today

The first slice is handbook Q&A over a fictional company's documents ([data/corpus/](data/corpus/)), plus turning a photo of a policy page into text with a confidence check. Python 3.11, standard library only.

```
pip install -r requirements.txt
python -m src.ask "How do I request time off?"             # needs OPENROUTER_API_KEY
python -m src.ask --offline "How do I request time off?"   # no key, stand-in model
python -m src.extract page.jpg                             # photo of a policy page
python -m evals.run                                        # golden set; --offline without a key
python -m pytest -q tests                                  # no key, no network
```

Replies are `{answer, citations, grounded}`. A question the documents do not answer gets one fixed refusal sentence, not a guess. The key and model come from the environment (`OPENROUTER_API_KEY`, `MODEL`; see [.env.example](.env.example)).

- **Spec:** [docs/spec.md](docs/spec.md) · **Design Review:** [docs/DESIGN-REVIEW.md](docs/DESIGN-REVIEW.md)
- **Evaluation:** [evals/golden.yaml](evals/golden.yaml), 5 questions; latest offline run 4/5 (0.80), [evals/results/](evals/results/)
- **Team:** [TEAM-CONTRACT.md](TEAM-CONTRACT.md) · roles in [docs/TEAM-REPO.md](docs/TEAM-REPO.md)
