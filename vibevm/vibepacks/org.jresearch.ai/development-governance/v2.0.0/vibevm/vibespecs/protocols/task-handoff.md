# Task handoff and continuation

Apply this protocol to governed task execution, result handoff and continuation
only when the owning project has explicitly adopted it. Installation, a package
update or reading this file does not activate it or replace local authority.
Use the project's declared binding for its tracker, execution authorization,
retry/recovery mechanisms, conversation reuse, publication, review sufficiency
and protected actions. Those mechanisms implement the shared Step semantics
below; they do not silently redefine them.
This protocol works manually; it grants no execution, review, merge, release,
installation, consumer-adoption or closure permission.

## Stable charter and chronological authority

Keep one current canonical Task reference: its goal, scope, completion conditions,
boundaries and authorized decisions. For governed GitHub-repository work, use
the Issue and its explicitly linked canonical records as the durable primary
reference. Another tracker needs an equally unambiguous project-owned binding.
Before first authorized execution, a placeholder or idea body may evolve into
an actionable charter. Proportionately choose body consolidation or a separate
Decision: consolidate when that improves clarity without hiding substantive
public discussion, contribution attribution or decision provenance. Preserve
or link meaningful earlier discussion as appropriate. Preliminary thoughts and
editorial refinements do not each need a formal Decision.

From first authorized execution onward, keep the body as the stable historical
charter. Append substantive changes to scope, requirements, permissions,
completion/closure conditions or newly admitted work as explicit owner-authorized
Task Decision comments in chronological order. Another tracker needs equivalently
durable, clearly linked decision records. Do not prepend later directions or
rewrite the charter after Outcomes. Only narrowly non-semantic editorial body
corrections are permitted; they must not obscure changed authority.

Completion or reopening preserves the original charter and historical execution
and acceptance. Append reasons, changes and new admissions as subsequent
Decisions; reopening resets neither Step numbering nor accepted history.
Resolve effective current authority from the original charter plus applicable
authorized Decisions, including explicit supersession or revocation. Neither
the latest body alone nor every conversational comment defines that authority.
Outcomes and reviews are evidence and assessment, not automatic scope permission;
historical discussion, prompt snapshots and upstream analysis supply none.

A Decision identifies what was decided, the relevant prior result/discussion
and resulting scope, authorization or Step direction concisely and readably.
Distinguish Task authority changes from PR-specific findings/remediation. Carry
substantive authorized amendments into effective authority before affected work.
No blanket JSON/typed publication or mechanical comment is required for routine
already-authorized actions.

## Step as an authorized execution cycle

Identify the Task, current work unit/Step and meaningful purpose explicitly.
A Step is one separately authorized architect/owner-to-executor work iteration:
hand off a bounded Task objective, investigate/implement, test and correct as
needed, then return a terminal execution result for assessment (an Outcome,
BLOCKED or another explicitly recognized terminal handoff).

The next newly authorized execution handoff after that terminal result allocates
the next Step, even for the same goal, findings, branch or PR. Internal
implementation/testing/corrections and ordinary clarifications during the active
execution retain its Step. Carry an admitted develop/test/fix cycle to a useful
result; do not invent separate coding, testing or research Steps as ceremony.

Retry, recovery or republication of the same execution/result without a fresh
execution cycle preserves identity. A genuinely new execution after BLOCKED
gets a new Step. Reconcile uncertain prior activity before deciding which case
applies. Review, discussion or a Decision alone allocates no Step; a Decision
may authorize the next execution, whose handoff starts that Step.
Step is not a PR, commit, conversation, transport attempt, test pass or formal
lifecycle phase. There is no fixed Step count or productivity measure, and a
terminal Step does not establish Task completion. Projects own authorization
and identity mechanisms, not an incompatible silent interpretation of this rule.

