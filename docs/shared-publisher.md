# Shared source-only VibeVM publisher

Task [45](https://github.com/jresearchsoftware/shared-governance/issues/45)
selects one Python CLI/library and one reusable GitHub workflow, outside the
Development Governance package. These are candidate tooling; no producer is
integrated by this change. The current [release entrypoint](releases.md) remains
in service. Source acceptance, remote publication and consumer adoption are
separate. Installing a flow neither executes this tool nor adopts release policy.
Preparation precedes source acceptance: a producer must deliberately adopt and
meet this publisher's readiness contract in its own accepted policy. That does
not require adopting every optional package-versioning topic.

## Producer-owned contract

An integration must independently accept a small JSON binding and a thin caller.
The caller pins `.github/workflows/vibe-publisher.yml` at a full Git SHA and
passes an independently accepted `policy_sha`, binding path, exact `source_sha`
and one package coordinate. A named `publish_token` covers only that coordinate's
distribution. Do not use `secrets: inherit`. One call per coordinate permits
separate least-privilege credentials and independently recoverable results.

The [governance compatibility example](../tooling/vibe-publisher/examples/shared-governance.json)
is illustrative, not an activated production binding. Its schema identifies:

- Source repository name **and numeric ID**, main branch, qualifying push CI
  workflow path, authorized owner integrators and `owner-squash-attestation-v1`.
- Stable package roots, coordinates, per-package accepted baseline commits and
  one credential-free HTTPS GitHub distribution repository per coordinate.
- An exporter adapter, including its public-file and metadata-disclosure contract.
  Authored `[package].version` is canonical; the binding duplicates no version.

Bindings are read from Git at `policy_sha`, never a candidate worktree or a
dispatch-provided `accepted=true`. The separately accepted caller owns that pin
and its event/retry selection. The reusable workflow checks out its own code with
`job.workflow_repository` / `job.workflow_sha`, then independently checks out the
producer's exact source and pinned policy. It rejects a production call whose
workflow reference is not pinned to that full code SHA. Ordinary `github` context
describes the caller; see GitHub's [workflow identity example](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#example-usage-of-job-context-workflow-identity).
Initial support is github.com on Linux x86_64, **squash integration**; rebase,
merge commits and maintenance source lines need a separately qualified extension.

The source must be on first-parent main. A changed package transition requires
exactly one actual merged PR with matching source squash SHA, target repository
ID/branch and authorized `merged_by`, plus successful matching **push** CI from
the bound workflow, repository and source SHA. All API result pages are read.
The report retains PR, reviewed head, integrator and CI references. The owner's
merge attests completed independent assessment under the producer's adopted rule;
it is not authenticated proof of independent review or a prose parser. Local
candidate/version-category checks and review sufficiency remain producer-owned.

Ordinary direct-main research or tooling with no exported payload change returns
`NO_PACKAGE_CHANGE`, without release-readiness or PR/CI eligibility requirements,
including when the unchanged historically accepted payload is incomplete. This
never releases that content or waives an applicable source-time preparation check. A green
direct-main package edit returns `AUTHORIZATION_PENDING`. A later owner squash
cannot launder its accumulated bytes: for a changed package, audit every changed
export on first-parent history from the explicitly accepted baseline to this
source. Every package-bearing transition needs the eligibility evidence. An
unresolved transition stops that package. Owner disposition can explicitly accept
the accumulated delta and establish a new baseline in a separately reviewed
binding revision. Do not advance the baseline automatically or infer that the
later PR accepted the inherited delta. This uses Git/PR/CI records, no standing
ledger. A source-only commit never opportunistically releases earlier changes.

The binding path is also source-controlled historical policy. Start from an
explicitly accepted baseline containing the initial binding, before package
creation if necessary. Each snapshot uses that revision's approved file inventory;
each transition uses its source-time CI path and the preceding binding's authorized
integrators. A binding rotation needs the preceding owner's integration; a new
integrator cannot self-authorize. Older merges are checked against their own
owner/CI evidence, never today's owner list. CI is resolved from exact-source run
records (including the recorded workflow path/ID), so later workflow deletion or
renaming does not require today's workflow-name lookup. Missing historic bindings,
unsupported identity/destination changes or unavailable evidence stay pending.
The caller's separately accepted policy pin must match the final source binding.
No policy history is inferred from current allowlists or an approval boolean.

When earlier package bytes lack eligible acceptance, adding an integrator or
renaming CI is not disposition. An owner may explicitly reconcile the accumulated
delta and pin a new `baseline`, recording its existing Decision URL in
`baseline_disposition`; the pin's external independent acceptance remains required.
That starts a bounded audit, without pretending to prove earlier eligibility.
It does not authorize same-version repairs of already accepted frozen content.

The eligibility audit baseline does not reset version identity. Separately read
the package and binding changes in canonical first-parent Git history up to that
baseline, retaining each version's first source-main payload with its historical
approved inventory. Earlier eligibility need not be replayed after explicit
disposition, but older frozen versions cannot be reused with different bytes,
even without a remote tag. Missing historical policy for package-bearing source
remains pending; today's inventory is not a substitute. Historical root changes
cannot be hidden by advancing the baseline: an unsupported identity/root mapping
still needs producer-owned qualification and disposition. This uses bounded Git
records, not a registry or ledger.

## Export adapters

`shared-governance-v1` invokes the existing governance exporter from the **same
publisher code pin**, pointing it at the exact producer Git objects. Its passive
shape checks, license, historical roots, frozen metadata, complete file set,
generated routing and `DISTRIBUTION.json` schema/bytes are preserved. This
adapter does not impose governance-specific checks on other producers.

`tree-v1` reads an explicit `files` allowlist of ordinary Git blobs under a stable
root. Example package fields for a synthetic second producer:

```json
{
  "coordinate": "org.fixture/landscape-subagents",
  "root": "packages/landscape-subagents",
  "baseline": "0000000000000000000000000000000000000000",
  "adapter": "tree-v1",
  "files": ["vibe.toml", "README.md", "LICENSE"],
  "redistribution": {
    "status": "approved",
    "license": "MIT",
    "approval": "https://github.com/fixture/producer/issues/1#issuecomment-1"
  },
  "disclosure": "opaque",
  "destination": "https://github.com/fixture/landscape-subagents.git"
}
```

Replace the illustrative zero baseline with the explicitly accepted source
commit before integration. It may precede initial package creation. Each package
may start at its own owner-chosen `1.0.0`. Changed payload with reused version,
removal, missing approved files, non-frozen manifest or identity mismatch stops
publication. Stable-path/coordinate changes need explicit owner disposition.
The exporter generates a path/hash-map receipt; source-only receipt differences
are excluded from payload selection. `opaque` omits repository/path/source SHA;
`public-source` deliberately includes path/SHA. Private/public licensing, notices,
source disclosure and approved files are producer decisions before real release.
No source history, sibling, root notes or worktree files are copied implicitly.

Before accepting frozen source into main, complete the actual public `LICENSE`,
applicable manifest/license metadata, approved redistribution rights, intended
export inventory and relevant source checks. The illustrative MIT value above
does not choose a license for a real producer. `redistribution` records the
owner-approved license and rights Decision; unresolved/missing approval, blank or
missing notices and mismatching metadata block readiness. The tool cannot decide
whether arbitrary legal text grants sufficient rights: owner review of the actual
notices remains necessary. A publisher may verify readiness, never invent rights
or add missing files after merge. Historic incomplete exports may be compared for
a forward source repair, but cannot be silently published as ready releases.
Production planning compares those historical exports without reapplying current
readiness requirements; historical package transitions still need their appropriate
owner/CI eligibility or explicit disposition. Every changed/new current release
and the source-time candidate check (including an unchanged candidate export)
enforce full readiness. A version-bumped, eligible
repair can therefore publish without trying to publish its incomplete predecessor.

An accepted frozen `(group, name, version)` is immutable at its first main
integration even if no remote tag exists. Add/delete/rename of approved files,
binding-only inventory changes, notice or manifest corrections require a new
version. Candidate branches may refine a new version before acceptance. The
already merged Landscape 1.0.0 packages therefore cannot receive missing licenses
under 1.0.0; preparing new versions, rights and first-release CI belongs to
separately authorized Landscape work. This PR changes no Landscape source or policy.

Both initial adapters support **empty included dependency closure**. The existing
governance exporter enforces this; tree-v1 rejects dependency sections. A later
dependency-capable adapter must reuse native manifest/lock/slot evidence for the
actually included frozen transitive closure and justified exceptions. Existing
native dependency tests are retained; this tool adds no second resolver. Omitted
dev/optional dependencies must be established by the adapter, not guessed here.

## CLI and publication mechanics

Python 3.11+ and Git suffice for planning. Run the CLI from its pinned checkout:

```sh
python3 tooling/vibe-publisher/publisher.py plan \
  --source /path/to/producer --source-sha FULL_SOURCE_SHA \
  --policy /path/to/policy --policy-sha FULL_POLICY_SHA --binding publisher.json \
  --publisher-sha FULL_CODE_SHA --package org.fixture/landscape-subagents \
  --report /tmp/publication.json
```

For source-time candidate CI, use `check` with those same source/code/binding
arguments plus `--base FULL_ACCEPTED_MAIN_SHA`. The policy checkout/pin for this
operation contains the proposed binding; it is validation data. `--main` still
identifies accepted source main. The check compares the final candidate export
against accepted main and its bounded frozen-version history, including inventory
changes and unpublished accepted identities. It permits candidate refinements of
a new version, performs no acceptance API calls or distribution reads/writes and
reports `CANDIDATE_VALID` or a safe pending reason. This is bounded source validation:
it does not independently qualify inherited historical PR/CI acceptance, promise
production eligibility, or grant owner acceptance, merge or publication authority.
Production planning retains the historical eligibility audit above; a candidate
can be valid while inherited acceptance remains unresolved. No privileged/API
pre-merge gate or second approval is implied. Producer candidate CI must invoke this check or its qualified equivalent
(Shared Governance retains its existing exporter and release-transition checks).

`GH_TOKEN` grants read access to the producer's API evidence; it is not a
distribution credential. A `stage` invocation with the same pins additionally
uses `--vibe /path/to/pinned/vibe --directory /tmp/disposable-stage`. Planning is
repeated from canonical evidence; it does not trust a manually edited READY file.
The native VibeVM 1.0.7 musl digest comes from this publisher's toolchain record.
Native execution gets an isolated settings directory and no API/publish token,
askpass or global Git credential configuration. Only `finalize --report ...`
receives the one destination credential through ephemeral askpass. Workflow
reports stay in runner temporary storage; no private source artifacts are uploaded.

An existing `vVERSION` is skipped **before native invocation**. Otherwise clone
the distribution to disposable bare staging, recheck that tag, invoke native
publication against that local repository, then push only main plus the new tag
in one ordinary `git push --atomic`, without force. An unsupported atomic server
fails; there is no two-push fallback. Concurrent existing-tag or divergent-main
writers cannot overwrite frozen identities or partially advance that final push.
There is no global highest-SemVer gate. Distribution main is last published.

Reports expose `NO_PACKAGE_CHANGE`, `AUTHORIZATION_PENDING`, `READY`, `STAGED`,
`PUBLISHED`, `ALREADY_PUBLISHED` and `FAILED_OR_PENDING`, with source/code identity,
acceptance evidence, destination/version and observed refs where available.
`ALREADY_PUBLISHED` retains the existing identity; it never asserts this retry's
different source was published. Ambiguous push results are read back: the exact
staged tag object proves publication, a competing tag is retained with a warning,
and unavailable/absent evidence remains pending. No frozen tag is repaired in place.

Publisher logs and the durable Actions summary show an allowlisted diagnostic code
and operator message for each package. Authorization-pending output distinguishes
missing or mismatched owner/PR/CI evidence, unresolved package baselines and owner
disposition from retryable staging/publication failures. `ALREADY_PUBLISHED`
explicitly warns when the existing tag does not prove that this source was
published. Failures before a report exists receive a non-sensitive workflow-phase
category; finalization failures direct operators to inspect exact destination refs.
Raw Git stderr, arbitrary exception text, private source details, credential URLs
and the full report remain out of the summary and logs; reports stay in runner
temporary storage and are not uploaded.

There is no cross-repository atomic transaction. If A succeeds and B fails, retain
both outcomes and retry **the same source, policy and publisher SHAs**: A skips its
tag; B resumes. An implementation-pin change for recovery needs a separately
accepted correction. The producer caller owns trigger/retry and concurrency;
use producer/source/coordinate groups with `cancel-in-progress: false`, not a
global group that can replace pending releases. For `workflow_run`, the core
reads the actual event's triggering run ID, retrieves that run through the API
and checks the configured push CI and source. It also acquires successful
exact-source push evidence on every run.
No new owner approval is required after an eligible accepted merge.

## Focused qualification and rollout

```sh
python3 tooling/vibe-publisher/test_publisher.py
python3 tooling/vibe-publisher/test_publisher.py --vibe /absolute/pinned/vibe
python3 scripts/test-release.py --vibe /absolute/pinned/vibe
```

All test distribution writes target local bare repositories. Focused fixtures
cover two packages, eligibility/CI failures, direct-main no-op, inherited
unaccepted bytes, fixed-version rejection, private-shaped export, existing tags,
concurrent writers, ambiguous response readback and same-source partial recovery.
Focused diagnostics checks exercise authorization-pending, retryable failure,
non-proving existing-tag warnings, redaction and failures before a report exists.
The accepted release/dependency tests retain their own coverage. These are bounded
integration checks, not a requirement to rerun native transport on every release.

The unprivileged PR workflow calls the candidate reusable workflow with a public
synthetic named-secret marker, checks its own code SHA and separate producer SHA,
and executes the focused tests. It has no distribution credential or publish step.
It does not qualify private caller access, actual cross-repository credentials or
real publication. Exact run evidence and remaining limits belong in the result PR
and [Step 2 evidence](task-45/step-2/validation.md) or
[Step 3 diagnostics evidence](task-45/step-3/validation.md), as applicable.
[Step 4 evidence](task-45/step-4/validation.md) records evolving file inventories,
temporal policy, source-time readiness and the real no-checkout shell fallback.

After independent acceptance, production integration still needs separate owner
authority in each producer, approved destinations/visibility, public payload
license/disclosure and credential provisioning. A producer's accepted integration
may authorize its automatic release; add no redundant manual permission where
that authority already exists. Shared Governance's existing post-merge automation
remains in service; this PR prepares 3.0.0 without cutting over to the shared tool.
Keep existing entrypoints until that replacement is qualified. Landscape #3/#4
content tasks and consumer adoption keep their separate authority. Roll back an
integration through ordinary Git; never move/delete a frozen release to recover.

## Explicit first publication of pre-onboarding source

Task [49](https://github.com/jresearchsoftware/shared-governance/issues/49)
adds an opt-in operation for a proven gap: `baseline_disposition` alone cannot
publish a frozen source snapshot that predates its first publisher binding.
Ordinary `plan`, `check` and release selection retain their existing behavior.
No passive package protocol or production producer is changed.

For **tree-v1, stable-root, previously unbound source only**, the independently
accepted onboarding binding may add these per-package fields:

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

These fields augment the ordinary package binding: coordinate, stable root,
`baseline`, approved `files`, redistribution rights, disclosure and one destination
remain required. The separately reviewed disposition explicitly attests the named
already accepted source, immutable version and approved export digest, and admits
first publication without claiming historical push CI. A URL alone is not owner
proof: as with ordinary baseline disposition, authority comes from independent
acceptance of this exact binding and caller pin. The publisher does not parse
Decision prose or infer permission from an arbitrary linked comment.

1. In the producer's separately authorized onboarding PR, approve the complete
   public inventory and actual notices/rights, choose `opaque` or `public-source`
   separately, and bind one destination per coordinate. Compute the digest with
   `snapshot(producer, FROZEN_SHA, package_binding)[1]['payload_sha256']` from the
   pinned publisher. Do not edit the frozen package to create this binding.
2. Qualify that candidate with ordinary CLI arguments plus
   `check --initial-publication --base EXACT_ACCEPTED_MAIN`. For this operation
   `source_sha` and `policy_sha` both name the candidate onboarding commit.
   It checks readiness, exact frozen bytes and source identity history offline;
   `CANDIDATE_VALID` cannot stage or publish, and does not assert acceptance/CI.
   The producer also runs its own package/source tests on these same bytes.
3. Independently review and owner-squash the onboarding PR, including the explicit
   initial-release disposition, caller and CI. Obtain successful matching **push**
   CI at that exact integration. The caller pins that integration as **both**
   `source_sha` and `policy_sha`; the historical payload SHA stays inside the
   per-package `initial_publication` record. Pin shared code separately by its
   accepted full SHA. A candidate head or a green arbitrary direct-main commit
   cannot substitute for accepted onboarding.
4. Explicitly invoke `plan --initial-publication`, then
   `stage --initial-publication` with those identical arguments and pins, and
   ordinary `finalize`. In the reusable workflow set `initial_publication: true`
   for this bounded call; leave its default `false` for ordinary releases. Use
   `mode: plan` for a read-only plan, `mode: publish` for authorized publication.
   One call receives only the named credential for that coordinate's destination.

The operation requires the source commit to precede onboarding on first-parent
main and to be the **first main integration** of the attested version under the
approved stable-root inventory. Both its authorized owner squash and the
onboarding owner squash are verified. Source acceptance uses the integrators
explicitly endorsed by the onboarding binding; this is a new attestation of the
old source, not reconstructed historical policy. If a binding already precedes
onboarding, its integrators authorize the rotation; new integrators cannot
self-authorize. Readiness CI belongs exclusively to onboarding. No historical
CI is fabricated, rerun or reported as successful.

Current and frozen exports must match, including disclosure choice, and all
observed occurrences of that version through onboarding must retain the same
exported bytes. Missing files/license, unresolved rights/dependencies, altered
same-version payload, wrong source/version/digest, missing owner squash or wrong
CI stays pending. Preexisting historical publisher policy is deliberately
unsupported by this narrow operation and returns `HISTORICAL_BINDING_UNRESOLVED`;
it is never overridden with today's inventory. The current approved allowlist
compares **previously unbound source**; it is not called historical export policy.
Older versions are not staged or licensed by this operation.

Only the accepted integration **introducing** the initial-publication declaration
is an initiation. A later commit retaining it cannot reinitiate, even with the
flag. Ordinary factual commits keep `NO_PACKAGE_CHANGE`. Reports distinguish
`initiation_sha` / top-level `source_sha` (onboarding) from per-package `source_sha`
(frozen payload), `source_acceptance` (without CI) and `readiness_acceptance`
(with onboarding CI). Private reports stay in runner temporary storage; choosing
`opaque` keeps source paths/SHAs out of distribution receipts.

Existing-tag bypass, pinned native staging, atomic non-force push and exact-tag
readback are shared with ordinary publication. Partial success has separate
per-package results: retain A, retry B using the **same onboarding/policy/code and
frozen payload pins**. An existing tag is retained, never overwritten, and does
not prove the retry's source was originally published. There is no new ledger,
credential type, cross-distribution transaction or production activation.

Ordinary subsequent releases still use the full historical policy, frozen-version
and exact-source owner/CI audit. This first-publication operation neither waives
that audit nor claims to reconstruct missing old bindings. A producer with
pre-binding history may still receive `HISTORICAL_BINDING_UNRESOLVED` for a later
ordinary package change; that migration needs separately qualified historical
policy/disposition. Do not claim complete subsequent-release onboarding from a
successful initial release. Unrelated ordinary commits remain no-ops.

Shared Governance owns this reusable operation and its disposable qualification.
Landscape separately owns any actual binding/caller, source checks, review and
initial-publication Decision, rights/inventory/disclosure choice, destinations
and visibility, credentials and activation. Its intended versions remain exactly
`org.jresearch.ai/landscape-subagents@1.0.1` and
`org.jresearch.ai/landscape-model-guidance@1.0.1` at accepted source
`638fbd7ca3c4ef778c9a371c9e6f5b9433c780cd`. Nothing here publishes their 1.0.0
predecessors, changes 1.0.1, or authorizes consumer adoption.
