# Task 32 Step 6: locked-slot INDEX membership

[Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6193249773)
admits this bounded correction on [PR 33](https://github.com/jresearchsoftware/shared-governance/pull/33),
starting at `d560862527859144d69bddd89db51a7882f87517`. The independently accepted
source-main remains frozen at `15e8191435a126e54b4d1739a73fab112e01c081`.
The complete Task chronology, five prior Outcomes and five independent
non-approving assessments were read. The [Step 5 finding](https://github.com/jresearchsoftware/shared-governance/pull/33#pullrequestreview-5531720879)
is correction evidence, not acceptance of the candidate architecture.

## Correction and bounded semantics

The shared [projector](../../../../packages/development-governance/tools/chatgpt/project.py)
previously verified receipt-declared hashes but accepted an INDEX path based on
its locked directory prefix alone. A committed extra file inside that slot could
therefore become a route despite being absent from its receipt. This was a
validator defect; no corruption of the shipped producer slot is alleged.

`native_inventory()` now retains the validated full file paths separately for
each locked slot. An INDEX entry within a materialized slot must both belong to
the native lock and appear in that exact slot's receipt. Existing lock identity,
ordinary committed blob, safe-path and SHA-256 checks remain. Entry order and
conditions are preserved without evaluation, resolution or topic adoption.
Unreferenced extra files are still inventoried; this change does not claim
receipt completeness for every file throughout a slot.

This directly enforces the admitted native-route invariant, with a set lookup
and no new operator command, prerequisite, service or authority mechanism.
Whole-package **2.3.0 remains the same unpublished, unaccepted candidate**;
the existing PR's minor transition from accepted 2.2.0 is retained. Native
registry/slot/lock regeneration uses the existing pinned VibeVM 1.0.7 path.
Accepted 2.2.0 guidance continues to govern this execution.

## Regression and preservation

The focused [real-Git/exported-tool test](../../../../scripts/test-chatgpt-projection.py)
first accepts a receipt-declared route. It then commits an extra file inside the
same locked slot and references it from a conditional INDEX entry. Another
locked slot declares the same relative filename, proving that its receipt cannot
authorize the first slot's file. Both the exported CLI and in-process projection
must refuse it; failed CLI update preserves the existing generated/custom files.

- [Before correction](logs/regression-before.txt): the new test fails because
  the old exported CLI returns success for the unreceipted route.
- [After correction](logs/regression-after.txt): the same test passes.
- [Lifecycle suite](logs/projection.txt): 23 tests pass, retaining unlocked-slot,
  corruption, lock/slot mismatch, conditional order, producer workflow and
  non-adopting consumer cases alongside the new regression.

The common governance-neutral base, project custom/binding data, generated
Instructions, optional Sources and owner-only live application remain intact.
Producer Instructions are unchanged (5,132 Unicode characters); their receipt
records this Step's Decision and corrected tool identity. Step 1-5 historical
artifacts, including the historical Relay preview receipt, retain their original
bytes at the final result. Earlier tool identities remain historical evidence.

[Authority snapshot](evidence/authority.json), [native installation](logs/native-install.txt)
and [installed-tool check](logs/installed-producer-check.json) support local
reproduction. Final exact-head source/export, suite results, CI job/check and
warning evidence are bound in this Step's canonical PR Outcome. All executor
checks are self-check evidence, not independent acceptance.

## Remaining boundary

Stop for independent substantive **NON-APPROVING Deliberative review** of the
final head and owner disposition. Task 32 and PR 33 stay open. No merge, release,
external consumer change, live Instructions/Sources edit or upload, new topic
adoption, settings/profile change, deployment, credential mutation, later Step
launch or closure is authorized. Live ChatGPT loading, settings readback,
Sources addressability, model behavior and reliability remain unqualified.
