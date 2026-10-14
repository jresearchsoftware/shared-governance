# Task 32 — Step 3: Outcome-aware bootstrap refinement

This is a bounded experimental refinement under the [Step 3 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6177571849),
following the [Step 2 non-approving assessment](https://github.com/jresearchsoftware/shared-governance/pull/33#pullrequestreview-5522927879).
It continues PR 33 from `981ca259fab7e533653a7efc8aef8acfad95d4e9`; the independently
accepted source boundary remains `15e8191435a126e54b4d1739a73fab112e01c081`.
The full [Task chronology](https://github.com/jresearchsoftware/shared-governance/issues/32)
controls scope. [Step 1 research](../step-1/README.md) and the
[semantic map](../step-1/semantic-map.md) are research evidence for ownership
distinctions, not new Task authority.

## Owner-reported experiments, 2026-10-14

These observations are attributed to the owner through the Step 3 Decision.
They are not first-hand Codex model trials or independently available complete
transcripts/tool traces. Approximate response times are owner-reported timings,
not controlled model telemetry or a reliable performance estimate.

| Case and intervention | Reported control | Reported experiment | Supported conclusion |
| --- | --- | --- | --- |
| C2: current Task-authority question; clean control versus the 4,305-character Step 2 bootstrap | Correct Issue/Decision chronology; ~2m20s | Correct Issue/Decision chronology; ~3m28s | No clear bootstrap advantage. |
| C3: fresh pair; explicit independent-review request for the Step 1 Outcome | Substantive evidence-grounded review; ~6m36s | Substantive evidence-grounded review; ~6m09s | No clear quality improvement when review was explicitly requested. |
| C3b: fresh pair; same Outcome URL with only read-only/no-mutation qualifiers | Summary and historical/current PR status checks; no own substantive primary-evidence review; ~46s | Autonomous report/map/source/CI inspection and non-approving assessment; ~3m33s | Better routing, but shallower than C3 and partly reliant on earlier review. Full review quality remains unqualified. |
| Historical BLOCKED: Task 24 Step 1 Outcome | Recognized historical BLOCKED, original causes and later Step 2/3, merge and closure; no action currently due | Same reconciliation; old 4,305-character bootstrap plus an additional short dispatcher paragraph manually appended to Project Instructions | Historical reconciliation only; no demonstrated dispatcher advantage or active unresolved-blocker qualification. |

The historical 4,305-character composition is preserved at the
[Step 2 result commit](https://github.com/jresearchsoftware/shared-governance/blob/981ca259fab7e533653a7efc8aef8acfad95d4e9/docs/task-32/step-2/shared-governance-instructions.md).
The historical BLOCKED intervention differs from that plain Step 2 bootstrap;
its appended paragraph is owner-reported, with no exact saved-text readback
available here. None of these observations tests the complete refined Step 3
Instructions. Screenshots, answer text, timing reports and underlying model/tool
traces support different claims; their availability must be recorded separately.
C1 and C4–C8 remain **NOT RUN / UNQUALIFIED**. Step 2's preparation-date NOT RUN
statements, historical reports, logs and evidence are preserved rather than
retroactively rewritten. [The capture sheet](capture-sheet.md) retains this
provenance and separates routing from substantive quality.

## Refinement and accepted review routing

The active [common template](../step-2/bootstrap-template.md),
[Shared Governance binding](../step-2/bindings/shared-governance.md) and
[complete experimental Instructions](../step-2/shared-governance-instructions.md)
remain static, manually composed artifacts. The dispatcher routes a bare
Outcome handoff through current Task/Decision/PR/result reconciliation, then the
currently authorized review, diagnosis, continuation or specific stop boundary.
It distinguishes completed/reviewable, active BLOCKED, historical/resolved and
ambiguous/partial results. A prior Outcome, green CI or later unrelated work
cannot determine permissions or prove that a blocker was resolved.

For reviewable work, the bound route is accepted project AGENTS, adopted Task
Handoff and its [accepted manual client binding](https://github.com/jresearchsoftware/shared-governance/blob/15e8191435a126e54b4d1739a73fab112e01c081/docs/manual-task-handoff.md),
together with current Task Decisions. Step 3 explicitly requires independent
substantive correctness, architecture, maintainability, risks/security, realistic
tests, exact-head source/diff/primary CI and warning assessment. Earlier reviews
are comparison evidence, not a substitute for that reasoning. Research findings
must be judged within research scope; historic heads cannot inherit new-head CI.

The separately available shared `independent-review` topic remains **unadopted**
by this producer's accepted root and experimental binding. Package presence and
Task Handoff adoption do not activate it. The local accepted acceptance method
and this experiment's requirements provide the applicable route; a future shared
topic adoption is still a separate owner decision, not an implicit Step 3 repair.

## Qualification and next boundary

[Cases](cases.md) add bare-Outcome and historical/current BLOCKED coverage while
reusing unchanged Step 2 case families. [The minimal owner runbook](runbook.md)
supports a small manual follow-up without new Codex settings access or repetitive
permission ceremony. Reused projects are exploratory/confounded, even with fresh
chats; they cannot establish a clean independent A/B comparison.

Run the existing bounded offline check with:

```powershell
python docs/task-32/step-2/verify-text.py
```

The full Instructions contain **6,742 Unicode characters** including the final LF,
leaving **1,258** below the experimental 8,000-character budget. The historical
Step 2 text remains available at its immutable result commit.
The verifier checks exact composition, placeholders, size, routes and historical preservation;
it cannot prove live settings readback, model behavior or review completeness.
Actual local qualification, exact-head CI, skips, warnings and capability limits
belong in [Step 3 validation evidence](evidence/validation.md) and the one canonical
English Step 3 Outcome on PR 33. No generator, service, Skill, resolver, recurring
preflight, package/version change or native adoption is introduced.

The executor stops after that Outcome for independent substantive **non-approving
Deliberative review** and owner disposition. PR 33 and Task 32 stay **OPEN**.
Live ChatGPT settings/Sources, consumer edits, new topic adoption, deployment,
credentials/production mutation, self-approval, merge, package publication,
follow-on launch and Task closure remain outside this Step.
