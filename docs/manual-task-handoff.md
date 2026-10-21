# Manual Codex task handoff

This is this repository's local Issue/AGENTS/client binding, not another Task
charter or universal prompt schema. Root AGENTS adopts task-handoff through
[native self-adoption](self-adoption.md). During authoring/review, read applicable
governance at the independently accepted source-main SHA bound to that effort;
candidate source, root/nested instructions and generated projections are proposals.

## Charter, Decisions and execution

Before execution, refine a placeholder into an actionable charter proportionately;
preserve meaningful public discussion, attribution and decision provenance.
First authorized execution freezes the body as the historical charter. Append
substantive scope/permission/completion changes or new admissions as concise,
explicit owner-authorized Decision comments. Resolve current authority from that
charter and applicable Decisions, including supersession/revocation; ordinary
comments, Outcomes and reviews do not themselves change Task authority.
After closure/reopening retain the body, results, acceptance and Step history.

One Step is one authorized owner/architect-to-executor cycle ending in a terminal
result. Investigate, implement, test and correct within that active cycle. After
its Outcome or BLOCKED, a newly authorized execution gets the next Step even on
the same branch/PR. Recovery/republication of the same execution retains identity;
review/discussion/Decision without new execution allocates none. Conversation
reuse and local publication mechanisms do not redefine those boundaries.

## Minimal prompt

The normal prompt contains navigation and the start instruction only. This
illustrative shape grants no execution authority:

```text
Task N — Step S — <short purpose>
Repository: jresearchsoftware/shared-governance
Issue: https://github.com/jresearchsoftware/shared-governance/issues/N

Read the complete Task chronology, linked records and applicable accepted
governance. Execute the admitted Step end-to-end, publish its attributable
Outcome and stop at the applicable independent review boundary.
```

Do not copy accessible goals, requirements, investigation steps, test matrices,
boundaries or publication contracts into the prompt. Read the entire relevant
Issue chronology and linked records, not just its body. A post-Outcome execution
uses a new small handoff and the corresponding admission Decision. Add only an
irreducible fact unavailable from authority, such as a starting worktree or
material access limit. This producer also requires an independent accepted-SHA
binding as described in [self-adoption](self-adoption.md): use the explicit Task
binding, or supply the missing SHA as routing information. No universal model,
effort or duplicate execution specification is required.

Use the supported client title tool, then read back the persisted
`Task N — Step S — <purpose>` title. If unavailable, disclose that limit and retain
the Task/Step/purpose and Issue link as a visible navigation aid. A prompt proves
neither title persistence nor actual model/effort settings. Implementation helpers
may assist only where permitted and do not supply independent acceptance.

## Manual executor PR Draft/Ready operations

