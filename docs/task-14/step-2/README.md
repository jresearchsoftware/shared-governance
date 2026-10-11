# Task 14 / Step 2: review correction (2026-10-12)

This dated evidence records the owner's Manual Codex Step 2 request to correct
[F1](https://github.com/jresearchsoftware/shared-governance/pull/21#issuecomment-6114033010)
within [Issue 14](https://github.com/jresearchsoftware/shared-governance/issues/14)
and update the same [PR 21](https://github.com/jresearchsoftware/shared-governance/pull/21).
The finding is an attributed advisory assessment, not a native GitHub review or
executable Relay Change Request. The owner's direct request authorizes this
bounded correction and ordinary GitHub evidence publication without Relay Writer.

Starting local/remote/PR head: `1b0149a5b76e013f6af4deff7016e18b338a6d1d`.
Accepted main read back: `129d452ddfa6b9ac1030ccc7803994793467ab2d`.
Correction commit: `4db4e64a7d8f4548bafaa91fd855277ce02f248c` on the existing
`codex/task-14-step-1-task-handoff` branch. The canonical Step 2 Issue Outcome
binds the final evidence-bearing head, CI and PR readback without a
self-referential commit identifier in this file.

## F1 correction and preservation

- [Self-adoption](../../self-adoption.md) now explains durable applicability:
  explicit adoption, assessment-only authoring/review routing, no activation or
  source acceptance from that route, and separately authorized independent
  review of self-adoption from accepted source. It no longer declares Task 14's
  current admission or predicts its acceptance state.
- [Manual binding](../../manual-task-handoff.md) retains the short prompt and
  local workflow, dates the Task 14 / Step 1 example to its 2026-10-11 admission,
  and describes that admission's limits historically. Current execution follows
  the then-current Issue/PR/review authority, not the example.
- The correction changes only those two documents. Package payload, protocol
  semantics, package version/category, root routing, active snapshot/receipt,
  scripts, workflows, frozen content, Step 1 evidence and historical Task 19 prose
  are unchanged. The evidence commit adds only this Step 2 directory.

Manual assessment of the changed prose covers three future states: before source
acceptance, after source integration without self-adoption, and after a separately
reviewed adoption. The general text assigns no mutable admission/approval state
to any of them; the historical example grants no present permission. This is an
implementation self-check, not independent acceptance. No wording-mirror test or
new validation gate is added.

## Qualification

Local commands run at the correction commit, with primary output retained below:

```sh
git diff --check origin/main HEAD
python scripts/qualify.py --export-ref HEAD
python scripts/test-distribution.py
python scripts/test-release.py
python scripts/package-release.py --source-ref HEAD --base origin/main --pr-body-file /path/to/pr-body
```

| Check / evidence | Observed result |
| --- | --- |
| [Source and exact-commit export](logs/qualification.txt) | PASS: 85 tracked files, 108 local links, bounded credential-marker scan, accepted-origin active protocol, passive flow export. |
| [Distribution regressions](logs/distribution.txt) | 35/35 PASS. |
| [Release regressions](logs/release.txt) | 10 ordinary tests PASS; 6 unchanged optional native tests explicitly skipped. |
| [Whole-package boundary](logs/version-boundary.txt) | PASS: current accepted main 1.1.0 to proposed 1.2.0 / minor. |
| [Scope preservation](logs/scope-preservation.json) | PASS: only the two F1 documents differ from the reviewed starting head; package and Step 1 evidence Git trees match exactly. |
| Whitespace | `git diff --check origin/main HEAD` PASS. |

Distribution fixture Git operations emit the same CRLF-normalization warnings
for old Task 19 logs documented in Step 1. Those original tracked bytes remain
unchanged; the warnings concern disposable fixture copies and no test fails.

Final exact-head source/export, whitespace, scope preservation, whole-package
boundary and GitHub CI are recorded in the canonical Step 2 Outcome. Local logs
qualify the correction commit; they do not impersonate final-head CI evidence.
The existing proposal remains `1.1.0 -> 1.2.0`, `Package bump: minor`, against
accepted main. This outside-package documentation correction adds no version
bump or release and changes no consumer contract.

Native VibeVM integration is unchanged, so its
[dated Step 1 materialization evidence](../step-1/README.md) is reused rather than
claimed as freshly executed. The six optional native publisher/resolver tests
and fresh installed-model/Relay Skill traversal remain unqualified. No
independent reviewer identity, native approval or general absence of runtime/UI
warnings is established by these local checks.

The chat title was changed through the supported Codex tool and read back as
`Task 14 — Step 2 — Review correction`. No subagents or Relay Writer were used.
Stop for independent review of the new exact head. No self-approval, merge,
actual package publication, consumer change, live installation or Issue closure
is performed or authorized by this evidence.
