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

Initial clean-clone qualification at `1092ab8c7dc81c17564a2e4d9b2277a0a639601a`
passed source/exact-export (675 files, 1,003 local links), all 43 focused publisher
tests including six native scenarios, 42 distribution tests, 17 release/dependency
tests including six native scenarios, and 12 self-adoption tests. No native tests
were skipped. The ChatGPT suite exposed two expected package-bump follow-ups:
the bounded preservation fixture still treated current package-versioning source
as forever unchanged, and the maintenance receipt recorded the earlier tool
version. Preservation now targets the unchanged retained 2.7.0 protocol; the
receipt is refreshed against the frozen accepted source/Step 4 authority.
Instructions content and live client settings are unchanged. This is fixture and
receipt maintenance, not activation of candidate policy or consumer adoption.

Follow-up at `f18cf6a16fb6f6044d9439a829298c9a3c858f59` passed all 24 ChatGPT tests
and confirmed `2.7.0 -> 3.0.0` with `Package bump: major`. Instructions stayed
5,132 Unicode characters and effective content was `NO_OP`; live settings were
not inspected or changed. The final focused implementation additionally requires
historical policy for every adapter and records policy-rotation PR/CI evidence
alongside package transitions. Its full pinned-native suite passes 44 tests,
zero skips; final-head CI checks the complete combined candidate separately.

The initial native authoring probe reported zero errors and three orphan-slot
warnings for retained 2.5.0/2.6.0/2.7.0 slots. No clean-check claim is made for that
inventory. A separate disposable clone performed deliberate fresh resolution of
the task-generated 3.0.0 lock with the pinned native installer; ordinary install
pruned the old slots there. With that native fixture inventory, the unmodified
authoring qualifier passed seven commands, zero findings, dependency installation
and overlay preservation. This did not delete any historical source/slot in the
PR and does not waive canonical exporter/lock/slot/route checks. Native absolute
URLs/timestamps remain location metadata, not acceptance evidence.

No production publication mechanics changed. Fresh local native tests nevertheless
also reran the six existing shared-publisher race/retry scenarios and all six
retained release/dependency integrations after temporal planning changed. All
distribution writes remained confined to disposable local bare repositories.
