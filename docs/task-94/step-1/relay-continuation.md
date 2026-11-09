# Codex Relay continuation required

Related to Shared Governance Task #94. This is a prepared continuation, not
authority to edit, merge or publish in another repository. Task #94 remains open
until actual Relay 5.0.0 publication is verified, unless an explicit owner
Decision transfers that condition to a linked producer Task.

## Caller change and review

At inspected accepted Relay source `10d2614372cbf578dfb552d3d62fdb8f640f7501`,
`.github/workflows/publish-guidance.yml` still declares `source_sha` required.
The shared reusable workflow cannot change that form. No accepted Relay caller
change was made by this execution, so the Relay UI is **not fixed** yet.

Under separately authorized Relay continuation, change that input to optional
and resolve it once before calling the publisher. Use Shared Governance's
`.github/workflows/publish.yml` and `scripts/test-publication-dispatch.py` as the
qualified pattern: blank dispatch input uses dispatch-event `github.sha` only on
selected `main`; explicit full SHA remains supported; automatic publication uses
the triggering successful push run's `head_sha`. Pass the single resolved output
through concurrency, source checks, the reusable call and visible reporting.
Qualify the actual Relay caller, including omitted/empty input, explicit historical
retry, moving main, malformed/non-main sources and rejected exact push CI.

The inspected caller uses
`jresearchsoftware/shared-governance/.github/workflows/vibe-publisher.yml@main`;
it is not currently a full-SHA pin. Recheck the accepted caller at continuation
time. If a pinned caller exists then, any required pin update belongs to that
producer's independently reviewed change. Preserve its named secret mapping,
coordinate and source-committed binding. No package payload change or version
bump is needed for this caller-only correction.

## Public recovery and completion evidence

First independently accept and integrate the Shared Governance implementation.
Then, with Relay's own execution/publication authority and reviewed caller,
qualify the exact accepted main commit selected by the dispatch. The later caller
change may itself be package-neutral: retain the original frozen 5.0.0 export
from `0aff32a6873262185f60364463f4e97ef330de89` and require successful **push** CI
for the exact later trigger SHA. A new blank dispatch must select its own exact
event commit, never silently substitute `10d2614` or moving main. An explicit
`10d2614372cbf578dfb552d3d62fdb8f640f7501` retry remains a qualified recovery
source while its binding, accepted membership and exact successful CI qualify.

Use the existing bound destination and authorized credential path. Verify the
real remote `v5.0.0` tag, its package payload and `DISTRIBUTION.json` source
readback; retain the exact tag object observed after publication. A green workflow,
merged fix, `READY`, local fixture tag or existing unverified tag is insufficient.
The [local incident replay](README.md) is secret-free implementation evidence,
not a public release or consumer migration. Record the actual authorized result
and link the producer continuation before satisfying Task #94's completion hold.
