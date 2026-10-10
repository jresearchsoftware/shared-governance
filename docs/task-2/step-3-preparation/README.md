# Task 2 — Step 3 preparation

**Historical Skill-payload packet.** [Task 10](https://github.com/jresearchsoftware/shared-governance/issues/10)
proposes a frozen flow-protocol payload before first publication. After its accepted
merge, regenerate source/content identities and seek new specific admission under
Task 2. The evidence and draft below do not authorize or identify that new release.

**PREPARATION FOR REVIEW — external publication and Step 3 execution remain NOT ADMITTED.**

The evidence snapshot was produced on 2026-10-09, with live authority read-back
at 17:54:51 UTC. The owner separately requested that these preparation results
be committed and opened as a PR in this authoring repository. The live
[Issue #2](https://github.com/jresearchsoftware/shared-governance/issues/2)
contains a destination decision, not publication admission. This preparation
does not change that authority or complete the Task. This review candidate
records the report, draft, receipts and logs in Git; it grants no external
execution or publication admission.

## Accepted source and faithful artifact

- Canonical semantic source: `jresearchsoftware/shared-governance`.
- Accepted source: `60704ce3e0f0243d157646989429c6e621fc8f04`, the owner-authorized
  squash integration of independently accepted [PR #4](https://github.com/jresearchsoftware/shared-governance/pull/4).
- Reviewed PR head: `47bf594cbff65dfc39a913a5dfd22fee6cc3aa2a`.
  Both commits have Git tree `c1120f55d18efc9dfabcbe15ea4636cb3f2f7c38`.
  Preparation uses the accepted squash SHA, which was remote main at the snapshot.
  A later documentation commit does not replace this selected payload source.
- Package: `org.jresearch.ai/development-governance`, version `0.1.0`;
  proposed initial annotated distribution tag: `v0.1.0`.
- Intended destination from the live Issue:
  `https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git`.
  The former proposed `jresearchsoftware` destination in accepted source
  documentation is superseded by the owner's destination decision. Package bytes,
  including the accepted prepublication README and `publish=false`, were not edited.
- [Prepared package receipt](receipts/DISTRIBUTION.json), [all content identities](content-identity.json)
  and [exact-source native Skill receipt](receipts/SOURCE.json) are committed here.
  The package and native Skill bytes can be regenerated from that accepted Git
  commit with the existing exporters; generated policy copies are not committed
  alongside their canonical source. Reproduction commands appear below.
  There are six passive payload files plus the generated receipt. The only
  declared Skill is `proportional-controls`; its instructions/procedure and MIT
  notice remain identical to the accepted bootstrap.

| Identity | Value |
| --- | --- |
| Payload path/hash-map SHA-256 | `4b611bc0a6dc9500dd9e7b6cc11c23092ecf81d25d329ea2066ac9bca9471609` |
| Receipt SHA-256 | `ce072ea1b991f2a1c22ff65cf62b057ecd07817b7f06a8a739cc09281f660b24` |
| VibeVM 1.0.7 Linux tree hash, including receipt | `sha256:9ee1caef5a62d56dc5bcc1890633e8395314f6a93ae9c85dfb8f47cf3d7a1af7` |
| Actual public distribution commit | Unavailable: nothing was published |

The temporary local lifecycle commit `5b5b9a6b76c04b52820e2e276766f7948124ded6`
appears in the fixture log only. It is not a public distribution identity.

## Fresh validation at the accepted squash SHA

A clean anonymous HTTPS clone was checked out at the full accepted SHA on
Debian WSL's native temporary filesystem, UID 1000, Python 3.11.2, Git 2.39.5.
The exact VibeVM 1.0.7 musl artifact was downloaded and verified against
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`
before execution. No global installation or home configuration changed.
Qualification logs are copied byte-for-byte from the preparation run, with
their `.log` filenames changed to `.txt` for committed evidence. Empty output
logs and the original temporary fixture paths are preserved.

| Check | Fresh result | Evidence |
| --- | --- | --- |
| Whitespace and clean source checkout | PASS | [whitespace log](logs/whitespace.txt) |
| Source/exact-commit native export | PASS: 25 tracked files, 18 local links; bounded credential-marker scan | [source log](logs/source.txt) |
| Distribution behavioral tests | PASS: 42 tests | [test log](logs/tests.txt) |
| Repeated preparation | PASS: complete file set and bytes identical | [first preparation](logs/prepare.txt), [second preparation](logs/reproduce.txt), [comparison](logs/reproducible.txt) |
| Canonical verification of retained package | PASS after copying to retained Windows artifact directory | [verification](logs/verify-retained.txt) |
| Hash-pinned VibeVM authoring/materialization | PASS: 7 commands; inspected check JSON has no findings | [materialization log](logs/materialization.txt) |
| Disposable direct-Git publisher/consumer lifecycle | PASS: 23 commands including classified expected failures | [lifecycle log](logs/distribution.txt) |
| Accepted-main GitHub CI | Completed successfully on this SHA; API annotation count 0 | [run 37967738820](https://github.com/jresearchsoftware/shared-governance/actions/runs/37967738820) |

Local lifecycle evidence includes dry-run nonmutation, local publication and
identical republish, a cold separate fixture consumer, repeated install, exact
canonical slot/lock/Skill verification, human-owned AGENTS preservation, tag-drift
rejection, synthetic version-only update and complete materialized Git rollback.
All publisher mutations in that run were confined to automatically removed
temporary `file://` repositories. The probed authoring clone remained clean.
CI/API annotation evidence does not establish absence of UI-only GitHub warnings.
An additional read-only preparation audit independently verified the retained
package against canonical accepted-source Git and checked all content hashes.
It also checked the draft's authority/authentication/ref boundaries. This audit
does not grant source acceptance or publication admission.

## Read-only destination preflight

At the recorded snapshot, GitHub API identity was `foal` (458209). The publicly retrievable organization
`jrs-vibevm` has ID `340262266`; that account's membership is `active` with
organization role `admin`. Its API repository listing was empty, and the intended
repository endpoint returned HTTP 404. No repository was created by preparation.
These observations are historical snapshot evidence, not a current existence
or permissions assertion.

These observations do not establish successful repository-creation capability or
authenticated Git push in the eventual publisher environment. Target visibility,
write permissions and existing refs cannot be verified while its endpoint returns
404. A 404 is not claimed to prove universal nonexistence; it may reflect access.
Recheck existence/access and refs under the expressly admitted publishing account.
Current Windows CLI identity does not prove Git authentication in isolated Debian.

## Concrete future gate

[The proposed owner admission](admission-draft.md) names the exact source,
destination, account, version/tag, initial refs, bounded publication and anonymous
disposable remote-consumer checks. It is proposed text for review, not effective
Issue authority. Acceptance or merge of this documentation cannot admit it.
It includes the future command sequence and mandatory read-back/stop conditions.

The pinned publisher creates `main` plus an annotated `v0.1.0` tag and internally
uses `--force-with-lease` for both refs and `git tag -f`. The proposed authority
is limited to initial refs in a new empty public repository, without scaffolding.
Any existing ref requires a stop and separate owner decision. Dry-run does not
check remote existence, permissions, refs or canonical provenance.
The tool has no create-only enforcement; an outer empty-ref check leaves a race
before its internal lease snapshot. The proposed initial-only boundary is an
operator restriction, not an enforced guarantee. If exclusive initial publishing
conditions cannot be established, a separate owner decision remains necessary.
[Publisher source](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-publish/src/git_publish.rs#L32),
[direct CLI route](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-cli/src/commands/registry/publish.rs#L79).

Future read-back must record the real public peeled distribution SHA and independently
verify its complete bytes against this accepted source. The consumer verifier
binds lock to its declared URL/ref; therefore separately assert the exact
`jrs-vibevm` URL, recorded full distribution SHA and `auth="none"`.
The upstream resolver does not itself enforce the expected hash or record a
resolved commit, so canonical verification remains necessary.
[Resolver source](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-registry/src/multi_registry_resolver/sources.rs#L173).

## Reconstruct and qualify the accepted artifact

Use Linux x86_64, Python 3.11+, Git and curl. Run on a native disposable Linux
filesystem. These commands reconstruct the recorded package from the accepted
commit, not the documentation candidate's HEAD. The VibeVM qualification scripts
publish only to their automatically removed local fixture repositories.

```sh
set -eu
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_TERMINAL_PROMPT=0
source_sha=60704ce3e0f0243d157646989429c6e621fc8f04
scratch="$(mktemp -d)"
git -c core.autocrlf=false clone --no-checkout https://github.com/jresearchsoftware/shared-governance.git "$scratch/source"
git -C "$scratch/source" checkout --detach "$source_sha"
cd "$scratch/source"
out="$scratch/results"
mkdir -p "$out/logs"

git diff --check > "$out/logs/whitespace.txt" 2>&1
python3 scripts/qualify.py --export-ref "$source_sha" > "$out/logs/source.txt" 2>&1
python3 scripts/test-distribution.py > "$out/logs/tests.txt" 2>&1
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --destination "$out/package" > "$out/logs/prepare.txt" 2>&1
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --verify "$out/package" > "$out/logs/verify.txt" 2>&1
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --destination "$out/reproduction" > "$out/logs/reproduce.txt" 2>&1
diff -r "$out/package" "$out/reproduction" > "$out/logs/reproducible.txt" 2>&1
python3 scripts/vendor-skill.py --ref "$source_sha" --skill proportional-controls --destination "$out/native-skill" > "$out/logs/native-export.txt" 2>&1

curl --fail --location --output "$scratch/vibe" https://github.com/vibevm/vibevm/releases/download/v1.0.7/vibe-bootstrap-x86_64-unknown-linux-musl
printf '%s  %s\n' 20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240 "$scratch/vibe" | sha256sum --check
chmod u+x "$scratch/vibe"
python3 scripts/qualify-vibevm.py --vibe "$scratch/vibe" --materialize > "$out/logs/materialization.txt" 2>&1
python3 scripts/qualify-distribution.py --vibe "$scratch/vibe" --source-ref "$source_sha" > "$out/logs/distribution.txt" 2>&1
```

Compare the complete generated `DISTRIBUTION.json` and native `SOURCE.json`
against the [committed distribution receipt](receipts/DISTRIBUTION.json) and
[native receipt](receipts/SOURCE.json). Verify all payload file hashes and the
tree hash against [content-identity.json](content-identity.json); the final
distribution log reports the independently recomputed payload and tree hashes.
Later runs have different temporary paths and may produce different fixture
Git commit IDs. They must retain the canonical source and content identities.
The empty [whitespace](logs/whitespace.txt) and [reproducibility](logs/reproducible.txt)
logs record successful commands with no output in the original run; they are
not standalone exit-status evidence.

## Retained limits and reconciliation

Actual remote publishing, authenticated publisher push, GitHub full-SHA acquisition,
cold remote materialization, remote idempotence and public content read-back are
UNPROVEN. No public tag immutability, measured context/time savings or automatic
client Skill discovery is claimed.

Fresh local probes reproduce upstream mutable-tag lock/retained-slot divergence
despite zero-finding `check`; canonical verification rejects it. Existing-slot
offline regeneration and full Git rollback pass, while cache-only recovery and
default local full-SHA archive acquisition fail as expected. Synthetic v0.1.1
tests mechanics only. GNU GLIBC_2.39, path-only empty-world/ORDER-LAW, mutable
tool release/tag and alpha compatibility limits remain disclosed.

The initial local preparation snapshot made no source/remote mutation;
[preflight-evidence.json](preflight-evidence.json) records that bounded run.
The subsequent owner-requested handoff adds this evidence packet and affected
documentation on an ordinary source branch/PR. The passive package, its canonical
Skills, exporter/qualifier implementation, toolchain pins and AGENTS.md are unchanged.
The first documentation candidate's [CI run](https://github.com/jresearchsoftware/shared-governance/actions/runs/37974484916)
failed during temporary Git repository cleanup with `Directory not empty: objects`,
after its behavioral assertions completed. The test harness now disables automatic
Git maintenance/GC in each disposable fixture to prevent background Git writers
outliving commands and racing cleanup; cleanup errors remain fatal. This is
fixture-local configuration only. The recorded accepted-source logs remain unchanged.
Git documents these controls in [maintenance.auto](https://git-scm.com/docs/git-maintenance#Documentation/git-maintenance.txt-maintenanceauto)
and [gc.auto](https://git-scm.com/docs/git-gc#Documentation/git-gc.txt-gcauto).
Unrelated untracked `.serena/` is preserved. No external distribution repository,
package ref/Release/registry mutation, permission/credential/settings change,
consumer migration, self-approval, merge or closure is part of this candidate.
Probe fixtures removed themselves. Reviewers need no access to the owner's
temporary directories: receipts, complete qualification logs and reconstruction
instructions are in this Git candidate.
Issue #2 remains OPEN / keep-open.