Use `Task N — Step S — <purpose>` for task-execution thread navigation in adopting
projects, with a concise purpose and the canonical Task link nearby to distinguish
projects with the same number. Number mappings for other trackers and any local
extensions belong to their declared binding. Rename when the client supports it;
verify the persisted title before claiming it changed. If rename or verification
is unavailable, disclose that limit and use a supported navigation aid. Title
limitations alone need not block useful authorized work. The title is navigation,
not authority, and specifies no labels, remediation identifiers or typed records.

## Startable handoff and bounded execution

The default execution prompt is a short navigation and start instruction:
Task, Step, short purpose, repository/canonical Task link, and a direction to
read the full Task chronology and linked authority, applicable accepted governance,
execute the admitted Step and publish its result for independent assessment.
Do not restate accessible goals, requirements, investigation steps, test matrices,
boundaries or publication contracts, even when duplication seems helpful.
Read the complete relevant discussion, Decisions, Outcomes/reviews and linked
records, not just the body. After an Outcome use a new small handoff and the
corresponding admission, not a rewritten charter.

Add only irreducible handoff-specific routing/environment facts unavailable from
canonical authority, such as a starting worktree or material access limitation.
There is no universal model/effort field or extra ceremony. If a project needs
a bounded execution snapshot, identify its origin/freshness; it is subordinate
to canonical authority and does not replace this minimal default.
Requested model/client settings
are not proof of actual execution; disclose relevant unavailable capabilities or
evidence. Delegation does not expand authority.

Before starting or resuming, refresh current Task decisions, the applicable
accepted result/review frontier and mutable work facts. Load detail needed for
the next decision. Preserve useful and unrelated work, inspect uncertain prior
activity, and reconcile the canonical branch/artifact safely before comparing
identities or repeating a mutation. A real authority or result mismatch is a stop
condition, not permission to reset, replace or silently overwrite work.

Continue evidence-backed corrections inside the admitted goal without adding
approval stages for every local fix. Stop when scope/permission or prior external
mutation is uncertain, a material policy choice needs its owner, a protected
boundary is inaccessible, or repetition yields no new evidence. Preserve useful
results and disclose unreconciled work. A preferred new workflow or material
obligation needs the owning project's decision before implementation.

## Exact result and independent assessment

Publish an attributable result through the project's authorized path, verify the
published target, and bind claims and evidence to the identifiable artifact or
immutable result under review. Report accomplished and blocked work, applicable
checks, remaining work, observations versus unverified claims, and material
limitations. For known material warnings, state source, impact, disposition,
next action and missing evidence; inaccessible evidence is a gap, not proof of
warning absence. A no-change, analytical or non-repository result needs no empty
commit, fabricated SHA or artificial PR. Use the existing Task/result records.

Require substantive independent assessment of the complete identified result
against current authority, completion criteria and affected behavior. Tests and
implementation helpers supply evidence, not independent acceptance. Record who
or what assessed which result and what evidence was available. Merely opening
another chat or checking one's own work does not establish independence.

A separate evaluator can provide an assessment outside GitHub, published with
honest attribution through one owner account. That publication does not prove
an authenticated distinct reviewer, create native GitHub approval, satisfy branch
protection or reproduce a product's enforced reviewer separation. A comment
headed `APPROVE` supplies none of those assurances. The adopting project's policy
decides sufficient acceptance evidence and native identity requirements; preserve
any stronger boundary. If only the implementer is available, disclose the gap and
leave independent acceptance pending.

Actionable findings identify the reviewed result/comparison, problem, impact,
correction and acceptance evidence. Distinguish introduced, pre-existing, newly
exposed/blocking and undetermined findings before claiming a regression. Correct
within authorized scope and assess the new result, covering prior findings,
changed behavior, adjacent risks and genuinely new findings. Explain a surviving
blocker through the unmet invariant or evidence gap. Pre-existing defects enter
remediation only within admitted scope or as a material dependency. A new
preference is not retrospective owner authority.
Reuse proof for the same invariant and unchanged result while retaining separately
justified checks and independent review. A changed result needs the applicable
fresh qualification and review; old exact-result acceptance does not carry over.

## Result acceptance strategies

