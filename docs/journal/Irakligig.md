# Pattern Journal · Irakligig

*My running Pattern Journal for the whole course. One entry per week.*

## Week 1 · Context as Budget

**Where I used it:** working with an AI assistant on a coding task, I can give it too much information or leave out details that matter. The useful part of this pattern is choosing what the AI needs before asking it to write code: a short description of the goal, the relevant files, and the expected result can be more useful than a long prompt with unrelated details.

**What I'd do differently:** explain the task and its limits first, then add more context only when the AI needs it.

## Week 2 · Spec to Ship

**Where I used it:** for my Python Club Events Lookup, I wrote the spec and golden questions before asking the agent to build the code. I ran the tests myself, all 11 passed, and I broke the code on purpose to check that a test could fail. Getting a working result is not enough; I need a way to check whether the result does what I asked for.

**What I'd do differently:** include more edge cases in my golden questions before asking the agent to write the code.

## Week 3 · Uncertainty-Aware UX

**Where I used it:** in a multimodal task the model may receive more than one type of input, such as text and an image. The app should not act completely certain when the input is unclear; it should make uncertainty visible instead of giving an answer that sounds correct but may be wrong.

**What I'd do differently:** test unclear or incomplete inputs, not just examples where the answer is obvious, and check how the app responds when it cannot interpret an input.

## Week 4 · Grounded Generation

**Where I used it:** for a document-based question-answering app, answers should come from the documents the app can access, with citations I can check. If the documents do not contain the answer, the app should say so instead of making something up.

**What I'd do differently:** include questions whose answers are missing from the documents and verify the app refuses to guess, and check that citations support the actual answers.

## Week 5 · 2026-10-22 · Tool Contract

**Where I used it:** I wrapped our capstone's retrieval step, `search_handbook`, as a tool with a contract in `src/contracts.py`. My first instinct was a `read_document(path)` tool, but the model would choose `path`, and nothing stopped it choosing a file outside the handbook. I changed the input to a *question*, not a location, with a pattern on the query and bounds on `top_k`.

**What I noticed:** a contract is a limit on what the tool can be *asked* to do, not just input validation for correctness.

**What I'd do differently:** write the adversarial case first, before the happy path.

## Week 6 · 2026-10-29 · Session State

**Where I used it:** my tool reads only and needs no identity, so I checked this pattern where it would bite a future write tool. In `src/act.py`, identity comes from the caller, never the arguments, and `tools_for()` hides write tools from a visitor. I wrote a test so a `student` or `user` field can never quietly appear in my contract.

**What I noticed:** the dangerous identity leak is the one that still passes the happy-path test, so the test must assert the field is *absent*.

**What I'd do differently:** write the "model cannot set identity" test before asking an agent to write any tool that touches a person.

## Week 7 · 2026-11-05 · Supervised Autonomy Loop

**Where I used it:** the red run. I removed the pattern from my own contract on a throwaway branch; the adversarial `../../.env` case reached the function and came back `grounded: True`. Two tests went red and the merge was blocked.

**What I noticed:** the function "working" was not what kept me safe — the one-line contract was. Removing it did not error, it silently did the wrong thing, so the gate has to test the refusals.

**What I'd do differently:** keep the red run as a permanent regression test (golden case `a1`), not a one-off demo.
