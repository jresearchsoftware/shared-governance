# Shared governance

Public authoring source for reusable AI-development governance owned by
`jresearchsoftware`, bootstrapped under
[Relay Task 83](https://github.com/jresearchsoftware/codex-relay/issues/83).

One passive VibeVM flow is authored at the stable
[Development Governance](packages/development-governance/README.md) path.
Its manifest owns the whole-package version. Ordinary proportional-controls
and package-versioning protocols use compact conditional boot routing, with no
native Codex Skills or executable capabilities. Package-versioning requires
explicit project adoption and preserves existing locally owned policies.

[Version tags](https://github.com/jrs-vibevm/org.jresearch.ai.development-governance/tags)
and [publication runs](https://github.com/jresearchsoftware/shared-governance/actions/workflows/publish.yml)
are the authoritative publication surfaces. The [release policy](docs/releases.md)
defines this producer's per-PR bump and automatic publication after independently
reviewed owner merge, with exact-source retry. Frozen
[0.1.0](vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0/README.md)
retains its original content, including historical publication-status wording;
corrections use later versions. Source acceptance and publication never migrate
Relay, Documentation, Model Landscape or other consumers automatically.

- [Repository instructions](AGENTS.md) and [contributing](CONTRIBUTING.md).
- [Authoring](docs/authoring.md), including semantic completeness and pinned-tool probes.
- [Distribution](docs/distribution.md) and [release policy](docs/releases.md).
- [Provenance](docs/provenance.md) and [active self-adoption](docs/self-adoption.md).

Python 3.11+ and Git suffice for ordinary source/export checks. Optional VibeVM
integration tooling is pinned in [toolchain/vibevm.json](toolchain/vibevm.json).
Content is [MIT](LICENSE) licensed.
