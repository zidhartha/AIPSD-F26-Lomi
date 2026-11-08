# 0001 · search_handbook takes a question, not a path, and only reads

**Status:** accepted · 2026-10-22

## Context

The AI Mentor capstone answers an employee's question from the company's documents. For HW2 I wrapped the retrieval step as a tool a model can call. The obvious first design was `read_document(path)`: the model names a file, the tool returns its text.

## Decision

The tool is `search_handbook(query, top_k)`. The model supplies a *question*, never a file location. The code decides which files exist and opens only `.md` files under `data/corpus/`. The query is constrained by a pattern (letters, digits, spaces and light punctuation; no slashes or markup) and `top_k` is bounded to 1–5. The contract forbids extra fields and has no identity field. The tool writes nothing.

## Alternatives

- **`read_document(path)`.** Simplest, but the model chooses the path, so `../../.env` or any file on disk is reachable. Rejected: it fails the least-privilege test — a hijacked model could read anything.
- **Return a full grounded answer (call the model inside the tool).** Rejected: it needs a key, cannot run in CI with no model, and couples retrieval to generation. Retrieval is the piece worth exposing as a tool; the answer is assembled by the loop around it.

## Consequences

- Even a fully hijacked model can do only one small, read-only thing: get back handbook passages. There is no path, no write, and no identity to abuse.
- The pattern is the load-bearing lock. The red run (`hw2/Irakligig/evidence.md`) shows that removing it lets `../../.env` reach the function. Golden case `a1` keeps it in place.
- Retrieval stays testable with no model and no key, so it runs in CI and blocks a merge when the contract is weakened.
