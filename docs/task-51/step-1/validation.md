# Task 51 Step 1 — Shared Publisher correction

Authority: [Task 51](https://github.com/jresearchsoftware/shared-governance/issues/51)
and [Step 1 admission](https://github.com/jresearchsoftware/shared-governance/issues/51#issuecomment-6285817475).
Frozen independently accepted source: `c26d0fc3a287dca86c36855b6b5230509f98152a`.
Direct implementation; independent exact-result acceptance remains pending.

## Changed behavior and coverage

Ordinary source eligibility now uses first-parent main, the immediate source
transition and successful matching exact-source push CI. No historic eligibility
replay, baseline/disposition, PR/integrator lookup or second producer identity is
required. The workflow/CLI load the binding from `source_sha`; implementation
selection remains in the reusable-workflow reference. Same-source retry remains
stable when main and the worktree advance. The approved license/redistribution
acknowledgement, source/CI, inventory, isolated destinations, pinned native staging,
existing tags, races, atomic non-force push and exact readback are retained.

The tests replace obsolete historical-audit expectations with the owner-selected
contract. Disposable late-onboarding histories contain unbound 1.0.0/1.0.1,
unchanged onboarding and non-package no-ops, then genuine native 1.0.2 and 1.0.3
publication without old PR/CI records. Other tests exercise actual squash,
ordinary merge, rebase and direct-main transitions; invalid/current same-version
payloads; source-time inventory changes; rights/license/CI failures; side branches;
private-file exclusion; sibling isolation; tag collisions and partial retries.

Task 49's explicit initial-publication mode retains isolated owner-squash
attestation, frozen first-source/version/digest and onboarding CI checks. Its CLI
also uses only source/binding arguments: older policy/publisher-SHA callers need
updating. Its history scan is confined to the explicit operation; it does not
participate in ordinary future releases. Historical Task 49 evidence/reproducer
is retained as published and is interpreted at its original accepted revision.

## Native dependency qualification

The pinned Linux x86_64 VibeVM 1.0.7 musl binary was verified against toolchain
SHA-256 `20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Native `install --offline --registry <disposable> --no-default-registry` resolves
a pinned direct dependency and frozen transitive dependency. Tests copy the
tool-produced lock/slots into the approved source inventory, then stage/publish
and compare every release blob. Included dependencies need frozen identities,
resolved sources, lock content hashes and matching native slot inventories/hashes.
Included mutable, missing transitive and mismatched native metadata are rejected.
Excluded optional suggestions publish with an empty included closure; included
development-labelled dependencies are checked too. The governance exporter and
its dependency-free contract are untouched.

**Actual upstream limit:** VibeVM 1.0.7 rejects `dev-requires` and inline
`optional=true` at native manifest parsing. Planning accepts their nonincluded
declarations without a blanket dependency blocker, but native staging still
fails; frozen manifests are not rewritten. The suite explicitly records this
expected native incompatibility, not successful publication of that syntax.
Native `[suggests]` exclusions do successfully stage/publish. Broader native
syntax support would require upstream/toolchain work outside this Step.

## Remaining differences and operator impact

| Condition | Disposition |
| --- | --- |
| Historic owner/CI/binding replay, ordinary baseline attestations | Removed by explicit Task 51 authority; reduced historic assurance accepted. No claim to rediscover every earlier unpublished identity. |
| Mandatory owner squash/integrator and extra policy/publisher SHA inputs | Removed for ordinary releases. Producer review/integration policy remains separately owned. Explicit Task 49 acceptance checks remain isolated. |
| Root license and affirmative redistribution/reference | Retained by explicit owner choice. Reference can be reused while applicable; no per-release approval. |
| Explicit tree-v1 file inventory/disclosure | Retained existing cross-producer contract, with configuration cost disclosed. Producers still assess embedded references/private content and self-contained links. |
| Generic version/payload invariant | Shared publisher rejects invalid and same-version changed payload. Producer-specific major/minor/patch category/arithmetic CI is untouched. |
| Native dependency closure | Blanket ban removed; use existing resolved lock/slot evidence, including transitive frozen identities and hashes. No new resolver or ledger. Native syntax limits above remain. |
| Producer-specific exporter | Existing governance payload/receipt/passivity/dependency-free checks retained; full cutover/parity assessment belongs to Task 53. |
| Publication boundary | No remote distribution writes, credentials/settings mutation, Landscape changes, producer activation, package bump, merge or closure. |

## Reproduction

Use a clean native Linux clone of the result commit and the pinned binary:

```sh
python3 tooling/vibe-publisher/test_publisher.py --vibe /absolute/pinned/vibe
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
python3 scripts/test-release.py --vibe /absolute/pinned/vibe
python3 scripts/test-self-adoption.py
python3 scripts/test-chatgpt-projection.py
python3 scripts/package-release.py --source-ref HEAD --base c26d0fc3a287dca86c36855b6b5230509f98152a
git diff --check c26d0fc3a287dca86c36855b6b5230509f98152a HEAD
```

Primary final results and CI are bound in the canonical PR Outcome. All fixture
distribution writes target disposable local bare repositories. Actual private
callers, cross-repository credential availability, remote publication and
Windows/macOS native staging are unqualified. These tests are executor evidence,
not independent acceptance. The active local release workflow and package
3.0.0 payload remain unchanged; Tasks 53 and 52 are not executed here.
