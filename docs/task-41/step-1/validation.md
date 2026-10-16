# Step 1 qualification

All checks here are contributor implementation evidence, not independent acceptance.
The single PR Outcome supplies the final remote head and primary exact-head CI.
No public release or real consumer migration was performed.

| Check | Result and primary evidence |
| --- | --- |
| Source and exact-commit export | [Log](logs/source-export.txt): PASS, including tracked bytes, local links, bounded secret markers, passive payload and complete source/registry/slot/receipt/lock/INDEX/agent consistency. This local run names committed `a23856c54481f8e57d9b0ebb00a3f55930c601c3` (619 files, 877 links), before later evidence-only additions. |
| Distribution regression | [Log](logs/distribution.txt): 42 PASS. New export/whole-version/guide-integrity checks reuse existing UTF-8, contained-link and passive-payload enforcement. Historical exports remain covered. |
| Self-adoption regression | [Log](logs/self-adoption.txt): 12 PASS, including clean ready checkout, missing/corrupt slot, metadata/lock/boot failures, regeneration and overlays. |
| ChatGPT regression | [Log](logs/chatgpt.txt): 24 PASS. Supported installed-tool [maintenance](logs/instructions-update.json) uses frozen accepted source `f67a29aeac6defef7220a169962bac611b6f8c79` and the Step 1 Decision. Instructions/effective content are `NO_OP`, Sources `DISABLED`; only receipt maintenance evidence changes. |
| Release regression | [Log](logs/release.txt): 10 executed PASS, six optional native publisher/dependency integrations SKIPPED. Publisher/resolver behavior is unchanged; skipped tests are not counted as passes. |
| Native producer | [Log](logs/native-producer.txt): pinned VibeVM 1.0.7 stages exact authored `226b88ab8b465e9edd509d2b7795cc2b68ada43b`, installs 2.7.0 from its isolated local registry and passes native check with zero findings, then exact producer integrity. The prior lock advances normally from 2.6.0, with no URL edits, force or integrity bypass. |
| Native fresh consumer | [Distribution log](logs/native-distribution.txt) and [installed route](logs/installed-methods.json): PASS. Actual independent ordinary consumer obtains complete payload and its relative guide route without the producer README, authoring tree or local instructions. No FPF client/server, connection or configuration participates. |
| Preserved accepted material | [Complete committed diff and Git-normalized blobs](logs/preservation.json): 173 protected files unchanged at `a23856c5…`, including nine protocols, onboarding guides, shared ChatGPT assets, all earlier native registry/slots, root/member agents, manual/self-adoption/release bindings, local Instructions/custom/binding, toolchain and workflows. The complete accepted compact-boot prefix is unchanged; one optional paragraph follows it. No accepted files are deleted. |
| Whole-package version and whitespace | Existing release-boundary check validates 2.6.0 → 2.7.0 MINOR against accepted/current main with `Package bump: minor`; final exact-head CI repeats it. Full/staged whitespace checks pass. |

The regression suites run in a clean native Linux clone after committing the
complete candidate projection. Native producer and distribution runs identify
the earlier authored commit; the exporter digest is unchanged by projection and
later evidence-only commits:
`4e3ca1fb4093bc14136c323deff7bfd64584159e6202470773bcde38f7e1d047`.
The final source check/CI binds that same payload to the handoff head rather than
pretending earlier logs ran at a later revision.

## Native scope and retained limitations

The existing disposable distribution probe executes 21 native commands over a
local Git remote: exact export, native publish/idempotence, cold/repeat and
independent installs, retained-slot offline reading, synthetic patch update and
complete Git rollback. The task-local [probe](probe-installed.py) verifies the
actual consumer AGENTS → INDEX → installed boot → engineering-methods route,
complete qualified files, nine protocols, passive manifest and preserved human
overlay. The guide is a conditional link, not an eager INDEX entry. This proves
native transport and static discoverability without MCP, not a live classifier,
model obedience, review quality or actual method application.

The pinned Linux x86_64 musl binary SHA-256 matches the accepted toolchain pin:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Its native install prunes earlier slots only in the disposable producer clone;
the source checkout retains every previously committed historical native file.
Generated absolute `file://` paths/timestamps are location metadata; exporter,
receipt and content checks establish identity.

The existing incident probe deliberately reproduces known upstream limits:
full-SHA `file://` archive acquisition and cache-only missing-slot recovery fail;
mutable-tag drift can split lock/slot identity, which canonical verification
rejects while `vibe check` alone misses it. INDEX remains static despite authored
dynamic linkage. These expected negative observations remain visible in the log;
they are not new guide regressions or newly qualified successful recovery.
No real remote tag is edited by this local probe.

Six optional native release integrations were not rerun. No consumer adoption,
live ChatGPT Instructions/Sources or GitHub settings/protection/credentials,
production, external repository or FPF service installation was changed.
Instructions retain 5,132 Unicode characters. Live model/client/settings and
runtime model/effort identity are unqualified; prior Windows CLI startup limits
are not retested. The bounded secret-marker scan is not proof of absence of all
secrets. Git normalization notices for new logs do not change the line-ending
policy; whitespace checks pass.

Contributor helpers checked reference accuracy, exporter/tests and the changed
prose. Their work is attributed implementation self-checking, not independent
acceptance. Persisted chat-title readback matches
`Task 41 — Step 1 — Expose optional FPF engineering methods`.
After one attributable English PR Outcome and verified publication, stop for
independent substantive exact-head assessment under the selected Direct strategy.
No self-approval, merge, release, Issue closure or further Step is authorized.
