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

Linux qualification used Debian WSL, Python 3.11.2, Git and the pinned VibeVM
1.0.7 x86_64 musl binary. Staging checks digest
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`
against `toolchain/vibevm.json`. At implementation commit
`48a52029b2896d9f7e5a11ae75cce7622b937b2f`:

| Check | Result |
| --- | --- |
| `python3 tooling/vibe-publisher/test_publisher.py --vibe /absolute/pinned/vibe` | 27 passed, including six native cases; 0 skipped; 2.932 seconds |
| `python3 scripts/test-release.py --vibe /absolute/pinned/vibe` | All 16 passed, including six retained native publication/dependency cases; 0 skipped; 6.930 seconds |
| [Candidate CI](https://github.com/jresearchsoftware/shared-governance/actions/runs/38959050197), check `117169184665` | PASS; source/native/exact-export, 42 distribution, 12 self-adoption, 24 ChatGPT tests; 10 ordinary release passes / 6 optional native skips; 0 annotations |
| [Reusable Actions fixture](https://github.com/jresearchsoftware/shared-governance/actions/runs/38959050207), check `117169184251` | PASS; 21 ordinary focused passes / 6 native skips, primary GitHub evidence, source/code identity and synthetic named-secret checks; 0 annotations |

The exact final PR head's checks and readback are recorded in its one canonical
Outcome, avoiding a self-referential committed head hash. Final documentation
updates leave these implementation bytes unchanged.

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

## Live Actions and API evidence

[Full-SHA reusable call](https://github.com/jresearchsoftware/shared-governance/actions/runs/38958801702)
passed at caller head `6f8605318a120814dcf90906f1dbf4fe1e555409` with publisher
`de60311f768986530e8a161d7cee9f7dcd76dac0`. Primary logs show
`job.workflow_ref` ending in that full pin, own code checked out at that same
SHA, and producer checked out independently at `6f8605318...`. The final fixture
returns to a local workflow reference so future candidate code changes are
actually tested; no transient candidate SHA is a standing integration dependency.

At `48a52029b...`, primary Actions logs show called code at synthetic PR merge
`625db0f677b7ca4cd31e38563d6df68a79fa8da2` and producer at `48a52029b...`.
Preparation has neither API nor publication token in its environment; the
read-only evidence step receives only the source token, and a later isolated
step receives the public synthetic named-secret marker. No secret setup occurred.
The probe positively resolves accepted source `ec048fb...`, owner `foal`,
[PR 42](https://github.com/jresearchsoftware/shared-governance/pull/42), reviewed
head `a91e93aaa8df2aa471ba5f9f508bdfc7120f895e` and successful
[push CI 38855502454](https://github.com/jresearchsoftware/shared-governance/actions/runs/38855502454);
it rejects the unaccepted candidate. This caught and corrected a trailing-slash
API endpoint defect, with a focused regression.

A read-only CLI `plan` using the pinned illustrative binding at `48a52029b...`
also returned READY for accepted source `ec048fb...` and canonical 2.7.0 digest
`4e3ca1fb4093bc14136c323deff7bfd64584159e6202470773bcde38f7e1d047`.
This is compatibility evidence, not activation of that candidate binding.

## Limits and handoff

The live fixture uses no destination credential and performs no publication.
Private caller access, real cross-repository permissions, secret
provisioning, production trigger/caller adoption, actual public distribution and
consumer adoption remain unqualified and separately authorized. Existing VibeVM
tag replacement, full-SHA local archive/cache-only recovery, GNU/glibc and static
INDEX limitations are not repaired or reclassified by this change.

The initial shared adapters admit empty included dependency closure. Existing
native frozen/transitive/diamond tests remain passing evidence of the retained
dependency tooling, not a claim of a new generic dependency-capable adapter.
Owner merge attestation is not authenticated independent-review proof.