Select by the decision needed to accept the result, not whether it contains code
or documentation. The two shared standard strategies are:

| Strategy | When applicable | Positive independent review |
| --- | --- | --- |
| Direct | Fixes, implementation of agreed requirements or other work with an established desired result and criteria. | May publish formal exact-result APPROVE immediately once applicable evidence, checks and authority requirements are satisfied. Previously authorized post-approval continuation, including safe automatic merge, is unchanged. |
| Deliberative | Open research, architecture selection, methodology/policy proposals or other results needing owner judgment about alternatives, trade-offs or proposed commitments. | First supply a substantive non-approving assessment/preview with findings and warnings. Even a positive assessment must not publish formal APPROVE or trigger approval-driven merge before intended owner discussion and the necessary Decision. |

Resolve selection in order: (1) explicit owner-authorized strategy in the charter
or subsequent Task Decision; (2) applicable adopting-project rules, including
additional named strategies; (3) shared defaults: Direct for an already decided
result/requirements, Deliberative when the output itself requires architectural,
methodological or policy choice. Technical research can be Deliberative; a
correction to already accepted governance can be Direct. An authorized Decision
may revise the strategy before acceptance. Resolve material ambiguity about
needed owner deliberation before formal APPROVE. Customization cannot weaken
independent assessment, accepted owner/trust boundaries or required checks.

For Deliberative acceptance:

1. The executor returns an attributable Outcome and reviewable immutable result.
   An independent evaluator substantively assesses that exact result, including
   findings/warnings, through the authorized project mechanism without approving.
   Record real defects as actionable findings; use a genuine change request when
   warranted, never a fake REQUEST_CHANGES solely to suppress approval/merge.
2. The architect/owner discusses and records an explicit Decision: accept, request
   corrections/new work, reject, or accept research-report quality without adopting
   its recommendation. Report acceptance does not authorize implementing,
   migrating, installing or releasing the proposed architecture/policy.
3. If the owner authorizes acceptance of the unchanged result, verify that the
   reviewed head and effective authority are still current, retain applicable
   checks/identity requirements, reuse sufficient independent evidence and publish
   the actual exact-result APPROVE. Do not require another complete review of
   the same head without a reason. A changed result needs fresh applicable review.
   Once genuine approval is published, existing authorized project continuation
   may proceed within its own boundaries.
4. Material rework or a new execution after terminal Outcome gets the next Step
   under the execution-cycle rule. Discussion and preliminary review alone do not.

This strategy governs publication of the review verdict, not merely a hold on
post-approval merge. A post-approval continuation hold alone cannot prevent
premature APPROVE. Result-quality acceptance, owner selection of a recommendation,
PR integration, Task closure, deployment and publication remain distinct
permissions/events; an evaluator can value a report whose solution the owner rejects.

These are reusable defaults, not a universal schema, rigid Task classifier or
replacement for a product's Reviewer/Writer. Bind review publication locally;
future consumer automation must enforce the selected boundary before its native
verdict while preserving exact-head, identity and merge guarantees. Shared
authoring or publication does not authorize that consumer implementation,
installation or changed automation.

## Authorized continuation and completion

Acceptance, integration, publication/installation, further execution and Task
closure are distinct. Continue only when current authority permits the next
action and applicable checks, acceptance and protected boundaries are satisfied.
Already authorized actions need no ceremonial reconfirmation; new scope needs
its owner. A completed or accepted Step does not prove the whole Task complete,
and accepted source does not prove deployment or release. Reassess concrete
completion conditions, remaining work and holds at meaningful transitions; do
not close with known remaining work or copy a stale disposition indefinitely.

Keep evidence and continuation proportionate in existing Issue/artifact/review
records. This protocol introduces no universal schema, registry, state machine,
automated gate, mandatory tooling or product execution mechanism. Technical
product fields can evolve without changing shared meaning; changes to authority,
warning disclosure or mandatory operator work need the applicable owner decision.
Shared-protocol adoption, a product upgrade and client-adapter compatibility are
separate project-owned decisions; none implies the others.
