Related to #74.

Package bump: patch

Restore the originally intended TH-029 requirement: when a Task changes its adopting
project's complete generated ChatGPT Project Instructions, it must reconcile live
Settings after accepted integration and before closure, even if the charter omitted
application. Preserve no-op/cache/SHA-only exemptions and earlier unresolved gaps.
Where text differs or currentness is unconfirmed, present the full raw Markdown
replacement for owner review/manual application and obtain supported readback or
attributable owner-confirmed live content. Generation and merge do not prove a match.

The [superseding owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/74#issuecomment-6386467528)
selects **5.2.0 -> 5.2.1 PATCH as an explicit single-task exception to PV-002**.
The requirement was narrowed during Task 62/PR 63 translation. Accepted 5.2.0
visibly documented the narrower explicit-application condition, so this correction
changes the published workflow obligation and ordinarily requires MAJOR. The PATCH
label does not claim unchanged consumer-facing behavior. General PV-002 and historical
acceptance/releases remain unchanged; consumers intentionally update/adopt under
their own authority. The superseded 6.0.0 candidate was never an accepted release.

Source, changelog, local bindings/operator guidance and native registry/slot/lock/boot
are aligned to 5.2.1. Relay 3.0.0 and frozen historical packages are preserved.
Recompute one PATCH against current accepted main if it advances before integration.

See [Step 2 qualification](https://github.com/jresearchsoftware/shared-governance/blob/codex/task-74/docs/task-74/step-2/README.md)
for local checks and evidence limits. Native exact-head CI and fresh independent
review remain required. Task 74 changes this producer's desired Instructions;
post-integration owner application/readback remains an unresolved completion hold.
No downstream consumer migration is required for this producer Task's completion.
