# Task 62 — Step 2: content generation without a projection receipt

Authority: [charter and owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/62#issuecomment-6319169919),
superseded for receipt retention by the explicit
[consolidated correction Decision](https://github.com/jresearchsoftware/shared-governance/pull/63#issuecomment-6322278504),
and the owner's Step 2 execution prompt. [Step 1](../step-1/README.md) and its
schema-3 rationale remain historical, not the current design. This Step continues
PR 63 from `e6e4e673ad4bdf093ecdcf7fe88723aec515f092` under frozen accepted
source-main `61aa3444365b02a27c392d48aa9ea33e85c5d5d4`.
Task 60 has [separate Step 2 coverage](../../task-60/step-2/README.md).

The owner declined local generated-edit protection as a requirement. The common
projector therefore returns only deterministic content outputs. It neither reads
nor creates ChatGPT receipts, migrates schemas, checks output ownership hashes,
nor reports receipt-only stale/change status. The producer's tracked receipt is
deleted. No registry, journal, replacement hashes or clean-worktree gate is added.
Consumer adoption removes its old tracked receipt once in the normal adoption PR;
the tool does not process it. Native VibeVM `.vibe-slot.toml`, lock hashes and
optional Sources snapshot provenance are distinct preserved contracts.

Check compares Instructions and optional Sources content without writing. Update
regenerates changed output, including local generated edits. Disabled cache
removes only the two known optional files, including edited or empty files;
unrelated files remain. All local paths are validated before writes/deletes.
Normal Git review owns useful changes and rollback. Every check/update still
requires an explicit accepted SHA and authority anchor, reads ordinary committed
source, and verifies native INDEX/lock/slot identity, hashes and route declaration.
No circular containing-commit identity or metadata upkeep is required.

Status schema 4 removes `maintenance_evidence`. With changed Instructions,
`application` says generation creates no Settings duty and explains the manual
application/confirmation requirement only for a Task that includes applying
changed Instructions. NO_OP and cache-only changes say unchanged Instructions
need no new application, without dismissing an earlier live-verification gap.
The tool cannot know Task scope or verify live Settings; it always reports
`live_settings_verified=false`. TH-029 and desired/live-state separation remain.

| Case | Expected result |
| --- | --- |
| First generation, edited output, changed custom/base/binding | Read-only stale/diff; explicit update writes deterministic content without ownership gates. |
| Same-output source/tool/dependency or containing-commit change | NO_OP; no receipt or new Settings action. Accepted-source/native validation still runs. |
| Optional cache enabled/changed/disabled | Content-based diff/update/removal of fixed cache outputs; unchanged Instructions add no application duty. |
| Changed Instructions in a generation-only Task | No live application obligation; only a separately included application scope requires owner action and supported confirmation/readback. |
| Bad SHA/authority, native corruption, unsafe local path | Refuse before output mutation; receipt removal does not remove these protections. |
| Owner export comparison | Read-only exact text comparison; cannot prove current live UI or automatic synchronization. |

Landscape recovery remains a recommendation only. Preserve the Step 1 recorded
closure disposition; do not reopen or reapply for historical receipt metadata.
Any future separately authorized adoption of the new release removes that old
receipt and regenerates in the same ordinary reviewed PR. Until then its pinned
4.0.0 behavior remains unchanged. No consumer-specific generator, downstream
source change or live Settings mutation is performed here.

One whole-package MAJOR remains proposed 5.0.0: receipt/API/status removal is a
breaking interface change; the conditional Task workflow also changes the contract.
The same unaccepted version can be refined before acceptance. Frozen 4.0.0 and
publisher workflows remain unchanged. See [qualification](validation.md).
