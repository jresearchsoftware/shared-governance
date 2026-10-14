# Task 32 — Step 2: controlled bootstrap experiment preparation

**Repository preparation only; no real ChatGPT trial has run.** This candidate
contains a small static bootstrap, a Shared Governance binding and complete
experimental Instructions, plus a controlled trial procedure and capture sheet.
It tests direct GitHub loading before architecture selection. It is neither an
adopted governance topic nor a production settings replacement.

Authority is the full [Task 32 chronology](https://github.com/jresearchsoftware/shared-governance/issues/32)
and [Step 2 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6173878844).
Frozen accepted source-main: `15e8191435a126e54b4d1739a73fab112e01c081`.
Before edits, remote main matched that SHA; local/remote PR 33 matched Step 1
head `bae27d667e953e9d4fa0da17cdc51860d13efbf4`, whose merge base was the
accepted SHA. [Task 28's acceptance Decision](https://github.com/jresearchsoftware/shared-governance/issues/28#issuecomment-6169665115)
and PR 31's accepted squash establish independent source provenance.

The [Step 1 report](../step-1/README.md), [semantic map](../step-1/semantic-map.md),
source inventory and [independent COMMENT assessment](https://github.com/jresearchsoftware/shared-governance/pull/33#pullrequestreview-5521478376)
are research evidence. Their acceptance or recommendation is not implied by
preparing this experiment. Step 1 files and its published Outcome remain intact.
This Step uses the same branch/result PR 33, with a fresh exact result and Outcome.

## Artifacts and minimal adaptation

| Artifact | Purpose |
| --- | --- |
| [Static common template](bootstrap-template.md) | One common GitHub/JIT/evidence loading procedure; no service, resolver or Skill. |
| [Shared Governance binding](bindings/shared-governance.md) | Repository, role, accepted SHA/provenance, native routes, conditional topic adoption and permissions. |
| [Complete experimental Instructions](shared-governance-instructions.md) | One full `markdown` block; copy only its contents after later owner authorization. |
| [Example consumer bindings](bindings/consumer-examples.md) | Frozen read-only Relay/DocReview routing examples; not complete consumer replacements or activation. |
| [Owner runbook](runbook.md) | One action at a time; clean control versus experiment. |
| [Eight behavioral cases](cases.md) | Identical paired prompts, expected observable behavior and specific evidence gaps. |
| [Capture sheet](capture-sheet.md) | Future observations, including partial, failed and unqualified results. |
| [Text verifier](verify-text.py) | Offline exact static substitution, Unicode length, accepted route existence and Step 1 preservation. No model or settings check. |
| [Preparation evidence](evidence/preparation.json) | Compact current authority, complete-comment/connector comparisons and observed source binding. |

Adaptation is manual: replace the sole `{{PROJECT_BINDING}}` in the common
template with the reviewed consumer binding, preserving the common text. The
binding supplies identity/role, accepted-source selection and provenance,
adopted native/local routes, compatibility/specialist references, language and
publication/protected-action permissions. No configuration schema or production
generator is introduced. The verifier reconstructs text only in memory; it
writes no Instructions or settings. A consumer migration must still explain
complete semantic coverage against Step 1's map under its separate authority.

The bootstrap remains explicit about primary reads and critical boundaries
because a bare AGENTS link did not address the reported PR 27/31 failure. Full
normative rules remain in accepted sources. Conditional topic reading and
routine-discussion economy preserve the accepted operator flow. The local
read-only trial role prevents these experiments from publishing reviews or
inheriting another consumer's automatic merge permission.

## What is observed, and what remains unqualified

Current accepted AGENTS/INDEX/authoring boot/slot boot and applicable full
Task Handoff, Proportional Controls and Requirement Authority were read at the
frozen SHA, together with accepted manual binding, authoring, self-adoption and
CONTRIBUTING. The independent-review text was consulted as research, not adopted.
The complete live Issue body and all four comments, both supplied originals,
Step 1 report/map/Outcome and linked assessment were read. The new Decision
does not supersede the consumer-owned differences identified in that research.

The connected GitHub `fetch_file` returned accepted AGENTS with the exact Git
blob identity/content; all-pages `fetch_issue_comments` returned all four Task
comments. Full supplied bodies still match the Step 1 snapshots, with lengths
9,740 and 7,884 Unicode characters and their ending sections intact. These are
**Codex-surface retrieval observations**, not fresh ChatGPT Project loading or
model-compliance results. Available GitHub operations include file/Issue/comment,
PR/diff, workflow-run/job/step/log reads. Run-list/job-list wrappers have documented
first-page/attempt limits; completeness must be assessed in the future client.
An annotation-list operation is not assumed available merely because logs are.

Official documentation describes shared Project instructions/Sources across
chats and distinguishes ChatGPT projects from local-folder projects.
[Projects and chats](https://learn.chatgpt.com/docs/projects).
Personalization controls vary by surface and memories carry context across chats.
[Personalize ChatGPT](https://learn.chatgpt.com/docs/personalize).
These product descriptions support the runbook's context controls; they do not
establish account-specific instruction-field availability, length behavior,
project-only memory isolation, GitHub tool completeness or model reliability.
The runbook treats those as observations to record, rather than promised UI paths.

No temporary project, field edit/readback, Source upload, new conversation trial,
consumer migration, VibeVM runtime or protected operation occurred. All C1–C8
model results are **UNQUALIFIED / NOT RUN**, including the positive and negative
review cases. Static correctness and CI cannot turn them into observed PASS.
Shared Governance's absence of a separate live Instructions field is Step 1
owner evidence, not a new UI observation; no actual settings diff/no-op is claimed.

## Validation and maintenance

Reproduce local text checks with Python 3.11+ and Git:

```powershell
python docs/task-32/step-2/verify-text.py
```

Like Step 1's evidence helper, consumer-path checks need the two frozen consumer
Git objects. They are already present in this research checkout. For a fresh
clone, obtain them through these ordinary read-only fetches (no consumer checkout,
remote configuration, credentials change or installation):

```powershell
git fetch --no-tags https://github.com/jresearchsoftware/codex-relay.git 52bebbc9cafc1e82737943a6d37f00945ffadfef
git fetch --no-tags https://github.com/jresearchsoftware/docs-evolution-review.git 6014e8e2c20faebfaa656ee1e8e6efb1dcd9d630
```

Then use the accepted CONTRIBUTING source/export/release/self-adoption checks
and applicable exact-head candidate CI. Stage new files before qualification,
commit before exact-commit export. Actual results and warning dispositions are
in [validation evidence](evidence/validation.md) and the canonical Step 2 Outcome.
Package/native/protocol content stays at 2.2.0, so no SemVer bump or VibeVM
reinstallation is justified. No recurring test gate is added to the workflow.

At deliberate maintenance, compare full old/new output, not just its filename.
Identical template and binding yield identical text: no re-paste. Changing the
accepted SHA, role, topic adoption or permissions changes actual Instructions
and needs a reviewed full replacement. A referenced native dependency change
does not silently adopt topics. For this fixed-pin prototype a new accepted
source requires a changed binding; main alone cannot authorize repinning.
Sources have their own optional owner-reviewed changes; this experiment uses none.
Missing/drifted guidance is a routing gap, not a reason to install tooling,
edit a lock URL, request credentials or fall back to candidate policy.

## Required next boundary

Independent substantive **non-approving Deliberative assessment** of the exact
candidate must precede owner discussion/Decision. Only a later owner decision
may authorize temporary test-project creation/settings application and trial
execution. The runbook is a prepared artifact, not that authorization.

If practical trials support the minimal direction, the owner can decide whether
to adopt it, revise it or test alternatives; no single polished answer proves
reliability. Any production shared delivery and Relay 101/DocReview adoption
remain separately decided. No self-approval, merge, package publication,
live settings/Sources change, consumer edit, follow-on launch or closure is
authorized here. **Task 32 and PR 33 stay OPEN.**
