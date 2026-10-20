# Task 53 Step 1 — Producer migration candidate

Authority: [Task 53](https://github.com/jresearchsoftware/shared-governance/issues/53)
and [Step 1 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/53#issuecomment-6289365518).
Frozen independently accepted guidance and executable publisher pin:
`5a1e5de66388501235fc9ffd23d45efb34df2b85`, the owner-integrated Task 51 / PR 54
result after independent Direct APPROVE. Strategy: Direct. Complete Task 53
chronology at execution start: charter and that admission. Package and installed
governance remain unchanged. No consumer adoption or live cutover is performed.

## Bounded baseline and condition comparison

Baseline: accepted publish.yml, candidate.yml, producer release/distribution
policy, package-release.py, prepare-distribution.py, shared publisher and export
adapter at the frozen pin. One publishing entrypoint delegates staging and
finalization to the exact accepted reusable workflow.

| Condition | Existing production path and candidate disposition |
| --- | --- |
| Eligibility | Preserve first-parent source-main and exact successful push CI. Pinned planner validates run repository IDs, branch, workflow path, event, status and SHA; fetches actual workflow_run trigger. No PR/squash/integrator restriction for ordinary merge/rebase/direct-main. |
| Identity | Source and embedded binding both come from triggering source_sha. Implementation is pinned in uses. No moving policy, redundant SHA input, historical audit or baseline disposition. |
| Version | Shared planner compares exported payloads with first parent, rejecting invalid/same-version changes. Existing local Package bump category/arithmetic and pre-merge tag checks stay active unchanged. Tooling-only migration has no package bump. |
| Export/inventory/disclosure | shared-governance-v1 calls the identical accepted exporter: version-aware explicit files, producer-only exclusions, standalone links, public-source receipt, SHA/path provenance and exact bytes. Tree-v1 inventory/disclosure configuration is inapplicable. Switching adapters would change receipt format and is avoided. |
| Dependencies | Existing dependency-free contract remains: exporter rejects unexpected manifest sections/capabilities. Common dependency support adds no producer capability or dependency requirement. |
| Rights | Identical actual MIT notices and metadata validated by exporter. Binding acknowledges original owner-authorized public MIT bootstrap. Governance adapter returns before tree-v1's rights check, so small producer readiness check enforces affirmative acknowledgement for changed packages. Missing/unapproved/mismatched rights reject; no-op precedes retrofitting. This implements the already owner-selected condition, not another legal approval system. |
| Publish/retry | Same destination/native pin, secret-free staging, single atomic non-force main/tag push, existing-tag skip and same-source retry. Shared readback improves ambiguous-push diagnostics without extra owner action. Old pre-binding sources recover through their original workflow runs. |
| Credentials | Existing destination-only named token used only in shared finalize/ephemeral askpass. Producer readiness uses read-only source token. PR fixtures pass only public sentinel; no secret inheritance. |
| Availability | Main's existing workflow remains active until authorized integration. Candidate replaces it in place, with no second publishing trigger. Tooling/binding-only integration is a no-op. |

Real rights reference: [Relay bootstrap Task Request](https://github.com/jresearchsoftware/codex-relay/issues/83#issuecomment-6037643777)
authorizes public neutral source with MIT licensing. Owner-authored
`a8d122a3f6121fcf5a52860f355b72626f214558:LICENSE` grants redistribution with
derived-governance notices; exact notices remain in accepted root/package LICENSE.
Accepted producer policy retains those rights and says Task 45 creates no new
rights decision. The binding reuses this actual grant while applicable; new
content with different rights needs its own disposition. No fabricated approval.

## Qualification and boundaries

test-publication.py uses the actual accepted 3.0.0 package in disposable Git
repositories. It exercises onboarding/later-tooling no-op before API/destination
work; exact committed binding despite worktree tampering; wrong source CI and
first-parent rejection; ordinary merge/squash/rebase/direct-main without PR API;
missing rights/license; version reuse; dependency-free export; complete file and
receipt equality. Native mode stages/publishes only to disposable local bare Git,
with failed-push/same-source retry and immutable existing collision. GitHub
evidence in local fixtures is synthetic, not live-release evidence.

The unprivileged PR workflow calls the exact accepted reusable pin in fixture
mode with public sentinel, checks the candidate's real embedded binding/no-op
against accepted main, and probes read-only real GitHub push CI. Common publisher
tests cover trigger mismatch, native atomic concurrent writers, secret stripping
and included dependency interactions. Existing release tests retain category,
arithmetic and pre-merge remote-tag rejection. Results are recorded below and
bound to final head in the one canonical PR Outcome.

Discovery readback: source main `5a1e5de66388501235fc9ffd23d45efb34df2b85`;
distribution main `b6fefd51c2c34e4001e1709c9c157dfa2296ad60`;
annotated v3.0.0 tag `ce178e7985170cbf6d25315782cc7f78007afba5`.
Most recent legacy production run
[39411743874](https://github.com/jresearchsoftware/shared-governance/actions/runs/39411743874)
and four preceding observed runs succeeded. Recheck refs before terminal handoff.

Independent review, owner integration/activation, new-main CI/no-op, actual
cross-repository credentials/live release and Task closure remain separate.
Fixtures do not qualify live publication or independent native reviewer identity.
Retained local publication code serves historical fixtures/original-run recovery;
the candidate's active workflow does not call it. Cutover and ordinary reviewed
rollback/recovery are documented in the producer release policy.
