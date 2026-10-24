# Task 75 Step 2 — CR-75-001 reconciliation

Authority: [Task 75](https://github.com/jresearchsoftware/shared-governance/issues/75),
its trusted admission Decision and CR-75-001 on existing PR #77. This launch is
“Task 75 — Step 2 — CR-75-001 — Bring Task 75 RA-006 correction onto published
5.2.0 baseline and restore required checks”. No title tool is available to verify
persisted client navigation. Accepted guidance remains frozen at
`2361868c41a916871d687aa8eea8f14573e2c82e`; the admitted reconciliation parent is
`1121fc8966a2c7142cc0d6067eff0cf1d15e9cd9`. Candidate guidance is proposed data.

## Correction and coverage

Package bump: patch

5.2.0 → 5.2.1 carries forward the reviewed RA-006 clarification unchanged. It
makes the existing authority rule explicit for binding prohibitions, preserving
ordinary delegated means and actual protected boundaries. It adds no mandatory
operator action, review gate, permission ritual or state machine. The complete
[Step 1 incident and protected-operation scenarios](../step-1/README.md#focused-scenario-walks)
remain applicable; its 5.1.1 selection and checks are historical, superseded by
this reconciliation. Task 68/PR 72 and other consumer work remain untouched.

The one local merge preserves the previous task head as first parent and exactly
the admitted main as second parent. All new commits use the supplied remediation
bot identity. Against admitted main, the only authored package changes are the
19-line RA-006 clarification, changelog entry and manifest version. All nine
other complete protocols, Small Improvements guide, conditional boot and package
README retain exact 5.2.0 bytes. SI remains separately opt-in and unadopted by this
producer/Relay Skill. Accepted 5.2.0 registry/slot, earlier retained history and
public Relay 3.0.0 slot/Skill remain unchanged; the unselected Step 1 5.1.1 proposal
is retained as well.

The SI distribution regression now binds its historical preservation assertion to
the accepted SI release, rather than requiring future authorized package changes
to leave RA forever unchanged. Its current-export completeness, corruption,
rule-ID, route and frozen-version retrofit checks remain active.

[PR body addendum](pr-body-addendum.md) supplies exactly one recognized standalone
`Package bump: patch` marker and the contract/operator-work explanation. The
trusted Writer must apply this to PR #77 while retaining its original correlation
and historical result links; this worker cannot edit/read authenticated PR metadata.
The local release check accepts the prepared text. The live PR body is not claimed
corrected by a repository file alone.

## Native generation and validation

Pinned VibeVM 1.0.7 musl SHA-256 matched
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
The existing exact-Git exporter staged authored source. Native install ran in a
disposable archive fixture under `/tmp/task75-run40105700587/`, with isolated
settings and a configured local source registry. It selected Shared 5.2.1 and the
unchanged public Git-pinned Relay 3.0.0, verified the complete native projection,
and transferred only the selected Shared slot, lock and root index. Generated
identities/URLs were not hand-edited; retained project history was not pruned.

The direct `--registry` override initially bypassed the mixed graph's Git source
and failed Relay resolution. A disposable registry-copy probe confirmed that
route's wrong source kind; it was discarded. Ordinary configured-registry
resolution restored the correct public immutable Git source and content hash.
Only verified outputs reached the project. No credentials or global configuration
were changed. The native tool created its new public slot receipt with mode 0600;
work-group read was restored only on that worker-owned generated public file.

Candidate `f96a1046980f4f6c1ca2a121b879b578ad0a1926` passed:

| Check | Result |
| --- | --- |
| qualify.py --export-ref HEAD | Exact source/export/native parity passed, including Relay Skill |
| test-distribution.py | 51 passed |
| test-release.py | 11 passed; 6 optional native integration tests skipped |
| test-chatgpt-projection.py | 28 passed |
| test-publication.py | 11 passed; 1 optional native integration test skipped |
| test-self-adoption.py in exact-commit bundle fixture | 17 passed |
| package-release.py against admitted main, with prepared PR body | PATCH 5.2.0 → 5.2.1 passed |
| git diff --check against admitted main | Passed |

The self-adoption suite cannot clone directly from this shared checkout because
Git rejects its ownership (exit 128). An ordinary Git bundle of the same exact
commit was cloned into a worker-owned disposable qualification fixture; all 17
tests passed there without changing safe-directory, repository configuration or
host permissions. This distinguishes fixture proof from the unavailable direct
shared-checkout invocation. Final exact-head qualification follows this evidence
update; it does not alter package bytes.

Unprivileged native `check` reports zero errors and nine orphan-slot warnings:
retained 2.5.0, 2.6.0, 2.7.0, 3.0.0, 4.0.0, 5.0.0, 5.1.0, Step 1's unselected
5.1.1 and now-inactive 5.2.0. They are preserved history outside selected routes;
no warning is suppressed or treated as proof of missing content.

## Handoff boundaries

Local implementation and task-owned commits are complete. The trusted Writer
owns publication and the PR metadata update; current CI/remote mergeability,
root-only installed-runtime proof, fresh independent exact-head review,
integration and ordinary accepted-source package-publication verification remain
with their authorized actors. No push, external publication, review invocation,
merge, Issue closure or consumer adoption occurred here. Passing local checks
is not acceptance or whole-Task completion.

The only remaining untracked checkout path is the pre-existing runtime
`.codex-sandbox/`, owned by nobody and the existing work group. It is not public
task source and remains untouched; no task-generated residue is hidden or committed.
