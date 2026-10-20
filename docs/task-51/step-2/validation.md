# Task 51 Step 2 — Correct shared publisher regressions

Authority: [Step 2 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/51#issuecomment-6287269790)
following the [independent Change Request](https://github.com/jresearchsoftware/shared-governance/pull/54#issuecomment-6287251064).
Accepted guidance remains `c26d0fc3a287dca86c36855b6b5230509f98152a`.
Starting result is PR 54 at `0bd120180b4db6a72a201bf1bb73542cc6f7d98f`.
This Step updates that same PR under Direct and leaves Step 1's Outcome/evidence
and Change Request intact. PR 54 was converted from Ready to Draft and verified
at the starting head before modification.

## Reproduction and correction

The seven new focused tests were run against the unchanged starting publisher
in a disposable Debian Git clone. They failed with five failures/one error,
including `NO_PACKAGE_CHANGE, READY` for binding-only B onboarding and sibling-A
inspection in selected-B plan/check/stage. Two positive new-package/new-version
controls and selected-A CI/trigger validation already passed. See the
[before-correction log](logs/before.log). These are executed reproductions,
not merely the reasoned paths reported by independent review.

| Change Request | Correction and focused evidence |
| --- | --- |
| CR-1: preexisting unbound B added to A's binding | If the immediate previous binding lacks B, export B's actual previous source with B's current approved selection. Unchanged old 1.0.1 is a no-op with no CI query. Same-version mutation is rejected; new 1.0.2 and genuinely first-introduced B qualify normally. Existing bound entries retain their own previous inventory. |
| CR-2: selected no-op B checks changed A | Select coordinates inside the planners before package export/readiness/API work, keeping the full source binding for exact-source identity checks. Actual CLI main plan/check/stage tests prohibit sibling export/readiness, API/CI, trigger, dependency and destination access and return only B's no-op. A valid selected A still verifies its exact current push CI and triggering run; wrong CI or trigger is rejected. Unknown selection fails before package evidence. |
| Affected staging/explicit-mode interaction | Stage by report coordinate rather than position in the full binding. A real selected-B native release has B's exact exported blobs/destination and leaves A's destination empty. Explicit initial-publication selection of B avoids A's payload while retaining B's old-source and onboarding owner acceptance/current CI. |

This is a repair of the existing no-op and sibling-isolation contract, without
historical audit, new release ledger, approval gate or dependency resolver.
The optional library `selected` parameter defaults to all packages; the CLI's
existing `--package` interface and reusable workflow input are unchanged.

## Qualification

The source/test bytes were exercised with Python 3.11.2 on Debian in a disposable
native Git clone. VibeVM 1.0.7 musl SHA-256 was reverified as
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Focused regression result: **7 passed**; full native publisher result:
**74 passed, zero skips**. Primary exact-commit results and final-head CI will
be bound in the canonical Step 2 Outcome. All native publication writes stay
inside disposable local bare repositories.

Reproduce at the result revision:

```sh
python3 tooling/vibe-publisher/test_publisher.py PackageOnboardingTests PackageSelectionTests
python3 tooling/vibe-publisher/test_publisher.py --vibe /absolute/pinned/vibe -v
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-release.py --vibe /absolute/pinned/vibe
python3 scripts/test-self-adoption.py
git diff --check 0bd120180b4db6a72a201bf1bb73542cc6f7d98f HEAD
```

The full publisher suite retains current source-main/CI/trigger, version,
license/redistribution, native frozen closure, existing-tag/atomic-push/race,
same-source retry and isolated initial-publication coverage. The active producer
workflow, package payload/version, consumer bindings and protected boundaries are
unchanged. No full package-manager transport requalification is introduced.

## Retained limits and handoff

VibeVM 1.0.7's unsupported literal `dev-requires` / inline `optional=true` syntax
remains explicitly documented in [Step 1](../step-1/validation.md). Its passing
negative test is not proof of successful publication for unsupported syntax.
Real private callers, cross-repository credentials, live remote publication and
Windows/macOS native staging remain unqualified; this correction needs none of
those protected mutations.

One attributable Step 2 Outcome belongs on PR 54; after its durable readback,
mark the same completed exact head Ready and verify. Independent review and any
merge/release remain pending. No package bump, producer cutover, Landscape or
consumer change, credentials/settings mutation, Task 52/53 work or closure is
performed. Historical Step 1 records are preserved.
