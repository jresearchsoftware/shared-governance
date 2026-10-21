# Task 58 Step 3 — Fine-grained credentials and moving publisher implementation

Authority: [Step 3 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/58#issuecomment-6316582552)
and the [owner's explicit complete-visibility clarification](https://github.com/jresearchsoftware/shared-governance/issues/58#issuecomment-6316903618).
Independently accepted source-main and guidance remain frozen at
`0998199043c228237dcdd6bc6ffe777c825ca1d5`. PR 59's Step 1/2 Outcomes, Change
Request, independent acceptance and squash integration remain historical records.
The clean old task branch was preserved; this separate candidate starts from
accepted main on `codex/task-58-step-3`. No reset, force push or package change.

## Credential contract and correction

The owner confirmed in the execution conversation that the token's user also
has access to every repository in `jrs-vibevm`, and explicitly instructed us to
proceed on that basis. Combined with the reported fine-grained token's all-current-
and-future repository selection and Metadata read, this supplies the complete
visibility premise. It is **owner-supplied configuration evidence**, not runtime
introspection of the injected Actions secret. The clarification is recorded
attributably on the Task, separately from the canonical execution Outcome.

Remove the unconditional classic `repo` scope and active org-owner membership
checks. Successful authenticated `GET /user` validates a well-formed user identity
without additional fine-grained permissions; it does not prove token selection.
Refresh the exact bound destination lookup, then use only the public create
endpoint with the source-bound name and `auto_init=false`. GitHub enforces
Repository creation write and organization policy. Unknown/failed authentication,
SSO, private/wrong identity, redirect, throttling and transient GET results cannot
authorize POST. Missing create permission cannot cause a push. The supported
credential must retain the owner-confirmed full visibility; if that premise is
withdrawn, missing-destination provisioning needs owner disposition. No selected-
repository credential or public-only token is represented as safely absence-aware.

The existing Git-first path still stages and publishes an accessible public
destination without REST, including REST 403/429/503/outage scenarios. Existing
repos receive no create or metadata mutation. No-op/retained tags skip creation;
source/CI/version/rights/export/dependencies and secret-free native staging precede
create. Empty-repo initialization, public readback, race/ambiguous transport
reconciliation, immutable tags, atomic non-force main/tag push and same-source
retry remain. No token value, secret setting or actual destination was accessed
or changed to qualify this implementation.

Current primary GitHub documentation inspected on 2026-10-21:

- [Create an organization repository](https://docs.github.com/en/rest/repos/repos#create-an-organization-repository): fine-grained Repository creation write (or Administration write), authenticated organization membership and server policy; public creation and disabled auto-init are explicit request parameters.
- [Get authenticated user](https://docs.github.com/en/rest/users/users#get-the-authenticated-user): fine-grained PAT support without additional permissions. This is authentication evidence only.
- [Masked private-resource 404](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api#404-not-found-for-an-existing-resource): a 404 by itself proves neither absence nor full visibility.
- [October 13 permission update](https://github.blog/changelog/2026-10-13-github-app-improvements-for-least-privilege-and-management/): repository creation permission is available for fine-grained PATs and GitHub Apps. This implementation supports the owner's PAT model; it does not claim App-installation `/user` compatibility.

## Moving implementation and exact producer source

The active producer uses `./.github/workflows/vibe-publisher.yml`. Readiness checks
out the publisher and its adapter using the caller's `job.workflow_sha`; the local
reusable workflow comes from that same caller commit and independently checks out
its implementation using its own `job.workflow_repository` / `job.workflow_sha`.
The producer source remains the exact triggering CI or explicit retry source SHA.
Readiness runs the workflow revision's adapter against that independent source,
so a historical source checkout cannot restore an obsolete implementation pin.
The readiness CLI asserts its actual publisher checkout matches the workflow SHA.
Reports record publisher repository/SHA; CLI finalize rejects missing or different
implementation identity before destination access. Temporary staging reports are
not a cross-version recovery format: repeat staging for the same source instead.

External documented callers use `@main`. Previously accepted full-SHA callers
remain valid but need separately authorized migrations to receive central updates;
Landscape and other repositories were not changed. No new credential input,
producer policy service, inventory ledger, permission escalation or package bump.

[GitHub's job context](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#job-context)
documents workflow repository/SHA. [Local reusable calls](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows#calling-a-reusable-workflow)
use the same commit as their caller. [Rerun semantics](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#behavior-of-reusable-workflows-when-re-running-jobs)
retain the original called commit for failed/specific-job reruns; rerun-all with
an external moving ref may resolve it again. A fresh same-source dispatch may
use a newer accepted implementation. Each run records identity, repeats source
qualification and preserves existing tags; it never silently publishes new HEAD.

## Qualification and limits

Disposable Debian native-filesystem clone, Python 3.11, digest-verified VibeVM
1.0.7 musl (`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`).

| Check | Result / primary log |
| --- | --- |
| Publisher with pinned native tool | [93 passed, no skips](logs/publisher-native.log) |
| Producer CLI and native integration | [12 passed, no skips](logs/publication-native.log) |
| Release/native publication boundary | [17 passed, no skips](logs/release-native.log) |
| Distribution/export | [48 passed](logs/distribution.log) |
| Self-adoption | [13 passed](logs/self-adoption.log) |
| ChatGPT projection | [24 passed](logs/projection.log) |
| Exact-commit source/export qualifier | [PASS](logs/qualification.log) |

Total **207 passed, zero skips**. Publisher/producer logs include fine-grained
authentication with no classic scope or owner lookup, malformed/authentication/
refresh failures, create permission denial, private-name race/readback failure,
native absent-destination stage/create/atomic first push and failed-push retry,
existing Git publication with zero REST calls, no-op, source-bound gates and
immutable-tag races. A real CLI fixture advances the publisher Git checkout twice
while retaining one older changed producer source, qualifies that source with both
implementations, and rejects a mismatched checkout SHA. Report identity mismatch
is rejected before destination access. API responses are simulated; native staging
and local Git publication are real disposable operations.

An initial test run caught misuse of the exact-source validator while recording
implementation HEAD; the implementation now resolves its own Git HEAD separately.
The affected full publisher suite was rerun successfully. Later evidence-only
commits do not alter tested implementation bytes. Exact final-head Actions and
source qualification are identified in the canonical Outcome.

No live provisioning, injected-token capability/approval, private producer caller
or production release was tested. The owner's complete visibility is an explicit
premise; successful authentication does not independently prove it. Existing
VibeVM unsupported dependency-manifest syntax and the historical read-only CI
fixture probe retain their prior disclosed limits in Steps 1/2. The fixture's
production plan/stage/finalize steps remain unprivileged skips; native tests
exercise those paths locally. Workflow event execution of a real accepted release
is a later boundary. Package 4.0.0 bytes/native projections are unchanged.

This is Manual Codex implementation evidence, not independent acceptance. The
canonical Outcome belongs to the single result PR, followed by verified Ready
state and a stop for fresh independent exact-head review. No merge, release,
consumer migration, secret/settings change, live destination create or Task closure.
