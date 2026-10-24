# Task 75 Step 3 — CR-75-002 reconciliation

Authority: [Task 75](https://github.com/jresearchsoftware/shared-governance/issues/75),
its trusted admission Decision and CR-75-002 on existing PR #77. Launch title:
“Task 75 — Step 3 — CR-75-002 — Reconcile RA-006 with accepted Development
Governance 5.2.1 as 5.2.2 and restore required checks”. Client title persistence
cannot be verified here. Accepted guidance remains frozen at
`2361868c41a916871d687aa8eea8f14573e2c82e`; the admitted reconciliation parent is
`80a088500d3944ad9b2391a56b16b949507a0070`. Candidate guidance remains proposed.

## Correction and preservation

Package bump: patch

Development Governance 5.2.1 → 5.2.2 preserves the published contract and operator
workflow. Only the reviewed 19-line RA-006 clarification, changelog addition and
manifest version change in the authored package. The complete accepted TH-029,
ChatGPT projector/base, SI opt-in topic/guide, other protocols and conditional
routes survive unchanged. This clarification creates no new operator work,
permission ritual, reviewer gate or state machine. The [incident/protected-operation
walks](../step-1/README.md#focused-scenario-walks) remain applicable. Task 68/PR 72,
Relay Task 182/189 and other consumers retain their own authority and history.

One bounded local merge preserves the reviewed task head as first parent and
exactly the admitted main as second parent. Conflicting 5.2.1 registry/slot files
and lock were resolved to accepted main; 5.2.1 is immutable. Earlier historical
slots, including the unselected Step 1 proposal, remain. Relay 3.0.0 and its Skill
projection retain their pinned identity. All task commits use the remediation bot.

The [PR description addendum](pr-body-addendum.md) is prepared for trusted Writer
application. It must replace any previous bump category/addendum, yielding exactly
one standalone recognized marker while preserving historical Task/Step/Outcome
correlation and result links. The worker cannot update live PR metadata, publish,
trigger CI, invoke review, integrate, release or close. A local file does not
prove that the live PR description or required event checks were corrected.

## Validation and handoff

Generation and exact-result evidence is recorded below after local qualification.
Fresh native exact-head CI, independent substantive review, safe integration and
ordinary accepted-source package-publication verification remain required through
their authorized actors. Root/sudo-only installed-runtime proof is reserved for
native CI; disposable projection is not that proof or independent acceptance.

### Generation and checks

Pinned VibeVM 1.0.7 musl matched the recorded SHA-256
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
The ordinary exact-Git exporter staged authored source. Native install used an
isolated configured local registry alongside the unchanged public Git-pinned Relay
root in `/tmp/task75-step3-native/workspace`. Before transfer the existing producer
verifier confirmed complete exact-source native parity. Only the generated 5.2.2
slot, root lock and root index were transferred; pruning in the disposable fixture
was not propagated to retained project history. Generated source URLs were not
hand-edited. All 47 selected public generated files were verified readable through
the existing work group. Group read was restored only on newly owned public files
where necessary; no host, private-file or repository-permission repair occurred.

Candidate `26c38e62d9b074170657b430b97bdce49d790d42` passed:

| Check | Evidence |
| --- | --- |
| `qualify.py --export-ref HEAD` | Exact authored export/registry/slot/lock/boot and pinned Relay Skill pass; bounded credential-marker scan passes |
| `test-distribution.py` | 52 tests pass |
| `test-release.py` | 12 pass; 6 optional one-time native integration tests skipped |
| `test-chatgpt-projection.py` | 29 tests pass |
| `test-publication.py` | 11 pass; 1 optional native integration test skipped |
| `test-self-adoption.py` in exact-commit bundle fixture | 17 tests pass |
| `package-release.py` against admitted main with prepared PR text | PATCH 5.2.1 → 5.2.2 passes, including the category and public-tag absence check at validation time |
| `git diff --check` against admitted main | Pass |
| Preservation and history inspection | Only three authored package paths differ; the 19-line RA correction matches Step 2 exactly; frozen 5.2.1 registry/slot, pinned Relay payload/Skill, generated Instructions and manual binding match admitted main; merge parents and bot identities match the admission |

The initial distribution run exposed Task 74's historical assertion incorrectly
requiring every future non-TH protocol to retain 5.2.0 bytes. It now checks that
preservation against Task 74's accepted 5.2.1 source, while separately requiring
current TH-029 to retain the complete accepted bytes. The successful rerun retains
all corruption/export/address and other historical-preservation checks; it does
not exempt the RA clarification from exact-source qualification or review.

Direct self-adoption fixture clones fail with exit 128 and Git's explicit dubious
ownership diagnosis for this shared checkout's `.git`. An ordinary bundle of the
same exact commit, cloned into a worker-owned disposable fixture, passed all 17
cases. No safe-directory, hooks, config, remotes or host permissions were changed.
This proves the fixture checks, not successful direct shared-checkout cloning.

Unprivileged native check reports zero errors and ten orphan-slot warnings for
retained 2.5.0, 2.6.0, 2.7.0, 3.0.0, 4.0.0, 5.0.0, 5.1.0, unselected proposed
5.1.1, 5.2.0 and now-unselected accepted 5.2.1. These are historical slots outside
selected routes; they remain intact and warnings are disclosed rather than
suppressed. No root-only installed-runtime proof was attempted.

### Effective Instructions and remaining work

The accepted projector reports `effective_content=NO_OP`, `instructions=NO_OP`,
`sources=DISABLED`, and `live_settings_verified=false` against this candidate.
Complete desired Instructions and the manual binding match admitted main byte for
byte. Task 75 therefore creates no additional changed-text application duty under
the preserved TH-029 trigger. Any earlier unresolved Task 74 live-settings mismatch
or verification gap remains with its existing obligation; this NO_OP does not
prove live synchronization or discharge that hold. No live Settings access is
available or claimed.

Trusted Writer must apply the prepared description to actual PR #77, retaining
historical correlation and precisely one category marker, and publish this result
through the existing handoff. Fresh candidate CI must bind that new exact head and
updated PR event metadata; the prior failed event is not corrective evidence.
Exact-head native proof and independent substantive review precede authorized
integration. The ordinary accepted-source publisher must then be verified before
whole-Task completion. No extra release permission is required by this PATCH,
and no external publication, Reviewer invocation or consumer migration occurred.

Task-owned work is committed. The sole remaining untracked path is pre-existing
`.codex-sandbox/`, owned by `nobody` and the existing work group, containing runtime
state rather than public Task source. It remains untouched. No useful task changes
are left uncommitted or hidden by new ignores. Final documentation-only evidence
updates receive exact-head qualification and whitespace checks before handoff.
