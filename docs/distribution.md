# One-package distribution preparation

[Task 10](https://github.com/jresearchsoftware/shared-governance/issues/10) proposes
the first frozen `org.jresearch.ai/development-governance@0.1.0` flow with one
ordinary proportional-controls protocol and no native Skill. Its source-only PR
must be independently accepted and owner-authorized for merge before
[Task 2](https://github.com/jresearchsoftware/shared-governance/issues/2) seeks
specific remote publication admission. No script infers authority from CI,
manifest metadata, source SHA, publisher success or dependency installation.

The [Task 2 Step 3 packet](task-2/step-3-preparation/README.md) remains a historical
snapshot for accepted `60704ce3e0f0243d157646989429c6e621fc8f04` and its previous
Skill payload. Its source/content identities and native projection instructions
must be replaced in a newly admitted remote execution request after Task 10's
accepted merge. Historical PR 3's old-coordinate evidence and PR 4's identity /
multi-Skill qualification remain accepted history; they are not current release
or remote acquisition proof.

## Source and intended transport

The only editable semantic source is `jresearchsoftware/shared-governance`.
The package stays at
`vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0` and exports to a
package-repository root. Its manifest, README, MIT/derived notices, compact boot
and complete ordinary protocol are copied byte-for-byte. `publish=false` and
`frozen=true` remain in source and export. Frozen release intent is not an
upstream enforcement guarantee. Future changes need later accepted versions;
no package-versioning or directory migration is included now.

Intended destination (not created/admitted by this Task):

| Item | Value |
| --- | --- |
| Repository | `https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git` |
| Package | `org.jresearch.ai/development-governance` |
| Version tag | `v0.1.0` |
| Transport | `vibe registry publish --repo-url` to a separately existing repository; direct Git-source consumer |
| Identity | Exact `=0.1.0`, full distribution commit where supported, canonical source SHA and independent hashes |

The direct route uses ordinary local Git authentication and requires the target
to exist; `publish=false` does not prevent it. No registry service/index, token
provisioning, repository creation or permissions change is included here.

## Prepare and verify without publishing

Use a full source commit with the new frozen flow. Candidate qualification may
use its own full head; eventual publication requires a separately accepted SHA.

```sh
source_sha="$(git rev-parse HEAD)"
prepared="$(mktemp -d)/package"
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --destination "$prepared"
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --verify "$prepared"
```

Output must be absent/empty, outside the source checkout and ordinary. The
preparer rejects unsupported dependencies, Skills, executable capabilities,
metadata/frozen drift, malformed/undeclared payloads and escaping/missing links.
Five ordinary source files plus generated `DISTRIBUTION.json` form this release.
The receipt records canonical repository, full SHA, path, package/version,
per-file hashes and the hash of their compact sorted map, excluding itself.
Independent verification reconstructs all bytes from canonical Git; a changed
file plus a self-consistent counterfeit receipt still fails.

Consumer verification binds installed receipt/ordinary bytes, complete schema-1
slot metadata, schema-7 lock/source declaration and exact-version Git tag/rev.
It rejects the removed native Skill and ownership receipt, checks a unique
installed package boot entry in generated INDEX and the human AGENTS managed
route to that index. Other consumer-owned native Skills are outside this bounded
package check. Pinned upstream emits `kind="static"` despite authored dynamic
linkage; the installed small boot conditionally selects the full protocol.
Model traversal is separate behavioral evidence.

## Disposable publisher/consumer qualification

With the hash-pinned musl VibeVM 1.0.7 binary from [authoring](authoring.md):

```sh
git diff --check
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
python3 scripts/qualify-vibevm.py --vibe "$tool_tmp/vibe" --materialize
python3 scripts/qualify-distribution.py --vibe "$tool_tmp/vibe" --source-ref "$(git rev-parse HEAD)"
```

The probe isolates settings/cache/Git configuration and writes only disposable
`file://` bare repositories and consumers. It exercises real dry-run, local
publish, identical republish, separate cold install, repeat install, source /
slot / lock / generated-route integrity and zero native projection. It retains
the demonstrated mutable-tag, offline, synthetic update and rollback probes:

| Pinned behavior | Interpretation |
| --- | --- |
| Dry-run, local publish, identical republish | Dry-run refs empty; identical repeat does not move refs |
| Exact-version tag, cold and repeated consumer install | Full canonical payload, receipt, lock/slot and boot route verified |
| Authored dynamic link -> generated static entry | Small boot read at startup; detailed protocol read is conditional |
| Changed bytes under same tag, including frozen metadata | Canonical verifier rejects; upstream can move tag and split lock/retained slot |
| Upstream check after lock/slot split | May report zero findings; independent canonical verifier rejects |
| Local default Git archive by full revision | `no such ref`; no server workaround imposed |
| Offline reinstall with retained complete slots | Works without destination |
| Warmed-cache install / clean or forced recovery with destination unavailable | Fails remote manifest or missing-slot requirement |
| Synthetic version-only `0.1.1` fixture | Tests update/pruning mechanics; not an authored or published second release |
| Complete materialized consumer Git rollback | Restores manifest, lock, boot, slots and protocol offline |

Exact current results are recorded in [Task 10 Step 1 evidence](task-10/step-1/README.md).
Historical `aa1e18085dee2aa59e19c5939e882cd8084eea00` six-file Skill payload hash
`e3d63ca16efe5a4d6e29eae18aba9893c7f857a49991efef552e6d0a660db40e` and VibeVM
hash `sha256:34aecab48a91e3128c06d8ae8c8f485ecdee50c30b0fa9269670aae49dfcfca0`
remain historical identities only. Rebuild current identities from the accepted
full SHA. `--source-ref` does not itself establish acceptance.

## Later protected remote boundary

After accepted merge, Task 2 must read live destination/account/permissions and
remote refs and obtain specific source/version/destination release admission.
Then prepare/verify that accepted source, separately authorize repository setup
if absent, dry-run and publish to the admitted destination using public tooling.
Read back/peel the remote tag, fetch its exact commit to an independent clean
checkout and compare with canonical Git. Never move or replace a published frozen
`v0.1.0`; a mismatch requires owner disposition, not forced repair.

A cold disposable remote consumer must declare exact `=0.1.0` and full
`rev=distribution_sha` where supported, install and run
`prepare-distribution.py --source-ref ACCEPTED_SHA --verify-consumer CONSUMER`.
There is no `skill install` step for this flow. Read the generated route and test
fresh model traversal separately. GitHub's raw-HTTPS full-SHA route is
source-supported but not qualified by local file transport; preserve failures.

No real consumer gains governance authority from package installation. Its own
reviewed migration must adopt the source and remove its canonical duplicate
together. Source acceptance, public release and consumer adoption remain separate.
The GNU/glibc, path-only ORDER-LAW, alpha compatibility, mutable tool/tag and
cache-only recovery limits remain. No model cost saving is established.
