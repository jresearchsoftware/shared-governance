# Task 52 Step 1 — preserve scope at review classification

Authority: [Task #52 and Step 1 Decision](https://github.com/jresearchsoftware/shared-governance/issues/52#issuecomment-6289901870).
Frozen independently accepted source-guidance baseline:
`e654d9e20a7c42c50cc05786dc83a4f7a16f84e4` (owner-integrated PR #55).
Strategy: Direct implementation of the owner-decided correction; independent
exact-head assessment remains pending. Candidate rules do not govern this effort.

## Bounded baseline and intended correction

Read the complete Task #52 charter/admission, its primary Task #9 / #45 / #51
records, and accepted native boot plus PC, RA, PV, TH, IR and SA protocols.
PC-004/PC-005/PC-009 already require owner authority and risk/cost assessment;
RA-002 distinguishes ratified requirements from engineering preferences;
IR-012–IR-015 already cover evidence, provenance and optional improvements.
The failure point is their application before a review finding becomes a
blocker or a proposed Task amendment. No publisher implementation changes belong
in this correction.

Planned semantic owners: new PC-013 for review-driven scope preservation;
IR-012–IR-015 for obligation binding, classification and owner-facing reporting.
Keep all existing IDs and conditional topic adoption. Keep specialist/local
rules, genuine security obligations and Task Handoff's authority, publication,
Step and readiness lifecycle. Use existing reports and canonical Decisions;
introduce no additional reviewer, checklist, ledger, service, approval or wait.

## Whole-package version intent

Package bump: major

Accepted 3.0.0 is frozen. The proposed 4.0.0 tightens mandatory report behavior
for existing PC/IR adopters: every blocking finding must explicitly identify
its binding obligation, and new requirements must be separately labeled before
negative publication or amendment discussion. Existing rules imply scope
discipline, but do not require that explicit obligation binding in each blocker.
This additional mandatory report content rules out PATCH; it changes existing
adopters' required behavior rather than merely offering a new optional topic,
so MINOR would also understate the change under PV-002. MAJOR is justified by
that concrete contract tightening, not the size or security label of the edit.
There is no additional approval event or per-PR owner reapproval. Consumer
migration remains separately authorized; this effort stays bound to 3.0.0.

Coverage, realistic authoring scenarios and executed qualification will be
completed here before the canonical Outcome and independent review handoff.
