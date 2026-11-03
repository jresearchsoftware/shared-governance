# Task 89 Step 1 — producer VibeVM 1.0.11

Authority: [Task 89](https://github.com/jresearchsoftware/shared-governance/issues/89),
Manual Codex Step 1, Direct acceptance. Accepted guidance stays frozen at
`5011228ec6706c6e0c51c7cbadff699590dc6115` throughout this effort.
This is executor qualification, not independent acceptance.

The producer pin moves to verified VibeVM 1.0.11 at
`5e470926ad0f34d61e37d387ce4b7c153356a804`, release `432408525`.
The mutable release API, tag and downloaded distribution manifest agree on source
and distribution identities. Downloaded manifest, musl/GNU bootstrap executables
and GNU archive match the API digests in [the pin](../../../toolchain/vibevm.json).

The temporary Task 87 identity mapping and active `--git-compat` wiring are
removed. The existing toolchain probe now isolates home/settings/cache, records
cold Git clone commands and verifies actual cache origins remain the original
GitHub URL. It rejects raw-file-host Git traffic and checks unchanged selected
versions/content hashes, native routing/projection and historical slot bytes.
[Dated Task 87 evidence](../../task-87/step-1/README.md) retains its historical
workaround and tested limitations; its removed-file link targets accepted history.

## Observed result

The [native report](native-qualification.json) records nine native commands,
including two expected refusals. Fresh resolution removed the copied lock and
both selected slots, with empty isolated home/settings and no remap. Git trace
records a real clone of `https://github.com/jrs-vibevm/org.jresearch.ai.codex-relay.git`;
its new cache has that exact `remote.origin.url`, with no raw-host Git request.

| Selection | Version | Content hash |
| --- | --- | --- |
| Development Governance | 7.0.0 | `sha256:5ce5f41aa48aa0604fc5f04e76e5b29cc5134d51b848b4be327ee7e621cd0b22` |
| Codex Relay | 3.0.0 | `sha256:451ee21dbfd63abd7918f0aee979220fb57cb8a8dffde20009a25f11bf9071e7` |

Relay remains pinned to `325c96371783e2d628bfa9903b3244468c688fe6`.
Canonical producer verification checks actual selected source/slot/receipt bytes,
lock identities, native INDEX/AGENTS routes and the projected Relay Skill.
Listing, projection dry-run and real projection pass. All 13 historical slots
retain their bytes. Native check reports only their 13 expected orphan warnings.
The generated diff is solely six lines of incidental lock metadata; it is not
imported. The committed lock, ready files, frozen export and immutable Relay
content remain unchanged, with no package bump or publication needed.

Forced offline reinstall refuses changed source with `lock_hash_mismatch` and
leaves project state unchanged. Ordinary Git restoration recovers the complete
committed project; retained-slot offline rebuild passes. Late static compilation
failure names `STATIC.xml` and rolls back manifest, lock, slots and boot, excluding
operational `.vibe/` journals. The distribution incident probe retains native
`lock_slot_hash` detection and canonical corruption rejection, cold/repeat local
Git transport, immutable payload/license verification, synthetic update and Git
rollback. No integrity bypass or replacement remap is introduced.

Complete effective `chatgpt/instructions.md` and its generation inputs remain
unchanged: 6963 bytes, SHA-256
`499a9c3116f58e3ec560f4ee2977e33dcaeb90dcc66132811c686e74f7060c0a`.
This creates no new Settings Apply obligation and makes no live Settings parity
claim; earlier reconciliation history is not discharged.

## Validation and reproduction

Executed on Debian WSL2 with native `/tmp` storage, Python 3.11.2 and Git 2.39.5.
All functional probes use the digest-verified musl executable. The
[release verification](release-verification.json) records downloaded asset IDs,
API/download digest agreement, manifest identities and GNU archive/executable
agreement. The upstream [remap repair](https://github.com/vibevm/vibevm/commit/756027375f041f84e9e47d83e1ea0b1245fc318c)
limits built-in rows to `RawFile`. Other 1.0.11 changes concern application-step
interrupt handling and documentation container builds; this passive producer
uses neither surface and adopts no application feature.

[Validation results](validation-results.json) bind native runs to implementation
`521909b5aa84ddbaf404f92f089f0453c58a4aa7`. Later changes document evidence and
clarify active prose only; the tested executable pin and probe code are identical.
Public candidate CI and the terminal Outcome bind the final pushed head.

| Probe | Observed result |
| --- | --- |
| Source/export and canonical native producer verification | PASS |
| Distribution regression suite | 52 tests passed |
| Release with native tool | 26 tests passed |
| Self-adoption | 17 tests passed |
| ChatGPT projection | 29 tests passed |
| Producer publication with native tool | 12 tests passed |
| Shared Publisher with native tool | 101 tests passed |
| Authoring with registry materialization | PASS, 7 commands |
| Distribution native integration | PASS, 21 commands |
| Native ChatGPT synthetic install/update | PASS, custom preserved, non-adopting negative passed |
| Mixed graph, Skill, integrity refusal, rollback and recovery | PASS, full report linked above |
| Path-source diagnostic | Expected nonzero `empty world / ORDER-LAW` limitation reproduced |

The six suites total 237 tests, no skips or failures. Ordinary CI may omit the
optional native integrations; those were exercised separately here. Reproduce
with the commands in `validation-results.json` and the toolchain probe:

```sh
python3 scripts/qualify-toolchain.py --vibe /absolute/path/to/verified/musl/vibe --output /tmp/toolchain-qualification.json
python3 scripts/package-release.py --source-ref HEAD --base origin/main --check-remote-tag
git diff --check origin/main HEAD
```

No real publication destination, token, consumer migration or live Settings write
is used. These are bounded upgrade probes, not new recurring release gates.

## Warnings and review boundary

- The 13 historical orphan-slot warnings remain expected retained history, not
  active guidance. No historical payload is deleted or silently adopted.
- Missing-remote cache-only recovery remains unavailable; committed-state Git
  restoration and retained-slot rebuild pass. This is the same bounded limitation
  as Task 87, not a newly promised recovery path.
- Path-source authoring still hits `ORDER-LAW`; the supported isolated registry
  workflow passes. No replacement resolver or extra operator step is added.
- GNU `--version` returns 0 but emits the existing weak `GLIBC_2.39` warning on
  Debian. Functional qualification uses musl. Windows/macOS runtime and fresh
  model/client behavior were not requalified; Linux CLI evidence does not prove them.
- The release remains mutable. Exact source, asset IDs and SHA-256 pins protect
  subsequent downloads from silently changed bytes.

The toolchain-only completing PR may carry `Closes #89` under the charter.
Independent exact-head acceptance and owner-authorized merge remain outstanding;
this executor performs no self-approval, merge, release or Issue closure.
