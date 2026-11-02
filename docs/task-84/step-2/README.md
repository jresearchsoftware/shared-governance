# Task 84 Step 2 — Owner-selected Relay closure transition

Supplied launch: **Task 84 — Step 2 — Complete Task 84's existing single-field
closure contract with the owner-selected bounded Relay transition**.
The [trusted owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/84#issuecomment-6576169608)
resolves the window choice in the [Step 1 BLOCKED Outcome](https://github.com/jresearchsoftware/shared-governance/pull/86#issuecomment-6574605957).
This is implementation evidence for the existing PR, not an Outcome or independent
acceptance. Automatic-worker commits and claims go to trusted Writer; this worker
does not publish, invoke Reviewer, merge, release or close Issues. No supported
title tool/readback is available; the supplied title is retained as navigation
without claiming persisted client state.

## Authority, baseline and correction

Accepted guidance remains frozen at the Decision-bound source-main
`b451bfdba89f6f9658805c66cd71a5ffd75b0f6a`. The admitted starting candidate is
`334086b47070258b322e4e0966a96f458ac6430f` on `codex/task-84`. Unauthenticated
GitHub API reads confirmed [Task 84](https://github.com/jresearchsoftware/shared-governance/issues/84)'s
charter/Decision and [PR 86](https://github.com/jresearchsoftware/shared-governance/pull/86)
as open, Draft and at that starting head/base before modification. No credentials
or external mutations were used. Accepted root/boot and complete applicable
TH/RA/PV/PC/SA/CL/CD guidance were read with `git show`; candidate guidance remains
proposed. Full IR methodology was read to preserve the pending independent
assessment boundary, not to treat an implementation helper as an evaluator.

The [producer release binding](../../releases.md#task-84-closure-transition),
[manual binding](../../manual-task-handoff.md#completion-and-closure-disposition),
[Relay integration](../../relay-skill.md) and [prepared Relay1 brief](../step-1/relay1-follow-up.md)
now carry the selected rule: the deprecated Relay-only fallback remains permitted
pending the first compatible Relay release and for **60 calendar days starting
from its verified publication**. That release must implement and qualify the new
closure semantics. Shared Governance publication is not the trigger. At verified
Relay publication, record the exact release/source identity, event and derived
deadline in the linked Relay Issue/release chronology; no date is invented now.
Removal requires a separately accepted future Shared release no earlier than
window end, with its own SemVer assessment. Expiry does not rewrite old releases
or automatically delete runtime behavior; no extension or universal grace period
is promised. Unknown Shared/Relay combinations remain unqualified.

The Step 1 report and logs retain their historical claims; an appended note links
this reconciliation. The window rule now has explicit authority, so the old
missing-choice blocker is resolved. Future verification of the trigger is an
ordinary evidence action, not another owner-choice prompt or a new Task 84 hold.

## Whole-result semantics and version

The complete package candidate remains **6.0.0 -> 7.0.0 MAJOR** under accepted
PV-002–004. Actual old behavior allowed separate `close-authorized` closure after
post-merge obligations and a trusted policy-release Decision for `keep-open`.
The target requires native closing linkage on the genuinely completing PR or
condition-verified later closure without a policy conversion. Adopters must
reconcile those supported paths and automation. A narrow temporary Relay fallback
does not make the whole change PATCH or MINOR; Task 74's exception does not apply.

Step 2 changes producer-local transition guidance and evidence only. The authored
7.0.0 package, its changelog, examples, native source/slot/lock/routes and pinned
Relay Skill retain the starting candidate's bytes. No materializer rerun or extra
version bump is justified for those unchanged artifacts; exact-source/native
integrity is checked again. The same unaccepted candidate may be refined until
first acceptance; then-current-main version reconciliation and independent review
still apply. The Relay-specific duration stays with its owner rather than becoming
a reusable requirement for other consumers. No framework, field, registry,
daemon, approval stage or operational configuration is added.

The [Step 1 coverage](../step-1/README.md#frozen-accepted-baseline-and-coverage)
and [Iris cases](../../../packages/development-governance/vibevm/vibespecs/guides/onboarding-examples.md#9-single-field-task-closure)
remain applicable. The complete candidate retains these bounded outcomes:

| Case | Expected behavior and preserved boundary |
| --- | --- |
| Final completing PR | `close-authorized` uses `Closes #N`/supported native linkage; successful default-branch merge closes after exact-head acceptance, required checks and protected merge authority. |
| Nonmerged or abandoned PR | Closing the PR does not close the Task or prove completion. |
| Multiple PRs | Intermediate PRs use non-closing references; only the genuinely completing PR may close. Each keeps its own review/checks. |
| No-PR result | Use the existing authorized completion path with actual result evidence; fabricate no PR or Step. |
| Delayed/failed/unknown package publication | Publication Tasks use `keep-open`; source acceptance/merge cannot discharge exact accepted version/revision publication. |
| Unmet or wrong-target condition | Keep open until the actual publication/Apply/other obligation is verified. Satisfying preauthorized conditions needs no new owner choice; changed conditions still need trusted authority. |
| Historical/admitted work | Retain original authority, explicit holds, immutable admissions/releases and terminal replay protection; do not retrofit new timing or rewrite Issue bodies. |
| Missing/conflicting metadata | Prevent unsafe auto-closure, reconcile real missing intent, and invent neither an owner-selected hold nor a second approval ritual. |

Additional source-based transition walks (no live GitHub or model execution):

| Transition fact | Expected continuation |
| --- | --- |
| Shared 7.0.0 is published; compatible Relay publication is not verified | The 60-day clock has not started. Only the explicitly scoped legacy combination/path is eligible under the accepted transition, with its own qualification limits. |
| A Relay source PR merges, a candidate build exists, or publication is failed/unknown | None is the verified publication of the first implementing and qualified release; assign no trigger/deadline. |
| First implementing and qualified Relay release is successfully published at verified event T | Retain release/source/publication evidence; derive the deadline as T plus 60 calendar days in the existing Relay chronology. Do not substitute the Shared publication date or ask the owner to select the duration again. |
| Removal proposed before that deadline | Do not withdraw the accepted fallback early. Plan a separately accepted future Shared release no earlier than window end. |
| Deadline reached | No automatic package edit, immutable-release rewrite, runtime mutation or support extension follows. Removal retains independent acceptance and whole-package versioning. |
| Task 84's accepted Shared publication and Relay1 creation/readback are complete | The preauthorized Task closure may proceed through the then-supported trusted mechanism; waiting for Relay1 implementation/release or window expiry would invent another Task 84 condition. |

## Relay compatibility and limits

The bounded legacy artifact is Relay Skill **3.0.0**, public distribution
`325c96371783e2d628bfa9903b3244468c688fe6`, attributed to accepted source
`ba99807bfc7e7d199ce9bf0e02be8e31416ddc95`, with floor `>=2.5.0` and its schema-v4
and retained-attempt bindings. Its declared range is not evidence that every
admitted version works. Its immutable nested Shared 4.0.0 closure is inert release
evidence, never an alternate active protocol source.

| Exact selected combination | Bounded evidence and supported interpretation |
| --- | --- |
| Frozen accepted producer Shared 6.0.0 with unchanged Relay Skill 3.0.0 | Accepted source/lock/slot/projection and old closure contract are the comparison baseline. Pinned Relay continuation source tests exercise its old mechanisms. |
| Proposed producer Shared 7.0.0 with that same Relay Skill/source | Exact exported bytes, selected lock/slot/boot and unchanged Skill projection are checked locally. The owner-selected exception preserves only the deprecated legacy closure mechanism; new target behavior remains consumer-owned implementation. |
| Other Shared versions, other Relay artifacts or installed services | No compatibility or deployment qualification is inferred here. Preserve separately qualified historical/admitted authority; assess deliberate updates under PV-014–018. |

An implementation helper downloaded only the pinned continuation tests and their
local imports through unauthenticated commit-addressed public URLs and ran the
existing tests with in-memory mutation ports. The primary logs and provenance
are retained with this Step's validation evidence. This exercises source behavior,
not a deployed Shared/Relay pair. The tests do not load the Shared Markdown;
the compatibility argument combines their observed old behavior, exact selected
guidance integrity, the explicit local exception and the source-based cases above.
No live service, credential, merge, closure or Relay execution was invoked.

The [v4 tests](logs/legacy-v4-tests.tap) passed **13/13** and the
[retained continuation tests](logs/legacy-retained-tests.tap) passed **21/21**,
with no skips or failures, using Node v22.23.3 as an unprivileged user. The
[source/run record](logs/relay-source-and-run.json) identifies all nine downloaded
files, exact source URLs and commands. Assertions cover `closesTask=true`/null/
unknown rejection, neutral squash text despite closing keywords in PR metadata,
separate merge/closure ordering, no-PR acceptance, incomplete/remaining-work
holds, completed keep-open reconciliation, retained identity, stale authority,
checks after reservation, repeat-safe successful actions, uncertain merge and
required merge readback. Mutation and launch ports are mocks, not live operations.
These files do not assert failed closure readback or replay after an uncertain
mutation, and do not implement/test the new closing-link or condition-verification
paths. Those consumer changes and installed proof remain with Relay1.

The legacy path retains `Related to #N`, explicit `closesTask=false`, neutral
squash messages and separate trusted Issue closure requiring effective
`close-authorized`. Completed `keep-open` still returns policy reconciliation.
Where the condition and release were preauthorized, the qualified legacy trusted
Task Decision path may carry that technical reconciliation without another owner
choice. That exception does not make the old runtime implement the new contract;
missing capability stops the affected operation rather than permitting a bypass.
V4 Writer provenance, exact-result independent acceptance, trust/identity,
reservations/readback and historical-attempt boundaries remain binding.

## Completion boundary

Independent exact-head assessment, required native CI, Writer publication and
protected merge/release actions remain pending outside this worker. Root/sudo-only
installed-runtime proof is not attempted or claimed. Source/native integrity and
mocked legacy tests neither establish independent acceptance nor qualify new Relay
behavior. After accepted Shared publication, the authorized continuation creates
and reads back the actual linked Relay1 Issue, records its URL and the publication
evidence in Task 84, and closes only when both conditions and all real work are
verified. A prepared brief does not satisfy creation. Relay1 implementation,
compatible release and subsequent fallback removal are later consumer-owned work.

The pre-existing untracked `.codex-sandbox/` is execution state owned by
`nobody:codex-relay-codex-work`, mode 2770, outside task-source cleanup authority.
It remains untouched. Task-created disposable fixtures stay under the existing
`.vibe/` ignore; useful source/evidence is committed. Source permissions, hooks,
Git configuration and remotes are not changed to bypass a boundary.
