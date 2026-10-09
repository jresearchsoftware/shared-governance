# Development governance

Authoring candidate: `org.jresearch.ai/development-governance` version
`0.1.0`, a passive, simple VibeVM flow. No package repository or tag has been
published. `publish = false` records that boundary in the manifest.

The semantic owner is the public `jresearchsoftware/shared-governance` source.
The package can contain distinct passive native Skills and their references;
one version identifies the entire included set. Adding or changing a Skill
requires a new accepted package version and explicit reviewed consumer update.
Initially only the unchanged accepted
[proportional-controls Skill](vibevm/vibespecs/skills/proportional-controls/SKILL.md)
and its [control procedure](vibevm/vibespecs/skills/proportional-controls/references/protocol.md)
are included. Skill details are read when needed through one compact
[boot pointer](vibevm/vibespecs/boot/development-governance.md), which introduces
no current task state or consumer authority. There are no dependencies, tools,
hooks, MCP declarations or applications.

The Git/native-Skill baseline exports this same skill directory from an exact
source commit; it does not maintain a second policy. See the repository's
authoring documentation for the comparison and extraction provenance.

Content is MIT licensed. Copyright (c) 2026 shared-governance contributors;
derived governance text Copyright (c) 2026 Codex Relay contributors. See LICENSE.
