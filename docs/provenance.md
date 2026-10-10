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
package LICENSE files. The first frozen flow's canonical protocol is
`vibevm/vibespecs/protocols/proportional-controls.md` inside the current package.
[Task 10](https://github.com/jresearchsoftware/shared-governance/issues/10) retains
the complete original procedure bytes (SHA-256
`cfa62afee0aa267aa58bb966faece0225cb717a82fbb93d3d3b4bf7b29704c6c`),
preceded by the accepted wrapper body. Only discovery frontmatter, its obsolete
navigation paragraph and the delivery noun `skill` are removed or adapted.
`scripts/project-protocol.py` reproduces that conversion from accepted
`fd609af8a1ea8ce015fda4652e5a8c444ca821c5`; source qualification compares the
result exactly, including all exceptions and attribution. Package
metadata and a Git export receipt identify source content; neither is a competing
policy or live execution record.

[Task 2](https://github.com/jresearchsoftware/shared-governance/issues/2) Step 1
was independently accepted through
[PR 3](https://github.com/jresearchsoftware/shared-governance/pull/3), reviewed at
`2f375e8c865896676a22171ab91e773f016248a3` and squash-merged as
`7cb702164b3e26c6f86e85b2d5596bbb9cb441ba`. Its
`org.jresearch.governance/proportional-controls` coordinate and proposed
distribution repository are historical evidence only; no package was published.
The admitted Step 2 source candidate uses
`org.jresearch.ai/development-governance` v0.1.0, initially retaining the accepted
`proportional-controls` Skill/procedure bytes and MIT/derived attribution.
That historical multi-Skill adaptation was accepted in PR 4. Task 10 proposes
one ordinary flow protocol, no Skills, and `frozen = true` for the first `0.1.0`
release without migrating its directory. The packaging/self-adoption change
requires independent exact-head acceptance and grants no publication or consumer
adoption authority. [Self-adoption](self-adoption.md) records accepted-origin
active guidance separately from candidate authoring.

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
