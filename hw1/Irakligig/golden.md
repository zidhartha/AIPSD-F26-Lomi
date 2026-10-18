# Golden questions

All run from the repo root with `--now 2026-10-20T09:00:00`.

| #   | Input                                | Expected                                                                                               | Actual                                                                                                                                   | Pass/Fail | How I ran it                                                                                        |
| --- | ------------------------------------ | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------- |
| 1   | `"Chess Club"`                       | 3 events in order: Weekly Blitz (21 Oct), Endgame Workshop (23 Oct), Rapid Tournament (28 Oct); exit 0 | Weekly Blitz (2026-10-21T18:00, B101), Endgame Workshop (2026-10-23T17:00, B204), Rapid Tournament (2026-10-28T10:00, Main Hall); exit 0 | PASS      | `python hw1/Irakligig/src/cli.py "Chess Club" --now 2026-10-20T09:00:00` then `echo $LASTEXITCODE`  |
| 2   | `"Robotics Club"` (only past events) | `[]`; exit 0                                                                                           | `[]`; exit 0                                                                                                                             | PASS      | `python hw1/Irakligig/src/cli.py "Robotics Club" --now 2026-10-20T09:00:00; echo $LASTEXITCODE`     |
| 3   | `"Chess Clubb"` (unknown club)       | `{"error": "club_not_found"}`; exit 1                                                                  | `{"error": "club_not_found"}`; exit 1                                                                                                    | PASS      | `python hw1/Irakligig/src/cli.py "Chess Clubb" --now 2026-10-20T09:00:00` then `echo $LASTEXITCODE` |

Also ran the unit tests: `python -m pytest hw1/Irakligig` → 11 passed.
