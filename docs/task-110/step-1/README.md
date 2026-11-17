# Task 110 — Step 1 — Standing small-improvement delegation

## Authority and bounded baseline

[Task 110](https://github.com/jresearchsoftware/shared-governance/issues/110)
and its owner decision in the live charter, read on 2026-11-17, authorize
changing the Small Improvements contract from case-by-case proposed inclusion
to standing delegated inclusion.
The independently accepted source-main is frozen at
`1aabc1b1131d6d73285f84d8dc8a8dd3725135a4`, including Development Governance
10.0.0 and the producer adoption accepted through
[Task 107 / PR 108](https://github.com/jresearchsoftware/shared-governance/pull/108).
Candidate AGENTS, boot, guide and protocol content remain proposals during this
Step; they do not govern their own implementation or review.

The bounded canonical baseline is that commit's complete SI-001–SI-008,
Small Improvements usage guide and conditional boot route, the root producer
adoption and its authoring/integration summaries, RA-006/007, package versioning,
and the existing Task Handoff authority/result/continuation boundaries.
[Task 69's original coverage](../../task-69/step-2/README.md), its
[version reconciliation](../../task-69/step-3/README.md), and
[Task 107's adoption evidence](../../task-107/step-2/README.md) preserve the
earlier decision provenance. Task 110 deliberately revises their relevance and
per-candidate authorization behavior; this is an owner-selected semantic change,
not a claim that the earlier accepted implementation was unauthorized.

## Semantic coverage

The canonical proposed owners are the
[SI protocol](../../../packages/development-governance/vibevm/vibespecs/protocols/small-improvements.md),
its [usage guide](../../../packages/development-governance/vibevm/vibespecs/guides/small-improvements.md),
and the [conditional package boot](../../../packages/development-governance/vibevm/vibespecs/boot/development-governance.md).
The following mapping concerns obligations and operator behavior, rather than
word matching. The current package contains ten protocols; the remaining nine
retain their own semantic ownership.

| Accepted 10.0.0 behavior | Proposed treatment and material effect |
| --- | --- |
| SI-001: separate explicit topic adoption; install/update, TH and references do not adopt SI; owning-repository Issues; existing local rules survive reconciliation | Preserve the applicability and local-policy boundaries. Explicit adoption now supplies standing same-repository delegation for eligible inclusion in otherwise authorized source work. It grants no new execution launch, foreign control, protected admission, review, merge, release, label/settings, adoption or closure authority. This delegation is an explicit semantic change. |
| SI-002: SI owns capture/discovery/proposed inclusion/disposition; CD owns decision promotion, TH owns execution/results/acceptance/continuation, RA owns binding requirements | Replace proposed inclusion with delegated inclusion; retain all other semantic owners, native admission, Writer/Reviewer identity and protected actions. RA-006 remains unchanged: an unaccepted suggestion or label creates no obligation; explicit accepted adoption supplies the bounded delegation here. |
| SI-003: ordinary owning-repository Issue; exact `small-improvement` label mandatory, title prefix optional; evidence/provenance/deferral/validation; authorized tracker path and label creation | Preserve these duties and exceptions, including capability disclosure, existing tracker fallback, no form/ledger/controller, and no extra Issue for corrections already in admitted scope. A candidate label still cannot start execution or authorize itself. |
| SI-004: only corrections relevant to the receiving change; boundedness judged by risk/contract impact; dependencies/conflicts/ownership checked; unsafe, urgent, large or unresolved work uses ordinary authority | Deliberately remove thematic relevance and necessity to the main objective as eligibility requirements. Include all reasonably implementable, safe, independently actionable same-repository candidates that remain bounded and reviewable together. Preserve the safety, contract, dependency, ownership and urgency exceptions; assess cumulative risk and current Task constraints. Package size never waives version/release duties. |
| SI-005: discover at suitable source-changing Task, first source-changing Step after analysis, or relevant CR; notify owner with proposed IDs; analysis exemption and no ceremonial repeats | Preserve those opportunities and add a genuine new source-changing PR opportunity. Inspect the complete exact-label result set, including pagination, and include all eligible candidates. Remove advance notification/per-candidate owner selection as prerequisites. Preserve analysis-only exemption, broader accepted local discovery rules, material-change refresh, no cross-repository/periodic scan, queue-empty gate or queue-triggered execution. |
| SI-006: receiving Task/CR explicitly accepts IDs/bounded scope before implementation; already delegated corrections need no new ritual; approved PR protected | Replace per-candidate authorization with exercise of accepted standing delegation. Record included IDs/bounds in ordinary receiving records and result, without a separate candidate Task, Step, PR, owner amendment or pre-implementation ceremony. Preserve explicit current exclusions/holds, execution/admission binding, native trust, material-scope Decision ownership and the PR-CR authority limit. Preserve approved-PR deferral and the ordinary path for required/urgent defects. |
| SI-007: accepted candidates link to source Issue/Task/PR with provenance; implement/test together and independently review one combined exact result; delivery/checks/warnings/remainder recorded | Apply the same duties to included candidates, with a receiving Task link where a Task exists. Preserve normal checks, coupled paths, changed-head rereview, package versioning, Draft/Ready, protected actions, merge and closure ownership. Successful tests, scheduling or a pushed commit still do not establish accepted integration. |
| SI-008: pending open/labeled traceability until accepted integration; reconcile a fix elsewhere and distinct installed outcomes; deferral/partial/cancel/drop/duplicate/superseded/no-longer-needed dispositions | Preserve the complete lifecycle and evidence boundaries. Add concrete reasons and the next suitable opportunity or ordinary route for deferral. Topic mismatch, non-necessity to the main goal and preference against delegation are no longer valid deferrals. Age neither executes nor closes work. Preserve authorized tracker handling and separately accepted label lifecycles that keep unfinished work discoverable. |
| Guide and boot: conditional complete-protocol routing, complete exact-label lookup, adoption/deduplication examples and consumer-owned migration | Align examples and producer summaries with the new delegation without creating a second normative copy or automatic adoption. Preserve the broader Docs Evolution Review planning rule, its label semantics, Relay native trust/compatibility/TEST-PROD boundaries and consumer-owned upgrade/adoption. Existing historical reports remain historical. |

No RA-006 change is needed: the authority source changes in SI's explicit
adoption contract, while RA continues to distinguish accepted delegation,
optional proposals and routine implementation choices. TH retains Task/Step
admission, chronological Decisions, attributable Outcomes, independent exact-head
assessment, Draft/Ready, continuation and closure. SI does not supply competing
automation or erase a product's supported admission rules. A genuine conflict
with a native binding remains a concrete authority limitation to reconcile, not
permission to bypass it.

## Source-based scenario walks

These are manual modeled applications of the proposed protocol and guide.
They are not actual model executions, real receiving Tasks, tracker mutations,
live consumer migrations or independent acceptance. The hypothetical consumer
below uses ordinary GitHub source PRs, has explicitly adopted the reviewed new
SI contract, and has no residual old-project relevance or per-candidate approval
rule. This makes the shared rule, rather than leftover consumer text, responsible
for the expected behavior.

| Scenario | Expected path and evidence boundary |
| --- | --- |
| An authorized parser bugfix PR discovers a bounded correction to an unrelated CLI help example | At the suitable source opportunity, inspect all open exact-label Issues. If the help correction is safe, independently actionable, same-repository and reviewable with the parser fix, include it automatically under accepted delegation. Record its Issue/provenance and bounded change; assess both behaviors in the combined result. Neither thematic mismatch nor non-necessity requires a new owner choice. |
| Three safe candidates affect an example, a test fixture and a small source correction | Assess each candidate and their combined risk/conflicts. Include all eligible candidates in the same reviewable PR, with individual Issue links and clearly identified corrections. Use normal proportionate checks and one independent review of the combined exact head; create no separate execution cycle or ceremony-only commit per Issue. If their combined impact ceases to be bounded/reviewable, record that concrete reason rather than silently selecting only the convenient one. |
| An analysis-only Task is followed later by its first source-changing Step | Analysis adds no SI scan unless a broader accepted local rule requires one. The first suitable source-changing Step performs discovery; analysis does not permanently discharge that opportunity. |
| A labeled candidate would change production credentials; another depends on an undecided platform or material operator choice | Preserve the credential boundary and unresolved choice. Record specific risks/dependencies, retain pending discovery and identify the ordinary authorized route. A small diff and exact label do not make either eligible. |
| The current Task explicitly excludes a candidate or preserves an owner hold | Respect the effective exclusion/hold. Record the concrete current-authority reason and future opportunity or required ordinary Decision. Standing delegation supplies no override. |
| An unrelated minor correction is noticed after exact-head approval | Leave the approved PR undisturbed solely for batching; capture or retain the candidate for the next suitable change. A genuinely required or urgent defect uses the ordinary correction and fresh-review path. |
| A selected correction is pending, then its receiver is cancelled, drops it or lands only part | Scheduling does not close the source Issue. Record the actual receiver outcome and exact remaining criteria; retain or restore open labeled discoverability. Partial delivery is never reported as fixed. |
| Another PR has already integrated the correction, or the candidate proves duplicate/superseded/no longer needed | Connect accepted integration evidence and reconcile any remaining criteria and distinct installed outcome before authorized fixed closure. For duplicate/superseded/no-longer-needed disposition, retain the surviving reference or concrete evidence/reason and never claim a fix occurred. Do not fabricate a new implementation or retrospective review. |
| A matching candidate exists only in another repository or separately governed project | No cross-repository SI scan, edit, label, execution, review, merge or closure follows. Keep any permissible incoming proposal distinct from foreign lifecycle control under RA-007; hand controlling work to the receiving project's own context. Common ownership or access supplies no transfer. |
| Several internal commits follow one completed discovery; then a genuine later source-changing PR starts | Do not repeat the lookup per commit or internal correction solely as ceremony. Refresh for material receiving-scope changes or new relevant information. The next genuine suitable source-changing opportunity performs discovery again; avoiding per-commit scans is not a permanent scan exemption. |
| Search is empty, lacks eligible work, or a candidate has a prefixed title but lacks the exact label | Empty/no-eligible results do not block the main task or force batching. A title alone is not discoverability. Preserve authorized capability reporting and existing tracker fallback rather than claiming unlabeled work is queued or creating labels without authority. |
| A consumer installs 11.0.0 without separately adopting SI or reconciling an incompatible local binding | Installation does not activate the topic or replace local authority. That consumer retains its accepted rules until its own reviewed upgrade/adoption reconciles the delegation. No behavior is inferred from transport success alone. |

For the original producer, the proposed root route must read the complete
selected accepted SI protocol after independent acceptance; compact summaries
must not retain the superseded relevance/advance-approval prerequisite or become
a parallel policy. Historical 10.0.0 and earlier frozen slots remain unchanged.
Ordinary Git recovery reverts the complete candidate source/materialization
change; it never rewrites an accepted release or a remote immutable tag.

## Current Step discovery and exclusions

This Step still applies frozen accepted 10.0.0, including its explicit proposed
inclusion and receiving-authorization requirements. Its own candidate delegation
cannot retroactively admit backlog work. Task 110 changes the policy itself;
the read-only public GitHub API lookup on 2026-11-17 returned exactly
[#105](https://github.com/jresearchsoftware/shared-governance/issues/105)
and [#106](https://github.com/jresearchsoftware/shared-governance/issues/106)
for disposition, both open with the exact label. The complete result came from
`/repos/jresearchsoftware/shared-governance/issues?state=open&labels=small-improvement&per_page=100`;
their Issue bodies supplied the constraints below. No credential was used and
no tracker mutation was performed. Discovery does not include their implementation.

#105 involves a material operator choice about optional GitHub bootstrap
settings. #106 retains an unresolved platform/owner choice about discretionary
chat-to-Work handoffs. Those concrete unresolved choices use their ordinary
authorized paths; neither is included in this Step. Both remain open with
`small-improvement` discovery and their original provenance. No fixed closure,
foreign repository mutation, relabeling or retrospective use of the proposed
policy is claimed.

## Compatibility, qualification and continuation

Package classification is **MAJOR: 10.0.0 → 11.0.0**, under PV-002–004. One
version identifies the whole package. The change removes the accepted relevance
filter and per-candidate authorization/advance-notification workflow and replaces
them with mandatory inclusion of all eligible candidates under explicit standing
delegation. This materially changes scope authority and operator/agent behavior;
it is not a PATCH wording repair or merely additive MINOR topic. Candidate
11.0.0 remains subject to version reconciliation against accepted main before
integration, exact-head review and normal frozen-source checks.

The operator cost shifts from repeated selection/amendment to complete bounded
discovery, eligibility/cumulative-risk assessment, combined validation and clear
disposition. It adds no per-commit scan, recurring audit, bot, ledger, controller,
approval stage or autonomous queue-triggered execution launch. Queue size and correction coupling can
increase review effort; no latency, cost or model-reliability measurement is
claimed. Existing safety and admission boundaries still limit eligibility.

This record supplies a source-to-rule mapping and modeled scenario evidence.
Actual source/export, release, distribution, self-adoption and native-generation
results must be reported for the concrete candidate by the executor's canonical
Outcome and applicable exact-head CI; no check is marked passed here without
its execution evidence. File/route/export integrity can show delivered text and
selection, but cannot establish actual model compliance, installed service
behavior, live tracker disposition or another consumer's adoption. Implementation
helpers supply evidence, never independent governance acceptance.

Independent exact-head assessment, owner-controlled integration and verified
publication remain separate events. The current admitted continuation and live
Task authority determine the next action; this evidence document grants no
review verdict, merge, release, closure or foreign adoption. Publication success
must identify the accepted source and actual package version before it can
satisfy any publication condition. Consumer upgrade, topic adoption, local
deduplication and any product runtime changes remain separately owned.


## Executed local qualification

The implementation and generated payload at the tested candidate passed:

- `python3 scripts/qualify.py --export-ref HEAD`: source, protocol anchors/links,
  complete exact-commit export, selected native slot/lock/boot, unchanged Relay
  projection and bounded credential-marker scan.
- `test-distribution.py`: 52 tests; `test-self-adoption.py`: 19 tests;
  `test-chatgpt-projection.py`: 29 tests, all passed.
- `test-release.py`: 26 tests, including 6 optional native integration tests
  skipped; `test-publication.py`: 12 tests, including 1 optional native test
  skipped; `test-publication-dispatch.py`: 7 tests. All executed tests passed.
- `package-release.py --base <frozen-baseline> --check-remote-tag`: 10.0.0 to
  11.0.0, one MAJOR step; no existing 11.0.0 public tag observed at check time.
- `check-publication.py` against the candidate and frozen baseline:
  `CANDIDATE_VALID`, using unchanged publisher code and the committed MIT
  redistribution/export binding. This is source readiness, not acceptance,
  push CI eligibility or actual publication.
- Hash-checked pinned VibeVM 1.0.11 performed native mixed-graph installation in
  contained disposable staging, selecting Shared 11.0.0 and retaining Relay
  5.0.0 / Landscape model guidance 1.0.3 / subagents 1.0.2. Native Skill install
  reported unchanged; exact projected Skill/receipt bytes match. Only selected
  new outputs were transferred; historical slots were preserved.
- `qualify-vibevm.py --vibe <pinned-binary>`: six native validation/check/Skill
  listing commands passed. Its 19 expected orphan-slot warnings identify retained
  frozen history, not active selection. There were no errors or other findings.
- Direct baseline comparison: all other nine protocol files and the complete
  ChatGPT tool payload are byte-identical. Whitespace checks passed.
- Candidate ChatGPT `update`: complete effective Instructions `NO_OP`, Sources
  disabled, generated Instructions unchanged. No live application occurred or
  is newly required by this unchanged text. Earlier live-verification gaps remain.

The first in-place check attempts encountered existing environment constraints:
TMPDIR was inside the authoring checkout (the exporter intentionally rejects that
as a distribution destination), and local fixture clones hit Git's ownership
check. No product code or host configuration was changed to bypass either.
A local Git bundle supplied an exact committed verification checkout, with its
sibling temporary directory still contained under the admitted workspace. The
affected checks then passed there. Native staging used a verified ordinary-file
Git archive and isolated settings; no outside workspace state or credentials
were imported. The initial exporter invocation using symbolic `HEAD` was also
corrected to its required full SHA before successful generation.

These checks ran on local candidate source and generated state. Required native
exact-head CI and any protected installed-runtime proof remain for the trusted
publication/review path. No root/sudo operation, GitHub write, consumer upgrade,
Workflow/credential change, live Settings write or independent acceptance was
performed. The [Relay handoff draft](relay-adoption-handoff.md) is prepared for
canonical incoming proposal publication only after exact accepted publication
is verified; it does not dispatch or control foreign work.
