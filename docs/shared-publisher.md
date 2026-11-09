# Shared source-only VibeVM publisher

The reusable Python CLI and workflow live outside the Development Governance
package. [Task 51](https://github.com/jresearchsoftware/shared-governance/issues/51)
corrects ordinary publication under its explicit Owner Decision. The
[producer release entrypoint](releases.md) describes this producer's local caller,
producer-specific readiness, cutover and historical-source recovery. Its migration
PR requires independent acceptance and authorized integration before activation.
Installing a package does not activate publication.

## Shared credential and destination provisioning

For producers in the approved `jrs-vibevm` public distribution namespace, use the
existing **`DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN`**. No project-specific token is
needed. External callers use the reviewed default branch and pass the named secret:

```yaml
jobs:
  publish:
    uses: jresearchsoftware/shared-governance/.github/workflows/vibe-publisher.yml@main
    with:
      mode: publish
      source_sha: ${{ needs.resolve.outputs.source_sha }}
      binding: vibe-publisher.json
      package: org.example/package
    secrets:
      DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN: ${{ secrets.DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN }}
```

Here `resolve` is the caller-owned exact-event SHA resolution job, as in
[this producer's caller](../.github/workflows/publish.yml). The caller still owns
its event filtering and source/readiness checks. The secret
must be visible **in that caller repository** through the existing organization
Actions secret's repository-access policy (or the existing repository arrangement).
A secret stored only in Shared Governance is not available to another producer,
and reusable workflows do not automatically receive caller secrets. The existing
`publish_token` mapping remains a compatibility alias; the established named input
takes precedence if both are supplied. Never use `secrets: inherit`, copy a token
into source, or create a separate token for each producer. An authorized secret
administrator can extend access to the existing organization secret when needed;
this implementation does not change secrets/settings. See GitHub's
[secret access rules](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
and [reusable workflow secret mapping](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

Only an exact source-bound `https://github.com/jrs-vibevm/NAME.git` destination
is eligible for automatic creation. Other existing destinations keep their prior
publication path; this is not general organization provisioning. For a qualified
changed package, credential-free staging first reads the public destination via
Git. A Git-accessible existing destination uses ordinary clone/stage/publication
without REST lookup, including when REST is forbidden, rate-limited or unavailable.
Only failed Git access enters the extra REST path. An unauthenticated 404 permits
local staging against an empty bare repository with `main` as HEAD; it does not
prove absence or authorize creation.
The pinned native publisher must finish successfully before any remote create.
No bootstrap commit or remote initialization push is needed: the normal single
atomic non-force push publishes both main and the new immutable tag.

Finalization first reads Git refs and follows the ordinary atomic push/readback
path when accessible. Existing Git-accessible repositories receive no REST,
creation or metadata request. If Git access fails, finalization uses the injected
token to verify the exact destination and public visibility.

The supported missing-destination credential contract is the owner's explicitly
confirmed complete visibility of `jrs-vibevm`: the token's user can access **every**
repository in that organization, and the fine-grained token selects all current
and future repositories with Metadata read. The established token also has
Contents write and Repository creation write. `All repositories` alone is
insufficient if its user cannot access some organization repositories. This is
an owner-confirmed configuration premise, not a claim that secret metadata or a
successful `/user` response introspects the injected token's repository selection.
Do not use a selected-repository, public-only or otherwise visibility-limited
credential for missing destinations. If the premise is no longer established,
stop for owner disposition before this path; do not substitute/escalate tokens.
The owner explicitly confirmed both user and token coverage during
[Task 58 Step 3](https://github.com/jresearchsoftware/shared-governance/issues/58#issuecomment-6316903618).

Under that premise, finalization verifies authenticated user identity with
`GET /user`, rejects malformed/failed/SSO-restricted authentication and refreshes
the exact repository lookup before POST. A naked unauthenticated 404 authorizes
only local staging. Neither classic `repo` scope nor organization-owner membership
is required. GitHub's [creation endpoint](https://docs.github.com/en/rest/repos/repos#create-an-organization-repository)
supports fine-grained Repository creation write; GitHub enforces the user's
organization policy and actual create permission at POST. Missing permission
fails without a push. A [masked private 404](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api#404-not-found-for-an-existing-resource)
cannot be distinguished by this tool if the confirmed visibility premise is false;
it is not silently treated as runtime-proven completeness. A hidden existing
name cannot be converted to public by the create-only endpoint; unsuccessful
creation or non-public/inconclusive readback cannot authorize publication.

After a refreshed 404, POST only the bound repository name with `private=false`
and `auto_init=false`, then verify its identity/public visibility by readback.
On this fallback path, 403, redirects, throttling, transient GET failures, private resources and wrong
identities never become creation permission. A 422 name race or ambiguous POST
transport is reconciled by exact public destination readback before any push;
failed readback stays pending. There is no blind create retry, visibility change,
deletion, force push or metadata repair. A created empty repo may remain after a
later failure; rerun the same source to reuse it. No-op and existing
release tags do not create repositories. API errors and reports expose safe codes
without raw response bodies or credentials.

## Invocation and source eligibility

A producer accepts its own source-committed JSON binding and thin caller. External
callers use `.github/workflows/vibe-publisher.yml@main`; Shared Governance uses
`./.github/workflows/vibe-publisher.yml`, from the same commit as its caller.
Future accepted implementation updates therefore become available centrally.
Pass the **exact triggering
main-push CI commit** as `source_sha`, a repository-relative `binding` path and
one `package` coordinate. Never reread moving main to select the release.
There is no separate `policy_sha`, policy checkout, caller `publisher_sha` or
publisher-selection input. The workflow checks out its own implementation using
`job.workflow_repository` / `job.workflow_sha` and independently checks out the
producer at `source_sha`. The binding is read from that same Git commit, never
the worktree. GitHub context describes the caller, not the reusable code identity.
The producer readiness CLI accepts `--publisher-sha` only as an assertion of
`job.workflow_sha`, never as a second independently selected implementation.
Its adapter and publisher checkout come from that executing workflow revision,
while `--source` selects the independent exact producer checkout. Workflow summaries
and temporary CLI reports record the publisher repository and resolved SHA.
The workflow identity contexts are documented by [GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#job-context).

Moving `@main` changes selection for future invocations, not the source SHA being
released. GitHub reruns of a failed job or a specific job retain the original
called workflow commit; rerunning all jobs can resolve the branch again. A new
same-source dispatch may likewise use a newer accepted publisher. Each execution
records its implementation and repeats source/CI/export qualification; old tags
remain immutable. A staged report from another implementation is rejected before
finalization. See [reusable workflow rerun behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations#behavior-of-reusable-workflows-when-re-running-jobs).
Other producers, including Landscape's historical full-SHA caller, need separately
authorized workflow migrations; this producer's change does not edit them.

The [illustrative binding](../tooling/vibe-publisher/examples/shared-governance.json)
identifies repository name/numeric ID, source branch, qualifying CI workflow,
package coordinates, stable roots, export adapters and one destination per
coordinate. Ordinary bindings need no `acceptance`, `authorized_integrators`,
`baseline`, `baseline_disposition` or historical inventory attestations.

Ordinary planning checks first-parent source-main membership and first compares
that commit with its immediate first parent. Candidate `check` instead compares
against the exact current accepted main supplied as `--base`. If the immediate
prior commit has a binding, its own package inventory selects its export; a new
allowlist cannot hide a current inventory change. At late onboarding, an absent
prior binding **or an absent coordinate in an existing binding** is normal:
compare the preexisting package source under the new inventory. Adding a binding
entry alone cannot release unchanged old source; a genuinely new package or
changed new version still follows ordinary qualification.
Identical exported payloads then check for the bounded current-version recovery
below. Without an eligible recovery they return `NO_PACKAGE_CHANGE` before
readiness, CI/trigger queries, destination access, credentials, tool preparation
or staging. This preserves late-onboarding no-ops, including unchanged historically
incomplete licenses or unresolved rights. A non-package commit does not create a
new version or select an arbitrary older release.

`--package` selects the coordinate before export/readiness and CI/trigger work,
in both ordinary and explicit initial-publication planning. A selected unchanged
B without an eligible recovery returns its own no-op even if sibling A changed,
without A's API/CI, trigger, destination or staging work. Calls without a package selection still assess each
coordinate. Staging associates decisions with bindings by coordinate, preserving
the selected payload/destination even when it is not the first binding entry.

For a changed package, require a valid authored frozen version, a **different**
version from the immediately preceding accepted payload, complete approved public
files, license/redistribution readiness, and successful completed **push** CI at
that exact source SHA, repository ID, branch and workflow path. Read all API
pages. For `workflow_run`, also retrieve and verify the actual triggering run ID.
A source outside first-parent main, wrong/missing CI or same-version change fails.
Squash, ordinary merge, rebase and direct-main changes are supported; the publisher
performs no PR association, owner/integrator/reviewer lookup or merge-method audit.
Producer-specific review, integration, bump-category and arithmetic controls stay
with producer CI/policy. No `Package bump:` annotation is required by this tool.

Changed-version planning retains Task 51's ordinary transition qualification:
there is no reconstruction of historical CI, PR acceptance or owner decisions,
and a new correctly versioned release can qualify without old publisher records.
The immediate transition still detects package removal and changes to an existing
root/adapter/destination mapping; these need producer-owned migration disposition.
Source/review/versioning policy still applies at its own boundaries.

### Recovery after a package-neutral CI repair

A successful current-source CI can recover the **current** version when the coordinate was already publisher-bound
before that version was introduced. Source Git history supplies focused evidence of that boundary;
it does not infer a release request from an old package discovered at onboarding.
Initial publisher onboarding, an unbound old package and an unchanged
onboarding entry retain the existing no-op path. A genuinely new package created
after its coordinate was bound can recover its first version too. Explicit historical initial
publication remains the separately authorized operation below.

For a package-neutral trigger, inspect only history affecting the current package
root or its binding to identify the first accepted frozen occurrence of the current
coordinate/version. Earlier unrelated versions do not acquire new readiness duties.
The version must retain its original approved inventory, disclosure, root, adapter,
destination and payload, including intervening same-version edits later reverted.
The original frozen source and current source must both satisfy license/rights and
included dependency-closure readiness; later source cannot complete an unready
frozen release in place. Repository identity remains bound throughout recovery.
Missing or incompatible evidence is `AUTHORIZATION_PENDING`, never a silent skip.
This is a source-only check for one current version, without a ledger, historical
CI/PR fabrication, removed owner audits or a general publication bypass.

Qualify successful **push** CI for the exact current trigger SHA, and verify the
actual triggering run for `workflow_run`. The original failed CI remains failed;
this does not qualify a direct retry of that old source. The report's top-level
`source_sha` and per-package `trigger_sha` identify current CI, while per-package
`source_sha` identifies the first frozen source exported for staging, including
its original `DISTRIBUTION.json` provenance. No payload edit or version bump is
needed. `READY` means eligible but still unpublished until staging/finalization.

After exact source/CI and automatic-trigger qualification, planning reads the real
remote recovery tag **before downloading VibeVM**. An existing recovery tag is fetched and
compared with the complete frozen export, including its receipt. A matching tag
returns `ALREADY_PUBLISHED` / `EXISTING_PAYLOAD_CONFIRMED` without native publication
or any ref write, even on later package-neutral accepted commits when the native
download is unavailable. A mismatch returns `FAILED_OR_PENDING` / `RECOVERY_TAG_MISMATCH`;
unavailable planning readback stays pending as `RECOVERY_READBACK_FAILED`.
Staging/finalization repeat the check for concurrent tags.
Absent tags use the existing credential-free native staging and atomic non-force
publication. `PUBLISHED_CONFIRMED` still requires exact staged-tag readback.

Shared Governance's manual **Publish accepted package** form accepts an optional
`source_sha`. Omitted or empty means the exact dispatch-event `github.sha` of the
selected `main`, captured once before checkout; it never rereads moving main to
select a source. An explicit full lowercase SHA retries that accepted source.
The single resolved SHA drives checkout, readiness/CI, publication concurrency,
the reusable invocation and reporting. Automatic publication retains the exact
successful `workflow_run.head_sha`. Non-main dispatches, malformed or inconsistent
event inputs, sources outside first-parent main and unqualified exact push CI
cannot reach a distribution write. A later movement of main cannot replace the
captured dispatch source.

Each producer owns its form. This shared implementation cannot make Codex Relay's
currently required caller input optional. The [tracked producer continuation](task-94/step-1/relay-continuation.md)
requires its own authorized change and independent review before claiming that UI
is fixed. The [actual Relay replay](task-94/step-1/README.md) qualifies source/CI and
local native publication, without granting public publication permission.

## Export and readiness

`shared-governance-v1` reuses the existing exporter from the workflow implementation
pin against exact producer Git objects. Its payload/receipt schema, license,
passivity and separate dependency-free package contract are unchanged.

`tree-v1` exports only explicit ordinary Git blobs beneath a stable root:

```json
{
  "coordinate": "org.fixture/example",
  "root": "packages/example",
  "adapter": "tree-v1",
  "files": ["vibe.toml", "README.md", "LICENSE"],
  "redistribution": {
    "status": "approved",
    "license": "MIT",
    "approval": "https://github.com/OWNER/PRODUCER/issues/N#issuecomment-ID"
  },
  "disclosure": "opaque",
  "destination": "https://github.com/OWNER/example.git"
}
```

The public LICENSE must be nonempty and authored manifest/license metadata must
match the approved license. The owner-selected redistribution acknowledgement
requires `status=approved` and an actual applicable owner decision/reference URL;
it can cover later releases while the content/rights/license remain applicable.
No new per-release approval is implied. The tool does not legally verify arbitrary
content, invent rights or complete a frozen release after acceptance.

The explicit inventory and disclosure choice remain accepted cross-producer
configuration obligations. `opaque` omits source SHA/path from the generated
receipt; `public-source` includes them. Neither mode removes private references
embedded in approved source text. Producers own public-file approval, self-contained
links and disclosure review. A private sibling file outside the allowlist is never
copied implicitly. Producer-specific content checks remain necessary.

Tree-v1 supports thin dependency-bearing packages. Before publication it reads
the native `vibe.lock` (schema 7) and versioned
`vibevm/vibedeps/<group>.<name>/<version>/` slots committed **beneath the package
source root at the exact source SHA**. Ordinary VibeVM resolution/materialization
produces this source-time qualification evidence before frozen source acceptance.
It need not appear in `files` or the public payload. Required direct/transitive
dependencies and any deliberately exported slots are qualified; unrelated source
slots do not enter the release closure. Each selected dependency needs a
matching resolved identity/source, frozen manifest, tool-produced content hash and
native `.vibe-slot.toml` inventory/hashes matching the qualified bytes. Exact
requirements and explicit Git source declarations must agree with the lock.
Missing required direct/transitive evidence or unqualified slots produce
`DEPENDENCY_CLOSURE_UNQUALIFIED`. Selection/range solving remains VibeVM-owned;
this check inspects its committed resolution, without a second resolver, dependency
ledger, live downloads or additional materialization during publication.

Only explicitly approved `files` enter the release and receipt. Deliberate
vendoring remains supported: each exported slot must have its complete shipped
inventory; unexported source bytes cannot fill a partial export. A source-only lock
can qualify these slots too. Existing frozen vendored distributions stay intact.
A thin release carries its own unchanged manifest requirements; native consumer
installation resolves them through the consumer's configured registries or explicit
Git roots and writes the consumer's own lock/slots. A producer lock does not force
that consumer's dependency selection. Offline acquisition needs retained native
consumer evidence/cache or an explicitly supported local source; thin publication
does not promise a self-contained offline bundle. See the bounded
[Task 67 qualification](task-67/step-1/README.md).

Excluded development/optional declarations are outside the included closure;
included dependencies are qualified irrespective of their label. An empty closure
is trivial. Native VibeVM 1.0.7 supports optional suggestions via `[suggests]`, but
**rejects `dev-requires` and inline `optional=true` as unknown manifest fields**.
The planner no longer invents a blanket rejection for these; actual native staging
still fails on unsupported native syntax. This is a disclosed upstream schema
limit, not proof that such manifests can publish. Do not rewrite frozen manifests
or claim broader native support. Native fixtures cover frozen direct/transitive
publication, excluded suggestions, included mutable/unresolved/hash failures and
the existing dependency-free path.

## CLI and publication mechanics

Python 3.11+ and Git suffice for planning:

```sh
python3 tooling/vibe-publisher/publisher.py plan \
  --source /path/to/producer --source-sha FULL_SOURCE_SHA \
  --binding publisher.json --package org.fixture/example \
  --report /tmp/publication.json
```

For unprivileged candidate CI replace `plan` with `check` and add
`--base FULL_ACCEPTED_MAIN_SHA`; `--main` selects accepted source-main history.
Checks make no API/destination calls and return `CANDIDATE_VALID` for a valid
changed candidate or `NO_PACKAGE_CHANGE`. Candidate validation grants no acceptance
or publication authority. `GH_TOKEN` is for read-only source CI, never distribution.

`stage` repeats the source plan and uses `--vibe /path/to/pinned/vibe` plus
`--directory /tmp/disposable-stage`. An existing `vVERSION` tag skips before native
invocation; pending recovery additionally verifies its exact frozen export. Otherwise clone the distribution into disposable bare staging, recheck
the tag, and publish exact exported bytes there using the pinned VibeVM 1.0.11 musl
binary. Native subprocesses receive isolated settings and no API/publication token,
askpass or global Git credentials. `finalize --report ...` alone receives the shared
publication token for API verification/creation and ephemeral Git askpass.
One call covers one coordinate; never
use `secrets: inherit`. Tokens are not stored in URLs, artifacts or logs.

Push main and the new tag with one atomic non-force push. A concurrent tag creation
or divergent main rejects the complete push; no two-push fallback exists. Existing
tags are always retained. There is no global highest-version gate; distribution
main means last published. Ambiguous transport is reconciled by exact staged-tag
object readback. A competing tag is retained with a warning; unavailable readback
stays pending. An existing tag does not prove a different retry source was published.

Reports distinguish `NO_PACKAGE_CHANGE`, `CANDIDATE_VALID`, `AUTHORIZATION_PENDING`,
`READY`, `STAGED`, `PUBLISHED`, `ALREADY_PUBLISHED` and `FAILED_OR_PENDING`. Logs and
Actions summaries expose allowlisted diagnostic codes, never raw private errors or
reports. Reports remain temporary and are not uploaded. Retry a failed/partial
release with the **same source SHA**. Prefer rerunning the failed job to retain its
resolved implementation; a new dispatch may use a later accepted publisher and
records that revision while requalifying the same source. A successful
sibling skips its tag while the failed sibling resumes. Caller concurrency groups
should include producer/source/coordinate with `cancel-in-progress: false`.

## Explicit first publication of pre-onboarding source

The opt-in [Task 49](https://github.com/jresearchsoftware/shared-governance/issues/49)
operation is preserved for previously unbound old frozen tree-v1 source. Ordinary
onboarding never selects it or publishes old 1.0.1 automatically. Its **isolated**
binding additionally retains `acceptance: owner-squash-attestation-v1`,
`authorized_integrators` and per-package:

```json
{
  "baseline_disposition": "https://github.com/OWNER/PRODUCER/issues/N#issuecomment-ID",
  "initial_publication": {
    "source_sha": "FULL_FIRST_ACCEPTED_VERSION_SHA",
    "version": "1.0.1",
    "payload_sha256": "64_LOWERCASE_HEX_DIGITS_FROM_APPROVED_EXPORT"
  }
}
```

These attest exact old source/version/export bytes and explicit owner disposition.
Use the normal single-source CLI plus `--initial-publication`, or workflow
`initial_publication: true` (default false). `source_sha` is the onboarding initiation;
its binding identifies the frozen payload commit. The removed policy/publisher SHA
arguments are removed here too; old callers must update their interface.

The frozen source must precede onboarding on first-parent main and be the first
integration of that version under the approved inventory. Old-source owner squash
acceptance remains separate from onboarding owner squash **and current push CI**;
no historical CI is invented. Existing earlier bindings cannot be overridden.
Current/frozen exports and observed occurrences of the attested version must match.
Only the integration introducing the declaration initiates; retaining it on later
factual commits cannot reinitiate. Candidate checks are offline and cannot stage.
Compute the digest with `snapshot(producer, FROZEN_SHA, package)[1]['payload_sha256']`.
Rights, inventory, disclosure and destination remain producer-approved. Staging
exports frozen source, while reports retain distinct initiation/source acceptance
and onboarding CI. Tag/race/retry safeguards are shared with ordinary publication.
Later ordinary versions use the immediate-transition path above, not this audit.

## Qualification and remaining ownership

```sh
python3 tooling/vibe-publisher/test_publisher.py
python3 scripts/test-publication-dispatch.py
python3 tooling/vibe-publisher/test_publisher.py --vibe /absolute/pinned/vibe
python3 scripts/test-release.py --vibe /absolute/pinned/vibe
```

All fixture distribution writes use disposable local bare repositories. See
[Task 51 Step 1 qualification](task-51/step-1/validation.md) for primary results,
remaining differences and native limits. Synthetic CI fixtures and the read-only
GitHub CI probe do not prove real private callers, credential availability, live
publication or independently authenticated review. Linux x86_64 is the native
execution environment. Source acceptance, producer cutover, public publication,
consumer adoption and Task closure remain separate owner boundaries.
