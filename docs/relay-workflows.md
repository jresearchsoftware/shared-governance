# Optional Codex Relay integration

This is the target-local integration prepared under
[Task #57](https://github.com/jresearchsoftware/shared-governance/issues/57) in
existing [PR #48](https://github.com/jresearchsoftware/shared-governance/pull/48).
Task #57 is the current local authority. Closed Issue #47 and Relay Task #141
are historical proposal records and do not admit or govern this work.

## Published Skill pin

The integration includes the complete standalone Skill at
[.agents/skills/codex-relay](../.agents/skills/codex-relay/SKILL.md), copied
from public release [v2.0.1](https://github.com/jrs-vibevm/org.jresearch.ai.codex-relay/tree/v2.0.1)
at peeled commit 935c6b15cb34fbed030833b5d61c0c0c11c502e6. The Task #57 Owner
Decision records the public receipt
`org.jresearch.ai/codex-relay@2.0.1`, source
1d69995364f371321369110253833507970075fc, digest
4afa1088115fd2d1b4633eb5f75e62bc53fb2b52ac827a47c09ef84509dde168, and
62 declared package files. The release's [installation.md](https://github.com/jrs-vibevm/org.jresearch.ai.codex-relay/blob/v2.0.1/skill/references/installation.md)
documents this standalone form; the copied folder retains its
`PROVENANCE.json` and its listed file hashes match the pinned source.

The native Skill package and its documented VibeVM 1.0.7 consumer template
require an explicit Development Governance `=4.0.0` root dependency because that
VibeVM version ignores transitive Git source declarations. This repository's
accepted `vibe.toml` already has an explicit root dependency on the same
coordinate at `=5.0.0`. The native route would introduce competing exact Shared
Governance versions and boot semantics; resolving that needs a separate
compatibility decision. This Step preserves the 5.0.0 root and boot and uses the
documented standalone Skill form. Its bundled 4.0.0 references remain part of
Relay product guidance; for overlapping local governance, this repository's
accepted 5.0.0 route and [Manual Codex binding](manual-task-handoff.md) remain
canonical. The VibeVM manifest, lock, native slots and generated boot are
unchanged.

## Workflow projection

The two workflows and schema-2 manifest are generated with the public projector
from accepted Relay main
`9bd60b27e23b98a0bcb58eac4f18af84098192ce`. The compatible parallel workflow
contract is `relay-workflows-v4`. The projection binds only this repository at
`refs/heads/main`:

- jresearchsoftware/shared-governance/.github/workflows/codex-relay-routing.yml
- jresearchsoftware/shared-governance/.github/workflows/manual-writer-publication-recovery.yml

The workflow-facing target tuple is the owner-selected six-member General
Runner pool: group `codex-relay-general-runner`, selector label
`relay-pool-e6987beab0b057123d402738`, runner name
`codex-relay-general-runner-pool` with system user
`codex-relay-general-runner`. The Relay projector retains its 32 stable logical
execution slots while the configured physical pool capacity is six. The
Production Runner group remains separate. The workflow files and manifest bind
the rendered bytes; no private consumer configuration or credential is stored
here.

## Activation and authority

This PR prepares the reviewed projection; it does not merge or activate it.
No GitHub runner-group settings were read or changed in this implementation
Step. Before these workflows can dispatch from main, the owner-controlled
General Runner group must be read back and restricted to this repository and
the two exact workflow refs above, with the expected six-runner identity and
selector. That readback and any minimum group adjustment belong to the
post-review owner continuation. Until then, this PR does not establish live
runner eligibility or dispatch.

Manual Codex remains supported through the repository's existing Task/Step
authority and local handoff binding. The Skill and workflows do not accept
results, approve a PR, merge it, change other consumers or close Task #57.
Independent exact-head review remains required.
