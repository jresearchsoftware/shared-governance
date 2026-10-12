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

At the start of work, run `python scripts/self-adopt.py` (Python 3.11+; `python3`
where appropriate). This automatically selects the latest eligible accepted and
published Development Governance; read its returned `directory`, exact identity
and warnings. Retain that selection for the effort. On a reported update failure,
use the retained verified guidance and report the warning; never substitute
editable package source. If no verified guidance is available, preserve work and
recover as described in [self-adoption](docs/self-adoption.md).

This producer explicitly adopts these four topics from that accepted directory's
`vibevm/vibespecs/protocols/`, preserving their conditional applicability:

- Read `proportional-controls.md` for proposed security, validation or operator
  controls, including behaviorally free hardening.
- Read `requirement-authority.md` when deciding whether a requirement is binding
  or an earlier implementation constraint can be revised.
- Read `package-versioning.md` for package lifecycle work, together with this
  producer's [release policy](docs/releases.md).
- Read `task-handoff.md` for governed execution, handoff or continuation, together
  with the [manual client binding](docs/manual-task-handoff.md).

Unrelated tasks skip the corresponding protocol. This adoption grants no Task,
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
