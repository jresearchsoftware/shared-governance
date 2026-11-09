# Task 94 — Step 1 — Current-version publication recovery

This qualification uses independently accepted Shared Governance source
`1110f10b996c2f81fa842e6339ab6d7c13111cd7` for the authoring baseline. It exercises the shared publisher against
actual public Codex Relay source and push-CI evidence, with every distribution
write redirected to disposable local bare Git repositories. It does not change
Relay, its consumer state, public distribution refs or repository settings.

## Concrete incident

Relay first accepted frozen `org.jresearch.ai/codex-relay@5.0.0` at
[`0aff32a6873262185f60364463f4e97ef330de89`](https://github.com/jresearchsoftware/codex-relay/commit/0aff32a6873262185f60364463f4e97ef330de89).
Its exact-source [Public CI run 42530062798](https://github.com/jresearchsoftware/codex-relay/actions/runs/42530062798)
failed. The next accepted main commit,
[`10d2614372cbf578dfb552d3d62fdb8f640f7501`](https://github.com/jresearchsoftware/codex-relay/commit/10d2614372cbf578dfb552d3d62fdb8f640f7501),
repairs historical runtime tests and contributor documentation. Its exact-source
[Public CI run 42579776332](https://github.com/jresearchsoftware/codex-relay/actions/runs/42579776332)
passed, while the approved 5.0.0 package payload remained unchanged. The previous
package version at `512b2b5ea2867b92958580f17f6aee24c23b1fba` was 4.1.1.

Both incident commits carry the producer's root `vibe-publisher.json`. It binds
the `guidance/artifacts/vpm` source root, `tree-v1` adapter, explicit public file
inventory and `.github/workflows/relay-exact-head-validation.yml` CI path.
The coordinate was already publisher-bound before 5.0.0 appeared. This is
recovery of a current publisher-bound version, not initial-publication authority
for an older unbound package.

The old immediate-parent-only planner returns `NO_PACKAGE_CHANGE` for the
successful test-only commit. The corrected planner must instead qualify that
exact current source's successful push CI and preserve the first frozen
version's bytes and receipt source revision. No source change or package version
bump is needed to retry transport of those already frozen bytes.

## Reproduction

Use Python 3.11+, Git and the SHA-256-verified Linux musl VibeVM binary pinned in
`toolchain/vibevm.json`. The probe reads no credential environment variables and
uses anonymous public API access. A disposable full-history public clone makes
the source inspection independent of this producer's checkout.

```sh
git -c credential.helper= clone --no-checkout \
  https://github.com/jresearchsoftware/codex-relay.git /tmp/relay-public
python3 tooling/vibe-publisher/probe_relay_recovery.py \
  --source-repo /tmp/relay-public --vibe /absolute/path/to/vibe \
  --output /tmp/relay-recovery.json
```

The captured [qualification evidence](relay-recovery.json) records the exact
source pins, public CI fields used by qualification, public destination refs,
planner decisions and the local distribution receipt. Its timestamp describes
the observation; public refs and run availability can subsequently change.

| Check | Observed result |
| --- | --- |
| Accepted old publisher at the fixed baseline | `NO_PACKAGE_CHANGE`, reproducing the missed retry |
| Corrected publisher, successful current source | `READY`, with current trigger/CI and original frozen source |
| First frozen source with failed exact CI | `AUTHORIZATION_PENDING` / `MATCHING_SOURCE_CI_MISSING` |
| Current source without successful exact CI | `AUTHORIZATION_PENDING` / `MATCHING_SOURCE_CI_MISSING` |
| Native local staging and atomic publication | `STAGED` → `PUBLISHED`; exactly one local push |
| Repeated local finalize and stage | `ALREADY_PUBLISHED`; existing tag preserved |
| Local distribution receipt | Original `0aff32a…` source; 41 payload hashes match planned digest |
| Public destination read-only observation | Main `50759fc657b10606f77c75129a5f18894276818e`; no `v5.0.0` tag |

The probe checks current successful CI, rejection without that exact current CI,
first-frozen-source provenance, real native staging, atomic local publication,
exact-tag readback and repeat-stage/repeat-finalize preservation. It substitutes
only Git distribution transport addresses; source-committed package bindings and
the package payload remain exact. Local writes use an empty bare destination,
so the probe does not reproduce public distribution history or claim successful
public publication.

## Qualification limits

This is a focused incident replay, not a new mandatory release gate. It does not
exercise reusable-workflow dispatch in GitHub Actions, publication credential
delivery, destination provisioning or consumer installation/migration. Passing
local checks supplies implementation evidence; independent exact-head acceptance
and separately authorized public publication remain distinct.
