# Repository self-adoption

[Task 10](https://github.com/jresearchsoftware/shared-governance/issues/10) proposes
an explicit human-owned AGENTS route to the active
[ordinary protocol](../.agents/protocols/proportional-controls.md) for relevant
security, validation and operator-control decisions, including free hardening.
Unrelated tasks skip the protocol. This replaces the native Skill adopted by
[Task 6 / PR 7](https://github.com/jresearchsoftware/shared-governance/pull/7),
merged as `d116cdaa8e8bbb3c9c991dd8b053927a9e2b6cd4`.
The proposal becomes accepted repository guidance only with independent
exact-head review and owner-authorized merge; authoring metadata alone does not
activate it. An existing chat may still have its startup Skill catalog in memory;
fresh sessions use the new AGENTS route after adoption.

The [source receipt](../.agents/proportional-controls-source.json) pins the original
accepted Skill/wrapper and procedure at
`fd609af8a1ea8ce015fda4652e5a8c444ca821c5`, the accepted source after PR 5.
`scripts/project-protocol.py` makes a deterministic delivery conversion: remove
Skill discovery frontmatter and the obsolete Read-reference navigation, retain all
substantive wrapper instructions, replace only `The skill` with `This protocol`,
and append the unchanged complete procedure. The output SHA-256 is
`b51934ec43ffd65e8728eca399715e887f26dc1badee588c760962c84374271e`.
The receipt retains original file hashes, canonical source path, repository,
full accepted revision, transformation name and generated output/license hashes.
The root MIT LICENSE covers the projection and retains derived attribution.

There is one editable canonical protocol in the flow package. The root active
file is a generated accepted-origin snapshot, not a separately authored policy.
It is deliberately independent of candidate authoring bytes and pins no
unreviewed candidate commit. Both source and active snapshot are byte-identical
to the reproducible conversion in this first-release proposal. The qualifier
rebuilds active expectations from accepted Git blobs, then checks the receipt,
active bytes, license and human AGENTS route. It separately checks first-release
semantic equivalence and exact-commit package export. No `.agents/skills`
projection or VibeVM Skill ownership receipt remains.

## Reproduce and review

From a checkout with the accepted origin Git objects available:

```sh
destination="$(mktemp -d)/protocol"
python3 scripts/project-protocol.py --destination "$destination"
```

Copy its `proportional-controls.md` to `.agents/protocols/proportional-controls.md`
and `SOURCE.json` to `.agents/proportional-controls-source.json`; compare the
exported LICENSE with the root LICENSE. Keep the explicit AGENTS route in the
same independently reviewed adoption change. No VibeVM installation, runtime
resolution, native discovery, dependency or global configuration is needed for
ordinary manual Codex work here. The repository itself is an authoring workspace;
it is not materialized as its own dependency.

After staging and committing the intended candidate:

```sh
git diff --check
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
```

Future policy edits belong to later package versions. They do not refresh this
active file or receipt. A separately authorized and independently reviewed
self-adoption update must select the newly accepted source, reproduce the ordinary
protocol snapshot/provenance, and update the human route and generated files
together. Retain active guidance during candidate authoring/review; ordinary
reviewed Git revert is rollback. This first-release conversion helper is bounded
to the accepted historical input, not a general future-version adoption framework.

## Qualification boundary

Task 6's native discovery and read-only model result remain historical evidence
for its old delivery. Task 10 requires fresh source/export, integrity regressions,
actual hash-pinned VibeVM local publisher/consumer materialization, and fresh Codex
traversal of the generated installed boot chain. See
[Step 1 evidence](task-10/step-1/README.md) for results and model limitations.
Local checks or model outputs are not independent acceptance. No other consumer
or remote publication is adopted here.
