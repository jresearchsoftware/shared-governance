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
      source_sha: ${{ github.event.workflow_run.head_sha || inputs.source_sha }}
      binding: vibe-publisher.json
      package: org.example/package
    secrets:
      DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN: ${{ secrets.DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN }}
```

The caller still owns its event filtering and source/readiness checks. The secret
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
The owner explicitly confirmed both user and token coverage during Task 58 Step 3.

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

Ordinary planning checks first-parent source-main membership and compares only
that commit with its immediate first parent. Candidate `check` instead compares
against the exact current accepted main supplied as `--base`. If the immediate
prior commit has a binding, its own package inventory selects its export; a new
allowlist cannot hide a current inventory change. At late onboarding, an absent
prior binding **or an absent coordinate in an existing binding** is normal:
compare the preexisting package source under the new inventory. Adding a binding
entry alone cannot release unchanged old source; a genuinely new package or
changed new version still follows ordinary qualification.
Identical exported payloads return `NO_PACKAGE_CHANGE` before readiness,
CI/trigger queries, destination access, credentials, tool preparation or staging.
This includes unchanged historically incomplete licenses or unresolved rights.
A non-package commit never opportunistically releases an earlier version.

`--package` selects the coordinate before export/readiness and CI/trigger work,
in both ordinary and explicit initial-publication planning. A selected unchanged
B returns its own no-op even if sibling A changed, without A's API/CI, trigger,
destination or staging work. Calls without a package selection still assess each
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

There is deliberately no reconstruction of earlier binding/CI/owner decisions,
first-accepted unpublished version inventories or historical baselines. The owner
accepted this reduced historical assurance in Task 51. Source/review/versioning
policy still applies at its own boundaries; existing public tags stay immutable.
A new correctly versioned release can qualify without old publisher records.
The immediate transition still detects package removal and changes to an existing
root/adapter/destination mapping; these need producer-owned migration disposition.
No history scan or adoption ledger substitutes for the removed audit.

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

Tree-v1 no longer rejects dependency declarations. Before publication it reads
the **actually exported** native `vibe.lock` (schema 7) and versioned
`vibevm/vibedeps/<group>.<name>/<version>/` slots, including transitives. Include
these files explicitly in `files`; ordinary VibeVM resolution/materialization
produces them before frozen source acceptance. Each included dependency needs a
matching resolved identity/source, frozen manifest, tool-produced content hash and
native `.vibe-slot.toml` inventory/hashes matching the shipped bytes. Missing
required direct/transitive slots or unqualified included slots produce
`DEPENDENCY_CLOSURE_UNQUALIFIED`. No resolver, dependency ledger, live downloads
or additional materialization during publication is introduced.

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
invocation. Otherwise clone the distribution into disposable bare staging, recheck
the tag, and publish exact exported bytes there using the pinned VibeVM 1.0.7 musl
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
