# Task 136 Step 1 — Closure-policy compatibility

[Task #136](https://github.com/jresearchsoftware/shared-governance/issues/136)
authorizes the first Shared Governance compatibility phase. The frozen source
baseline is `af56ce1fdf355212926e2c3982ce6827875d0643` with Development
Governance 12.4.2. This result includes the bounded producer-local correction
from [Small Improvement #135](https://github.com/jresearchsoftware/shared-governance/issues/135)
under SI-004–SI-008. The combined PR and Outcome should refer to both Issues.

## Coverage against accepted TH-026

| Accepted behavior | Candidate coverage |
| --- | --- |
| One field, prose condition, fail-safe when closure intent is unclear | TH-026 lists the two pairs of equivalent spellings. A charter uses one selected value. Missing, invalid and conflicting metadata still prevent automatic closure. |
| The designated PR's authorized default-branch merge completes the whole Task | The final-result mode keeps exact-head acceptance, required checks and protected merge. Intermediate PRs use non-closing references, and abandoning a PR leaves the Issue open. A published Step Outcome establishes only that Step's result. |
| No PR is needed for a valid no-PR result | The existing authorized completion mechanism and actual result acceptance apply. |
| Publication or Apply as a stated completion condition | The condition-based mode keeps PR linkage non-closing. Closure follows verification of the actual stated obligation, all required acceptance/integration and resolution of real work or protected holds. A satisfied condition needs no policy conversion. |
| Historical authority and genuine amendments | Read the historical charter and applicable trusted Decisions with the admitted authority, protected holds and supported mechanism. The new spellings change no recorded value or terminal identity. |
| Existing owner authority to resolve backlog Issues | Use supported status reasons and actual completion evidence for completed/fixed. Record the genuine reason and any replacement reference for a non-completion disposition. Honor outstanding protected/admitted work and use existing Decisions for substantive changes where applicable. |

The [onboarding walks](../../../packages/development-governance/vibevm/vibespecs/guides/onboarding-examples.md#9-single-field-task-closure)
cover these results under both spellings and the combinations that control
authoring. The [manual binding](../../manual-task-handoff.md#completion-and-closure-disposition)
retains the old spellings for this producer's current Relay-backed authoring.
This is a MINOR change under PV-002–004. The addition preserves accepted input
and behavior and requires no new fields, approvals, operator actions or gates.

## Compatibility evidence

The pinned Relay 10.0.0 Skill describes legacy literals for authoring and retains
the typed exact-result path for accepted no-PR results. Its bundled v1 and v4
schemas match the corresponding public Relay source at
`3337e74b4a54846122eac9dc2111781b8a1056a7`. The public JavaScript
`stableClosurePolicy` function was exercised on all four spellings. Both old
spellings parsed without warning and appeared in the v4 Decision and admission
enums, while both new ones produced `ISSUE_CLOSURE_POLICY_INVALID` and were absent
from both enums. The Rust Reviewer implements the same legacy-only policy.
[JavaScript source](https://github.com/jresearchsoftware/codex-relay/blob/3337e74b4a54846122eac9dc2111781b8a1056a7/contracts/src/github-authority.mjs#L61-L65)
· [Rust source](https://github.com/jresearchsoftware/codex-relay/blob/3337e74b4a54846122eac9dc2111781b8a1056a7/reviewer/src/task_authority.rs#L879-L895)

The upgraded-runtime cases in the authoring table are modeled. Public
[Relay proposal #294](https://github.com/jresearchsoftware/codex-relay/issues/294)
still concerns separately owned support, so this result establishes no upgraded
Relay runtime or live consumer qualification. A consumer with an upgraded
runtime and old Shared guidance or Skill continues legacy authoring. A compatible
consumer can prefer new names after its accepted Shared version, applicable
Skill, authoring rules and tooling support them together. Shared-only manual
adopters can use the new names where their effective tooling permits them.
Exceptional downgrade to an incompatible Relay version is outside the automated
migration support promise and may require separately authorized manual handling.

Historical readback confirms #133 still has its original `keep-open` field
and is closed as completed after recorded exact-version publication. The trusted
Task 84 Decision retained its then-applicable publication and follow-up Issue
conditions after source merge. Both records retain their original meaning.
[Task 133 completion](https://github.com/jresearchsoftware/shared-governance/issues/133#issuecomment-7109009106)
· [Task 84 Decision](https://github.com/jresearchsoftware/shared-governance/issues/84#issuecomment-6576169608)

The Issue and PR walks are source-level scenarios. GitHub documents closing
linked Issues on default-branch merge and recording completed, duplicate and
not-planned Issue dispositions. Cancellation or supersession uses the supported
status reason with the actual rationale.
[Linked pull requests](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
· [Issue status reasons](https://docs.github.com/en/graphql/reference/issues#issuestatereason)

## Producer-local FPF scenarios

| Conversation | Expected guidance |
| --- | --- |
| Advise the owner on this naming migration | Consider the actual ambiguity and compatibility cost. PSDA.8 helps compare dual-name coexistence with a forced switch. The charter's qualified FPF snapshot (`ailev/FPF@55ef163f91d42b48785bd297b50322e072d0a950`) and method effect are decision evidence. A gain in model reliability remains hypothetical. |
| Answer a routine technical question or report an ordinary check result | Answer directly without method notes. |
| Independently assess a material solution or author a substantially new Task | Retain the accepted #129 method use and source qualification. Applicable review authority and acceptance evidence still govern. |

The FPF additions live in root AGENTS, the custom Instructions source and its
generated projection. They add no package-wide adoption, external service or
validation gate. Projection verifies the complete text within the existing
budget. It supplies desired source text for later owner reconciliation.

## Continuation after this candidate

Independent assessment and owner integration precede exact accepted package
publication and its verification. The complete desired ChatGPT Project
Instructions changed. After integration, use the existing TH-029 procedure to
reconcile the whole accepted text with live Project Settings, including owner
application and supported readback or attributable confirmation as needed.
Then the owner-facing continuation can close #136 on its actual completion
condition and reconcile #135 against the same integration and readback evidence.

Separate producer follow-up for the tracker: **Retire legacy closure-policy
spellings from current Shared authoring after observed consumer migration.**
Base timing on actual compatible consumer adoption and a separate accepted
retirement decision. Remove both old values from current normative Shared text,
examples, new-Task guidance and affected projections at that time. Preserve
immutable editions and historical Task/Decision authority. Classify the eventual
removal under PV-002–004 using its actual compatibility impact. Relay owns its
legacy handling through #294. Trusted actors own separate Issue publication.
Relay Apply, other consumer migrations and this later retirement do not hold
completion of #136.
