# Authoring and the bounded experiment

The root `vibe.toml` remains a virtual authoring workspace with one member,
`org.jresearch.ai/development-governance` v0.1.0, in its existing versioned directory.
The member is a passive `kind="flow"`, `format="simple"`, `epoch=1` package with
`publish=false`, `frozen=true`, no dependencies and no executable capabilities.
The frozen first-release proposal is authorized by
[Task 10](https://github.com/jresearchsoftware/shared-governance/issues/10).
It is not remote publication or independent acceptance. Package-versioning and
source-layout migration are deferred to Task 9 / later versions.

One compact `vibevm/vibespecs/boot/development-governance.md` conditionally points
to the one complete `vibevm/vibespecs/protocols/proportional-controls.md`. Relevant
security, validation and operator-control decisions read the protocol, including
behaviorally free hardening; unrelated tasks skip it. No native Skill declaration,
discovery wrapper, projection or ownership receipt is shipped. The protocol
preserves the accepted wrapper's substantive instructions plus the exact complete
procedure and attribution. [Provenance](provenance.md) explains the conversion.

The authoring-local boot pointer remains outside the exported package.
Qualification scripts are authoring utilities outside that passive payload.
The root [self-adoption](self-adoption.md) has its own accepted-origin active
snapshot and explicit human AGENTS route. Candidate authoring edits cannot
silently refresh it. Normal sessions read committed files without runtime
remote resolution or VibeVM installation.

## Semantic completeness

[Task 15](https://github.com/jresearchsoftware/shared-governance/issues/15)
establishes the accepted invariant for future governance extraction, package
adaptation and consumer adoption: preserve the complete accepted reusable
semantics when moving policy ownership. Working behavior supplied by leftover
consumer instructions does not prove successful extraction.

Before moving ownership, read all relevant current canonical policy slices,
their project integrations and outcome/correction evidence. Where earlier splits
or adaptations matter, consult accepted source history and original instructions.
Bound this baseline to the domain's decisions and behaviors; one current
paragraph or like-named file is not necessarily its complete contract.

Explain source-to-shared coverage of each material obligation, trigger, qualifier,
exception, cost/authority boundary, operator flow and agent-routing condition in
the existing Task/PR/review evidence. Distinguish exact preservation,
meaning-preserving reformulation, explicitly accepted semantic change,
omission/weakening, and genuinely consumer-specific binding. Map obligations,
not strings; byte equality alone cannot establish completeness of the baseline.

An omitted or weakened reusable requirement is a producer migration defect.
Repair canonical shared source and independently accept a new package version
before relying on it for that behavior; do not rewrite or republish frozen
`development-governance@0.1.0`. Product-owned contracts and deliberate local
overlays remain local only with an explicit, defensible ownership rationale.
Record material omissions and owner dispositions rather than silently relying
on the old consumer to supply missing shared semantics.

Exercise the shared guidance in at least one other plausible consumer or
scenario without the old project's residual rules, and assess the original
consumer after replacing its reusable duplicates. Prove loading and application
where possible. Separate file/text evidence, CLI behavior and actual model
behavior; identify unavailable evidence instead of claiming it passed. A
scenario supports the coverage argument, not an always-on global test gate.

Under each consumer's separately admitted migration, adopt pinned reviewed
content and remove the genuinely duplicated canonical local guidance in the
same reviewed change. Preserve documented product bindings and verified local
overlays, checking for missing, weakened or doubly authoritative rules. Use
normal independent exact-head review and ordinary Git rollback. Source
acceptance alone transfers no consumer authority.

Scale this argument to the material change. Trivial editorial edits need no
exhaustive manual mapping; this procedure adds no standing ledger, rigid global
checklist, service or extra owner step. Assess any proposed new gate using
[proportional controls](../.agents/protocols/proportional-controls.md).
Task 15's first demonstration compares the frozen `proportional-controls` flow
with its [Relay provenance](provenance.md) in Task/PR evidence. Unresolved
producer findings and consumer-owned verification belong in the handoff to
[Relay Task 97](https://github.com/jresearchsoftware/codex-relay/issues/97);
the separate [routing investigation, Task 99](https://github.com/jresearchsoftware/codex-relay/issues/99),
does not accept or repair semantic migration gaps.

## Git baseline and exact-commit export

Git and Python 3.11+ suffice. Stage intended additions; commit before testing its
exact-commit export. Consumers later select an independently accepted full SHA;
choosing a candidate SHA does not infer acceptance.

```sh
git diff --check
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
source_sha="$(git rev-parse HEAD)"
destination="$(mktemp -d)/package"
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --destination "$destination"
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --verify "$destination"
```

The export reads ordinary Git blobs only and carries the exact five passive
package files plus generated `DISTRIBUTION.json`: manifest, README, MIT LICENSE,
boot and protocol. It binds full canonical source SHA, path and file hashes;
verification reconstructs those bytes from canonical Git. It rejects occupied
output directories, capabilities/dependencies/Skills, changed identity/frozen
metadata, undeclared/non-ordinary payloads, escaping/missing links and counterfeit
receipts. It writes no source, publication or real consumer state.

`vendor-skill.py` remains solely for accepted historical native-Skill exports and
the deterministic origin check; current flow commits have no Skill to export.
Historical source acceptance (PRs 1, 3, 4 and 5) and their probes remain evidence
for their respective original payloads, not current remote release proof.

## Pinned VibeVM probe

Run these optional authoring/materialization probes on Linux x86_64. Python
3.11+, Git and curl suffice to prepare them. Download into a disposable directory,
verify the hash and invoke the absolute binary. No global install, registry index,
user Skill, account credentials or package publication is needed.

```sh
tool_tmp="$(mktemp -d)"
curl --fail --location --output "$tool_tmp/vibe" \
  https://github.com/vibevm/vibevm/releases/download/v1.0.7/vibe-bootstrap-x86_64-unknown-linux-musl
printf '%s  %s\n' \
  20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240 \
  "$tool_tmp/vibe" | sha256sum --check
chmod u+x "$tool_tmp/vibe"
python3 scripts/qualify-vibevm.py --vibe "$tool_tmp/vibe" --materialize
python3 scripts/qualify-distribution.py --vibe "$tool_tmp/vibe" --source-ref "$(git rev-parse HEAD)"
```

The authoring probe copies tracked candidate bytes to a native disposable
filesystem and relocates VibeVM settings/cache using `VIBE_SETTINGS` and
`VIBEVM_USER_CONFIG`. It validates/checks workspace/member, verifies no native
Skills, and installs exact `=0.1.0` from an explicit offline source-tree registry.
It compares complete slot bytes/file set and human AGENTS outside the one managed
block. The distribution probe separately exercises real local publisher/consumer
Git transport, cold install, retained-slot offline behavior, integrity drift,
synthetic version-only update and complete materialized Git rollback.
All check JSON is inspected for errors, warnings and findings; exit 0 alone is
insufficient. Temporary local repositories are test transport, not a published
remote source. [Distribution](distribution.md) records the boundaries.

## Known limits and model traversal

- Pinned VibeVM 1.0.7 emits an INDEX `kind="static"` package entry despite authored
  `link="dynamic"`. Static loading reads the small conditional boot; the protocol
  remains a separate explicit relevant-task read. No native JIT behavior or
  context/cost reduction is inferred. Fresh model probes must actually traverse
  generated AGENTS -> INDEX -> installed boot -> protocol where applicable.
- The GNU release needs `GLIBC_2.39` and failed on the earlier Debian environment;
  the hash-pinned musl artifact works there. This does not impose a mandatory
  consumer platform restriction for ordinary guidance/source checks.
- Path-only requirements fail upstream with `empty world / ORDER-LAW`. Reproduce
  with `--materialize --path-source`, expecting a failure. The explicit local
  registry form works; no upstream workaround/patch is shipped.
- `validate` writes lease/lifecycle state and `install` adds generated boot/AGENTS
  state. Probes use copies; neither operation replaces human-owned instructions
  or authorizes a real consumer migration.
- Mutable tags can yield a lock/retained-slot split that upstream check misses.
  `frozen=true` is release intent, not demonstrated publisher tag protection.
  Independent canonical hashes and complete generated route checks remain needed.
- Existing materialized slots and complete Git-state rollback support offline
  reading/reinstall. Warmed cache alone cannot rebuild when the remote manifest
  or slots are unavailable in the pinned direct-Git probe.
- VibeVM is closed alpha without compatibility promises; release/tag mutability
  is handled by pinned tool and independently verified payload identities.
  GitHub raw-HTTPS full-SHA acquisition, actual public release, wider platforms,
  transitive dependencies and real consumer adoption remain unqualified.

[Task 8](https://github.com/jresearchsoftware/shared-governance/issues/8) evaluated
Skill versus ordinary-protocol routing and the owner accepted the latter for
simpler delivery. Its model probes did not traverse generated boot; Task 10's
[evidence](task-10/step-1/README.md) addresses that requirement without claiming
causality, general reliability or measured cost gains from single observations.
VibeVM adds dependency transport, lock/slot state and generated linkage; a
Git-pinned ordinary protocol remains sufficient when transport is unnecessary.

Only after independent review and owner-authorized merge may Task 2 seek specific
remote release admission against the new accepted source SHA and destination.
A later consumer-owned migration must review adoption and remove the local
canonical duplicate in the same transition, preserving local overlays.
