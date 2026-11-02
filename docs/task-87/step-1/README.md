# Task 87 Step 1 — producer VibeVM 1.0.10

Authority: [Task 87](https://github.com/jresearchsoftware/shared-governance/issues/87),
Manual Codex Step 1, Direct acceptance; accepted guidance is frozen at
`bee96f1715142fde598318e7db402168dcfabf5f`. The
[owner-authorized compatibility Decision](https://github.com/jresearchsoftware/shared-governance/issues/87#issuecomment-6577910678)
permits the narrow correction described below. This evidence is executor
qualification, not independent acceptance, merge, release or consumer adoption.

## Verified upstream identity

The live release API and tag independently identify release `431101942`, tag
`v1.0.10` at `49a2d745ec2ad8bb123ba867a53400b0a3ff0c3d`, with `immutable=false`.
Downloaded `DISTRIBUTIONS.json`, both Linux x86_64 bootstrap executables and the
GNU ZIP match their API SHA-256 digests. The manifest agrees on the source commit
and all three executable/archive digests. The complete supported identities,
asset IDs, URLs and checksums are in [the pin](../../../toolchain/vibevm.json).
The musl executable reports `vibe 1.0.10` and is used for native probes.

## Mixed graph and compatibility correction

An unmodified cold install in isolated settings fails: the built-in raw-file
mapping sends Relay's Git clone to
`https://raw.githubusercontent.com/jrs-vibevm/org.jresearch.ai.codex-relay.git`,
which returns 404. An ordinary Git request to the original GitHub URL succeeds.
[The failed probe](cold-install-failure.json) retains the actual refusal.
Upstream 1.0.10's `crates/vibe-registry/src/git_backend/shell/raw_http/hosts.rs`
defines that default raw-file endpoint. No host credential or access change is
needed to reproduce the issue.

The owner-approved [identity row](../../../toolchain/vibevm-git-compat.toml) keeps
only this existing Git origin unchanged through `VIBE_REMAP` in the isolated
staging environment. It adds one environment variable to mixed-graph native
maintenance, without changing root requirements, Git source SHA, package bytes,
global settings or other projects. No remap package/application feature is
adopted. Removing it requires a later tool upgrade and a successful unmodified
cold acquisition probe; a cache hit alone does not establish that the defect is
fixed. This is an upstream compatibility limitation, not a claim of general
remap qualification.

With the correction, native fresh resolution selects exactly:

| Package | Version | Content hash |
| --- | --- | --- |
| Development Governance | 7.0.0 | `sha256:5ce5f41aa48aa0604fc5f04e76e5b29cc5134d51b848b4be327ee7e621cd0b22` |
| Codex Relay | 3.0.0 | `sha256:451ee21dbfd63abd7918f0aee979220fb57cb8a8dffde20009a25f11bf9071e7` |

Relay remains Git-sourced at `325c96371783e2d628bfa9903b3244468c688fe6`;
Shared remains the in-tree registry export. Canonical producer verification
checks source/slot bytes, lock identities, dynamic dependency linkage, exact
INDEX/AGENTS routing and native Skill projection. Listing, projection dry-run and
actual Codex projection succeed. Restoring the 13 historical slots pruned by
native install preserves their original bytes; native `check` reports just those
13 orphan warnings, with no errors. They remain retained history, not selected
guidance. The current authoring probe now recognizes those bounded warnings and
the separately installed enclosing Relay Skill instead of incorrectly requiring
an empty workspace.

After materialization/projection, the only tracked diff is six lines of lock
metadata (generator, timestamp and absolute local source location). Those
incidental bytes are deliberately not transferred into the producer checkout.
The committed lock remains the truthful earlier 1.0.7 materialization record;
its selected identities and ready files are valid with 1.0.10. No boot, payload,
Skill or historical slot regeneration is necessary. The existing AGENTS boot
block, slot marker schema and bounded legacy source-hash recipe are verified
unchanged, so `prepare-distribution.py` needs only accurate qualification comments.

## Integrity and recovery

The distribution incident probe still reproduces mutable-tag lock/slot drift,
but 1.0.10 now rejects `check` with an error finding named `lock_slot_hash`,
addressed to the lock's `content_hash`. The probe now requires that diagnostic;
the canonical byte verifier remains necessary for payload/index corruption.
Upstream source owners are `crates/vibe-check/src/checks/lock_slot_hash.rs` and
`crates/vibe-cli/src/commands/reinstall/pin.rs` at the pinned commit.

On the actual mixed graph, changing only disposable local source bytes causes
`reinstall --force --offline` to refuse with `lock_hash_mismatch`; manifest,
lock, slots, boot and Skill state remain unchanged. Ordinary Git restoration
recovers the complete committed project. Two newly generated ignored boot
receipts are removed only inside the disposable clone; lifecycle journals are
retained as diagnostic state. Plain offline reinstall and canonical producer
verification succeed after recovery.

A separate disposable reproduction of upstream B-206 installs a good package,
then adds a wrapper with an invalid static dependency. The late failure names
`STATIC.xml`; all project files and directories except `.vibe/` journals match
the pre-command snapshot, including manifest, lock, slots and boot. This tests
actual rollback after materialization begins, not only an early resolver refusal.

The distribution probe also retains cold/repeat local Git installation,
publisher idempotence, immutable-license/payload verification, synthetic update,
offline retained-slot rebuild and complete Git rollback. Cache-only recovery
with a missing remote manifest remains unavailable and is not presented as a
new supported recovery path. Native publisher/release tests cover guarded local
publication, competing writers, frozen dependency closure, diamond conflicts
and intentional lock update; no real publication occurs.

## Scope and reproduction

The frozen Development Governance 7.0.0 export, in-tree source, selected slots,
Relay 3.0.0 immutable content and projected Skill are unchanged. No package bump
or publication is needed. The complete effective `chatgpt/instructions.md` bytes
and all generation inputs remain unchanged; this Task introduces no live-setting
application obligation or claim of live Settings parity. Earlier reconciliation
history is not discharged by this no-change result.

Use Python 3.11+, Git and the digest-verified musl binary on a native Linux
filesystem. These are one-time upgrade probes, not additional recurring CI gates:

```sh
git diff --check
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
python3 scripts/test-release.py --vibe /absolute/path/to/vibe
python3 scripts/test-self-adoption.py
python3 scripts/qualify-vibevm.py --vibe /absolute/path/to/vibe --materialize
python3 scripts/qualify-distribution.py --vibe /absolute/path/to/vibe --source-ref "$(git rev-parse HEAD)"
python3 scripts/qualify-toolchain.py --vibe /absolute/path/to/vibe \
  --git-compat toolchain/vibevm-git-compat.toml --output /tmp/toolchain-qualification.json
```

The persisted [native report](native-qualification.json) and
[validation summary](validation.md) identify tested source revisions and limits.
Windows/macOS runtime and fresh model/client behavior are not qualified by these
Linux CLI probes. The GNU bootstrap also verifies its version on this Debian
host but emits a weak `GLIBC_2.39` warning; all functional probes use musl.
Independent exact-head review and applicable GitHub checks remain outstanding
until their actual native evidence exists. The executor stops at that boundary.
