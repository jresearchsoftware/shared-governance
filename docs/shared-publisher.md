# Shared source-only VibeVM publisher

The reusable Python CLI and workflow live outside the Development Governance
package. [Task 51](https://github.com/jresearchsoftware/shared-governance/issues/51)
corrects ordinary publication under its explicit Owner Decision. The active
[producer-local release entrypoint](releases.md) remains in service; cutover is
separately owned by Task 53. Installing a package does not activate publication.

## Invocation and source eligibility

A producer accepts its own source-committed JSON binding and thin caller. Pin
`.github/workflows/vibe-publisher.yml` in `uses: ...@FULL_COMMIT_SHA`, or use the
supported local reusable-workflow reference. Pass the **exact triggering
main-push CI commit** as `source_sha`, a repository-relative `binding` path and
one `package` coordinate. Never reread moving main to select the release.
There is no separate `policy_sha`, policy checkout, caller `publisher_sha` or
`--publisher-sha` argument. The workflow checks out its own implementation using
`job.workflow_repository` / `job.workflow_sha` and independently checks out the
producer at `source_sha`. The binding is read from that same Git commit, never
the worktree. GitHub context describes the caller, not the reusable code identity.

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
askpass or global Git credentials. `finalize --report ...` alone receives the named
destination token through ephemeral askpass. One call covers one coordinate; never
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
release with the **same source SHA and workflow implementation pin**. A successful
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
