# Shared governance

Public authoring source for reusable AI-development governance owned by
`jresearchsoftware`. This repository was bootstrapped under
[Relay Task 83](https://github.com/jresearchsoftware/codex-relay/issues/83),
following the accepted [Task 59 analysis](https://github.com/jresearchsoftware/codex-relay/pull/81).

The current source candidate contains one extensible package:
[`org.jresearch.ai/development-governance` v0.1.0](vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0/README.md).
It is a passive VibeVM flow with one compact boot pointer and distinct native
Skills for guidance loaded when needed. Initially it contains only the accepted
`proportional-controls` Skill and control procedure, with unchanged bytes and
attribution. One package version identifies the entire included Skill set;
adding or changing a Skill requires a new independently accepted package version
and separately reviewed consumer update. No distribution repository, package tag
or registry index is published.

The initial `org.jresearch.governance/proportional-controls` source was accepted
through [PR 1](https://github.com/jresearchsoftware/shared-governance/pull/1)
at `aa1e18085dee2aa59e19c5939e882cd8084eea00`. Its distribution preparation was
accepted through [PR 3](https://github.com/jresearchsoftware/shared-governance/pull/3)
at `7cb702164b3e26c6f86e85b2d5596bbb9cb441ba`. These are historical source
identities, not published dependencies. [Task 2](https://github.com/jresearchsoftware/shared-governance/issues/2)
Step 2 authorizes the current source identity and multi-Skill adaptation before
publication, pending independent exact-head review.

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
- [Distribution preparation](docs/distribution.md) prepares one faithful package
  root and qualifies disposable Git consumers under [Task 2](https://github.com/jresearchsoftware/shared-governance/issues/2).
  Actual public publication remains a separately authorized boundary.

Git and Python 3.11+ are sufficient for the source/native baseline. VibeVM
`1.0.7` is optional authoring tooling, pinned by source commit and release
artifact hashes in [toolchain/vibevm.json](toolchain/vibevm.json).

Content is licensed under [MIT](LICENSE).
