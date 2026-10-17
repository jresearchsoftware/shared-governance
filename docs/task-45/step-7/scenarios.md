# Task 45 Step 7 — executor PR readiness coverage and walks

Authority: [Step 7 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6239052197).
Frozen independently accepted source-main: `ec048fb39ae28cf2d747101466a603ddd062b1b0`.
Starting candidate: PR #46, Draft/open, `b76ea98e6ee2645be674690094f88a6fa265d77d`.
The complete Task/PR chronology, including the Step 6 exact-head APPROVE,
remains history. This is a new execution under Direct, not inherited approval.

## Bounded semantic change

The canonical baseline is the complete accepted 2.7.0 Task Handoff protocol,
its producer manual binding and the complete starting candidate Task Handoff.
Accepted lifecycle already separates Step/Outcome, independent acceptance,
integration and completion, but has no common executor Draft/Ready obligation.
The owner explicitly adds that material operator work in Step 7. This document
does not claim an extraction or adoption of Relay's implementation; the owner
Decision supplies the new reusable behavior and preserves Writer ownership.

New [TH-028](../../../packages/development-governance/vibevm/vibespecs/protocols/task-handoff.md#TH-028)
owns all readiness clauses. TH-001–TH-027 and their anchors retain their meaning;
no retired ID is reused. TH-006–TH-008 still own execution/recovery identity,
TH-012/TH-013 reconciliation, TH-014–TH-018 Outcome routing/verification,
TH-019–TH-025 independent assessment/strategy, TH-026/TH-027 continuation/local
bindings. Independent Review's method remains separately adopted and unchanged.

| Owner requirement | Coverage and deliberate boundary |
| --- | --- |
| Common meaning and executor duty (1–2) | TH-028 defines execution handoff state; local manual binding supplies existing connected-tool/`gh` choices. Qualified automation keeps ownership, with no competing executor or new privilege. |
| Start and successful finish (3–4) | Same PR/head verified Draft before modification; candidate push → canonical Outcome/readback → same PR/head verified Ready. New Draft PR, no redundant toggle and per-result multi-PR cases are explicit. |
| Failure/recovery and scope (5–6) | Draft for blocked/incomplete/uncertain execution; preserve durable Outcome and identity on Ready failure, disclose capability gap and reconcile only the idempotent transition. Supported equivalent states/no synthetic PR; consumer adoption separate. |
| Semantic owner, operability and walks (7–9) | One new TH rule, root local route, manual commands and bounded walks below. No IR changes, global CLI, settings or Relay changes. |
| Version/materialization (10) | Same unaccepted 3.0.0 MAJOR; installed README/CHANGELOG disclose mandatory lifecycle and migration. Existing exporter/native/projector synchronize actual payload and routes. Historical versions remain untouched. |

The real workflow cost is two state boundaries around applicable admitted PR
work, using existing GitHub state and publication evidence. It prevents active
work appearing handed off and completed manual work being left indefinitely
Draft. Already-correct state requires readback only; no extra approval, ledger,
bot or credential is introduced. This cost is explicitly owner-authorized.

## Desk-based behavior walks

These walks apply the full proposed TH-028 plus the local binding, without
residual Relay policy or a new executable policy engine. P/Q are artifacts and
A/B exact revisions. PASS means the written candidate gives the stated result
and rejects the counterexample. These are bounded authoring checks, not proof
that a model follows instructions or that a remote permission is available.

| Case / input | Decision and observable boundary | Rejected counterexample / observation |
| --- | --- | --- |
| L1: New admitted implementation on existing Ready P/A, previous independent APPROVE. | Read P/A, convert to Draft, read back P/A/Draft before editing; preserve PR/branch/review history. New B needs fresh review. | Editing first, treating old approval as B acceptance, or opening replacement P. PASS. |
| L2: Existing P/A already Draft (actual Step 7 start). | Read back P/A/Draft; no mutation; then implement. | Toggle Ready/Draft merely to demonstrate capability. PASS. |
| L3: New implementation PR is authorized and Draft mode supported. | Create as Draft and read back identity/head/state; finish via L4. | Create Ready before the executor's successful handoff. PASS. |
| L4: P/B completed and pushed; canonical successful Outcome saved and complete readback matches target/author/body/B. | Only then mark P Ready; read back P/B/Ready before independent review. | Ready before durable Outcome, wait for APPROVE, or claim Ready from mutation response alone. PASS. |
| L5: P/B is BLOCKED/failed/incomplete, with useful partial work and a truthful terminal Outcome. | P remains verified Draft; disclose blocker. | Every terminal Outcome implies Ready. PASS. |
| L6: One Issue Outcome covers completed P/A and blocked Q/B. | Outcome binds both; after readback P alone can become verified Ready, Q stays Draft. | Blanket Ready or blanket Draft merely because the aggregate is partial. PASS. |
| L7: One result PR plus an independent Task-level result; Issue Outcome. | Ready depends on completed P/A and verified canonical Issue Outcome, not which surface holds the comment. | Require a duplicate P Outcome to set Ready. PASS. |
| L8: Known no-PR analytical result or non-GitHub tracker with no Draft state. | One locally routed Outcome; use only supported equivalent states. | Create PR/UI/CLI/account solely to satisfy the common rule. PASS. |
| L9: Outcome durable; Ready action lacks permission or tool capability. | Retain exact Outcome/Step/result; report P's observed Draft state or unknown state, missing operation/permission and needed authorized action. No code-defect claim from permission alone. | Duplicate Outcome, redo execution, change identity/credentials or claim success. PASS. |
| L10: Ready request times out; readback finds same P/B already Ready. | Keep same Outcome and Step; verified target state completes that transition, no second mutation. | Republish Outcome or force an extra Draft/Ready cycle. PASS. |
| L11: Ready response/readback unavailable or now names C instead of B. | Readiness unconfirmed; retain Outcome/B, report exact gap and reconcile before retry. If readback establishes P/B still Draft, retry only the authorized transition and verify. | Claim Ready from exit 0, silently adopt C, or publish another Outcome. PASS. |
| L12: Qualified automation owns P lifecycle (e.g. separately adopted Relay Writer). | Follow its qualified completion/recovery path; no competing Codex mutations. | Common protocol installs a second writer or changes Relay admission/identity. PASS. |
| L13: P/B successfully handed off; CI red or base conflict, independent review pending. | Ready still means successful executor handoff; report checks/conflict, preserve separate merge/review gates. | Draft solely because CI/mergeability is red, or infer merge permission from Ready. PASS. |
| L14: Review/discussion alone on P/B, no newly admitted implementation. | No new Step or Draft transition; assessment/Direct/Deliberative rules still apply. | Reviewer APPROVE itself is the executor Ready trigger. PASS. |

The earlier [Task 26 lifecycle walks](../../task-26/step-1/scenarios.md) and
[Outcome-routing walks](../../task-26/step-2/scenarios.md) retain their historical
scope. L1–L14 add the newly authorized state behavior; they do not rewrite old
Outcomes, retroactively reject prior Draft results or broaden review authority.

## Executed evidence and limits

Focused distribution tests preserve every starting TH anchor/heading and locate
TH-028 only in Task Handoff. Native self-adoption tests open the real installed
rule and verify byte equality with authored/exported source plus local agent
access. Existing corruption/lock/index/recovery tests check actual files rather
than simulating a GitHub permission. [Qualification](validation.md) records
fresh native materialization, applicable suites and actual Step 7 handoff.
The final Outcome binds exact head, CI and durable publication; subsequent
native PR readback is the live Ready evidence. No test fixture publishes comments
or mutates a real PR. Missing-capability/ambiguous/split/non-GitHub paths above
are semantic applications, not claimed live fault injection or model execution.