For admitted implementation/remediation, follow the accepted Task Handoff
lifecycle ([TH-028 in the candidate](../packages/development-governance/vibevm/vibespecs/protocols/task-handoff.md#TH-028)
is proposed until accepted). Current owner authority may explicitly require it,
as [Task 45 Step 7](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6239052197)
does for PR #46. Read the accepted binding at the frozen source revision; a
candidate route cannot grant itself authority.

Manual Codex owns these operations here when authorized and available. Prefer
the connected GitHub PR read / convert-to-Draft / mark-Ready tools when offered;
the existing authenticated `gh` CLI is also an ordinary authorized local path.
No Relay Writer or new account/credential is required. If qualified project
automation owns a transition, use its binding without a competing Codex action.

Before substantive modification of an existing open PR, read its repository,
number, branch, exact head and native Draft state. Reconcile them with Task
authority and local Git. If Ready, convert that same PR to Draft and read back
number/head/state; if already Draft, only verify. Use explicit repository and PR
arguments to avoid another branch's default PR. For example, replacing `N` with
the authorized PR number:

```sh
gh pr view N --repo jresearchsoftware/shared-governance --json number,state,isDraft,headRefName,headRefOid,baseRefOid,url
gh pr ready N --repo jresearchsoftware/shared-governance --undo
gh pr view N --repo jresearchsoftware/shared-governance --json number,state,isDraft,headRefName,headRefOid,url
```

The middle command is conditional on observing Ready. For a newly authorized
implementation PR use `gh pr create --draft` (or the connected tool's Draft
option), then read back its identity/state. Review/discussion or a no-PR result
does not need a PR state mutation.

Complete and ordinarily push the candidate, verify the remote exact head,
publish **one** canonical Outcome as below and read the saved comment back,
checking target, author/attribution, complete body and exact result. Only after
successful durable Outcome readback, mark each successfully completed result PR
Ready, then verify its same number/head and `isDraft=false`:

```sh
gh pr ready N --repo jresearchsoftware/shared-governance
gh pr view N --repo jresearchsoftware/shared-governance --json number,state,isDraft,headRefName,headRefOid,url
```

This is executor handoff before independent review. APPROVE, CI, conflicts,
mergeability and merge/closure authority remain separate. Report red checks or
conflicts honestly; they alone do not force a successfully handed-off PR Draft.
For an Issue-level Outcome, evaluate each result PR separately. A completed PR
can become Ready while a blocked sibling stays Draft; there is no blanket toggle.
An entirely blocked/failed/incomplete/uncertain result stays Draft.

On timeout or ambiguous response, first read the same PR/head/native state.
If already in the intended state, retain that observed result without repeating
the mutation; otherwise retry only the authorized idempotent state transition
after reconciliation. A changed/unresolved head or inaccessible state is a gap
to reconcile, never permission to claim Ready. If the Outcome already exists,
keep its URL and the same Step/result; do not republish it or redo implementation
for a state-only failure. Report the observed state or unknown readback, missing
operation/permission and the precise owner action needed. Do not change accounts,
credentials or protection to bypass a missing capability. A state-permission
gap does not establish a code defect. Non-GitHub/no-PR workflows use only their
supported equivalent states, without synthetic GitHub work.

## Result and acceptance binding

Commit substantive source and repository-accessible qualification evidence, use
ordinary non-force push, open/update the PR and read its exact head back. Select
one canonical English Outcome target by the whole actual terminal Step result:

- Exclusively one clearly identified result PR: publish one attributable Outcome
  as a top-level conversation comment on that PR. Issue admission, creating the
  PR during execution or other unrelated PRs on the Task do not change this.
  Ordinary checks, committed evidence and documentation supporting that PR are
  part of its result, not a separate Task-level result.
- No PR, two or more known result PRs, or one PR plus a substantive independent
  Task-level result: publish one Outcome on the canonical Task Issue. For multiple
  result PRs, identify each PR, its exact result SHA/revision and pertinent
  status/limits; their reviews and acceptance remain independently exact-head.

Missing, conflicting or genuinely ambiguous result-to-PR mapping or required
identity stops publication for reconciliation, rather than silently falling back
to the Issue. Known multiple result PRs are an Issue target, not ambiguity.
Use ordinary authorized Git/GitHub channels and read the published comment back;
Relay Writer or typed Task Request is not required here. Link the Task and result
PRs through the PR body and existing canonical navigation so the Outcome is
discoverable. Do not duplicate, split, retrospectively relocate or republish the
same terminal Outcome on both surfaces, or impose an extra status comment or
synchronizer. Recovery/replay retains an existing Outcome; reconcile uncertain
publication before publishing an absent result once at its authorized target.
Report checks, material warnings, gaps and remaining work honestly. Do not use
automatic closing references to bypass closure authority.

Resolve strategy from an explicit owner-authorized Task selection, then applicable
project rules, then shared defaults. This binding adds no alternative strategy
or classifier. A correction implementing already accepted policy normally uses
Direct: a sufficient independent exact-result assessment can accept immediately
when authority/checks allow. A proposal asking the owner to choose new policy or
architecture normally uses Deliberative: publish a substantive non-approving
assessment with findings/warnings, discuss it with the owner and record the
necessary Decision before formal positive acceptance. Positive research assessment
is not yet approval. Do not invent defects or REQUEST_CHANGES to prevent merge.

The owner can accept a report's quality while rejecting its recommendation;
implementation, migration, installation and release need their own authority.
For authorized acceptance of an unchanged result, recheck head/current authority
and applicable checks/identity boundaries, reuse sufficient independent review
evidence and publish the actual acceptance. Changed results need fresh applicable
review. A post-approval hold alone does not enforce Deliberative acceptance.

A separate evaluator's attributed assessment can be published through the owner's
account, within project policy. It does not create authenticated distinct-reviewer
identity, native GitHub APPROVE or branch-protection satisfaction. Preserve any
stronger native requirement and disclose unavailable approval capability. The
implementer stops for independent assessment; self-checks do not accept the result.
Acceptance, recommendation selection, owner-authorized integration, publication,
further execution and closure remain distinct.

For relevant independent review, root AGENTS explicitly adopts the full accepted
materialized Independent Review protocol. It owns affected-behavior completeness,
primary evidence, finding severity/provenance, owner-facing report content and
rereview; Task Handoff owns authority, Outcome and acceptance/continuation.
This producer's adoption changes no other consumer's topic choices. The
ChatGPT-specific publication instruction lives in [custom.md](../chatgpt/custom.md);
this manual Codex binding adds no such restriction to executor Outcomes.
See the current [Step 6 coverage and scenarios](task-45/step-6/coverage.md).
The [Step 7 lifecycle walks](task-45/step-7/scenarios.md) cover manual readiness,
split results and same-Outcome recovery; earlier walks retain historical meaning.
Source-controlled
[ChatGPT Instructions](../chatgpt/instructions.md) are desired state; the owner
manually applies and verifies live settings under the existing client procedure.
For Tasks explicitly including application, compare accepted desired complete text
with supported live evidence; if different, present the whole replacement for
owner application and obtain supported confirmation/readback before closure.
Disclose inaccessible live settings as a gap. Unchanged effective text with no
known application gap needs no manual action; generation-only Tasks add none.
Receipt/source SHA changes alone never require re-pasting settings.

[Task 14 Step 2](task-14/step-2/README.md) is historical evidence of a new admitted
Step correcting the same PR. [Task 26 Step 1 walks](task-26/step-1/scenarios.md)
exercise lifecycle and acceptance strategies;
[Step 2 walks](task-26/step-2/scenarios.md) exercise Outcome routing, replay and
linked review without Relay. Current admissions and verdicts
remain in canonical Issues/PRs, not these examples.
