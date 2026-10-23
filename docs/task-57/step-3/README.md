# Task 57 Step 3: native Relay 3.0.0 consumer

Authority: [Step 3 Decision](https://github.com/jresearchsoftware/shared-governance/issues/57#issuecomment-6367694493).
Frozen independently accepted source: `d0971c4d6c5a9b39f8caa1ec1538077a46271bf5`.
Earlier Step 1/2 Outcomes remain historical; merged PR 48 is the workflow baseline.
PR 64 remains an untouched Draft fallback. This source result requires independent
exact-head review; it grants no merge, runtime execution or Task closure authority.

## Bounded coverage

| Obligation | Result / evidence |
| --- | --- |
| Exact public Relay 3.0.0 | Public annotated tag and peeled commit verified; native slot matches the entire published distribution, including receipt and inert closure. The project Skill has all 13 exact published files and a native receipt. |
| Preserve Governance 5.0.0 | Both immutable public Git roots resolve together. Shared payload equals the current authored package and retained producer registry; public distribution receipt accounts for the different native content hash. |
| One active Shared route | Root lock has two packages, exactly one Shared 5.0.0. Root INDEX has authoring, Shared 5.0.0 and conditional Relay boot only. Skill's complete nine-protocol route selects the root lock/slot; nested 4.0.0 remains inert. |
| Conditional scope and authority | Five existing project-wide topics and conditional producer self-adoption survive unchanged. Relevant Relay workflows load the Skill's applicable complete topics; unrelated work skips Relay. Manual Codex/local Task binding persists. |
| Preserve existing behavior | Workflow projection, publisher/CI, package source and historical slots/registry are unchanged. Root/member human routing is preserved; only root INDEX gains Relay. |
| Offline integrity | Existing project qualifier now checks both pinned Git identities, full slot inventories/hashes, public receipts, authored Shared parity, Skill provenance and projection receipt. Negative tests cover drift and wrong source/receipt. |
| Recovery | Full-integration Git rollback restores predecessor manifest/lock/routes/projection together; native uninstall and offline projection are exercised in disposable staging. |

## Native materialization

Ran in a disposable Debian WSL ext4 clone using Linux musl VibeVM 1.0.7,
SHA-256 `20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Explicit public sources were fetched without a registry account. Initial install
retained the old lock's local Shared source. Preserved that generated lock and
slots outside staging; fresh resolution with `--no-default-registry --no-prefer-local`
selected the declared public revisions. Generated identities were never edited.
Both package nodes and root/member boot regenerated successfully. Native Skill
list found exactly one Skill; dry-run reported `would-create`; offline project
installation reported `created`. Selected generated files were transferred to
the task worktree; accepted historical slots pruned by VibeVM were retained.

Exact native content hashes:

- Relay 3.0.0: `sha256:451ee21dbfd63abd7918f0aee979220fb57cb8a8dffde20009a25f11bf9071e7`.
- Shared 5.0.0: `sha256:e686314f26c82f32f55958a242481d792e9fcd0d755a6eebf933431f3e0875d9`.
- Project Skill main: `c81f6addcc3c76b691604fd40c1943af84c82a56371d1adfa49ce2e0778f51a3`.

## Validation and limits

Offline native discovery found one Skill; repeat dry-run returned `unchanged`.
Native uninstall returned `removed`; reinstall returned `created`, with no Git
diff afterward. A disposable Git revert of the integration returned a tree with
no diff against the frozen predecessor. The candidate and restored baseline
both report exactly five historical orphan-slot warnings and zero errors.
Final command results and exact-head CI are recorded in the canonical PR Outcome.
Qualification covers file/CLI resolution, reachability, routing and projection,
not fresh model compliance or desktop discovery. This session uses frozen accepted
guidance, not candidate Skill rules. No automatic routing/Writer lifecycle,
runner-group configuration, installed-service qualification, settings application
or external deployment is claimed. The separately owner-authorized real Task
remains the runtime verification boundary.

The pinned `vibe check` has pre-existing orphan-slot warnings for historical
Shared slots 2.5.0–4.0.0. These retained inactive slots are not active boot paths;
the complete source/slot/lock/Skill integrity check is the relevant proof.
See [maintenance and rollback](../../relay-skill.md).
