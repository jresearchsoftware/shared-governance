# Task 74 — Step 2 — CR-74-001

Implement owner-selected PATCH 5.2.1 reclassification for the restored
effective-Instructions closure rule.

## Authority and retained history

The [superseding Task 74 Decision](https://github.com/jresearchsoftware/shared-governance/issues/74#issuecomment-6386467528)
and CR-74-001 authorize this automatic remediation on the existing result PR #78.
The admitted launch supplies Step 2; the earlier manual execution is not replayed.
Execution guidance remains frozen at accepted
`414077e956aa47b18ddc436f68c3245b508baf46`. The admitted release baseline is
`1121fc8966a2c7142cc0d6067eff0cf1d15e9cd9`, Development Governance 5.2.0,
already an ancestor of starting head `1ef35714d3a739e8d36ceb17b6aee214c39376d0`.
No additional base merge is needed. Current main must be checked again by the
authorized integration path; this worker has no GitHub credential or publication authority.

The owner identifies the effective-text duty as the originally intended
requirement narrowed during translation into Task 62/PR 63. Accepted 5.2.0
expressly documented the narrower explicit-application condition. Restoring the
intended duty changes the published consumer workflow and ordinarily requires
MAJOR under PV-002. The owner expressly selects 5.2.0 -> 5.2.1 PATCH for this one
correction. General PV-002 remains unchanged, and this does not claim unchanged
consumer-facing behavior or retroactive invalidity of earlier acceptance.

The dated [Step 1 record](../step-1/README.md), its original manual admission,
Outcome and qualification remain historical evidence under then-current authority.
Its prospective-policy/MAJOR classification is superseded by the later Decision.
The 6.0.0 artifacts were an unaccepted candidate, not a frozen release; only those
superseded generated artifacts are removed. Frozen historical packages and other
Tasks' evidence remain unchanged. The [replacement PR description](pr-description.md)
is prepared for authorized Writer publication; this worker does not edit GitHub.

## Bounded result

Retain the complete Step 1 TH-029 rule, client generator/base, manual binding,
operator examples and desired Instructions. A Task changing its adopting project's
effective complete Instructions text must reconcile live Settings after accepted
integration, regardless of a missing application clause. Full raw Markdown replacement,
owner review/manual application preserving unknown live rules, supported readback
or attributable live-content confirmation, concrete evidence gaps and ordinary
already-authorized closure remain intact. No-op/cache/SHA-only changes create no
new application duty and do not erase an earlier mismatch.

Retarget the whole package, root requirement, selected native registry/slot/lock
and boot route to 5.2.1 through exact Git export and pinned native VibeVM generation.
Keep Relay 3.0.0, its immutable public source, projected Skill and inert closure.
Keep general RA/PV rules and the other nine protocols. Other consumers must
intentionally update/adopt under their own authority; this producer's candidate
neither migrates them nor applies their Settings.

## Qualification and completion boundary

Source/CI checks establish content and native integrity, not real owner UI activity.
Step 2 changes no effective Instructions text relative to Step 1, but Task 74's
change relative to accepted 5.2.0 and its unresolved live-settings gap remain.
Independent exact-head assessment, integration and owner-controlled live
reconciliation are still required. The automatic worker hands ordinary local
commits to Writer; publication, native exact-head CI, independent acceptance,
merge, release, live Settings mutation and Task closure are not worker actions.

The complete implementation and native projection were qualified at
`733080319b8486e9fd071279a91c74e44d312995`; subsequent evidence-only additions do
not change that package, generated projection, Instructions or test code.

| Check | Result and evidence |
| --- | --- |
| Exact source/export/native parity | PASS: 1,105 tracked files, 2,396 local links, bounded credential-marker scan, all 10 protocols, Relay 3.0.0. [Output](logs/source.log) |
| Distribution | 52 tests PASS, including retained historical transitions and the bounded current TH-029 comparison. [Output](logs/distribution.log) |
| Release | 18 tests PASS, no skips, with the hash-verified pinned VibeVM 1.0.7 musl binary. Includes the new unaccepted-candidate reclassification fixture, unchanged arithmetic and immutable-publication checks, and local native publication/dependency fixtures. [Output](logs/release.log) |
| Self-adoption | 17 tests PASS, including corruption, source/slot/lock/boot mismatches, clean checkout, native Skill and inert closure. [Output](logs/self-adoption.log) |
| ChatGPT projection | 29 tests PASS: base/custom changes, same-text dependency/binding changes, cache/no-op, inaccessible live Settings, full raw/fenced owner-export comparison and retained earlier gaps. Export equality does not simulate live UI proof. [Output](logs/chatgpt.log) |
| Native ChatGPT lifecycle | PASS: install 5.2.1, synthetic update to 5.2.2, preserved custom text and non-adopting consumer. Local disposable consumer only. [Output](logs/chatgpt-native.log) |
| Producer publication regressions | 11 PASS, one optional native fixture SKIP (12 total). No production publication. [Output](logs/publication.log) |
| Actual PATCH transition and registration | PASS: 5.2.0 -> 5.2.1 with the replacement PR body's single PATCH line and unauthenticated public tag lookup; no existing v5.2.1 tag at this check. Recheck mutable main/tag facts before integration/publication. [Output](logs/transition.json) |
| Scope and history | PASS: only authored manifest/changelog differ from Step 1's package; TH-029, generator/base, local manual binding and Instructions are byte-identical. General PV/RA and all accepted historical source/slots plus Relay remain unchanged. Only superseded unaccepted 6.0.0 outputs are absent. [Output](logs/preservation.json) |
| Whitespace | `git diff --check 1121fc8966a2c7142cc0d6067eff0cf1d15e9cd9 HEAD`: PASS. |

The accepted-source-bound producer check was:

```sh
python3 scripts/project-chatgpt.py check --repository . --binding chatgpt/binding.json --accepted-sha 414077e956aa47b18ddc436f68c3245b508baf46 --authority-anchor https://github.com/jresearchsoftware/shared-governance/issues/74
```

It returned `effective_content=NO_OP`, `instructions=NO_OP`, `sources=DISABLED`,
`live_settings_verified=false`, explicitly retaining the earlier reconciliation
obligation. No Settings readback or owner application was available or claimed.

## Native preparation and execution limitations

Commit authored source before `prepare-distribution.py --source-ref <full-SHA>
--producer-source`. Follow [the mixed-source native procedure](../../relay-skill.md#maintenance-and-rollback)
with a run-specific local registry/settings directory and unchanged public Relay
root. Pinned native install selected 5.2.1, regenerated root/member boot and
retained Relay 3.0.0; [native output](logs/native-install.log) records it. Transfer
only selected output because VibeVM prunes historical slots in disposable staging.
Full native parity also passed in the actual governed checkout after transfer.
Generated identity fields were not edited. The initial exporter invocation with
symbolic `HEAD` was rejected before staging; the corrected invocation used the full
source SHA as required. A staging extraction helper also encountered this Python
3.11 build's unsupported `tarfile` filter argument before extracting files; bounded
ordinary-file extraction of the same local Git archive completed preparation.

Initial tests exposed execution-layout restrictions, not candidate failures:
the exporter rejects destinations within its authoring source, and Git's local
clone rejected the shared checkout's different ownership as `dubious ownership`.
No Git trust configuration, ownership, permissions or test expectations were
relaxed. An ordinary Git bundle supplied the exact same committed objects to an
owned disposable qualification checkout inside this execution's ignored `.vibe`
directory. Its scratch directories were siblings, outside that fixture's source
root. The four affected suites then passed unchanged. Release/publication tests
passed from the actual governed checkout with disposable local repositories.
All checks were unprivileged; local fixture publication touched only disposable
file remotes. Root/sudo-only installed-runtime proof was not attempted and remains
with native Exact-head CI after Writer publication.

The worker checked actual work-group readability of new public source/slot files
and root/member boot indexes after generation and transfer. Existing root Skill
files required no replacement and remained byte-identical. The launcher's
pre-existing, untracked `.codex-sandbox/` is not task source and is left untouched;
generated test staging is confined to the already ignored `.vibe/` directory.
Task-owned source and qualification evidence are preserved in ordinary commits
using the supplied remediation bot identity. This record supplies executor evidence,
not independent acceptance or a Writer Outcome.
