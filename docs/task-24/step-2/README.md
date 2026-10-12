# Task 24 — Step 2 — Self-adoption qualification

**Result: comparisons completed; native producer replacement remains unqualified.
Owner disposition is required before replacing the helper or packaging an exception.**
The actual upstream registry route works. Neither path-only ORDER-LAW nor an
absolute lock URI, by itself, proves that native dogfooding cannot work. The
remaining gaps are the producer's portable source/provenance contract and actual
supported Codex file-reading startup, described below.

## Work identity and authority

This is the separately owner-admitted Step 2 of
[Task 24](https://github.com/jresearchsoftware/shared-governance/issues/24), dated
2026-10-12. The current admission explicitly supersedes the mistaken same-Step-1
continuation instruction. Its [read-back snapshot](logs/admission.json) records
the admission used here. The
[Step 1 Outcome](https://github.com/jresearchsoftware/shared-governance/issues/24#issuecomment-6120052165)
and research at `e091718b0b6eb8c2a64726174317bce69afd42d8` remain historical evidence.
The [starting PR/reviews](logs/starting-pr.json) retain the bounded independent
research assessment and the superseded same-Step-1 change request. That assessment
does not accept this new head, implementation or merge.

At entry, local HEAD and PR #25's remote branch were the same Step 1 head; the
worktree was clean and accepted source main was
`96d26c51b6d05ee5ec4576a44f541b904f0f13fb`. Updating the same PR/branch is the smallest
safe reconciliation: retain the original commits and evidence, append the Step 2
result, update the PR description and publish a distinct canonical Outcome.
No universal one-PR-per-Step rule is imposed. The supported title tool set and
read back `Task 24 — Step 2 — Self-adoption qualification`.

The accepted startup command succeeded without warnings and selected Development
Governance 1.2.0, source `73798b919efbd0d8b0ee1317bf84a6c48d7e99d1`, release commit
`4e701dcb0c97bb7a220800a550eb2f668a8ab20b`, payload SHA-256
`23d2f2ea4b28c5aafb17007d5e875b78f4b472c36d89fd66a1549e79070d0349`.
This effort retained that selection and read its four applicable protocols,
current local authoring/release/manual-handoff bindings and canonical authority.
The source-main SHA used in the diagnostic prompts identifies accepted source
containing those same authored protocols; it does not change the active helper's
publication-gated selection.

## Actual Codex launches

The [official discovery description](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
and [official prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)
describe startup discovery and user-role injection before the task prompt.
Preloading text is not evidence that a command ran before the prompt. Later
explicit owner instructions can resolve these user-level conflicts; they cannot
override system/developer instructions or establish OS isolation.

[Reproducible CLI harness](../../../scripts/probe-task24-codex-step2.py) launches
the installed `codex-cli 0.162.1` through its normal Node entrypoint, preserving
the configured default model, global instructions, credentials and configuration.
Disposable clones at accepted main carry public conflicting root/nested/boot
markers. The accepted control/handoff fixture files contain exact `git show`
bytes. Marker AGENTS are synthetic instrumentation, not newly accepted rules.
Saved prompts and [actual events/warnings](logs/codex.json) are repository-accessible.

| Actual case | Observation |
| --- | --- |
| Candidate launch, no accepted binding | `CANDIDATE_ROOT` is selected. |
| Candidate root + explicit accepted-source prompt | `ACCEPTED_ROOT`; candidate root marker is visible but inactive. |
| Candidate nested CWD + same explicit binding | Both candidate root/nested markers are visible; `ACCEPTED_NESTED` is selected. |
| Accepted snapshot `-C` + candidate `--add-dir` | Accepted root is discovered; the same accepted contract is applied. |
| Fresh review-oriented prompt after candidate AGENTS edit | Changed candidate marker is visible but inactive. This is a probe, not independent assessment. |
| Persisted session + supported `exec resume`, with another candidate edit | Accepted SHA/rules remain frozen; changed candidate text is still data. |
| Actual file-read/edit attempt, direct candidate | First `Get-Content` cannot create the exec process: `helper_unknown_error: setup refresh had errors`. |
| Actual file-read/edit attempt, accepted snapshot | Same failure. No successful file reads or candidate edits. |

[Continuation evidence](logs/codex-continuation.json) and its
[small harness](../../../scripts/probe-task24-codex-continuation.py) cover actual
resume without changing model or global policy. Supplied accepted bytes retain
the free-hardening exception; outputs apply controls, independent review and merge separation. An
unrelated translation skips the two protocol topics. These conditional choices
were assessed from supplied text, **not demonstrated by successful conditional
file reads**. The two attempted edits left `nested/target.txt` unchanged.

The least costly *tested guidance* approach is an explicit accepted-SHA prompt
classifying candidate root/nested/generated rules as data. A separate accepted
checkout adds work and did not solve this host's execution failure. The successful
application probes supplied full accepted protocol text inline: they establish
conflict handling, not automatic loading from a short SHA-only prompt. Actual
ready-file startup and a minimal link-based launch remain unqualified here.
No guarantee against hostile candidate code, arbitrary conflicting rules,
other clients/models, desktop rebinding or authentic independent review follows.

All launches disclosed existing IntelliJ MCP handshake warnings and an unsupported
PowerShell shell-snapshot warning; tool cases additionally failed exec setup.
The no-tool cases completed despite those warnings. Server model identity was
not independently verified. No permission, credential, sandbox, connector or host
repair/bypass was attempted. A CLI exit 0 here records a completed response, not
successful startup qualification. The current desktop effort's working shell and
startup selection do not prove a fresh candidate-discovered CLI launch.

## Faithful pinned VibeVM dogfooding

[Native harness](../../../scripts/probe-task24-step2.py) and [complete native
evidence](logs/native.json) use Debian WSL's native filesystem and the exact musl
binary SHA-256 `20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
The upstream checkout is pinned to `b6659978453f50e6d1d4d99626d70b980a2c5847`.
Every install, source edit, tag, commit, move and recovery is disposable. These
synthetic commits have no production acceptance or publication authority.

The harness reproduces the **complete upstream root manifest**, including
`flow:org.vibevm.world/multi-user-planning`, `version="^1.0.0"`,
`link="static-transitive"`, the checked-in versioned `vibevm/vibepacks` tree and
`install --offline --registry <root>/vibevm/vibepacks`. Both retained-lock and
cold-slot/cold-lock upstream installs succeed. It then adapts that same table
form and versioned layout to this producer's one stable workspace member.

| Property | Separate meaning and measured result |
| --- | --- |
| `flow:` | Typed package identity constrains package kind; it is not a transport or a source path. Adapted typed registry resolution succeeds. |
| `^1.0.0` / `^1.2.0` | Compatibility range below the next major; a lock selects one concrete version/hash. Local-registry `update --all` retained 1.2.0 after a synthetic 1.2.1 appeared. |
| Exact constraint | `=1.2.1` followed by deliberate install selected/materialized the synthetic candidate. Version availability and lock advancement are distinct. |
| TOML | A string is a compact registry constraint; a named table/inline table carries version/link or Git/path attributes. Formatting itself supplies no authority or different solver. |
| Registry versus path | Registry uses `<group>/<name>/v<version>` under the supplied root. A typed path dependency still fails ORDER-LAW with static-transitive linking. Changing link mode did not fix path resolution. |
| Static-transitive | Compiles the package boot and transitive boot closure into host STATIC. It changes loading/projection, not source resolution. This passive package has no dependency closure. |
| Dynamic | Keeps the compact package boot at its slot path. Pinned INDEX still labels the entry static; topic reads remain conditional inside the unchanged boot text. |
| Source layouts | Upstream already authors versioned registry roots. Our active package is stable `packages/development-governance`; adaptation needs a versioned copy/export or an explicitly chosen layout change. Historical `v0.1.0` is retained separately. |

Both adapted link modes preserve exported payload bytes and human AGENTS overlays.
Static compilation retains the boot's literal `../protocols/*.md` strings in a
different host directory where those literal relative paths do not exist. Dynamic
slot routing preserves their conventional file-relative targets. This is a
structural observation, not fresh model traversal of the compiled provenance
comments; do not silently equate static-transitive with this flow's conditional
source-file reading contract. Dynamic routing is the smaller fit for our boot.

The synthetic authoring overlay is deliberately file-reading only. The real
accepted `00-authoring.md` helper route was not replaced. Clean synthetic clone
proves slot/index bytes are available without a tool; it does not prove that the
unchanged production checkout already has native no-bootstrap startup.

## Lock portability, lifecycle and integrity

Upstream's checked-in lock contains absolute Windows `file://` paths. Fresh cold
installation regenerates source URLs for the native fixture. Adapted registry
locks similarly contain absolute fixture paths. Repeated installation changes
the generated timestamp; package/root identity is unchanged. Byte-identical lock
regeneration is therefore not a passing claim for this pattern.

Moving the producer makes the old recorded URI nonexistent. Retained-slot install
and update still succeed, retaining the old source URL. A clean clone has readable
committed slot/boot files without contacting that URI. Removing the slot in a
different cloned location and reinstalling against **that clone's own registry**
restores canonical bytes and writes the new local source URL. Thus ready-file
reading and reconstruction are portable in this probe, while lock provenance is
location-dependent and can be stale. No hand-edited lock or fake portable URL was
used. This narrows Step 1's claim: absolute URIs are not by themselves a broken
clone/reinstall, but do not meet the requested machine-independent provenance.

Source and generated outputs were co-committed in a synthetic branch. Clean
clone, candidate exact install, fast-forward pull, checkout rollback and checkout
forward keep source/projection together. Prior source/slot canonical verification
passes after rollback. Human overlays survive native generation. These are
fixture Git lifecycle checks, not an accepted production migration.

`vibe check` returns success with zero findings for corrupt/missing installed
protocols and a missing INDEX. Repeat install leaves corrupt/missing protocol
bytes unrepaired, while restoring INDEX. Existing `prepare-distribution.py`
`verify(..., installed=True)` rejects both slot incidents with precise file-set
or byte mismatches. Git/file-existence checks detect the removed INDEX. A future
native producer can reuse the exporter plus source/slot/lock/route comparisons
in existing CI; no new integrity framework, ledger or recurring manual hash
ritual is justified. Existing CI currently validates the accepted helper and does
**not** automatically validate an unimplemented native committed projection.

## Direct Git and source provenance

The real producer layout includes an in-tree historical local registry. Initial
typed Git declarations silently selected local **0.1.0** despite declared Git
`=1.2.0`; exit 0 was misleading. The evidence preserves this actual precedence.
Using supported `--no-prefer-local` isolates the declared direct Git route:

- The exact accepted source tree, mirrored under a disposable local tag, fails
  because its root `vibe.toml` is a virtual workspace without `[package]`.
  The supported direct source is a **single-package repository**, not our nested
  source workspace; no subdirectory selector was established by the pinned
  manifest grammar or this probe.
- The existing deterministic exporter supplies a flat single-package source.
  Direct-Git install then produces a `source_kind="git"` lock and verifies the
  complete canonical payload. A synthetic tag/constraint update to 1.2.1 passes
  and materializes the expected candidate bytes. The fixture historical registry
  is relocated outside the consumer for this update; update exposes no
  `--no-prefer-local` flag. None of this modifies real frozen history.
- Local `rev=<SHA>` preflight encountered Git upload-archive's refusal to expose
  raw SHA refs. The completed route uses ordinary disposable named tags without
  changing archive configuration; this local-provider limitation is not proof
  that public HTTPS SHA resolution fails.

This requalifies Task 22's flat-export route and explains why it cannot simply
be pointed at our nested producer source. Real remote distribution already has a
separately qualified publication contract. Depending on that published export
would retain publication coupling, failing accepted-source-before-publication.
A new pre-publication flat Git source or changing the producer root/layout adds
workflow/scope; neither is implicitly authorized as the selected architecture.

The harness initially assumed a caret update would create a new slot, then
mistook a local-registry selection for direct Git. Both diagnostic assumptions
were corrected and the resulting paths rerun; they are not claimed as upstream
failures. The final evidence records actual selection/provenance and canonical
payload checks, including successful transport and observed gaps separately.

## Concrete disposition and remaining work

The preferred complete design is **not yet qualified**. Two concrete gaps remain:

1. The working in-tree registry route has location-specific lock source metadata
   and requires a versioned source representation of our stable package. Accepting
   that metadata behavior, choosing a new flat Git/source layout, or changing the
   pinned tool is a material policy/scope choice. Successful readable clones do
   not silently waive the Issue's portable-provenance contract.
2. Neither supported Windows launch completed actual boot/protocol reads or the
   candidate edit because exec setup failed. The prompt comparison supports a
   cheaper guidance-consistency approach; it cannot qualify the required actual
   startup path or justify removing the verified helper. Host repair and widening
   tool/client scope are not silently performed.

Recommended owner disposition: retain the current helper while resolving those
specific gaps; prefer an explicit accepted-SHA prompt over a mandatory separate
checkout for accidental-rule consistency in the tested manual client. If the owner
chooses additive protocol packaging with a transitional producer exception,
explicitly preserve its publication/bootstrap limitations; that option has not
been selected. Alternatively admit a bounded native source/provenance/tool choice
and separately qualified supported startup. No permanent manager, new approval
ceremony, universal PR rule, TEST service or forced upgrade is proposed.

The [revised shared protocol candidate](proposed-protocol.md) preserves the full
eight admitted reusable semantics and adds the new guidance/security distinction.
It is outside the package, neither exported nor active. Its wording does not
require separate-checkout isolation when a supported explicit prompt suffices.
Protocol packaging, producer migration and Task completion remain pending this
disposition and independent acceptance. The accepted helper, root/authoring
instructions, four-topic rules, package/version 1.2.0, release workflow, frozen
history and all other consumers remain byte-unchanged.

## Reproduction and validation

From the review head, on a native Linux filesystem with the pinned source/binary:

```sh
python3 scripts/probe-task24-step2.py --vibe /absolute/path/to/vibe \
  --upstream /absolute/path/to/pinned/vibevm --output /absolute/path/to/native.json
```

From the repository root on this Windows CLI installation, using its ordinary
Node executable and installed `bin/codex.js` entrypoint:

```text
python scripts/probe-task24-codex-step2.py --node NODE_EXE --codex-js CODEX_JS --output docs/task-24/step-2/logs/codex.json
python scripts/probe-task24-codex-continuation.py
```

The latter creates one persisted disposable probe session solely to test supported
resume; other cases are ephemeral. Fixtures and private raw logs stay in ignored
`.vibe/`; public prompts/events are committed. The unchanged configured model is
used. Do not repair denied sandbox operations to turn this evidence into a pass.

Final source/export, distribution, release, self-adoption, package-boundary and
whitespace validation is recorded in [validation evidence](logs/validation.json).
Exact-head CI and the published candidate identity are reported in the distinct
Step 2 Outcome. Passing existing checks is not replacement qualification,
independent acceptance, merge, publication or closure authority.
