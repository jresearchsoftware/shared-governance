# Task 45 Step 7 qualification

Authority: [Step 7 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6239052197).
Frozen independently accepted source-main: `ec048fb39ae28cf2d747101466a603ddd062b1b0`.
Starting candidate: PR #46 at `b76ea98e6ee2645be674690094f88a6fa265d77d`.
[Semantic coverage and lifecycle walks](scenarios.md) explain changed behavior,
preserved authority, scope and evidence limits. The final canonical Outcome on
PR #46 identifies the exact qualified head and CI. Successful Outcome readback
must precede the final Ready transition; the subsequent native PR readback is
state evidence without another Outcome or source commit.

## Source and affected-behavior qualification

Implementation commit: `3e7397b47b18f5be67ceef271a80967dd94fe9db`.
Native projection commit: `b0bb3198a91d0ea6514df7d38d16375274dc4ff5`.
All ordinary suites below ran against a clean native Debian WSL clone of that
complete projection commit. Later qualification text/logs change no package bytes.

| Check | Observed result / primary record |
| --- | --- |
| Source/exact export/native integrity | PASS: 693 tracked files, 1,111 local links and bounded credential-marker scan; [source log](logs/source.txt). |
| Distribution | 47 passed, zero skips; all starting TH anchors/headings retained, new rule owned only by TH, installed changelog/README references, no shared CLI command; [log](logs/distribution.txt). |
| Self-adoption | 13 passed, zero skips; actual installed TH-028 equals authored bytes and local AGENTS/manual operation routes are accessible; existing corruption/lock/index/recovery checks retained; [log](logs/self-adoption.txt). |
| ChatGPT | 24 passed, zero skips; [log](logs/chatgpt.txt). Existing projector update/check confirms complete Instructions NO_OP (6,135 Unicode characters), Sources DISABLED; only maintenance authority points to Step 7. Frozen accepted inputs remain unchanged. |
| Release | 17 total: 11 passed, six optional native transport/dependency cases skipped; [log](logs/release.txt). |
| Shared publisher | 50 total: 44 passed, six optional native transport cases skipped; [log](logs/publisher.txt). Publisher implementation/workflows/transport remain unchanged in Step 7. |
| Lifecycle behavior | 14 desk-based applications in [scenarios](scenarios.md), including the required missing-capability, ambiguous readback and split-result paths. These are semantic checks, not simulated remote permissions or model compliance. |
| Local GitHub capability | Existing authenticated `gh pr view 46` confirmed exact starting PR/head and Draft before modification. Installed `gh pr ready --help` exposes Ready and `--undo` Draft; connected GitHub tools also offer both actions. No needless initial toggle. |
| Preserved material | Git comparison preserves historical frozen source/slots, all other protocols (including Independent Review), shared client tools, existing production publisher/credentials, and prior Outcomes/reviews. INDEX and generated agent blocks keep their already-correct 3.0.0 routes. |

The changed shared contract is only TH-028 plus package README/CHANGELOG. Complete
Task Handoff and material manual/agent/acceptance clauses were examined together:
state ownership, start/end ordering, actual-result routing and same-Outcome
recovery fit existing Step/independence/continuation rules. No method migrated to
Independent Review. This is self-check evidence, not independent acceptance.

## Fresh pinned-native materialization

Verified existing VibeVM 1.0.7 Linux musl binary against the toolchain digest:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
The exact Git exporter staged **20 payload files**, digest
`e28422aac0be3827a150e3a4f43cdc091e9fca4f1d7d76ead1e79fbaa4f97763`;
[generation receipt](logs/generation.json). In a disposable clone, refresh only
the task-generated unaccepted candidate lock, then ordinary offline native
install resolves/materializes 3.0.0 and prunes three old slots;
[actual install](logs/install.txt). Canonical producer verification passes;
[verification receipt](logs/verify.json). Only current source/slot/lock outputs
were copied back; historical repository inventory was preserved.

In that separately native-pruned disposable fixture, reconcile only its removed
slot inventory in its temporary Git index; the unchanged authoring qualifier
then passes **seven commands**, zero findings, full materialization equality and
human overlay preservation; [native authoring log](logs/native-authoring.txt).
This qualifies changed package materialization and local access, not publication.

On the actual retained repository inventory, native check still reports **zero
errors / three warnings**, for deliberately retained installed 2.5.0/2.6.0/2.7.0
slots outside the current lock; [native retained inventory](logs/native-retained-inventory.json).
Impact: orphan warnings and pruning on deliberate install; no current 3.0.0
source/slot inconsistency. Preserve history and use ordinary accepted reading
without install. Canonical integrity passes. No zero-warning claim is made for
retained inventory; the zero-finding authoring fixture is separate.

## Handoff, reuse and limits

The single canonical terminal Outcome belongs to sole result PR #46 and binds
the final exact head and current CI. PR was verified Draft at commencement.
After successful Outcome publication/readback, the authorized manual executor
performs Ready and reads back the same number/head/native state. A state-only
failure must retain this Outcome and identity and report its exact capability
gap; it cannot trigger a second execution or duplicate result publication.
Fresh independent exact-head review follows. No review APPROVE is supplied here.

The title tool plus list readback confirmed the persisted
`Task 45 — Step 7 — Manual PR Draft/Ready lifecycle` navigation title.
Instructions/Sources remain source-controlled desired state, with no live
settings readback/application. Native transport skips are skips; sufficient
unchanged Step 2/4 atomicity/race/retry evidence is reused. The unprivileged
Actions fixture skips production planning/publication/summary and uses synthetic
secret isolation. Real private caller/destination permissions, credentials,
remote publication, consumer/Relay adoption, publisher activation, Landscape
integration and Windows/macOS native publisher behavior remain unqualified and
outside scope. No new fault injection against real PRs or model-behavior claim.

Same unaccepted 3.0.0 MAJOR from 2.7.0, `Package bump: major`; no 4.0.0.
No merge, package/distribution tag/ref publication, live settings/credential/
protection change, consumer migration or Task closure is authorized or performed.
