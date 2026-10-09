# Bootstrap provenance

This source was prepared under
[Relay Task 83](https://github.com/jresearchsoftware/codex-relay/issues/83)
and its [Step 1 execution request](https://github.com/jresearchsoftware/codex-relay/issues/83#issuecomment-6037643777).
The bootstrap is a public, neutral source, MIT licensed, with one intentionally
small extraction. It transfers no consumer operational authority.

The accepted architecture comes from
[Task 59](https://github.com/jresearchsoftware/codex-relay/issues/59) and
[PR 81](https://github.com/jresearchsoftware/codex-relay/pull/81), squash commit
`9aad5bbc746c9ba0ff25534efca33eae3ef1e472`:

- [Design analysis at that commit](https://github.com/jresearchsoftware/codex-relay/blob/9aad5bbc746c9ba0ff25534efca33eae3ef1e472/docs/vibevm-governance-design.md)
  identifies proportional controls as the strongest first neutral package,
  separates semantic ownership from distribution, and requires the credible
  Git/native-Skill comparison.
- [Execution policy at that commit](https://github.com/jresearchsoftware/codex-relay/blob/9aad5bbc746c9ba0ff25534efca33eae3ef1e472/docs/execution-policy.md#proportional-controls-and-operator-usability)
  supplies the reusable control procedure. Its qualifiers, examples, exceptions,
  risk-acceptance option, cost boundary, human usability and supported-environment
  requirements are retained. Only the last Relay-specific
  `OWNER_DECISION_REQUIRED` binding is expressed as an owning-project authority
  requirement. The Relay implementation and local rules are unchanged.

Copyright notices for derived Relay text are retained in both repository and
package LICENSE files. There is one canonical procedure, inside the skill's
`references/protocol.md`. Both export paths carry those same bytes. Package
metadata and a Git export receipt identify source content; neither is a competing
policy or live execution record.

VibeVM is pinned to `v1.0.7`, source
`b6659978453f50e6d1d4d99626d70b980a2c5847`, and
[release 403150895](https://github.com/vibevm/vibevm/releases/tag/v1.0.7).
The release API reports `immutable=false`; hashes in the toolchain pin protect
this experiment from silently changed download bytes.

Relevant pinned upstream sources:

- [Manifest/workspace schema](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-core/src/manifest/document.rs)
  and [package wire schema](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-core/src/manifest/package/wire.rs).
- [Boot snippet schema](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-core/src/manifest/package.rs)
  and [boot redirect behavior](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-workspace/src/boot_artifacts/redirect.rs).
- [Skill byte snapshot](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-agent-projection/src/pkgskill/snapshot.rs)
  and [agent scope paths](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-agent-projection/src/agents/ambient_paths.rs).
- [Alpha posture](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/docs-legacy/ALPHA-NOTES.md).

Future publication repositories/tags, consumer adoption, registry credentials,
private governance and broader extraction require their own later authority.
The authoring source remains the semantic owner when distribution is introduced.
