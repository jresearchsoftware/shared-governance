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

The existing ChatGPT owner-facing report before publishing a Change Request or
negative assessment follows adopted Task Handoff's finding-preview rule: each
finding states severity, origin (or explicit undetermined plus the comparison
gap), exact result/comparison and evidence, qualified impact, remediation and
closure evidence. Include a supported Step/commit; distinguish confirmed failure,
analytical risk and missing tests. Missing fields leave the report incomplete;
published findings retain the same classification and fields. This is content
for the existing report, with no added approval, reviewer or waiting step and
no adoption of the optional Independent Review topic. See the focused
[preview scenarios](task-45/step-5/review-scenarios.md). Source-controlled
[ChatGPT Instructions](../chatgpt/instructions.md) are desired state; the owner
manually applies and verifies live settings under the existing client procedure.

[Task 14 Step 2](task-14/step-2/README.md) is historical evidence of a new admitted
Step correcting the same PR. [Task 26 Step 1 walks](task-26/step-1/scenarios.md)
exercise lifecycle and acceptance strategies;
[Step 2 walks](task-26/step-2/scenarios.md) exercise Outcome routing, replay and
linked review without Relay. Current admissions and verdicts
remain in canonical Issues/PRs, not these examples.
