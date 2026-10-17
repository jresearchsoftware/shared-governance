# Task 45 Step 4 qualification

Authority: [Step 4 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6233276390).
Frozen independently accepted source-main: `ec048fb39ae28cf2d747101466a603ddd062b1b0`.
Starting reviewed candidate: `0eea7329556a25992a0e11f8c4fb8b7525ff80f9`.
The exact final result and Actions evidence are bound by the single Step 4 Outcome
on [PR 46](https://github.com/jresearchsoftware/shared-governance/pull/46).

## Corrections and semantic coverage

- F1 and F2 originated in Step 2's shared implementation (`48a52029b2896d9f7e5a11ae75cce7622b937b2f`),
  newly identified by the whole-solution review. Revision-specific source bindings
  now preserve public file inventories and source-time acceptance rules. Exact
  Git snapshots, add/delete/rename and binding-only changes are exercised; owner
  and CI rotations cannot reinterpret earlier evidence. Explicit baseline
  disposition remains a separate externally accepted producer decision.
- F3 originated in Step 3 (`39924ec30b7fd56f9ad9f3312e5caf62cae04d0b`). The actual workflow shell
  fallback distinguishes input failure/cancellation from failed publisher checkout.
  The Linux test runs the real validation and no-code summary scripts in an empty
  directory. This covers the previously skipped production branch without
  destination credentials or a deliberately failing public workflow.
- Package preparation and source-acceptance immutability were pre-existing policy
  specification gaps. Owner Step 4 admits their repair. Protocol/README changes
  add actual license/notices, aligned metadata, approved redistribution rights,
  complete export and source-time checks before frozen-source acceptance. First
  accepted main integration freezes the identity even without a remote tag.
  Candidate refinement, cadence, explicit owner exceptions, independent review,
  normal direct-main non-package work and non-automatic topic adoption remain.
  New mandatory operator work requires 3.0.0 MAJOR under accepted 2.7.0 rules.
  The other eight protocols and all package tool payloads retain accepted bytes.
- Shared Governance keeps its existing exporter/receipt and post-merge publisher.
  Its accepted MIT notices are reused. Landscape's accepted 1.0.0 packages need
  new versions for license/content repairs under separate owner authority; no
  rights decision, producer cutover or consumer migration is performed here.

## Test realism and limits

Focused tests use real disposable Git histories and explicit synthetic GitHub
PR/run evidence. They are not a replay of private producer permissions or proof
of substantive independent review. Source-time `check` also runs through the CLI,
without API or destination access. Missing/empty licenses, metadata mismatches,
unresolved rights, unpublished accepted same-version repair and candidate
refinement are separate scenarios. Arbitrary legal text still requires owner
review; the publisher cannot grant redistribution rights.

Pinned native staging, race, atomic push and retry mechanics remain unchanged.
Their earlier Step 2 evidence remains scoped to its recorded revisions. Fresh
native package materialization and exact export qualify the new 3.0.0 candidate;
no real distribution write is part of this Step. Linux is the supported shared
publisher platform. Native CI skips, if present, are not passes. Private caller
access, actual destination credentials/publication, producer activation and
consumer adoption remain separately authorized and unqualified.

## Commands and result binding

Run source/exact-export, distribution, release, self-adoption and ChatGPT tests
from a committed clean clone. Use the repository's pinned VibeVM 1.0.7 musl binary
for intentional local materialization and optional native tests. Record actual
counts/results below after execution; the canonical Outcome supplies the final
head's CI links and annotations without a self-referential source commit pin.
