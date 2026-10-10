# Development governance

Authoring candidate: `org.jresearch.ai/development-governance` version
`0.1.0`, a passive, simple VibeVM flow. No package repository or tag has been
published. `publish = false` records that boundary in the manifest.

The semantic owner is the public `jresearchsoftware/shared-governance` source.
The first release is frozen at `0.1.0` in this authoring path. One version
identifies the entire flow; future changes require a new accepted package version
and explicit reviewed consumer update. The
[proportional-controls protocol](vibevm/vibespecs/protocols/proportional-controls.md)
retains the accepted wrapper instructions and the complete unchanged control
procedure. Relevant security, validation and operator-control decisions read it
through one conditional
[boot pointer](vibevm/vibespecs/boot/development-governance.md), which introduces
no current task state or consumer authority. There are no dependencies, tools,
hooks, MCP declarations or applications.

There are no native Skill declarations or projections. Exact-commit package-root
export carries the same ordinary protocol and provenance; it does not maintain
a second editable policy. `frozen = true` records release intent, not proof of
remote publication or an upstream enforcement guarantee. See the repository's
authoring documentation for the historical comparison and extraction provenance.

Content is MIT licensed. Copyright (c) 2026 shared-governance contributors;
derived governance text Copyright (c) 2026 Codex Relay contributors. See LICENSE.
