# Joint Step 2 qualification

Task 60 and Task 62 retain separate Step 2 scope/assessment records. Accepted
guidance is frozen at `61aa3444365b02a27c392d48aa9ea33e85c5d5d4`.

## Observed results

Disposable Debian WSL checkout, Python 3.11, exact candidate
`20b8ee67e6532671370623197bc650508c9d8c53`. The package/generated payload is
identical to `8a9dc716717ab679f3d51cbbddc822f888abb953`, used for the earlier
suite/native runs; only historical-link navigation and distribution tests changed.

| Check | Result / primary log |
| --- | --- |
| Projection lifecycle and status | 28 passed; [log](logs/projection.log). |
| Distribution, historical compatibility, integrity | 49 passed at `20b8ee67e`; [log](logs/distribution.log). |
| Self-adoption, committed ready state and recovery | 13 passed; [log](logs/self-adoption.log). |
| Release boundary regressions | 11 passed / 6 optional native publisher/dependency skips; [log](logs/release.log). |
| Producer/publisher parity | 11 passed / 1 optional native publisher skip; [log](logs/publication.log). |
| Native exported ChatGPT install/update | PASS; [log](logs/native.log). Disposable local Git consumer only; preserved custom, cache export and non-adopting negative. |
| Source, links, marker scan, exact export and native parity | PASS, 880 tracked files / 1,595 links before adding logs; [log](logs/qualify.log). |
| Whole-package transition with updated PR body | PASS, 4.0.0 → 5.0.0 MAJOR; [log](logs/transition.log). |
| Producer desired Instructions at frozen accepted guidance | NO_OP, schema 4; [log](logs/chatgpt-check.log). No ChatGPT receipt or Settings proof. |
| Whitespace and protected surfaces | `git diff --check 61aa344 HEAD` passed. Frozen 4.0.0 source/slots, publisher workflows/binding have zero diff against accepted main. TH/IR and desired Instructions have zero diff from the Step 1 result. |

Total local suites: **112 passed, 7 optional skips**, zero remaining failures.
Pinned VibeVM 1.0.7 musl digest:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
The accepted producer-source/export and native install commands regenerated the
unaccepted 5.0.0 source/slot/lock together. Native install normally pruned old
slots; historical tracked slots were restored from Git before committing. Native
absolute location/timestamps are generated metadata, not authority.

Reproduce with CONTRIBUTING's qualifier/release/self-adoption commands plus
`python3 scripts/test-distribution.py`, `python3 scripts/test-chatgpt-projection.py`,
`python3 scripts/test-publication.py` and
`python3 scripts/qualify-chatgpt.py --vibe <pinned-musl> --source-ref <exact-SHA>`.
The source qualifier and hosted CI bind the final evidence-bearing result in the
canonical Outcome; this avoids a commit cycle solely to name its own SHA.

## Corrections and limits

The initial distribution run found an outdated assertion that the onboarding
guide was annotation-only. The historical assertion is now bound to accepted
3.0.0; a separate current-guide comparison permits exactly the authorized receipt
and conditional-application corrections against accepted 4.0.0. The qualifier
found a historical relative link to the removed receipt; only that link now pins
accepted Git content. Historical substantive claims and Step 1 records remain.
No production check was bypassed to obtain passing results.

Tests cover first/missing/stale generation; content diffs and regeneration of local
generated edits without an ownership gate; containing-commit and same-output
generator/source/dependency NO_OP; changed custom/base/binding; selected cache
update/disable (including edited and empty cache outputs); validation of the full
local path plan before writes; native lock/slot/INDEX corruption and route checks;
and conditional CLI application status for check/update/NO_OP/cache-only paths.

Policy scenario tables are analytical. CLI/native tests prove neither live
Settings currentness nor model compliance or independent acceptance. Seven
unchanged one-time publisher/dependency probes were skipped proportionately,
not counted as passes. No downstream cold-install requirement, new registry,
ownership replacement, worktree-clean gate or release choreography was added.
No external consumer, live Settings, protected configuration, merge, release or
Task closure was changed. Independent exact-head assessment remains the next
boundary; hosted CI status and any material warnings are recorded in the Outcome.
