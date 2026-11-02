# Validation evidence — 2026-11-02

Executed on Debian WSL2, native `/tmp` filesystem, Python 3.11.2 and Git 2.39.5.
The verified musl VibeVM SHA-256 is recorded in the pin and native report.

| Probe | Observed result | Tested source/input |
| --- | --- | --- |
| Authoring with `--materialize` | PASS, 7 commands | `1e526688feedcc0383529185fd5ded61bd45485b` |
| Distribution native integration | PASS, 21 commands | `1e526688feedcc0383529185fd5ded61bd45485b` |
| Native ChatGPT install/update lifecycle | PASS, custom preserved, non-adopting negative passed | `1e526688feedcc0383529185fd5ded61bd45485b` |
| Shared Publisher with `--vibe` | 101 tests passed, no skips | `1e526688feedcc0383529185fd5ded61bd45485b` |
| Release with `--vibe` | 26 tests passed, no skips | `1abc63fc3ce3e2e54cbec626177301b2918df6ea`; release code and pin identical to final implementation |
| Mixed graph, missing selected slots, Skill projection, recovery | PASS, 9 native commands including 2 expected refusals | `1bce78b5dea24388687e21671221a5dcf8a6a99b`; full report alongside this file |
| Distribution regression suite | 52 tests passed | `1bce78b5dea24388687e21671221a5dcf8a6a99b` |
| Self-adoption regression suite | 17 tests passed | same implementation revision |
| ChatGPT projection regression suite | 29 tests passed | same implementation revision |

The later qualification-report commits change evidence only. Public candidate
checks and the single terminal executor Outcome bind the final published head.
No native integration used a real distribution destination or publication token.
The raw mixed-graph report records native stdout/stderr and expected failure codes;
canonical byte checks and tree-equality assertions also passed in that probe.

Warnings are bounded and retained: 13 historical unselected-slot warnings; the
upstream Git-origin remap defect requires the owner-approved staging row;
cache-only recovery cannot replace an unavailable source manifest. GNU `--version`
emits a weak `GLIBC_2.39` warning on this host; functional qualification uses musl.
Windows/macOS and fresh model/client execution were not requalified. These probes
do not establish independent acceptance, live ChatGPT Settings parity, package
publication, deployed Relay compatibility or Task closure.
