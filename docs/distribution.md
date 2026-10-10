# Package distribution

The only editable semantic source is shared-governance. The current single
package is authored at `packages/development-governance`; historical exact-commit
exports select their original root from the chosen commit's workspace manifest.
Distribution is flat, with `vVERSION` tags in
[jrs-vibevm/org.jresearch.ai.development-governance](https://github.com/jrs-vibevm/org.jresearch.ai.development-governance/tags).
Frozen `0.1.0` remains unchanged. Package source, distribution main/tags and
consumer versioned slots are distinct. Actual status lives in tags and Actions.

## Exact source export

```sh
source_sha="$(git rev-parse HEAD)"
prepared="$(mktemp -d)/package"
python3 scripts/prepare-distribution.py --source-ref "$source_sha" --destination "$prepared"
```

Preparation selects full canonical Git blobs, checks the passive package shape,
frozen metadata, license and local links, and writes a generated
`DISTRIBUTION.json` receipt with source repository, exact revision, authoring path,
whole-package version and tool-produced payload hashes. The target is absent or
empty and outside the checkout. No source or consumer files are modified.
The flow has no dependencies; snapshot/transitive closure handling for future
admitted dependencies is defined in the shared package-versioning protocol.

`--verify`, `--verify-installed` and `--verify-consumer` remain available for
integration qualification and incident diagnosis. They reconstruct expected bytes
from Git and check lock, slot metadata and generated AGENTS/INDEX routes. They are
not a mandatory recurring remote per-file hash ritual. Native-Skill export is
historical only. Pinned VibeVM emits a static INDEX entry for the compact boot;
its protocol reads are conditional.

## Publication and consumers

[Release policy](releases.md) documents automatic publication of accepted
version-bearing source-main changes, fixed destination, secret configuration,
existing-tag no-op, atomic non-force push and safe retry of the same accepted SHA.
The native publisher is never called for an existing tag. No central registry,
repository-creation service, release ledger or second owner approval is required.

Consumers choose constraints and intentionally update their own lock. For example:

```toml
[requires.packages]
"org.jresearch.ai/development-governance" = { version = "=1.0.0", git = "https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git", tag = "v1.0.0" }
```

The example identifies a version, not current publication status. Exact pins,
patch-only ranges and caret compatibility windows are explained in the protocol.
Installation or update does not adopt newly available normative topics; an
existing local versioning policy remains authoritative. Consumer migrations
require their own accepted changes, including reconciliation of duplicates.

## Qualification scope

[Authoring](authoring.md) gives optional pinned-tool integration commands. Real
local publisher/cold consumer/update/conflict/concurrency paths use disposable
Git repositories and isolated VibeVM settings. Frozen-tag drift and offline
recovery probes are incident evidence, not permissions to modify real tags.
Routine release CI reuses focused source/export and release-boundary checks.
Reviewers inspect their adequacy without duplicating package-manager transport.

Task 2's [preparation packet](task-2/step-3-preparation/README.md) and Task 10's
[qualification](task-10/step-1/README.md) retain dated historical evidence.
VibeVM's known tag-replacement capability motivates only the targeted publication
guard. Path-only, GNU/glibc and cache-only offline limitations are recorded in
[authoring](authoring.md); no broad platform or model-performance claim is implied.
