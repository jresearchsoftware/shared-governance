# One-package distribution preparation

[Task 2](https://github.com/jresearchsoftware/shared-governance/issues/2) Step 2
adapts the source package identity and declared passive Skill set before first
publication, using source changes and disposable local Git fixtures. The
completed Step 1 was independently accepted through
[PR 3](https://github.com/jresearchsoftware/shared-governance/pull/3), reviewed at
`2f375e8c865896676a22171ab91e773f016248a3` and squash-merged as
`7cb702164b3e26c6f86e85b2d5596bbb9cb441ba`. Its local qualification remains
historical evidence for the old coordinate, not fresh proof for this candidate
or a real remote distribution. Actual GitHub repository creation, package tags,
releases, registry entries, credentials and real consumer migration require
separate owner authority after independent source acceptance and merge. The
Task stays open. This document allocates no later Step or execution profile.

## Source and proposed transport

The only editable semantic source remains `jresearchsoftware/shared-governance`.
The current `org.jresearch.ai/development-governance` v0.1.0 member at
`vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0` is
exported to a package repository root, rather than addressed as a nested member
of the authoring Git URL. Its ordinary passive source files, MIT/derived notices,
manifest, one compact boot pointer and every declared Skill/reference are copied
byte-for-byte. Initially only the accepted `proportional-controls` Skill and
procedure are included, with unchanged bytes. One package version identifies the
complete declared Skill set; subsequent additions or changes need a new accepted
version and explicit reviewed consumer update. They do not create separate
VibeVM dependencies merely because another rule group is added. `publish=false`
remains in the source and export; no workspace-wide publishing is enabled.

Proposed, **unallocated** destination:

| Item | Proposed value |
| --- | --- |
| Repository | `https://github.com/jresearchsoftware/org.jresearch.ai.development-governance.git` |
| Package | `org.jresearch.ai/development-governance` |
| Version tag | `v0.1.0` |
| Transport | `vibe registry publish --repo-url` to a separately prepared repository; direct Git-source consumer |
| Consumer identity | Exact `=0.1.0`, full distribution commit where supported, canonical source SHA and verified content hashes |

This is the pinned tool's `<group>.<name>` naming convention, without an index
or new registry service. The Step 1 proposed
`jresearchsoftware/org.jresearch.governance.proportional-controls` destination
is historical only and is not the owner's intended publication destination.
Direct publishing bypasses registry token loading and
host APIs, and uses ordinary local Git authentication. It requires the
destination to exist. `publish=false` is **not** an enforcement gate for direct
`registry publish`; local dry-run and publishing accept it. Keep external
authority separate from that metadata and from the publisher's exit status.

## Prepare and check without publishing

Use Git and Python 3.11+. A full commit containing the new coordinate is required.
For a local candidate check, use its committed exact head as below. Before any
later external publication, the caller must select and verify an independently
accepted source SHA; no script infers acceptance from branch names, hashes or
CI. A later accepted authoring commit changes provenance and the distribution
tree hash even when policy bytes agree. Current preparation requires the new
coordinate; accepted old-coordinate commits remain available as historical
Git/native-Skill baselines through `vendor-skill.py`.

```sh
# Local candidate check only; publication needs separately accepted source identity.
source_sha="$(git rev-parse HEAD)"
prepared="$(mktemp -d)/package"
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --destination "$prepared"
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --verify "$prepared"
```

Preparation validates the committed package before writing output. Unsupported
capabilities, identity/license drift, non-ordinary files, incomplete payloads,
moving/short refs and occupied destinations fail explicitly. Output must be
outside the authoring checkout. Uncommitted source changes cannot affect it.
Every Skill is declared by a unique name and its package-local directory, with
`include = ["SKILL.md", "references/*.md"]`. Preparation checks the complete
declared passive file set; undeclared, executable or malformed Skill payloads
cannot expand the package. Consumer verification binds all declared projections
to canonical package bytes alongside receipt, lock and slot identity.

Generated `DISTRIBUTION.json` records the canonical repository, full source SHA,
source path, package/version, sorted per-file SHA-256 map and a SHA-256 of its
compact sorted JSON map. The receipt excludes itself from that map. Verification
reconstructs all expected bytes and the receipt from canonical Git, so a changed
file plus a self-consistent counterfeit receipt still fails. The artifact is
not a second editable policy or an approval record.

Historical Step 1 used the accepted old-coordinate source
`aa1e18085dee2aa59e19c5939e882cd8084eea00`. For that six-file payload,
payload-map SHA-256 was
`e3d63ca16efe5a4d6e29eae18aba9893c7f857a49991efef552e6d0a660db40e`.
The VibeVM 1.0.7 Linux tree hash, including its generated receipt, was
`sha256:34aecab48a91e3128c06d8ae8c8f485ecdee50c30b0fa9269670aae49dfcfca0`.
These different identities use different recipes; neither is a Git commit SHA.
They do not identify the renamed package. Rebuild current content identities
from its selected full source SHA rather than copying historical hashes.

## Reproduce the disposable qualification

Use the exact hash-verified Linux x86_64 musl VibeVM 1.0.7 binary prepared by
[the authoring instructions](authoring.md#pinned-vibevm-probe). No global install
is needed. Run on an isolated Linux filesystem, with the source Git objects
available locally:

```sh
git diff --check
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
python3 scripts/qualify-vibevm.py --vibe "$tool_tmp/vibe" --materialize
python3 scripts/qualify-distribution.py --vibe "$tool_tmp/vibe" --source-ref "$(git rev-parse HEAD)"
```

The disposable probe creates temporary bare Git destinations and consumers,
isolates VibeVM settings/cache and disables ambient Git configuration/prompts. Its only
publication writes are to those temporary `file://` repositories. It checks
dry-run nonmutation, real local publishing, identical republish, a cold
independent consumer, repeated install, source/file/lock/slot identity and
Codex project-scope projection for every declared Skill. Every VibeVM result,
including expected failures, is printed; check findings are parsed, not inferred
from exit 0.
All temporary fixtures are removed. Qualification scripts remain outside the
passive package and are optional for ordinary prose edits.

The following accepted Step 1 results were observed with the historical
`org.jresearch.governance/proportional-controls` package on Debian WSL, UID 1000,
Python 3.11.2, 2026-10-09. They describe pinned upstream behavior and do not
replace Step 2 exact-head qualification:

| Behavior | Result and practical limit |
| --- | --- |
| Local direct publisher dry-run / publish / identical republish | PASS; dry-run leaves refs empty, repeat keeps refs unchanged |
| Exact-version tag install, cold separate consumer and repeated install | PASS; all source and receipt bytes match |
| Native Skill comparison | Identical file set and bytes to exact-commit Git export; LICENSE remains in package slot |
| Human-owned AGENTS | Preserved outside one generated `<vibevm>` block; installation adds boot linkage |
| Changed bytes at the same version/tag | Preparation rejects; upstream publisher moves tag and install can rewrite lock while retaining old slot |
| VibeVM check after that lock/slot split | Zero errors/warnings/findings; canonical consumer verifier rejects the split |
| `--rev` via default local bare Git archive | Fails `no such ref`; no server setting is changed to hide this restriction |
| Offline reinstall with existing materialized slots | PASS with destination unavailable |
| Offline install from warmed cache, destination unavailable | FAIL fetching remote manifest |
| Offline clean then reinstall, or forced reinstall | FAIL without slots / fetching remote manifest; cache-only recovery unqualified |
| Explicit update to synthetic local v0.1.1 | PASS, old slot pruned, skill bytes unchanged; version metadata only, no second authored/released package |
| Rollback of complete materialized consumer Git state | PASS offline; manifest, lock, slot and native skill return to canonical v0.1.0 |

The synthetic v0.1.1 fixture intentionally is not a valid prepared source
artifact. It tests upstream update mechanics only. A real update needs its own
accepted source/version and regenerated provenance. Fixed tag/rev declarations
do not provide an automatic latest-version update. Restore the complete reviewed
consumer commit for rollback; manifest+lock alone cannot recover a pruned slot
offline. Reproject and verify skills during deliberate maintenance, then commit
the accepted materialized state together. Normal agent execution reads those
committed files and performs no runtime remote resolution.

## Concrete external publication plan — protected boundary

After independently accepted source review and an owner-authorized squash merge,
the owner must separately authorize the destination, exact source SHA, version,
publication account and remote qualification. Verify repository ownership,
public visibility and intended package root, with existing ordinary Git access.
Do not acquire credentials or change repository settings in this Step.

1. Prepare from the chosen accepted full source SHA and independently verify the
   complete diff, receipt and hashes. Confirm the pinned binary's digest again.
2. Inspect destination heads/tags. If `v0.1.0` already exists, stop and compare
   its full peeled commit and content; never move a public version tag to changed
   content. The alpha publisher permits that mutation and its dry-run is not a
   provenance, destination-existence or immutable-version proof.
3. Under that specific publication authority, the supported commands are:

   ```sh
   target_url=https://github.com/jresearchsoftware/org.jresearch.ai.development-governance.git
   "$tool_tmp/vibe" --json registry publish "$prepared" --path "$prepared" --repo-url "$target_url" --dry-run
   # Actual push only under the separate owner publication admission:
   "$tool_tmp/vibe" --json registry publish "$prepared" --path "$prepared" --repo-url "$target_url"
   ```

4. Read back the actual `v0.1.0` peeled full distribution SHA, independently
   clone that commit, and run `--verify` against the accepted source SHA. Record
   both Git identities, receipt/map/tree hashes and complete file set. The
   version tag remains mutable; checks before/after publishing are not atomic
   host-side tag protection. Content identity, not a version label, is the
   reproducibility basis. No VibeVM wrapper or patched tool is proposed.
5. In a fresh independent disposable remote consumer with empty isolated
   settings, use the exact version and recorded full distribution SHA:

   ```toml
   [project]
   name = "disposable-consumer"
   version = "0.0.0"
   spec_format = "mixed"

   [requires.packages]
   "org.jresearch.ai/development-governance" = { version = "=0.1.0", git = "https://github.com/jresearchsoftware/org.jresearch.ai.development-governance.git", rev = "FULL_RECORDED_DISTRIBUTION_SHA", auth = "none" }
   ```

   Run pinned `install --path CONSUMER --no-default-registry --assume-yes`, then
   `skill install --path CONSUMER --agent codex --scope project --skill
   proportional-controls --yes` for the initial single-Skill package. A later
   accepted version must project every Skill declared by that package. Finally run
   `python3 scripts/prepare-distribution.py --source-ref "$source_sha"
   --verify-consumer CONSUMER`. This validator is bounded to this single v0.1.0
   Git requirement and mixed-format fixture: it checks installed receipt/bytes,
   slot metadata, lock hash/source declaration and every declared native
   projection together.
   The source-supported GitHub raw-HTTPS full-SHA path is **not yet remotely
   qualified**. Report any actual acquisition failure as a decision input.

No new consumer becomes governed through these tests. A consumer-owned Task must
adopt the pinned materialized source and remove its local canonical duplicate
together, preserving overlays. Otherwise both loss of authority and dual
authority remain possible. Publication, source acceptance and consumer adoption
are separate decisions.

## Comparison and retained limits

| Property | Git/native Skill | Proposed VibeVM path |
| --- | --- | --- |
| Canonical identity | Full accepted source SHA plus SOURCE.json file hashes | Same source SHA plus distribution SHA, receipt and independently checked tree hash |
| Producer work | Local export; no remote publication | Package-root export, extra repository/tag, pinned alpha publisher and remote read-back |
| Consumer maintenance | Git/Python export, review and materialized commit | Tool binary, manifest, lock, slots, boot/AGENTS state, skill projection and independent integrity check |
| Offline / rollback | Committed skill and reviewed Git revert | Complete materialized Git snapshot works; warmed-cache rebuild fails in this direct-Git probe |
| Authority | Consumer-owned reviewed migration | The same; dependency graph/managed block grants no operational authority |

No measured context/time savings or automatic Codex discovery is established.
The GNU `GLIBC_2.39` requirement, path-only empty-world/ORDER-LAW failure, mutable
tool release/tag and alpha compatibility limits remain as documented in
[authoring](authoring.md#observed-evidence-and-limitations). No real remote
publication, transitive dependency behavior, real consumer migration or wider
platform guarantee follows from these local results. The simpler Git/native
baseline remains viable; extra VibeVM maintenance cost is explicit.

Pinned upstream evidence (all at `b6659978453f50e6d1d4d99626d70b980a2c5847`):

- [Direct publishing route](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-cli/src/commands/registry/publish.rs#L86)
  and [mutable version publisher](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-publish/src/orchestrator.rs#L153).
- [Git fetch ignores expected hash / omits resolved commit](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-registry/src/multi_registry_resolver/sources.rs#L178)
  and [tree-hash recipe](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-registry/src/shippable.rs#L123).
- [GitHub raw-HTTPS route](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-registry/src/git_backend/shell.rs#L329)
  and [offline reinstall requires existing slots](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-cli/src/commands/reinstall/regenerate.rs#L62).
