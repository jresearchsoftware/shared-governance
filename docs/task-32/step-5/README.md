# Task 32 — Step 5: source-controlled ChatGPT Instructions lifecycle

One versioned base/projector now ships as optional files in the existing VibeVM
flow. Each project owns reviewed custom Markdown and binding data, plus its
complete canonical generated Instructions in source control. One interface
checks, updates and compares desired state without live settings access.
The common base prescribes client discovery/loading mechanics; project-owned
accepted routes supply substantive workflows and adoption conditions.

Authority: complete [Task 32 chronology](https://github.com/jresearchsoftware/shared-governance/issues/32),
[Step 5 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6187417393),
and the [Step 4 independent assessment](https://github.com/jresearchsoftware/shared-governance/pull/33#pullrequestreview-5529653254).
Starting candidate: `c7003e8fdd57e796f6aec4daffe5d946e4792250`.
Frozen independently accepted source-main: `15e8191435a126e54b4d1739a73fab112e01c081`.
Live remote main, PR head and merge base matched the admission before edits;
Task 28's acceptance and PR 31's merged squash corroborated source acceptance.
Candidate code, custom text and generated native files remain proposed data.
No rebase or accepted-governance repin occurred.

## Ownership and distributable interface

| Layer | Canonical source / owner |
| --- | --- |
| Shared client mechanics | Package [base](../../../packages/development-governance/tools/chatgpt/base.md) and [projector](../../../packages/development-governance/tools/chatgpt/project.py), one producer-owned version. |
| Project-specific client text | Producer [custom Markdown](../../../chatgpt/custom.md) and [small binding](../../../chatgpt/binding.json); consumers own their equivalent files. |
| Complete desired state | Producer [generated Instructions](../../../chatgpt/instructions.md) and [receipt](../../../chatgpt/receipt.json), committed alongside custom/binding. |
| Common maintenance | [Package interface](../../../packages/development-governance/tools/chatgpt/README.md): `check`, `update`, `compare`, optional selected Sources. |
| Historical different consumer | [Relay read-only preview](relay-preview/instructions.md), [custom](relay-preview/custom.md), [binding](relay-preview/binding.json) and selected cache. Same implementation, no consumer edit. |
| Qualification | [Evidence](evidence/validation.md), [semantic coverage](semantic-coverage.md), and optional [native fixture](../../../scripts/qualify-chatgpt.py). |

The table's links are relative to this report; the package interface is the
portable maintenance procedure, not a bespoke consumer exporter. The producer
convenience script delegates to the same code. The former outside-package
template is removed to leave one canonical source. Historical Step 4 commands
remain reproducible with their original exact commit, not today's interface.

**Package bump: minor** — 2.2.0 to 2.3.0 adds optional maintenance assets.
All seven protocols and the compact boot keep their accepted bytes. No hook,
capability, Skill, dependency, mandatory operator action or topic adoption is
added. Export allowlisting recognizes only the three declared maintenance files;
historical package shapes remain valid. Producer registry, slot, lock and index
are generated with pinned VibeVM and committed in this PR. Active authority for
this effort still comes from the frozen 2.2.0 accepted snapshot. This is a source
candidate; public release and external consumer upgrade are not performed.

## Maintenance behavior

Stable Instructions navigation does not embed the maintenance SHA or one current
Task Decision. Each substantive effort must independently establish and freeze
its accepted revision before reading applicable local/native routes. Exact
maintenance identities and tool/source/generated hashes live in the receipt.
An unrelated accepted commit changes evidence only; actual Instructions are
`NO_OP`. Relevant materialized guidance changes appear in source changes and
are read JIT. Base/custom/client-routing changes produce exact Instructions diffs.
An enabled versioned cache has its own changed/no-op result and provenance.

`check` reads without writing and returns stale status for missing/mismatched
generated artifacts or receipts. `update` intentionally writes only recognized
owned output after checking every planned target against the previous receipt.
Unknown or manually changed generated files are preserved. Custom Markdown is
never rewritten. Recover/reconcile through ordinary Git if interrupted or if
useful live/generated edits need moving into custom source. The tool does not
provide transactional multi-file filesystem writes or an acceptance oracle.

The real exported-tool suite covers changed base/custom/binding, accepted local
routes and materialized dependencies, no-op, unrelated commits, source authority,
conditional boot, role limits, stale detection, safe rewrite, cache selection,
owner-export comparison and realistic missing/unsupported input failures.
The native fixture prepares the exact candidate package, publishes only to a
temporary local Git repository, installs it in a disposable non-adopting project,
invokes the tool **from its installed slot**, upgrades a synthetic compatible
version through VibeVM and invokes that new slot with the same interface.
This is transport/CLI evidence, not model behavior or real consumer adoption.

The historical accepted Relay source remains `52bebbc9cafc1e82737943a6d37f00945ffadfef`.
Its separate product Skill/compatibility and local boot supply authority; neither
shared Task Handoff nor Independent Review is adopted by the preview. It is not
today's Relay configuration, a complete live replacement or Relay 101 migration.
DocReview's product/specialist/corporate/controller ownership stays unchanged.

## Owner handoff and remaining boundary

The owner can review the full canonical Instructions, reconcile any unknown
actual live rules, and manually apply/read back the chosen complete text after
independent assessment and disposition. On demand, export the actual field as
raw Markdown and invoke the same tool's read-only `compare`; it gives an exact
diff/no-op, never proof of UI freshness. No live export or application happened
here. Unchanged Instructions require no re-paste; unchanged cache needs no upload.

Prefer observation during ordinary subsequent project work after owner
application. Actual loading, spontaneous independent review depth, role
adherence, active-blocker handling, Sources addressability/freshness and repeated
reliability remain unqualified. Prior C2/C3/C3b/BLOCKED reports stay historical
with their existing provenance limits. No artificial live session is manufactured.

Commit/push and exact-head CI culminate in one attributable English canonical
Outcome on PR 33, then stop for independent substantive **NON-APPROVING
Deliberative review** and owner disposition. All checks here are implementer
self-checks. Task 32 and PR 33 remain **OPEN**. No live settings/Sources mutation,
external consumer change, runtime/Writer/Reviewer change, new topic adoption,
deployment/credential action, self-approval, merge, release, subsequent launch
or closure is performed.
