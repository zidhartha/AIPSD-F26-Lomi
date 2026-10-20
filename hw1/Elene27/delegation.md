# HW1 delegation log · Course prerequisite checker

**Date:** 2026-10-20 · **Tool:** Cursor agent · **Rung on the Autonomy Ladder:** 3 (the agent writes and commits files on a branch; I read the diff, the author line and the command output before anything reaches main)

**What I delegated.** "Clone the team repo and add my HW1: a course prerequisite checker in my own `hw1/` folder, same five items as the brief. Do not change my teammates' work."

**What it got wrong.** Before I said whose homework it was, the agent assumed I was the repo owner. It edited my teammate's `hw1/zidhartha/` folder (dated his journal, moved his test) and pushed that to a new branch. I caught it by reading the `git show` output: the author line was my name on a commit that only touched his folder. The branch was never merged; I had the agent delete it from GitHub and locally, and checked `main` against `origin/main` with `git diff --stat` (empty).

**Second miss.** To find my GitHub username, the agent tried to list the credential manager's saved accounts, and then to read another repo outside this project. Both were blocked. The username has to come from me, not from the machine.

**How I verified the feature.** Read `test_prereqs.py` before trusting "passed". Ran `python -m pytest hw1/Elene27` (16 passed) and the three commands in `golden.md`, pasting stdout and exit codes from that run. `git show --stat` lists only files under `hw1/Elene27/`.

**What I would change next time.** Put "my GitHub username is ..., only touch `hw1/<it>/`" in the first prompt. The agent fills a missing fact with a guess, and a guess about whose folder this is cost more than any code bug.
