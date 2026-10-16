# Task 45 Step 2 qualification

Authority: [Task 45 chronology](https://github.com/jresearchsoftware/shared-governance/issues/45)
and [Step 2 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6223120222).
Frozen independently accepted source-main:
`ec048fb39ae28cf2d747101466a603ddd062b1b0`, owner-integrated PR 42. Direct acceptance;
the implementation must stop for fresh independent exact-head review.

## Scope and boundaries

The source-only Python CLI, one reusable workflow, an unprivileged PR fixture,
producer binding/export contract and disposable tests implement the selected
hybrid. [Operator contract](../../shared-publisher.md) defines eligibility,
baseline reconciliation, export, status and exact-source recovery. No package
payload/version, installed/native producer state, production release entrypoint
or consumer is changed. The illustrative governance binding is inactive.

## Executed evidence

Initial Linux qualification used Debian WSL, Python 3.11.2, Git and the pinned
VibeVM 1.0.7 x86_64 musl binary. Its digest is checked by staging against
`toolchain/vibevm.json`. The first 22-test focused suite passed, including four
native scenarios; all 16 existing release/dependency tests passed with zero skips.
Additional automatic-trigger, A-only publication/private receipt and native
failure/retry cases are included in the final suite; final results and exact
head CI will be bound in the result PR's canonical Outcome.

The tests establish two independent initial versions, unaffected-package and
source-only no-op, exact PR/owner/repository/SHA/push-CI eligibility negatives,
unaccepted direct-main then eligible squash rejection, explicit reconciled
baseline behavior, reused-version rejection, complete API pagination, immutable
binding reads, secret-free native environment and governance exporter/receipt
byte compatibility at the accepted SHA. Native fixtures use local bare
distribution repositories for same-source partial recovery, existing-tag skip,
competing same-tag/different-main writers, failed staging and ambiguous final
transport readback. Synthetic public-file allowlists exclude private root notes,
package-local private files and sibling package payloads; opaque receipts omit
private source identity. No actual private producer was exported.

## Live integration limits

The PR fixture is designed to check `job.workflow_repository` / `job.workflow_sha`
code checkout, separate producer checkout and a synthetic named-secret marker
in a real GitHub Actions reusable call. Final run evidence must be inspected
before claiming this passed. It does not use a destination credential or perform
publication. Private caller access, real cross-repository permissions, secret
provisioning, production trigger/caller adoption, actual public distribution and
consumer adoption remain unqualified and separately authorized. Existing VibeVM
tag replacement, full-SHA local archive/cache-only recovery, GNU/glibc and static
INDEX limitations are not repaired or reclassified by this change.

The initial shared adapters admit empty included dependency closure. Existing
native frozen/transitive/diamond tests remain passing evidence of the retained
dependency tooling, not a claim of a new generic dependency-capable adapter.
Owner merge attestation is not authenticated independent-review proof.
