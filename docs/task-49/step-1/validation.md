# Task 49 Step 1 — initial publication qualification

Authority: [Task 49 charter](https://github.com/jresearchsoftware/shared-governance/issues/49)
and [conditional Step 1 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/49#issuecomment-6266210920).
Frozen independently accepted source-main: **9caedb8a073d030a5a9b4e721cfd8430b002debd**.
Verified current origin/main and owner-merged PR 46 against its exact-head
independent Step 8 assessment and source Git facts. This binding does not move
with candidate instructions. Interactive executor: Manual Codex; no helper agent
or independent acceptance is claimed.

## Proven gap and smallest paths

The disposable [reproducer](reproduce.py) creates canonical unbound 1.0.0 history
without LICENSE, accepted licensed 1.0.1 without prior binding/push CI, then a
binding-only onboarding integration with baseline disposition. Both coordinates
return these results from the **ordinary accepted publisher path**:

| Input | Status | Reason |
| --- | --- | --- |
| Original frozen 1.0.1 source | AUTHORIZATION_PENDING | HISTORICAL_BINDING_UNRESOLVED |
| Later binding-only onboarding | AUTHORIZATION_PENDING | HISTORICAL_BINDING_UNRESOLVED |
| Subsequent unrelated direct-main evidence | NO_PACKAGE_CHANGE | No release |

Reproduced against the accepted implementation before editing and again through
the unchanged ordinary path in this candidate. Baseline disposition alone does
not resolve missing historical export policy and does not initiate an unchanged
release. No historical CI was invented or counted as green.

- Existing configuration alone: insufficient for this case, as reproduced.
- Recommended compatible addition: explicit initial-publication operation under
  an independently accepted binding; exact frozen SHA/version/export digest,
  independently checked source owner squash, accepted onboarding owner squash
  and matching current push CI. Reuses baseline disposition and existing export,
  readiness, staging, no-overwrite and retry machinery. Adds no standing state.
- Ordinary 1.0.2 source release: a forward repair/version change is valid only
  under separately accepted producer authority and ordinary history qualification;
  it does not satisfy the owner's exact-1.0.1 objective. Rewriting old CI, a
  fake package delta or a broad skip-checks switch is not a compatible solution.

The optional bounded operation is explicitly admitted by the Owner Decision.
No mandatory operator work or new security gate is added to existing callers.
Its accepted onboarding PR is the authority/readiness event; source acceptance
and current readiness evidence remain separately named in the report. The
[operator procedure and contract](../../shared-publisher.md#explicit-first-publication-of-pre-onboarding-source)
define caller pins, candidate checks, initiation, disclosure and retries.
No shared package bytes or normative protocol changed, so development-governance
remains accepted 3.0.0 and no package bump/publication is requested.

## Qualification and evidence

Clean independent Debian WSL Git clone, Python 3.11.2, Linux x86_64. Pinned native
VibeVM 1.0.7 musl SHA-256:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
All distribution writes used fixture-owned **local bare repositories**.
Primary logs below qualify runtime implementation revision
`297aa42dac4f9cdc70ebf81e3416a8cf2f0d70b7`; later candidate refinements add CLI
coverage and evidence only. At `37174f9fea744b8cfecae8643f68bdeb8238edfa`, the [final native rerun](publisher-final.log) passes all **64 publisher tests, zero skips**, including the added actual CLI check; exact-commit source qualification passes (720 tracked files, 1,137 local links). Final-head GitHub CI is bound by the canonical Outcome.

| Command | Result | Primary log |
| --- | --- | --- |
| `python3 docs/task-49/step-1/reproduce.py` | Exact ordinary statuses above | [reproduction](reproduction.log) |
| `python3 tooling/vibe-publisher/test_publisher.py --vibe PINNED_VIBE` | 63 passed, zero skips at implementation revision | [publisher](publisher.log) |
| `python3 scripts/qualify.py --export-ref HEAD` | PASS, source/export/native consistency and bounded credential-marker scan | [qualifier](qualify.log) |
| `python3 scripts/test-distribution.py` | 47 passed | [distribution](distribution.log) |
| `python3 scripts/test-release.py --vibe PINNED_VIBE` | 17 passed, zero skips | [release/dependencies](release.log) |
| `python3 scripts/test-self-adoption.py` | 13 passed | [self-adoption](self-adoption.log) |
| `python3 scripts/test-chatgpt-projection.py` | 24 passed | [ChatGPT](chatgpt.log) |
| `python3 scripts/package-release.py --source-ref HEAD --base ACCEPTED_SHA` | unchanged 3.0.0, no bump | [release boundary](boundary.log) |
| `git diff --check ACCEPTED_SHA HEAD` | PASS | No whitespace diagnostics |

New fixtures exercise both packages, no historical CI, missing/failed/mismatched
current CI, forged/wrong/unmerged owner records, separate old-source acceptance,
wrong version/source/digest, missing rights/public files, opaque vs public-source
receipts, changed frozen bytes and first-integration identity, existing historical
policy rejection, irrelevant commit/no-op, same-initiation retry and offline
candidate checks that cannot stage. One extra CLI regression exercises the actual
`check --initial-publication` entrypoint, including mismatched source/policy pins.

The fresh native initial-release test publishes A locally, injects B failure,
then reruns the same pins: A is ALREADY_PUBLISHED and B becomes PUBLISHED. Each
v1.0.1 distribution blob equals the frozen snapshot export; no private sentinel
or v1.0.0 tag is present. The full native publisher suite also freshly exercises
existing-tag bypass before binary invocation, same/different-version races,
ambiguous push readback and private-file boundaries. The release suite exercises
frozen transitive closure, snapshot rejection and deliberate dependency updates.
These integration probes add no recurring native requirement for ordinary users.

## Limits, ownership and stopping point

The mechanism deliberately **does not reconstruct historical publisher bindings**.
Preexisting historical policy is rejected by initial publication, and ordinary
subsequent releases retain their complete history/CI eligibility checks. A later
ordinary package change in a formerly unbound producer can still be pending for
missing history; a successful initial release is not full subsequent-release
onboarding. Stable root and approved export inventory/rights are explicit owner
attestations, not a claim that current policy existed in the past. Source/CI API
fixtures are synthetic; they do not independently prove real review identity.

Source inspection reverified Landscape PRs 5/6/8 and the 1.0.1 squash
638fbd7ca3c4ef778c9a371c9e6f5b9433c780cd. Its API reports zero check runs and zero
push workflow runs at that source; these observations do not claim fresh
qualification of its private payload. Landscape separately owns its exact public
inventory and actual notices/third-party rights, disclosure selection, readiness
source tests, accepted binding/caller/CI and initial-publication Decision,
destinations/visibility/creation, one narrow credential per distribution and
activation. Destination writes need only that distribution's Contents permission;
source API evidence uses read-only source access. Consumer adoption stays separate.

No Landscape writes, private source copy, real distribution ref/tag/release,
credential/setup, production activation, merge, adoption or Task closure occurred.
Windows Python covered the initial non-native checks; native qualification is
Linux x86_64 only. Native Windows/macOS and actual private caller/credential/
public distribution integration remain unqualified. Reusable workflow CI uses
its unprivileged fixture and synthetic named-secret sentinel; it does not run
production publication. The implementer stops for fresh independent exact-head
assessment; the conditional agreed implementation can be assessed under Direct,
while any additional policy/architecture choice requires owner disposition.
