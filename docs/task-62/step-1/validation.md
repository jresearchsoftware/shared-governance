# Joint Step 1 qualification

Task 60 Step 1 and Task 62 Step 1 share one implementation PR but retain separate
scope/assessment in their README records. Frozen accepted guidance:
`61aa3444365b02a27c392d48aa9ea33e85c5d5d4`.

## Results and binding

Local native Linux/Python 3.11 disposable clone, with pinned VibeVM 1.0.7 musl
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`:

| Check | Result / primary log |
| --- | --- |
| Source, links, marker scan, exact export and committed native parity | PASS; 871 files / 1,582 links at `411ad1715a26e48f3ada862be9d6127d9714d36f`; [log](logs/qualify.log). Final evidence files increase counts. |
| Projection lifecycle | 26 passed; [log](logs/projection.log). |
| Distribution/integrity/preservation | 49 passed at `7294832e7e4a7fb9dc65b6549bd0331cc6145f90`; [log](logs/test-distribution.log). |
| Self-adoption / clean committed ready state / recovery | 13 passed; [log](logs/test-self-adoption.log). |
| Release boundary | 11 passed / 6 optional native integration skips; [log](logs/test-release.log). |
| Producer parity | 11 passed / 1 optional native publisher skip; [log](logs/test-publication.log). |
| Exported native ChatGPT install/update lifecycle | PASS; [log](logs/native.log). Real disposable local Git publication/install/update, same versioned-slot projector, optional cache and preserved custom, non-adopting negative. No live remote publication. |
| 4.0.0 → 5.0.0 MAJOR transition | PASS at `7294832e7e4a7fb9dc65b6549bd0331cc6145f90`, existing release CLI with actual PR body and frozen main baseline. |
| Producer projector check at frozen accepted guidance | NO_OP for Instructions and ownership receipt; source/native checks still execute; live_settings_verified=false. |
| Whitespace / protected surfaces | Diff check passed; workflow/publisher binding and frozen 4.0.0 registry/slots have zero diff against accepted baseline. |

Total local suites: **110 passed, 7 explicitly optional skips**, zero remaining
failures. Native ChatGPT lifecycle is additional. Full package and generated
payload bytes at final tested `7294832` are identical to `411ad1715`; only historical
preservation tests changed afterward. Hosted exact-final-head CI supplies final
source/export/transition and regression validation. Its URL/result is bound in the
canonical Outcome, avoiding a self-referential commit solely to record its own CI.

Reproduce with CONTRIBUTING's commands plus `python3 scripts/test-distribution.py`,
`python3 scripts/test-chatgpt-projection.py`, `python3 scripts/test-publication.py`,
and `python3 scripts/qualify-chatgpt.py --vibe <pinned-musl> --source-ref <exact-head>`.
The initial source stage rejected symbolic HEAD (rerun with its full SHA). Native
materialization pruned old slots as its normal behavior; restored those historical
tracked slots with Git before commit, retaining frozen content and accepted routes.

## Corrections and honest limits

Initial projection and native fixtures rejected the literal Task vocabulary in
an otherwise non-adopting common base. Corrected it to neutral client wording,
regenerated through supported tools and reran the affected tests successfully.
Initial distribution checks encoded Task 52's former unchanged RA/TH contract;
bound that historical transition to accepted 4.0.0 and added bounded current-delta
preservation against frozen main. Corrected two fixture setup errors (object-store
selection and export receipt exclusion); final 49/49 passed. The first hosted run
on intermediate `81ce958` had that fixture failure; it is superseded, not final proof.
No production assertion was disabled to pass qualification.

Policy scenario tables are analytical, not model-execution evidence. Static and
CLI/native tests do not prove model compliance, live ChatGPT Settings, protected
remote release or independent acceptance. Existing one-time publisher integrations
were not rerun because publication transport/workflows are unchanged; optional
skips are disclosed, not counted as passes. No credentials, external consumers,
Landscape source/settings, repository protections, release procedures or live
publication were modified. This Task prepares desired text; it does not apply it.

Next boundary: independent substantive assessment of the exact final PR head.
Owner-authorized integration and existing automatic publication remain subsequent,
separate events. Neither Task is closed and no self-approval is supplied.
