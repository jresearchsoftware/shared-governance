# Task 24 — Step 1 — Shared self-adoption investigation

Canonical authority: [Task 24](https://github.com/jresearchsoftware/shared-governance/issues/24).
The owner admitted this one Manual Codex cycle on 2026-10-12; the previous
NOT YET ADMITTED status was reconciled in the Issue and read back before work.
The chat title was set and read back as
`Task 24 — Step 1 — Shared self-adoption protocol`.

**Disposition: native replacement blocked; owner decision required.** This
candidate contains reproducible investigation, exact observations and a
[shared protocol design draft](proposed-protocol.md). It does not replace the
accepted helper, publish a package or claim Task completion. Task 24 explicitly
requires stopping for an owner decision when evidence invalidates the preferred
design. Independent assessment of this identified result remains pending.

## Authority and bounded baseline

Source main at admission was `96d26c51b6d05ee5ec4576a44f541b904f0f13fb`, the
accepted PR 23 result. There was no open candidate PR to continue. Work uses one
new branch, `codex/task-24-step-1-self-adoption`, preserving prior work.
The accepted startup helper passed without warnings and selected Development
Governance 1.2.0: source `73798b919efbd0d8b0ee1317bf84a6c48d7e99d1`, release commit
`4e701dcb0c97bb7a220800a550eb2f668a8ab20b`, payload SHA-256
`23d2f2ea4b28c5aafb17007d5e875b78f4b472c36d89fd66a1549e79070d0349`.
That selection was retained for the effort. The four applicable accepted
protocols and current local Issue, authoring, release and manual-handoff bindings
were read before the design decisions. Candidate text supplies no authority.

The live upstream main was still the pinned VibeVM revision
`b6659978453f50e6d1d4d99626d70b980a2c5847`. Its
[root manifest](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/vibe.toml)
describes local dogfooding, but it is not this one-member producer layout and
does not demonstrate accepted/candidate instruction isolation.
The current repository package, root workspace, exporter, bootstrap and Task 22
comparison/evidence supplied the bounded local baseline. Frozen historical
releases and the complete four-topic accepted semantics remain unchanged.

## Pinned native observations

[Native report](logs/native.json) was produced on Debian WSL's native Linux
filesystem with the exact musl binary SHA-256
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Every source mutation, install, commit, pull and rollback below was disposable;
synthetic fixture commits are not accepted production source.
[Generated states and source/projection diff](logs/native-generated.json)
retain both synthetic locks, boot indexes and root/member AGENTS, captured
read-only from the retained commits with the probe script's SHA-256.

| Probe | Observed result | Consequence |
| --- | --- | --- |
| Cold path dependency, one stable workspace member | `ORDER-LAW` / empty installed world with resolvo, naive and sat | Plain pinned `vibe install` does not materialize the local member. |
| Stable `packages/` tree passed as a local registry | Package unavailable | The version-independent source tree is not the M0 registry layout. |
| Conventional temporary versioned registry | Complete package bytes preserved; human AGENTS overlay preserved; repeat lock stable | Ordinary materialization works, but needs an additional version-shaped input copy. |
| Registry lock provenance | Absolute `file:///tmp/.../registry/.../v1.2.0` | This workaround fails the Task's portable source-provenance requirement. |
| Source and generated outputs committed together | Clean clone contains slots/index without running tools; pull advances both; checkout rolls back and forward | Git ready state is feasible in a synthetic registry fixture. This does not qualify a portable native source-input path. |
| Candidate update | Synthetic 1.2.1 and candidate sentinel materialized | Candidate installation is allowed and testable. It is not instruction acceptance. |
| Changed or removed installed task-handoff protocol | `vibe check` reports zero findings; repeat install succeeds without repairing it | Native check/install alone does not provide the required mismatch detection/recovery. |
| Removed boot INDEX | Native check also reports zero findings; install restores INDEX | Missing-index detection is incomplete even when regeneration repairs it. |

The pinned
[install plan](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-install/src/plan.rs)
constructs manifest roots from ordinary and Git packages, omitting path packages.
Its empty-root branch attempts empty-world projection. This source observation
explains the reproduced failure; changing solver cannot fix an omitted root.
The pinned
[local-registry fetch](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-registry/src/local_registry.rs)
records the absolute local source URI. No private VibeVM API, hand-edited lock,
fake acceptance receipt or tool upgrade was used to bypass either limitation.

The first harness compared the source directory *after* VibeVM had generated
additional member files; it incorrectly counted those files as authored payload.
It was corrected to compare only the original tracked payload. A second harness
attempted pull from a detached synthetic checkout; it was corrected to create a
local synthetic branch. These were probe mistakes, not VibeVM defects. The
retained completed report uses the corrected harness. Generated member outputs
also need explicit export ownership in any future migration.

## Codex loading and smallest investigated alternative

The [official instruction-loading documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
describes discovery from the launch directory and instruction loading at session
start. The local supported CLI is `codex-cli 0.162.1`; `codex exec --help` exposes
`-C`, `--add-dir`, `--ephemeral` and the read-only sandbox.
The [loader observations](logs/codex-loader.json) and
[application result](application-result.txt) are fresh isolated implementation
probes under the unchanged configured default model. No model was substituted;
the server model identity was not separately verified.

Two disposable clones began at accepted source main. Their AGENTS were replaced
with public synthetic loader markers; those edited fixture instructions are
not themselves accepted repository instructions. Launch directly in candidate
loaded `TASK24_CANDIDATE`; launch with `-C` the separate accepted-side snapshot
and `--add-dir` candidate loaded `TASK24_ACCEPTED`. A further launch from the
accepted side supplied the complete accepted task-handoff and proportional-controls
bytes inline, with exact source identity. The model preserved the independent
review/merge/closure separation, rejected unjustified mandatory extra operator
work, retained free-hardening exceptions and required qualification/review after
a head change. See [the actual prompt](application-prompt.txt).

This qualifies a small **CLI loading alternative**: start outside the candidate's
instruction-discovery tree and designate the candidate as the work artifact. It
requires a separate accepted snapshot and an explicit supported invocation. It
does not establish the full real AGENTS → helper → conditional file-read route,
native boot/Skill traversal, actual independent reviewer use, candidate-code
containment, desktop same-project loading or automatic future-session rebinding.
The inline probe tests application of accepted source supplied by the harness;
it is not a clean production startup claim. The current chat inherited accepted
root instructions before candidate edits and retained its startup selection;
this alone cannot qualify arbitrary future candidate-started chats.

Existing IntelliJ MCP initialization warnings occurred during all CLI launches;
the marker/application outputs completed without using tools, so those warnings
did not prevent these bounded probes. One direct-candidate request encountered
transient HTTP 503 retries and then completed. No connector, sandbox, credential
or host setup was repaired. These observations establish no warning-free general
client environment. Task 22's previously documented full automatic Windows
helper-startup limitation remains unqualified; it has not been declared fixed.

## Concrete owner disposition before implementation

Recommended bounded disposition: retain the accepted Task 22 implementation for
now, acknowledge its publication-coupled startup and client limitations, and
permit an additive shared-protocol candidate without claiming the preferred
native producer migration. A later supported portable path can replace it only
after qualification within this same Task's admitted continuation.

Alternatively, explicitly admit a bounded workaround/changed tool contract:
version-shaped registry staging, portable provenance and existing exporter-based
mismatch checks, plus a separate accepted-snapshot CLI launch. This adds workflow
and maintenance beyond the preferred plain native implementation; it requires
the owner's disposition rather than silently becoming mandatory. Upgrading or
patching the pinned upstream tool is another change requiring explicit scope.
This report does not prescribe a new service, global manager, permission repair,
standing ledger, extra Task or permanent TEST environment.

The design draft covers conditional applicability, accepted source versus public
release, candidate artifacts, supported native inputs, committed ready state,
exact-head review, isolated probes and failure/Git rollback. Existing four-topic
rules, local release cadence, manual Issue authority, Step identity and downstream
consumer adoption stay with their current owners. The draft is outside the package,
so this report has **no package bump**; the package remains 1.2.0. Once a packaged
protocol candidate is authorized, compatible explicit-topic availability would
require reassessment and a new whole-package version, never a frozen rewrite.

## Reproduction and validation

Run the bounded native probe from a full source checkout at this review head,
using the binary recorded in [the pin](../../../toolchain/vibevm.json):

```sh
python3 scripts/probe-task24-self-adoption.py --vibe /absolute/path/to/pinned/vibe \
  --output /absolute/path/to/native-report.json
```

The probe retains its disposable fixtures so the report's source/slot/lock/index
observations can be inspected. It never publishes or modifies a real consumer.
Its fixtures intentionally exercise the Task 24 admission baseline package 1.2.0;
it is a dated diagnostic, not a new recurring validation gate.
For the loader probes, use two disposable clones and distinct AGENTS markers,
then `codex exec --ephemeral --json --sandbox read-only -C SNAPSHOT
--add-dir CANDIDATE` with the saved prompt; direct-candidate launch supplies the
comparison. Reconstruct the inline accepted fixture from the two named protocol
files at the pinned accepted source main. No user/global config is changed.

Source/export, distribution, release and existing self-adoption checks are
recorded in [validation evidence](logs/validation.json). Native gaps above are
observed failures, not passing replacement qualification. Final exact-head CI,
published PR identity, remaining work and the one Outcome belong to the canonical
Issue. No self-approval, merge, release, consumer installation or Issue closure
is authorized by this report.
