# Task 32 — Step 4: universal content-agnostic bootstrap

The candidate adds one reusable offline projection path for owner-reviewable
ChatGPT Project Instructions. It consumes an independently bound accepted Git
snapshot, native boot/lock/materialized files and small client data; it does not
enumerate governance topics in common logic or copy policy into settings.

Authority: full [Task 32 chronology](https://github.com/jresearchsoftware/shared-governance/issues/32)
and [Step 4 Decision](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6186228339).
Starting PR 33 head: `24e1c3e76e172b033d157ef7a2ff7d20f6789d93`.
Independently accepted source-main remains frozen at
`15e8191435a126e54b4d1739a73fab112e01c081`, verified against main, merge base,
Task 28 owner acceptance and PR 31 accepted squash. No rebase or authority repin.
Candidate tool/template/bindings remain proposals, not accepted governance.

## Why a small projector now

Step 3's common dispatcher is useful proposed client steering, but its manually
maintained binding enumerates specific adopted topics, version and slot, and
contains a temporary read-only prohibition. Extending that shape per consumer
would require repeated manual composition, route inventories and settings/cache
diff work. The Step 4 Decision explicitly admits a deterministic generator where
needed for reliable single-implementation reuse. One template plus data gives
byte-reproducible full replacements, explicit baseline provenance, no-op detection
and the same maintenance interface for distinct project roles. The cost is a
small Python schema/tool and bounded tests; no service, new approval gate or
ordinary-chat installation is introduced. Native dependency resolution stays
with VibeVM. This architecture still awaits independent Deliberative assessment
and owner disposition.

| Artifact | Purpose |
| --- | --- |
| [Common interface and maintenance](../../chatgpt-bootstrap.md) | One reusable process, schema, native limitations and optional cache selection/export. |
| [Shared Governance binding](bindings/shared-governance.json) | Non-sandbox orchestration/review role with current-authority-limited lifecycle capabilities. |
| [Complete Shared Governance Instructions](outputs/shared-governance/instructions.md) | First-consumer owner-reviewable full replacement from the common template. |
| [Settings proposal](outputs/shared-governance/settings.diff) / [maintenance](outputs/shared-governance/maintenance.json) | Exact text versus **assumed empty**, unverified live baseline. |
| [Historical Relay binding](bindings/relay-preview.json) / [output](outputs/relay-preview/instructions.md) | Structurally different three-entry native boot, older locked payload and read-only client. No migration. |
| [Optional cache manifest](outputs/relay-preview/sources-manifest.json) / [snapshot](outputs/relay-preview/sources.md) | Same generic method; two small routing files, no mandatory producer Sources. |
| [Semantic coverage](semantic-coverage.md) | Preserved Step 3 semantics and project-owner boundaries. |
| [Owner handoff](owner-handoff.md) | Practical application/readback and normal-work dogfooding. |
| [Qualification](evidence/validation.md) | Actual checks, warnings, corrections and limits; no behavioral PASS claim. |

Both outputs share the identical common-template hash. Their own receipts give
exact Unicode lengths, source hashes and native entries. No common branch on
repository, package version, protocol name or Task exists. The historical Relay
source is the accepted PR 125 squash `52bebbc9cafc1e82737943a6d37f00945ffadfef`,
not a claim about today's consumer settings/runtime or latest main. Product
contracts and actual migration remain with Relay Task 101; DocReview's retained
source/reader/controller/corporate methods remain separately owned. A second
consumer is sufficient for this bounded demonstration; no DocReview output is
misrepresented as complete or migrated.

Steps 1–3 reports, templates, verifier, observations, logs and source snapshots
remain byte-preserved at their historical paths. Their Outcomes and independent
COMMENT assessments remain intact on PR 33. The Step 3 assessment found no
material defect in its experimental scope and explicitly left source annotations
and live behavior evidence limited. Step 4 addresses the owner's newly admitted
universal architecture, rather than calling that prior bounded result a regression.
Do not run Step 3's frozen scope verifier against a Step 4 tree: its deliberate
Step-3-only path allowlist describes a historical execution. Step 4 separately
checks historical byte preservation and its own changed scope.

## Reproduction

From this producer checkout, use Python 3.11+ and Git. The exact historical Relay
object is already present locally; a fresh clone needs an ordinary authorized
read-only fetch of that exact commit from its owning repository. No consumer
checkout is edited. Use new output directories to preserve existing artifacts.

```powershell
python scripts/project-chatgpt.py --repository . --binding docs/task-32/step-4/bindings/shared-governance.json --accepted-sha 15e8191435a126e54b4d1739a73fab112e01c081 --authority-anchor https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6186228339 --baseline-kind assumed-empty --output .vibe/task32-step4/shared-review
python scripts/project-chatgpt.py --repository . --binding docs/task-32/step-4/bindings/relay-preview.json --accepted-sha 52bebbc9cafc1e82737943a6d37f00945ffadfef --authority-anchor https://github.com/jresearchsoftware/codex-relay/pull/125 --baseline-kind assumed-empty --output .vibe/task32-step4/relay-review --cache
python scripts/test-chatgpt-projection.py -v
```

For a no-op comparison, rerun into another new directory with
`--baseline-kind candidate --baseline <first-output>/instructions.md
--previous-receipt <first-output>/receipt.json`. No-op describes these exact
candidate bytes, never an unread UI field. The immutable source-pin tradeoff and
accepted payload/overlay refresh process are documented in the shared interface.

## Terminal boundary

Commit, push and qualify the exact result, publish one English canonical Outcome
on sole result PR 33, then stop for independent substantive **non-approving
Deliberative review** and owner disposition. No live settings/Sources edit,
consumer edit, unrelated topic adoption, package/native SemVer change, runtime
change, deployment, credentials mutation, self-approval, merge, release, later
Step launch or closure. Task 32 and PR 33 remain **OPEN**. Behavioral activation
awaits owner-controlled application/readback and ordinary future work.
