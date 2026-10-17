# Task 45 Step 5 qualification

Authority: [Step 5 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6236224883).
Frozen independently accepted source-main: `ec048fb39ae28cf2d747101466a603ddd062b1b0`.
Starting reviewed result: `c15bd73c2525ede12c2037109f0cee3d6ef1f511`.
The single canonical Step 5 Outcome on [PR 46](https://github.com/jresearchsoftware/shared-governance/pull/46)
binds the complete final head and its primary CI evidence. Earlier Outcomes remain
historical and are not republished.

## Correction coverage and provenance

| Requirement | Implementation and evidence |
| --- | --- |
| R1 / P1, introduced Step 2 (`48a52029b2896d9f7e5a11ae75cce7622b937b2f`), incompletely corrected Step 4 | Historical exports are compared without current readiness enforcement. The current release and source-time candidate still require complete notices/rights/export. A real Git history starts with an incomplete accepted 1.0.0, checks a candidate 1.0.1, squash-integrates it and plans the exact accepted source. Historical owner/CI eligibility remains required; removing predecessor acceptance still blocks. |
| R2 / P1, introduced Step 2, incompletely corrected Step 4 | A separate first-parent Git walk of package/binding changes up to the disposed baseline retains first-main version payload identities. Eligibility auditing remains bounded by the explicit baseline. With no tags or earlier API attestation, baseline advancement past 1.0.0/2.0.0 rejects changed-byte reuse of 1.0.0 in candidate and production paths, while a genuinely new 3.0.0 passes both. Revision-specific inventories remain in force; absent historical binding cannot fall back to today's policy. |
| Owner-report gap, pre-existing at accepted 2.7.0 | Existing review taxonomy did not explicitly require all fields at the owner-facing prepublication report. Optional Independent Review owns methodology; adopted Task Handoff owns the operational report/verdict lifecycle. Local manual binding and custom/generated Instructions carry the rule to this ChatGPT client without adopting the optional topic. [Scenarios](review-scenarios.md) cover supported provenance, explicit undetermined/gap and an incomplete report. No extra reviewer, approval, wait, schema or universal gate is introduced. |
| Same unaccepted package candidate | Aggregate impact remains 2.7.0 -> 3.0.0 MAJOR, including Step 4's preparation obligations and Step 5's explicit report content. Authored source, native registry/slot/receipt/lock/routes and relevant documentation are reviewed together. The other six protocols, shared ChatGPT tooling and frozen 2.7.0 source/slots remain unchanged. |

The two new regression tests were run against the original Step 4 publisher:
both fail at their intended invariants (R1 production stays pending; R2 candidate
accepts old-version reuse). With the corrected publisher, the complete temporal
suite passes 13 tests. These are real disposable Git histories with synthetic
GitHub PR/CI evidence, not actual remote publication or proof of independent
review. Current source readiness negatives, earlier F1-F3, owner/CI rotations,
inherited-ineligible changes, no-op and private-file export remain covered.

## Guidance, projection and client limits

The semantic change is minimal content at an existing report point: severity,
supported origin or undetermined plus gap, exact result/comparison and evidence,
qualified impact, remediation and closure evidence stay consistent through the
published negative assessment. Confirmed behavior, analytical risk and missing
tests remain distinct. Direct/Deliberative, local publication permissions, owner
role and stronger identity boundaries remain intact.

The existing projector uses frozen accepted source for authority/routing inputs,
updated owner-authorized custom Markdown and the Step 5 authority URL. It reports
effective Instructions CHANGED, optional Sources DISABLED, and a complete output
below the 8,000-character budget. Its normal check reproduces the output/receipt.
Live Instructions/Sources were not read, applied or activated; owner application
and verification remain manual. Static scenario and output checks do not prove
model compliance. The client-title tool accepted a rename but listing readback
retained another title; title persistence is unconfirmed and nonblocking.

The ChatGPT preservation fixture now protects the retained accepted 2.7.0 copies
of the two intentionally edited protocols, just as Step 4 did for versioning.
It still protects historical file sets and unchanged protocols; it does not
freeze the current authoring path against owner-authorized future edits.

## Validation and boundaries

Run source/exact-export, distribution, release, self-adoption and ChatGPT checks
from a committed clean Linux clone. Regenerate the current unaccepted 3.0.0
projection through the existing exporter and pinned VibeVM 1.0.7 musl installer;
its binary digest is `20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Actual results are recorded below once executed; the Outcome binds final-head CI.

Publication transport, atomic non-force staging, credentials and existing-tag
recovery are unchanged. Prior Step 2/4 native transport evidence remains applicable
to those unchanged invariants; six optional native transport skips in ordinary
focused runs are skips, not new passes. No unrelated native transport suite is
repeated solely as ceremony. Fresh package export/materialization checks cover
the changed 3.0.0 payload. Existing Shared Governance post-accepted-merge automatic
publication remains active under its prior policy; this PR does not cut over to
the new publisher. Real private callers, destination credentials/permissions,
remote publication, Landscape integration, consumer adoption and shared-publisher
Windows/macOS operation remain unqualified and outside this Step.
