# Pattern Journal · Irakligig · Weeks 5 to 7

*Copied from `docs/journal/Irakligig.md`. One entry per week: the pattern, one place I used or saw it, what I noticed, one thing I would do differently.*

## Week 5 · 2026-10-22 · Tool Contract

**Pattern:** Tool Contract.

**Where I used it:** I wrapped our capstone's retrieval step, `search_handbook`, as a tool with a contract in `src/contracts.py`. My first instinct was a `read_document(path)` tool, which was simpler to write. Then I noticed the model would be the one choosing `path`, and nothing stopped it choosing a file outside the handbook. I changed the input to a *question*, not a location, and put a pattern on the query string and bounds on `top_k`.

**What I noticed:** a contract is not input validation for correctness, it is a limit on what the tool can be *asked* to do. The question "what is the worst thing a confused model could ask for here?" changed the design more than any feature requirement did.

**What I'd do differently:** write the adversarial case first. I wrote the three normal cases, got them green, and only then thought about the path-smuggling case. Next time the attacker's case comes before the happy path.

## Week 6 · 2026-10-29 · Session State

**Pattern:** Session State (identity and scope come from the session, never from the model).

**Where I used it:** my tool reads only and needs no identity, so I checked this pattern by looking at where it would bite if `search_handbook` ever became a write tool. In `src/act.py`, `call_tool()` passes identity from the caller, never from the arguments, and `tools_for()` hides write tools from a visitor. I wrote `test_contract_has_no_identity_field` so that a `student` or `user` field can never quietly appear in my contract.

**What I noticed:** the dangerous version of an identity leak is the one that still passes the happy-path test. A tool that lets the model set `student=` would work perfectly in a demo and be wrong in exactly the way you cannot see. The test has to assert the *absence* of the field, not the presence of a correct result.

**What I'd do differently:** write the "the model cannot set identity" test before asking an agent to write any tool that touches a person, instead of after.

## Week 7 · 2026-11-05 · Supervised Autonomy Loop

**Pattern:** Supervised Autonomy Loop (CI is the supervisor that blocks a weakened contract).

**Where I used it:** the red run. On a throwaway branch I removed the pattern from my own contract and ran the gate. The adversarial case `../../.env` reached the function and came back `grounded: True` — the tool answered an attacker's string as a real question. Two tests went red and the merge was blocked.

**What I noticed:** I had assumed the function body was keeping me safe, because the tool "worked". It was the contract, one line, that kept me safe. Removing it did not throw an error; it silently did the wrong thing. A gate that only runs the happy path would have merged that change. The supervisor has to test the refusals.

**What I'd do differently:** keep the red run as a permanent regression test, not a one-off demo. The failing case I reproduced by hand is exactly the test that should stay in the suite so the lock can never be removed by accident again — which is what `evals/tools/Irakligig.yaml` case `a1` now is.
