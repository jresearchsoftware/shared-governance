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

This producer explicitly adopts these five topics through the accepted native
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

For relevant Codex Relay product workflows, the native boot routes to the pinned
3.0.0 Skill; its projected copy is [.agents/skills/codex-relay/SKILL.md](.agents/skills/codex-relay/SKILL.md).
Its shared protocol references use this consumer's single locked Development
Governance 5.2.3 slot. Preserve the topic applicability above and the
[manual client binding](docs/manual-task-handoff.md); Manual Codex remains supported.
Skill installation grants no automatic execution or operational authority.
See [native Relay integration](docs/relay-skill.md) for maintenance and rollback.

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
