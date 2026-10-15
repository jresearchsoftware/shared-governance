# Step 6 validation and warning disposition

Executor evidence only; independent assessment remains pending. Starting head:
`d560862527859144d69bddd89db51a7882f87517`. Frozen accepted source-main:
`15e8191435a126e54b4d1739a73fab112e01c081`. No rebase or authority repin.

## Local results

| Evidence | Observed result |
| --- | --- |
| [Regression before](../logs/regression-before.txt) | New exported-tool case fails on the original implementation: the CLI wrongly returns 0 for a same-slot unreceipted conditional route. |
| [Regression after](../logs/regression-after.txt) | Same case passes after correction, including positive declared route, exact-slot isolation and refused-update preservation. |
| [Lifecycle](../logs/projection.txt) | 23 passed; real Git snapshots and the exact exported tool, including existing adjacent route/hash/condition and lifecycle cases. |
| [Distribution](../logs/distribution.txt) | 33 passed. |
| [Release](../logs/release.txt) | 10 passed; six opt-in native resolver/publisher integrations skipped, not counted as passes. |
| [Self-adoption](../logs/self-adoption.txt) | 12 passed after complete native state was committed. |
| [Native source comparison](../logs/native-verify.json) | Exact export, local registry, installed slot/receipt, lock and native routes agree; 14 payload files. |
| [Installed common tool](../logs/installed-producer-check.json) | Read-only producer `check`: Instructions and maintenance evidence both NO_OP; Sources disabled. |
| [Version boundary](../logs/package-boundary.txt) | Whole-package 2.2.0 → 2.3.0 minor, unchanged candidate version within Step 6. |

The corrected package/exported-tool suites used source commit
`423e08b6af7178bbb8e4a703b3fe856dc291763a`; the complete native snapshot and
successful clone-based self-adoption suite used
`fcd33517fe8e61493149a8931cbe144b2f8ae1a0`. Later changes add evidence and fix
two report links, with no further implementation or package payload change.
Final exact-head qualification, CI checkout/job/check/annotations and final
remote identity are recorded in the canonical PR Outcome, avoiding a circular
self-referential commit claim here.

## Native reproduction and semantic scope

Pinned VibeVM 1.0.7 musl executable SHA-256 matched the repository toolchain:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Used the accepted `prepare-distribution.py --producer-source` path and native
offline install with the existing in-tree registry. The prior task-generated
candidate lock was moved to task-local backup before fresh resolution of the
revised unpublished 2.3.0, as supported by accepted self-adoption guidance.
No URL/receipt hash was hand-edited or public distribution ref changed.

Both producer and historical Relay regeneration reported Instructions NO_OP;
the producer's active receipt records the corrected tool and Step 6 authority.
The historical Step 5 preview receipt retains its old tool identity; reproduction
output is task-local evidence, not a rewrite of the earlier result. Complete
Step 1-5 artifacts, root policy, all seven protocol/compact-boot bytes, common
base, custom/binding/Instructions and workflows were compared with the starting
head and are unchanged. The existing three-layer lifecycle remains intact.

## Corrections and limits

- The first self-adoption invocation ran too early: it cloned the intermediate
  source commit before native regeneration was committed, giving 12 setup errors
  (`distribution bytes differ: tools/chatgpt/README.md`). The complete native
  commit removes that mismatch; the rerun passes all 12 tests. The initial full
  failure log is retained in task-local scratch, not reported as a pass.
- Source qualification caught two incorrect relative report links; they were
  corrected within this Step and source/export qualification then passed.
- Six optional native release integrations were not rerun. Release machinery is
  unchanged; native candidate materialization, installed-tool invocation and
  source/slot integrity were exercised separately. Step 5's disposable consumer
  install/upgrade remains historical proof, not a new Step 6 integration run.
- Normal CRLF-to-LF notices on evidence files are informational. Whitespace,
  exact Instructions bytes and historical preservation checks pass. Check
  annotations are acquired separately from logs for the final head; unsupported
  UI-only/pre-execution warnings are outside the evidence and not asserted absent.
- The validator checks INDEX membership in each exact locked receipt, not receipt
  completeness for unreferenced slot extras. Conditions stay unevaluated and
  package presence grants no adoption. Existing ordinary-blob/hash/identity
  validation is preserved. No dependency resolver or acceptance oracle is added.
- Live ChatGPT loading, settings application/readback, Sources upload/addressability,
  role compliance, review quality and model reliability remain UNQUALIFIED.
  No external consumer or live settings changed. Actual serving model/effort
  telemetry is unavailable; the requested Task/Step title was persisted/read back.

Stop for independent substantive exact-head NON-APPROVING Deliberative review
and owner disposition. Task 32 and PR 33 stay open; no self-approval, merge,
release, later Step or closure is inferred from these checks.
