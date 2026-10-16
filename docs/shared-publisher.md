# Shared source-only VibeVM publisher

Task [45](https://github.com/jresearchsoftware/shared-governance/issues/45)
selects one Python CLI/library and one reusable GitHub workflow, outside the
Development Governance package. These are candidate tooling; no producer is
integrated by this change. The current [release entrypoint](releases.md) remains
in service. Source acceptance, remote publication and consumer adoption are
separate. Installing a flow neither executes this tool nor adopts release policy.

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
`NO_PACKAGE_CHANGE`, without a PR/CI eligibility requirement or release. A green
direct-main package edit returns `AUTHORIZATION_PENDING`. A later owner squash
cannot launder its accumulated bytes: for a changed package, audit every changed
export on first-parent history from the explicitly accepted baseline to this
source. Every package-bearing transition needs the eligibility evidence. An
unresolved transition stops that package. Owner disposition can explicitly accept
the accumulated delta and establish a new baseline in a separately reviewed
binding revision. Do not advance the baseline automatically or infer that the
later PR accepted the inherited delta. This uses Git/PR/CI records, no standing
ledger. A source-only commit never opportunistically releases earlier changes.

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

There is no cross-repository atomic transaction. If A succeeds and B fails, retain
both outcomes and retry **the same source, policy and publisher SHAs**: A skips its
tag; B resumes. An implementation-pin change for recovery needs a separately
accepted correction. The producer caller owns trigger/retry and concurrency;
use producer/source/coordinate groups with `cancel-in-progress: false`, not a
global group that can replace pending releases. For `workflow_run`, the caller
must validate the triggering run identity against its configured push CI; the
core independently acquires successful exact-source push evidence on every run.
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
The accepted release/dependency tests retain their own coverage. These are bounded
integration checks, not a requirement to rerun native transport on every release.

The unprivileged PR workflow calls the candidate reusable workflow with a public
synthetic named-secret marker, checks its own code SHA and separate producer SHA,
and executes the focused tests. It has no distribution credential or publish step.
It does not qualify private caller access, actual cross-repository credentials or
real publication. Exact run evidence and remaining limits belong in the result PR
and [Step 2 evidence](task-45/step-2/validation.md).

After independent acceptance, production integration still needs separate owner
authority in each producer, approved destinations/visibility, public payload
license/disclosure, credential provisioning and an admitted first publication.
Keep existing entrypoints until that replacement is qualified. Landscape #3/#4
content tasks and consumer adoption keep their separate authority. Roll back an
integration through ordinary Git; never move/delete a frozen release to recover.
