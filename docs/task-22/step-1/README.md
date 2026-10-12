# Task 22 / Step 1 qualification

Canonical scope: [Issue 22](https://github.com/jresearchsoftware/shared-governance/issues/22).
Starting accepted source: `73798b919efbd0d8b0ee1317bf84a6c48d7e99d1`.
This source-only candidate is pending independent exact-head review. No release,
consumer migration, merge, approval or Issue closure is performed by this effort.

## Alternatives and selected mechanism

The [upstream root manifest at the pinned revision](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/vibe.toml)
declares self-consumption from its local package tree. That establishes actual
dogfooding, not this producer's accepted/candidate isolation. The upstream
[workspace guidance](https://vibevm.org/doc/org.vibevm.core/vibevm-docs/1.0.0/howto/set-up-a-workspace/),
[self-hosted tutorial](https://vibevm.org/doc/org.vibevm.core/vibevm-docs/1.0.0/tutorials/obsidian-to-project/)
and [update guidance](https://vibevm.org/doc/org.vibevm.core/vibevm-docs/1.0.0/howto/update-packages/)
describe explicit membership and intentional re-resolution/lock/boot rewriting.
Current upstream documentation was checked alongside actual pinned behavior;
it is not assumed to describe newer features in the pinned binary.

| Arrangement | Actual pinned evidence | Trade-off for this producer |
| --- | --- | --- |
| Published dependency in the existing one-member workspace | A registry version installs without being shadowed by the same-coordinate candidate member. Direct-Git exact-tag install and `vibe update --all` move 1.2.0 → 1.2.1 and rewrite lock/materialized boot. | Works, but still needs accepted-publication selection before changing an exact constraint/tag; adds pinned executable, manifest/lock and generated-root ownership to ordinary startup. |
| In-tree workspace package | Local candidate sentinel is excluded from registry installation. Cold path-only dependency fails with empty-world `ORDER-LAW`. | Membership alone does not make a safe accepted snapshot; directly reading the editable member leaks candidate policy. A separate accepted snapshot would still be required. |
| Direct accepted-source projection | Existing exporter reproduces all published package bytes. Latest published first-parent source revision selects an atomic local projection; live and offline 1.2.0 match. | Selected: reuses Python/Git already needed by ordinary source work and avoids an additional resolver/materializer layer. No root dependency/lock or custom registry is introduced. |

[Native comparison](logs/native-comparison.json) uses SHA-256-pinned VibeVM 1.0.7
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Its local-registry `update --all --registry` reports zero resolved packages and
leaves the lock unchanged: that flag is for global applications, not a project
registry update. The direct-Git experiment uses the supported project update
path and succeeds. The initial unsupported-flag probe was corrected before this
retained result; it is not counted as an upstream defect. Generated INDEX uses
`static` despite authored dynamic linkage, as previously documented.

## Semantic coverage and proportional cost

The complete accepted 1.2.0 export preserves every package path and byte,
including LICENSE/attribution, all applicability qualifiers and boot text.
Proportional-controls retains the historical complete procedure and free-hardening
exception and activates the accepted Task 19 existing-proof/friction corrections.
Requirement-authority becomes explicitly adopted conditional interpretation.
Package-versioning moves from editable source to accepted content; producer
cadence/publication remains local. Task-handoff is explicitly adopted with the
existing Issue/manual-Codex binding; no universal Step counter or product schema
is invented. The root routes all four topics only in their applicable contexts.
Future added topics require a project-owned adoption decision.

The old generated proportional-controls snapshot/receipt and authoring-only
routes are removed atomically in this candidate. Their accepted provenance and
conversion helper remain in history/frozen 0.1.0. Generic duplicated handoff
wording is removed from the manual binding; concrete title, GitHub Outcome,
identity and review requirements stay local. Other consumers are unchanged.

Concrete harm: candidate package edits becoming active or a partial/mutated
release replacing trusted rules. Existing source review and guarded publication
already establish ownership; the small selector reuses their Git artifacts.
First-parent filtering, exact exporter comparison and atomic selector replacement
address silent policy substitution. Costs are two bounded read-only Git network
operations and disposable local files at effort start; failure retains accepted
guidance with a warning. No VibeVM installation, credentials, recurring owner
approval, service, post-merge writes or protected-boundary repair is introduced.
These costs/mechanism are explicitly in Issue 22's authorized investigation scope.

## Validation and limitations

The [self-adoption regressions](logs/self-adoption.txt) pass 18 tests on native Linux
with one Windows-only ACL test skipped. They exercise fresh-clone/offline
reproduction, dirty feature isolation, merged side-branch exclusion,
acceptance-before-publication, major eligibility, unchanged payload/retry,
registry failure, counterfeit payload, moved tag, interrupted selector commit,
rollback, poisoned active guidance and preservation of project refs/index/
instructions. [Distribution](logs/distribution.txt): 31 PASS.
[Release integration](logs/release.txt): 16 PASS, including the pinned publisher,
closure and concurrency probes. [Materialization](logs/materialization.txt):
7-command PASS. [Windows checks](logs/windows-cache-access.txt): inherited DACL,
interruption and rollback all PASS. [Source/export](logs/qualification.txt),
[unchanged release boundary](logs/version-boundary.txt), whitespace and
[scope preservation](logs/scope-preservation.json) PASS.

[Live selection](logs/live-selection.json) and [offline selection](logs/offline-selection.json)
identify 1.2.0, accepted source `73798b919efbd0d8b0ee1317bf84a6c48d7e99d1`,
peeled distribution commit `4e701dcb0c97bb7a220800a550eb2f668a8ab20b`, payload
`23d2f2ea4b28c5aafb17007d5e875b78f4b472c36d89fd66a1549e79070d0349`.
The initial bootstrap confused the annotated tag object with its peeled commit;
that pin was corrected and the retained successful results use the latter.

Automatic activation means the first subsequent effort selects a successful
eligible publication through root AGENTS. Existing efforts retain their reported
selection. This is agent startup routing, not a daemon or promise of hot reload.
Publication failure retains prior eligible guidance; the publication workflow
remains responsible for its existing CI/source/atomic-push boundary. This
candidate has not yet been independently accepted or activated through owner merge.

## Windows correction and model evidence

The initial fresh probe could read root instructions but could not launch the
helper (`helper_unknown_error: setup refresh had errors`; alternate spawn EPERM).
The first prepared-cache probe then exposed a real materialization defect:
Python's private temporary-directory DACL survived rename and prevented sandbox
readers from accessing the accepted protocols. Both failures remain in the
[initial result](probe-result.txt) and [prepared result](probe-fallback-result.txt).

The correction creates public guidance with ordinary inherited workspace access
and keeps generated files plus the local Git-object cache under ignored `.vibe`,
outside protected `.agents` and project `.git`. No existing ACL, credentials,
sandbox settings or host capability is repaired. [Before/after ACL evidence](logs/acl-correction.json)
confirms a protected private old DACL versus inherited new access. An initial
Windows test harness used Windows PowerShell with an incompatible inherited
module path; [its failed log](logs/windows-activation-fixed.txt) is retained.
The final ACL regression reads the native Win32 descriptor directly and passes.

The [corrected fresh result](probe-fixed-result.txt) and
[actual protocol-read events](logs/codex-fixed.jsonl) demonstrate root AGENTS →
verified retained identity → complete accepted proportional-controls and
requirement-authority reads. The model correctly rejects added mandatory ceremony
without owner authority and retains required checks, independent review,
changed-head revalidation, protected-boundary purposes and free hardening.
It reads the accepted projection, not editable authoring or external memory.

**Full automatic CLI startup remains unqualified:** the shell helper is rejected
before Python starts by the existing setup failure. Standalone live refresh and
prepared retained-protocol traversal are separately qualified; this is not a
claim that the fresh CLI ran automatic refresh. The probes use the unchanged
configured default model, with no substitute or separate verified server-model
identity. They are implementation observations, not independent acceptance or
broad reliability/context/quota evidence.

[Probe inputs](probe-prompt.txt), [prepared-cache input](probe-fallback-prompt.txt)
and [corrected input](probe-fixed-prompt.txt) preserve the scenarios. Initial
JSONL is filtered to task commands, tool metadata/errors and startup/usage;
unrelated memory/source dumps and reasoning are omitted, with raw hashes and
local archival provenance in [filter receipt](logs/model-evidence-filter.json).
No unrelated private memory content is published. No broad reliability/cost or
native JIT claim is made. [Self-adoption](../../self-adoption.md) documents safe retry, new major,
unavailable tool/registry, shallow clone and temporary rollback behavior.

The corrected model and native fixtures use implementation commit `c6a269f9b933672cd6962a5b7841190d3621249e`.
The final evidence commit also repairs only the Windows test harness and adds
reports/logs; production selector/package bytes are identical. Exact final-head
source/export and CI results belong in the canonical Outcome.
