# Optional Relay workflow proposal

This repository's routing and publication-recovery workflows are an opt-in
proposal prepared under [Codex Relay Task #141](https://github.com/jresearchsoftware/codex-relay/issues/141).
They were projected with the public interface from accepted Relay
`b52670f7f8a1a253f30243fac4c4384e282a79d8`, using a validated, non-installed
desired configuration derived from the owner's verified SERIAL configuration.
The private configuration stays outside this repository.

The proposed installation has one Writer/Reviewer target list covering
`codex-relay`, `shared-governance`, `codex-model-landscape` and
`docs-evolution-review` in `jresearchsoftware`, sharing six managed General
Runners. This repository's projection binds only `jresearchsoftware/shared-governance`
at `main`. It uses `relay-workflows-v4`, the shared General Runner group/pool
selector and a configured runner/user identity guard. The schema-2
[manifest](../.github/relay-workflows.json) records the exact workflow digests.
No owner-lifecycle workflow is projected here; that belongs to the protected
`codex-relay` installation anchor.

Shared Governance Issue [#47](https://github.com/jresearchsoftware/shared-governance/issues/47)
supplies the local proposal authority. The existing package, native boot,
candidate validation and release/publisher workflows retain their own policy.
This proposal does not alter the governance package or publish a release.

The repository owner independently decides acceptance, merge and activation.
Publication of this PR does not enable workflows on the default branch, admit
work, upgrade the installed runtime, or change runner-group access, GitHub App
permissions, credentials, repository settings or protected services. A configured
Writer/Reviewer target may remain inactive for automatic work. Activation needs
compatible accepted source, qualified installed Writer/Reviewer/runtime support,
trusted workflow-ref restrictions and separate owner authorization.

Review the exact PR head and generated files before any adoption. The parent
Task remains open for separately authorized installation work; source/static
checks establish neither live concurrency nor consumer adoption.
