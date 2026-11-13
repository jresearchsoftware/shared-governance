# Task 96 Step 3: recovered source and current qualification

Related to [Task 96](https://github.com/jresearchsoftware/shared-governance/issues/96)
and [Decision 6866786370](https://github.com/jresearchsoftware/shared-governance/issues/96#issuecomment-6866786370).
Manual admission: `run-43521778128`, Step 3, requested `gpt-6.1-sol / xhigh`,
Subagents On. These are requested settings, not measured backend telemetry.
Accepted guidance stays frozen at `0b72349f3ab0b2d88e836a6ba3d4fc675a87f75a`,
the owner-merged PR 93 result. Candidate guidance remains proposed.

## Recovery and source boundaries

The canonical checkout was clean and safely normalized to the admitted branch
and required head `56f4f7cd4d834af865a554906476366f240d6cab` before the starting
gate. Execution uses a separate worktree and fresh native Linux resources.
No original runner checkout or exclusive slot was reused for execution.

The existing qualified read-only WSL/SSH route copied only bounded regular Git
object/pack bytes from the preserved incident. No worker configuration, hooks,
refs, index, alternates or executable Git metadata was imported. The new snapshot
contains 72 files and matches the Task 247 evidence SHA-256
`1c9e075f08f87e3453c38b4387ce9973d3b7ead75a94ae202b6f0e5e219fa1ea`.
Fresh trusted Git, with system/global configuration, hooks and replacement objects
disabled, passed `fsck --full --no-reflogs`; one unrelated dangling tree was
reported, with no corrupt or missing objects.

Original identities independently match the admitted Decision:

- `c65d38160f3773cc7e2194713869a85b25b90e74`: parents are the admitted starting
  head and accepted `0b72349...`; author and committer both match Writer identity.
- `e4f554ea7872a55d404cc35192a21b6601c16ddd`: sole parent is `c65d381...`,
  with the same Writer identity.
- Final tree: `40762e62d767aea224dd5a1f04a8f011bbffcb95`.

After regular-mode/path inspection, the source delta was applied to the fresh
worktree; its staged tree matched that exact tree before the first ordinary
single-parent recovery commit. The prohibited original merge history was not
introduced. Step 1 progress and both terminal Outcomes remain preserved; neither
original operation was replayed or reclassified as successful.

Compared with accepted source, Relay 5.0.0, its Skill and workflows, Development
Governance 7.0.1, the exported public package and ChatGPT generation inputs are
unchanged. Landscape remains producer-root-only at the requested frozen versions.
The current integration guide describes Relay 5.0.0; Step 1/2 evidence retains
its historical wording. No package bump, public distribution mutation, deployment,
Apply, merge, closure or live Settings write is part of this result.

## Current validation

The implementation and qualification-script candidate is
`2fc054749c7e244e7caf621202e4263a42558c84`; the subsequent evidence commit adds
this report and logs only. Exact final-head native CI remains a separate check.
All commands ran in owned clean Git checkouts on native Linux storage, with an
execution-owned temporary root and isolated native settings. The copied VibeVM
1.0.11 musl binary matches accepted SHA-256
`5fe5b3efeb2eab7c7c49a8dc864864ffacac08a9d7be3dc9df0bc0bb15a8bd58`.

| Check | Result |
| --- | --- |
| `qualify.py --export-ref HEAD` | PASS, including bounded credential markers, exact export and complete native graph |
| `test-self-adoption.py` | 19 tests PASS, including Landscape corruption/removal, pin and route rejection/recovery |
| `test-distribution.py` | 52 tests PASS |
| `test-release.py --vibe <pinned-musl>` | 26 tests PASS, no optional native tests skipped |
| `test-chatgpt-projection.py` | 29 tests PASS |
| `test-publication.py` | 12 tests, PASS with one existing optional skip |
| `test-publication-dispatch.py` | 7 tests PASS |
| `package-release.py --source-ref <full-sha> --base <accepted-sha> --check-remote-tag` | PASS, package unchanged at 7.0.1 |
| `qualify-vibevm.py --vibe <pinned-musl> --materialize` | PASS, 7 native commands |
| `qualify-distribution.py --vibe <pinned-musl> --source-ref <full-sha>` | PASS, 21 native commands in disposable local Git transport |
| `qualify-toolchain.py --vibe <pinned-musl> --output <report>` | PASS: cold four-package resolution, projection, integrity, mismatch refusal, rollback and Git recovery |
| Clean accepted and candidate native offline `validate` / `check`, without install | PASS; identical 0 errors and 15 retained historical-slot warnings; clean tracked state |
| Public tags, frozen manifests, complete inventories and receipts | PASS; fresh public Git snapshots byte-match both committed slots |
| Full Instructions projector `check` | `NO_OP`, no diffs, Sources disabled; live Settings unverified |

Initial extended checks exposed two stale accepted test assumptions: native
qualification only recognized historical Governance slots and expected Relay
3.0.0, while the mismatch probe modified historical Governance 7.0.0 instead of
selected 7.0.1. The correction derives selected versions and historical top-level
slots from the actual lock/receipts. Unexpected warning kinds, severity, paths
and messages still fail; forced reinstall now rejects the deliberately corrupted
selected source with `lock_hash_mismatch`. This repairs false test failures
without changing package/runtime policy or adding operator work.
The first distribution probe also used `HEAD` where its existing interface
requires a full SHA; the corrected full-SHA invocation passed.

The [current native report](logs/toolchain.json) records four selected identities,
cold acquisition, 15 retained historical slots and expected negative exits.
[Public identity evidence](logs/public-identities.json) confirms model guidance
1.0.3 at `48432f00802f5aad106f3e1a9264e17c1edc354c` and subagents 1.0.2 at
`042e92884278d748502157945301dbc3f3c8318c`, including annotated tag objects.
Original distribution source disclosure stays opaque; receipt consistency is
not a claim about private producer history.

## Passive behavior and warning disposition

The complete installed policies, compact boots, authored root applicability and
the [Step 1 scenario matrix](../step-1/README.md#conditional-applicability-scenarios)
were reassessed against the recovered/current graph. With Landscape absent,
accepted boot has no Landscape route. With packages installed but recommendations
irrelevant, detail stays conditional. Subagents Off, task prohibitions, unavailable
tools and higher-priority limits prevent spawning. Substantial permitted work may
delegate useful independent assignments, with zero helpers still valid. New model
advice cannot substitute an admitted parent/child profile, establish eligibility,
launch nested Relay work or provide independent acceptance. One read-only helper
assisted this implementation assessment; it did not accept the result. No extra
live model/client probe is needed to qualify passive dependency installation.

- The original Step 1 child failure and Step 2 `COMMIT_OWNERSHIP_INVALID` remain
  immutable terminal failures. The current owner-authorized recovery verifies and
  reuses their source; it does not make those attempts green. Supported initial
  exact-head evidence included Step 1's terminal annotation. Original Step 2's
  complete native Outcome and accepted incident disposition were also inspected.
- The Step 2 GNU-binary weak `GLIBC_2.39` warning is avoided by the pinned musl
  binary in this fresh execution. All relevant native operations passed without
  that warning. No host library upgrade or protected permission change was needed.
- The 15 orphan-slot warnings are identical in accepted and candidate checkouts,
  exclusively intentional retained history, including old Relay 3.0.0. Preserve
  the slots; they neither add active dependency closure nor justify deleting history.
- Privileged installed-worker proof was not performed. This result is passive
  producer-source integration and manual qualification, not a runtime/PROD change;
  it claims no qualification of a new protected worker, sudo boundary, provider,
  Windows/macOS client injection or backend model identity.
- Complete Instructions remain byte-identical. No new replacement/application is
  caused by this integration. Earlier live-settings reconciliation gaps remain
  unresolved; `NO_OP` is not readback. Keep Task 96 open for independent exact-head
  acceptance, authorized integration and any outstanding completion obligations.
- UI-only GitHub service/pre-execution annotations are outside supported automated
  acquisition. The client confirms an abbreviated thread title only; exact full
  title persistence and actual backend profile/token telemetry are not claimed.

All logs below are bounded output from this execution's disposable qualification,
not protected original runtime streams. Native checks and helper evidence do not
constitute independent acceptance. The final manual Outcome belongs exclusively
on PR 97 through the admitted Writer transport.
