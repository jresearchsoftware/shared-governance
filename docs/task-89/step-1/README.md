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

Native results and full validation will be recorded here before handoff.
