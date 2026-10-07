# Shared governance

Public authoring source for reusable AI-development governance owned by
`jresearchsoftware`. This repository is being bootstrapped under
[Relay Task 83](https://github.com/jresearchsoftware/codex-relay/issues/83),
following the accepted [Task 59 analysis](https://github.com/jresearchsoftware/codex-relay/pull/81).

The first experiment contains one authoring candidate:
[`org.jresearch.governance/proportional-controls` v0.1.0](vibevm/vibepacks/org.jresearch.governance/proportional-controls/v0.1.0/README.md).
It is a passive VibeVM flow with a small boot pointer, one native skill and one
control procedure. No distribution repository, package tag or registry index is
published. The candidate requires independent review before acceptance.

Existing consumers retain their local canonical rules until a separately
authorized consumer migration is independently accepted. Source acceptance does
not migrate Relay, Documentation or Model Landscape. Future substantive work
belongs to Issues in this repository; #83 owns only this bootstrap.

- [Repository working instructions](AGENTS.md) define authoring boundaries.
- [Contributing](CONTRIBUTING.md) describes ordinary changes and source checks.
- [Authoring and comparison](docs/authoring.md) reproduces the VibeVM and
  Git/native-Skill experiments from the same source bytes.
- [Provenance](docs/provenance.md) identifies accepted Relay sources and the
  exact VibeVM baseline.

Git and Python 3.11+ are sufficient for the source/native baseline. VibeVM
`1.0.7` is optional authoring tooling, pinned by source commit and release
artifact hashes in [toolchain/vibevm.json](toolchain/vibevm.json).

Content is licensed under [MIT](LICENSE).
