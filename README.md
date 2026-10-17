# Shared governance

Public authoring source for reusable AI-development governance owned by
`jresearchsoftware`, bootstrapped under
[Relay Task 83](https://github.com/jresearchsoftware/codex-relay/issues/83).

One passive VibeVM flow is authored at the stable
[Development Governance](packages/development-governance/README.md) path.
Its manifest owns the whole-package version. Ordinary proportional-controls,
requirement-authority, package-versioning, task-handoff and producer self-adoption
use compact conditional
boot routing, with no native Codex Skills or executable capabilities.
Workflow-aware GitHub repository governance is an additional explicitly adopted
topic with conditional setup/protection guidance; it does not apply settings.
Package-versioning and task-handoff require explicit project adoption and preserve
existing locally owned policies. [Manual task handoff](docs/manual-task-handoff.md)
and [native self-adoption](docs/self-adoption.md)
illustrates this repository's Issue-owned execution path and local client binding.

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
- [Onboard a new or existing project](docs/onboarding.md): human-initiated discovery,
  topic choices, authorized setup and evidence-backed readiness.
- [Authoring](docs/authoring.md), including semantic completeness and pinned-tool probes.
- [Distribution](docs/distribution.md) and [release policy](docs/releases.md).
- [Provenance](docs/provenance.md) and [active self-adoption](docs/self-adoption.md).

Python 3.11+ and Git suffice for ordinary source/export checks. Optional VibeVM
integration tooling is pinned in [toolchain/vibevm.json](toolchain/vibevm.json).
Content is [MIT](LICENSE) licensed.

See the [optional Relay workflow proposal](docs/relay-workflows.md) for its
preparation provenance and separate acceptance/activation boundary.
