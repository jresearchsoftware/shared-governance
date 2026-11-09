# Task 94 — Step 2 — CR-94-001

The frozen accepted authoring baseline remains
`1110f10b996c2f81fa842e6339ab6d7c13111cd7`; remediation starts from the reviewed
candidate `0c07197075168ce9098b942bc1c92e8d22679af2`. This launch authorizes local
task commits and unprivileged qualification only. It does not authorize GitHub
credentials, push, review invocation, integration or distribution writes.

## Correction and preserved behavior

F1 is corrected at the shared CLI planning boundary, after source-time readiness,
first-parent membership, exact successful push CI and automatic-trigger checks.
For eligible publisher-bound recovery, planning reads the destination tag and
fetches its exact Git object. The complete first-frozen export, including the
original receipt, must match before returning `ALREADY_PUBLISHED` with verified
payload. The reusable workflow then emits `ready=false` and skips native-tool
download and staging. A missing tag stays `READY`; tag mismatch fails closed,
and unavailable readback is explicitly `RECOVERY_READBACK_FAILED`.

The source-only planner remains separate from destination observation. Candidate
checks and late-onboarding no-ops do not gain remote accesses. Staging and
finalization retain their concurrent-tag checks, exact destination binding and
atomic non-force push/readback. No release ledger, historical authorization
audit, workflow bypass, new credential or package-version change is introduced.
Development Governance exported bytes remain unchanged.

## Qualification

The pinned SHA-256-verified VibeVM 1.0.11 musl binary runs only against disposable
local destinations. The new regression publishes a frozen version, advances a
package-neutral accepted fixture commit and executes CLI planning plus the actual
reusable workflow readiness-output code with native download unavailable. It
checks verified `ALREADY_PUBLISHED`, `ready=false`, unchanged refs, same-source
retry, mismatched receipt, failed readback and mixed package publication states.
Separate tests retain current CI/trigger rejection before destination access and
missing-tag readiness. The existing real mismatched-tag fixture also exercises
planning before staging/finalization.

The [fresh Relay replay](relay-recovery.json) uses actual public source and CI
records for `10d2614372cbf578dfb552d3d62fdb8f640f7501`, preserving first-frozen
`0aff32a6873262185f60364463f4e97ef330de89`. It publishes 5.0.0 exactly once to
an empty disposable bare destination, verifies the original receipt and plans a
verified already-published no-op without download. Only distribution transport
addresses are substituted. No public write occurs. Its timestamp bounds mutable
public observations; it is not proof of GitHub Actions execution.

Normal local checks cover the publisher, dispatch shells, producer parity,
distribution, release boundary and ChatGPT projection. Direct self-adoption
fixture cloning encounters the launch checkout's Git dubious-ownership boundary;
qualification uses an exact committed bundle imported into an owned disposable
checkout, without changing source ownership, permissions, hooks, config or remotes.
The applicable local results are:

| Check | Result |
| --- | --- |
| Shared publisher with pinned native tool | 118 tests passed |
| Focused recovery suite with pinned native tool | 17 tests passed |
| Actual manual/automatic workflow shell resolution | 7 tests passed |
| Producer publication parity with native staging | 12 tests passed |
| Distribution | 52 tests passed |
| Release boundary with native fixtures | 26 tests passed |
| Self-adoption from exact committed bundle | 17 tests passed |
| ChatGPT projection | 29 tests passed |
| Source, links, bounded credential markers and exact committed export | `qualify.py --export-ref HEAD` passed |
| Whitespace and exported package scope | Diff checks passed; package bytes unchanged |

`actionlint` is unavailable. Workflow source-resolution scripts and the reusable
readiness-output script execute locally; this does not claim hosted Actions or
native installed-runtime proof.

## Remaining completion boundary

Fresh independent exact-head review, native Exact-head CI and authorized
integration remain external to this launch. No root/sudo-only installed-runtime
proof or GitHub Actions dispatch is claimed. Task 94 stays open until the
[separately authorized Relay continuation](../step-1/relay-continuation.md)
accepts the caller correction and verifies real public `v5.0.0` tag/source
readback, unless an explicit owner Decision transfers that condition. The replay
still observes Relay's required caller input at the inspected source and no public
5.0.0 tag; the Relay UI and real publication are not claimed fixed.

The pre-existing untracked `.codex-sandbox/` is launch-owned runtime state
(`nobody:codex-relay-codex-work`, directory mode `2770`). It is preserved untouched;
no task source or generated qualification residue is left there by this correction.
