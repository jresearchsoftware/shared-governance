# Task 52 Step 1 — qualification record

Frozen accepted execution guidance:
`e654d9e20a7c42c50cc05786dc83a4f7a16f84e4`.
Candidate source, native outputs and semantic walks are implementation evidence;
independent exact-head review remains pending.

## Identity and native generation

2026-10-20, Windows PowerShell/Python 3.12 and disposable Debian WSL native
filesystem/Python 3.11.2. Authored candidate:
`dc0f04246de155a2e07cd1fd5eafb434ff418716`; native materialization committed in
`e75eb9f381981e0d1e3f98ae101ad2ad8fe0da6b`. Receipt-only correction:
`9c632fabdd9435b6dedde8a7453dfe37116da48b`. Later evidence-only commits do not
change the qualified package payload. The canonical Outcome binds final head/CI.

Used the retained musl VibeVM **1.0.7** binary; live SHA-256 matched
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`
from `toolchain/vibevm.json`. In a disposable native clone:

```sh
python3 scripts/prepare-distribution.py --source-ref dc0f04246de155a2e07cd1fd5eafb434ff418716 --producer-source
vibe install --offline --registry vibevm/vibepacks --assume-yes
```

Isolated VibeVM settings were used. Native resolution moved the exact dependency
3.0.0 → 4.0.0 and regenerated boot for both workspace nodes. Export reported
20 payload files, digest
`8af5b949fd0f5ebeb435d838b41f5a21fad09a5b005ea267fecba20b7c2440cf`.
VibeVM pruned stale slots in the disposable clone; restored the tracked historical
2.5.0/2.6.0/2.7.0/3.0.0 slots from its unchanged Git baseline. Copied only the
new 4.0.0 registry source/slot, lock and generated indexes back to the authoring
checkout. No old package bytes were edited or removed. Generated absolute
`source_url` is native metadata, not an acceptance pin or portable source proof;
canonical export/source/slot comparison passed on both operating systems.

The committed address test verifies all prior PC/IR anchors, unique PC-013
ownership, byte-identical earlier PC rules and all seven unaffected protocols
against accepted 3.0.0. Existing payload/link/export checks validate actual
materialization and routing, not a second resolver or semantic classifier.

## Executed checks

Debian checks at materialized `e75eb9f38`, with ChatGPT/producer/source checks
completed at receipt-corrected `9c632fabd`:

| Command | Observed result / retained evidence |
| --- | --- |
| `git diff --check origin/main HEAD` | PASS, no whitespace errors. |
| `python scripts/qualify.py --export-ref HEAD` (Windows and Debian) | PASS: canonical flow export/native projection, bounded credential markers, local links and retained frozen source; [source log](logs/source-final.log). |
| `python scripts/package-release.py --source-ref HEAD --base origin/main --pr-body-file <body>` | PASS: accepted 3.0.0 → candidate 4.0.0, category major; current main verified still e654d9e20. Numeric/category check is evidence, not independent semantic category acceptance. |
| `python3 scripts/test-distribution.py` | **48 passed**, zero skipped; [log](logs/distribution.log). Includes actual export, anchor/reference ownership, preservation and negative integrity cases. |
| `python3 scripts/test-release.py` | **11 passed, 6 optional native tests skipped**; [log](logs/release.log). Package reuse/category/readiness/source boundaries pass. |
| `python3 scripts/test-self-adoption.py` | **13 passed**, zero skipped; [log](logs/self-adoption.log). Clean-checkout native availability, corruption/lock/index detection and recovery. |
| `python3 scripts/test-chatgpt-projection.py` | **24 passed**, zero skipped after receipt refresh; [final log](logs/chatgpt-final.log). |
| `python3 scripts/test-publication.py` | **10 passed, 1 optional native test skipped**; [log](logs/producer.log). Existing producer integration unchanged. |
| Disposable local Git positive blocker control | PASS: non-force push rejects changed frozen tag, forced variant replaces it; [observations](logs/positive-control.log). No public remote or actual publisher modification. |
| S1–S9 in [coverage/scenarios](README.md#authoring-regression-walks) | Nine authoring walks PASS under written candidate rules; not model executions. |

Debian unit-suite total: **106 passed, 7 explicitly skipped**, no remaining
failures. Native publisher/transport/dependency integration was not rerun: those
mechanics are unchanged, and the relevant changed native materialization/export
was executed directly. This Step neither bypasses nor manually triggers the
active publisher. Existing PR CI may run its normal unprivileged fixtures.

## Correction and evidence limits

The first ChatGPT suite had one real failure:
[initial log](logs/chatgpt.log). Bumping the whole package changed the projector's
version metadata, but the existing receipt still recorded tool 3.0.0. Used the
unchanged projector's supported `update` with the **frozen accepted** SHA
`e654d9e20a7c42c50cc05786dc83a4f7a16f84e4` and Task #52 admission URL. It reported
`effective_content=NO_OP`, `instructions=NO_OP`, `maintenance_evidence=CHANGED`.
The refreshed receipt records candidate tool 4.0.0 while its guidance snapshot
remains independently accepted 3.0.0. No candidate SHA was labeled accepted;
Instructions/custom/binding and shared client tool bytes stayed unchanged.
No live settings were applied or inspected. Final suite passed after this repair.

The S4 fixture is an intentionally unsafe alternative, not a security defect
found in the accepted publisher. S5 is a credible supplied disclosure scenario,
not a real private-data incident. Desk checks and structural tests do not prove
fresh model adherence, native reviewer identity, all-secret absence, legal
correctness, live publication or consumer migration. Live settings remain
unverified. CI and implementer checks cannot accept the candidate.

No merge, source-main integration, public distribution/tag write, consumer,
Relay/Landscape, credential/settings mutation or Task closure was performed.
Independent exact-head substantive review (including truthful SemVer category)
remains the next boundary. The Step's one canonical Outcome is on PR #56;
verified Outcome precedes Ready under the accepted local binding.
