# Codex Relay Skill integration

This is the standalone Relay Skill proposal separated under
[Task #57](https://github.com/jresearchsoftware/shared-governance/issues/57)
from the workflow projection in [PR #48](https://github.com/jresearchsoftware/shared-governance/pull/48).
The Skill PR remains Draft as a deferred fallback while the owner chooses the
supported integration form. This proposal does not activate or merge the Skill.

## Published Skill

The 34-file Skill subtree at
[.agents/skills/codex-relay](../.agents/skills/codex-relay/SKILL.md) is copied
byte-for-byte from the public [Relay v2.0.1 release](https://github.com/jrs-vibevm/org.jresearch.ai.codex-relay/tree/v2.0.1),
peeled commit 935c6b15cb34fbed030833b5d61c0c0c11c502e6. The [published installation guide](https://github.com/jrs-vibevm/org.jresearch.ai.codex-relay/blob/v2.0.1/skill/references/installation.md) documents this form. Its public package
receipt is org.jresearch.ai/codex-relay@2.0.1, source
1d69995364f371321369110253833507970075fc, with digest
4afa1088115fd2d1b4633eb5f75e62bc53fb2b52ac827a47c09ef84509dde168.
The checked-in PROVENANCE.json retains the release version and source hashes;
the main Skill file SHA-256 is
ddc3d678f4f4b770da29e64c48b50aa7629650657d3d9930ba94a24059a314ff.

The root AGENTS.md routes relevant Relay product work to this Skill. The
Skill's bundled Shared Governance 4.0.0 material remains product guidance;
the producer's accepted 5.0.0 native route and
[manual task binding](manual-task-handoff.md) remain canonical for this
repository's Task/Step authority, Outcomes, PR state, review and merge. Manual
Codex remains supported. The route does not activate Relay workflows or confer
review, merge, runner-group or closure authority.

## VibeVM 1.0.7 investigation

The pinned Linux x86_64 musl binary from the [VibeVM v1.0.7 release](https://github.com/vibevm/vibevm/releases/tag/v1.0.7) reported vibe 1.0.7; its SHA-256
was 20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240.
The investigation ran in disposable WSL ext4 fixtures with isolated Vibe
settings. It did not change this repository's manifest, lock, native slots or
generated boot.

The published Relay package declares
org.jresearch.ai/development-governance =4.0.0. Its documented VibeVM
consumer template uses explicit Git roots for Relay 2.0.1 and Development
Governance 4.0.0 because VibeVM 1.0.7 does not resolve transitive Git source
tables on its own.

A positive control materialized that documented graph. The command
vibe --json install --no-default-registry --assume-yes --path <fixture>
completed with complete=true and ok=true, resolving Relay 2.0.1 and
Development Governance 4.0.0. The resulting lock entries had content hashes
00bb4c086a39996fe3988bb76009eff0e0ead542919110ba8d3f7a34614ab9dc and
d27a004b5f2dcc8ae0f7fd33289d97be1eab84ddbdf54d7e880cc6def7ad3746.
vibe --json skill list found the Relay Skill; dry-run reported
would-create, and installation reported created. Its installed SKILL.md
matched the published/provenance hash above. Generated boot routes included
both package boot entries. This establishes that the native path works with
a consumer rooted at Shared Governance 4.0.0.

The target compatibility probe used an archive of accepted Shared Governance
d0b3d67ef94a5537ebd4a2bbf4a38e3a6629c0c9 (root dependency 5.0.0) and the
exact Relay 2.0.1 package source. Running
vibe --json install --assume-yes --offline --path <fixture> returned the
resolver's unsatisfiable result: Relay requires Shared Governance 4.0.0 while
the direct producer root requires 5.0.0. Explicit Git roots therefore solve
source discovery, but they do not make the two exact versions compatible.
The failure was established with local fixture packages and offline resolution,
without contacting an ambient registry. An earlier online fixture attempt
stopped at registry authentication before reaching dependency resolution and is
excluded from this finding.

## Finding and owner choice

The documented native Skill path is technically viable for a consumer that
chooses the 4.0.0 governance root. It cannot coexist in the current accepted
5.0.0 root graph. Do not downgrade this repository, mix the competing boot
routes, or edit generated Vibe state. The owner must select a later compatible
native route after any upstream VibeVM/Relay change is separately proposed and
accepted, or select the preserved standalone Skill. This PR leaves that choice
open and remains Draft.