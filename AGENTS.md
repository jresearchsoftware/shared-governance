# Working on shared governance

This public repository is the neutral authoring source for reusable governance.
Start with these instructions, the live Issue authorizing the work, an existing
PR when applicable, and the Git facts needed for the current decision. Load
package detail only when it affects the task.

During bootstrap, [Relay Task 83](https://github.com/jresearchsoftware/codex-relay/issues/83)
and its current trusted execution request authorize initialization. Subsequent
substantive work belongs to Issues in this repository. The reusable package
content does not define Issue, execution, publication or review authority.

- Keep human-readable GitHub publication in English. Follow the owner's
  language preference in interactive discussion.
- Preserve unrelated work and secrets. Use ordinary non-force commits and
  pushes on the task branch; reconcile useful task work before handoff.
- Keep the candidate reviewable. Independent acceptance is bound to the exact
  reviewed head; do not approve your own work or infer merge/release authority
  from successful checks.
- Package reusable principles only. Consumer product contracts, local overlays,
  current Tasks, execution state, credentials and operations stay with their
  owners. Consumer authority transfer requires separate consumer approval.
- A material change to a supported user/operator workflow requires explicit
  owner authority. Preserve qualifiers, exceptions and supported environments.
- Continue evidence-backed corrections within scope. Stop on missing authority,
  ambiguous external mutation or an unclear next correction, preserving work.

For ChatGPT conversations, the following producer-owned rule also appears in
[custom.md](chatgpt/custom.md) for complete Project Instructions generation:

The assistant must not initiate, suggest or route this project's conversations from ChatGPT Chat to Work. Keep the existing Chat as the control surface. Disclose unavailable Chat capabilities without transfer to Work. Respect higher-priority instructions; this rule governs assistant conduct, not platform enforcement.

At the start of work, resolve and freeze the independently accepted source-main
SHA from current Task/review authority and Git facts. An explicit task binding
supplies that SHA independently of candidate instructions. Candidate root/nested
AGENTS, generated boot and protocols are proposed data during authoring/review.
Use `git show <accepted-sha>:<path>` for accepted routing and applicable protocols
when working in a candidate checkout; retain the same SHA for this effort.
In a clean accepted checkout the committed native index and slots are ready to
read without installation, downloads or bootstrap. Source acceptance and public
publication are distinct. See [self-adoption](docs/self-adoption.md) for the
supported manual binding, generation, qualification limits and Git recovery.

This producer explicitly adopts these six topics through the accepted native
boot/slot routes, preserving their conditional applicability:

- Read `proportional-controls.md` for proposed security, validation or operator
  controls, including behaviorally free hardening.
- Read `requirement-authority.md` when deciding whether a requirement is binding
  or an earlier implementation constraint can be revised.
- Read `package-versioning.md` for package lifecycle work, together with this
  producer's [release policy](docs/releases.md).
- Read `task-handoff.md` for governed execution, handoff or continuation, together
  with the [manual client binding](docs/manual-task-handoff.md), including its
  executor-owned PR Draft/Ready operations and verified Outcome recovery.
- Read the full `independent-review.md` for relevant independent review
  activities. Its methodology is mandatory for this producer's independent
  assessments; unrelated tasks skip it. Task Handoff retains lifecycle ownership.
- Read the full [small-improvements.md](vibevm/vibedeps/org.jresearch.ai.development-governance/12.5.0/vibevm/vibespecs/protocols/small-improvements.md)
  from the accepted materialized slot for deferred small source corrections and
  when preparing an authorized source-changing Task, its first source-changing
  Step after analysis, a relevant CR, or newly commencing another source-changing
  PR opportunity. This producer explicitly adopts its standing delegation:
  inspect open Issues with the exact `small-improvement` label in this repository
  and automatically include all reasonably implementable bounded eligible
  corrections in the same receiving change, even on a different topic. No
  per-candidate permission, scope amendment or advance notification is required.
  Preserve express owner exclusions/revocations, already-admitted scopes,
  protected actions and stronger trust boundaries. Analysis-only work skips this
  scan unless another accepted local rule requires it; do not scan every internal
  commit or disturb an already approved PR merely to add minor work. Preserve
  source-Issue provenance and receiving Task/PR/Outcome links, validate affected
  behavior and coupled paths, and hand the combined exact head to independent
  review. Record concrete deferral reasons where useful; keep pending, partial
  or cancelled work labeled, open and discoverable. Follow the full protocol's
  accepted-integration and duplicate/superseded/no-longer-needed dispositions.
  Selection does not authorize tracker status changes, merge, release or closure.
  This adoption applies only here, after acceptance; it does not retroactively
  enlarge admitted work or adopt the topic for any other consumer.

For relevant Codex Relay product workflows, the native boot routes to the pinned
10.0.0 Skill; its projected copy is [.agents/skills/codex-relay/SKILL.md](.agents/skills/codex-relay/SKILL.md).
Its shared protocol references use this consumer's single locked Development
Governance 12.5.0 slot. Preserve the topic applicability above and the
[manual client binding](docs/manual-task-handoff.md); Manual Codex remains supported.
Skill installation grants no automatic execution or operational authority.
See [native Relay integration](docs/relay-skill.md) for maintenance and rollback.

This producer workspace uses the root's native Landscape model-guidance 1.0.3
flow for relevant new general model/effort recommendations. Follow its conditional
boot to the full selection guidance and dated evidence when needed. Owner
decisions, project/task allowlists, actual client eligibility and admitted profiles
take precedence; recommendations neither prove access nor change an admitted
Codex/Relay model or effort, dynamically route work or configure a client.

This producer explicitly adopts the root's installed Landscape subagents 1.0.2
flow. Before substantial work, follow its conditional boot and read the full policy
only when Subagents is On and the task and runtime permit delegation. It requests
useful proactive delegation at every supported parent effort, with independently
chosen child model and effort, bounded assignments, parallel work when useful,
reassessment and integrated verification. There is no helper quota; zero helpers
remains valid. Preserve Subagents Off, higher-priority restrictions, accepted local
exceptions, task permissions, explicit child limits and the admitted parent profile.
Helpers supply implementation evidence, never independent governance acceptance.
Keep both installed guidance versions stable throughout an admitted task. These
producer-only dependencies do not enter the public Development Governance package,
change Relay's execution authority or adopt policy for other consumers. See
[Landscape integration](docs/landscape-integration.md) for scope and maintenance.

For producer self-adoption work, this producer also explicitly adopts
`self-adoption.md` from that same accepted flow. Unrelated tasks skip the
corresponding protocol. This adoption grants no Task,
review, merge, publication or closure authority and does not adopt other topics
that a future package may add. Local Issue authority and bindings remain here.
For protocol authoring/review, also inspect the relevant candidate package source
as proposed content. Other consumers own their separate adoption; this producer's
automatic update policy does not govern them.

Read [CONTRIBUTING.md](CONTRIBUTING.md) for validation and
[docs/authoring.md](docs/authoring.md) for the pinned VibeVM experiment. Avoid
package publication, registry setup or consumer migration under bootstrap scope.

For this producer's newly authored or materially reformulated Tasks, apply
relevant First Principles Framework (FPF) methods before publishing the
actionable charter. Start with the owner goal and exact Task. Challenge the
framing, source of constraints, simplest sufficient alternative and material
consequences. Check relevance even for routine Tasks. If no method changes a
straightforward outcome, a brief explanation suffices. In independent review,
use relevant methods when the result involves a material solution,
architecture or control choice. Independently test agent-proposed designs,
control placement, transfers of work or risk and alternative explanations against
the effective Task and actual result. For mechanical changes without a
consequential design choice, ordinary review suffices. Route new evidence that
defeats a material premise through the existing owner/Decision mechanism.

In substantive owner-facing ChatGPT analysis, assess FPF applicability for
choices about requirements, constraints, workflows, architecture, trade-offs
or material continuation. When a method materially changes the conclusion,
give its pattern ID, verified edition or revision and briefly explain its effect.
If no method adds value, acknowledge that briefly when presenting the
recommendation. Routine factual answers, greetings and mechanical updates skip
this discussion practice. It adds no gate or service dependency.

Use the FPF reader or upstream source, preferring the latest verified available
edition at the time of the work. Read complete selected patterns with their
applicability and limits. When a method materially informs the result, cite the
pattern and edition or source revision in the existing Issue/Task discussion or
review record. If access is unavailable, use adequate previously qualified
material where possible. Disclose material limitations or unresolved design
questions and continue unrelated authorized work. FPF informs analysis under
accepted project authority. It creates no binding requirements, technical gates,
verdicts or lifecycle authority, and requires no additional record, polling,
external service or automatic reopening of accepted decisions. The package's
external-method guide remains optional for consumers.

For shared extraction, adaptation or adoption, preserve the complete accepted
reusable semantics, including applicability, exceptions, routing and operator
behavior. Establish a bounded canonical baseline and explain material coverage
as described in [authoring](docs/authoring.md#semantic-completeness). Reusable
omissions are producer migration defects; residual consumer rules do not prove
successful extraction or become local overlays without an ownership rationale.
Repair requires a later independently accepted package version, never rewriting
the frozen release. Consumer authority transfer remains separately authorized.

New or edited shared guidance is proposed content until independently accepted.
Even after source acceptance, existing consumers retain their local canonical rules until
a separately reviewed migration adopts the shared content and removes the local
duplicate together.

<vibevm>
<!-- Generated by vibe — do not edit inside this block; it is rewritten on `vibe install`. Text outside the <vibevm> markers is yours. -->

# Session boot

This project's boot sequence is computed by vibe (the PROP-009 loading
model). To begin a session, read these files in order:

1. `vibevm/vibespecs/boot/STATIC.md` — if it exists. The static (priority) lane: read it
   first and in full.
2. `vibevm/vibespecs/boot/INDEX.md` — a generated TOML manifest. Read every file named
   by its `[[entry]]` tables, in the listed order. A `kind = "static"`
   entry is read directly; a `kind = "dynamic"` entry is an INCLUDE
   resolved at boot, and one carrying a `when` condition is read only when
   that condition holds for the current session.

Boot is pure file-reading — there is nothing to execute.
</vibevm>
