# Step 2 qualification

All results below are contributor qualification, not independent acceptance.
The canonical PR Outcome binds the final remote head and its primary exact-head
CI separately. No package has been publicly released by this Step.

## Passed qualification

| Check | Evidence and scope |
| --- | --- |
| Source/exact-commit export and native producer integrity | [Source/export log](logs/source-export.txt), then final-head CI. Checks tracked text/JSON/TOML, local links, bounded secret markers, passive payload, exact export and complete producer source/registry/slot/receipt/lock/index/agent routes. |
| Distribution regression | [Final log](logs/distribution-final.txt): 40 PASS in a clean native Linux clone after corrections. Includes genuine 2.5.0 historical export, new whole-package version requirement, installed guide completeness/UTF-8/local-link/escape failures and unchanged nine protocols/client tools. |
| Self-adoption regression | [Final log](logs/self-adoption-final.txt): 12 PASS from the committed complete candidate, including clean ready checkout, corrupt/missing slot, forged metadata, lock and boot failures, source regeneration and preserved overlays. |
| ChatGPT regression | [Final log](logs/chatgpt-final.txt): 24 PASS. [Supported maintenance](logs/instructions-update.json) used the installed 2.6.0 tool with independently accepted SHA `88a95f7604b2d81d7a3dd3f76f095beddb71bdab` and the Step 2 Decision. Effective content and Instructions are `NO_OP`, Sources `DISABLED`; only maintenance evidence changed. |
| Release boundary regression | [Log](logs/release.txt): 10 executed PASS, six optional native publisher/dependency tests SKIPPED in this default run. No publisher/resolver behavior changed; those six are not counted as passes or newly qualified. |
| Whole-package transition | [Boundary log](logs/version-boundary.txt): 2.5.0 → 2.6.0 MINOR against the frozen accepted source, recomputed against live main before handoff. Source, native projection and receipt are proposals until independent acceptance. |
| Protected bytes and scope | [Preservation](logs/preservation.json): complete Git-normalized equality for 133 accepted files across nine protocols, shared client assets, all historical registry/installed files, root/member agents, manual/self-adoption/release bindings, local custom/binding/Instructions, toolchain and workflows. Instructions retain 5,132 Unicode characters. [Diff scope](logs/diff-scope.json) separately verifies the bounded Step 2 paths and unchanged complete accepted compact-boot prefix. |
| Whitespace and local links | Staged/full candidate whitespace and final exact-commit source qualifier; no link/whitespace rule was relaxed. |

The native producer and distribution logs identify authored
`9cb8421bf2ac6b292b4cb374e453b30718954286`; complete native projection was then
committed at `f8f0b4d7b...`. The corrected regression logs use that committed
candidate. Later evidence/test-only commits preserve the same package payload,
whose generated digest is
`92d36c21e74fbfc44cffa72e7270bc3eb13fc03cc4db7d72e66c5802e8301c14`.
Final-head source/export checks and CI establish that identity for handoff;
the local logs do not pretend to have run at a later commit.

## Real native fresh-consumer evidence

[Producer materialization](logs/native-producer.txt) uses the exact pinned Linux
x86_64 musl VibeVM 1.0.7 binary (SHA-256
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`), isolated
settings and a disposable native filesystem. Exact source staging, native
install/check and producer verification pass with zero check findings. Root
and member human/managed agent text is preserved. The revised unaccepted 2.6.0
proposal was resolved through the supported fresh-lock path: preserve/discard
only the cloned candidate's generated lock, then ordinary install. No accepted
lock, frozen release, URL or integrity check was edited to bypass a failure.

[Distribution integration](logs/native-distribution.txt) executes the existing
21-command disposable local-Git probe: public-format exact export, local native
publisher/idempotence, cold/repeat installs, independent cold consumer, retained
slots offline, synthetic patch update and complete Git rollback. The
[installed-onboarding probe](logs/installed-onboarding.json) opens the actual
fresh consumer with no producer README, authoring tree or local producer policy.
Its only INDEX entry is the installed compact boot; that file's explicit-request
link resolves to the complete installed guide and examples, and their relative
protocol links stay inside the qualified payload. All nine protocols and the
optional ChatGPT maintenance files are present; the consumer's human overlay is
unchanged. Guide/examples are not eager INDEX entries. Reading follows the
conditional prose; this proves static routing and native file transport, not a
live request classifier or model obedience.

The integration deliberately reproduces retained upstream limitations:
full-SHA `file://` remote archive acquisition and cache-only missing-slot
recovery fail as expected; mutable-tag drift can split lock/slot identity,
which canonical verification rejects. `vibe check` alone does not detect that
split. INDEX remains static despite authored dynamic linkage. These expected
incident results are disclosed, not silently relabeled integration successes
or attributed to the new guide. No real remote tag was changed.

## Initial failures, corrections and limits

- The [initial distribution run](logs/distribution-initial.txt) passed 39 tests
  and exposed one new test passing `HEAD` into a full-SHA API. Resolving the full
  commit in the test fixes it without changing the API or weakening checks.
- [Initial self-adoption](logs/self-adoption-initial.txt) was launched before
  the generated projection was committed; seven disposable-clone tests could
  not find that uncommitted versioned source. The complete projection commit
  and clean-clone repeat pass all 12. This was a check-order error, not missing
  delivery left in the terminal candidate.
- [Initial ChatGPT tests](logs/chatgpt-initial.txt) found two mismatches: the
  appended-route preservation fixture rejected insertion before the accepted
  prefix, and the maintenance receipt still named tool 2.5.0. The onboarding
  paragraph now follows the complete unchanged accepted boot, and supported
  [check](logs/instructions-check.txt)/update refreshes the receipt while
  preserving Instructions/custom/binding. All 24 pass; no fixture was weakened.
- Earlier [native producer](logs/native-producer-initial.txt),
  [distribution](logs/native-distribution-initial.txt),
  [route](logs/installed-onboarding-initial.json) and
  [source](logs/source-export-initial.txt) logs retain the initial boot placement
  and old payload digest. They are historical intermediate evidence; the later
  corresponding logs qualify the corrected payload.
- Git reported CRLF-to-LF normalization for new Windows-written evidence logs
  under the existing attributes. Full/staged whitespace checks pass; no
  line-ending policy or preserved source bytes changed.
- The seven portable examples remain explicitly fictional. Cedar now states
  actual-in-the-fiction PR head usage, the planned merge, current auto-delete
  setting and missing applicable protection. It claims prospective exposure,
  not an observed deletion or a general risk from retained-branch existence.
- No real consumer onboarding/adoption/migration, live GitHub/configuration,
  credentials, publication or ChatGPT Instructions/Sources setting changed.
  Live model/client traversal, settings currentness and runtime model/effort
  identity remain unqualified. Existing Windows Codex startup limitations are
  neither retested nor resolved. Static desired Instructions are not live UI.
- The title tool's persisted readback exactly reports
  `Task 30 — Step 2 — Ship discoverable onboarding`; title is navigation only.
  The FPF experiment's exact calls, edition, applicability and bounded effect
  are recorded in [the Step 2 account](README.md#bounded-advisory-fpf-consultation).
  FPF adds no package dependency, binding rule or acceptance gate.

Stop after one attributable PR Outcome and verified publication for fresh
independent exact-result assessment. Direct acceptance may be used by that
evaluator under the Step 2 Decision; executor checks supply no self-approval,
merge, release or Task-closure permission.
