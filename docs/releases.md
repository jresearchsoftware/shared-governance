# This producer's release policy

This repository adopts accepted `package-versioning` through its
[native self-adoption](self-adoption.md) route for its package lifecycle.
Editable package source is assessed as candidate content. It owns one package at the stable
`packages/development-governance` path. `[package].version` is the sole authored
whole-package version. Frozen `0.1.0` and historical evidence remain unchanged.
Active guidance is frozen from independently accepted source-main, separately from
public publication. Package splitting,
parallel major maintenance lines and consumer migration need separate decisions.

Task 45 refines one unaccepted 3.0.0 MAJOR candidate from accepted 2.7.0, including
preparation requirements, review-topic ownership and installed rule/change-history
addresses. Refinement before first acceptance needs no 4.0.0. See the packaged
[changelog and adoption impact](../packages/development-governance/CHANGELOG.md).
Independent Review is explicitly adopted only for this producer's relevant
assessments. Other consumers retain their own adoption and local policy.

## Contribution and integration

Task 52 proposes 4.0.0 against frozen accepted 3.0.0: explicit per-blocker
obligation binding and prepublication proposed-requirement classification tighten
mandatory PC/IR report content. This is a concrete MAJOR contract change, without
an additional approval or publication stage. See the installed changelog and
[coverage/scenarios](task-52/step-1/README.md). Earlier references here to an
unaccepted 3.0.0 candidate retain Task 45's historical context; 3.0.0 is now the
accepted baseline and cannot be refined in place.

Each independently accepted package-changing PR increments the whole-package
version once against current accepted `main`. Its English description contains
one `Package bump: major`, `Package bump: minor` or `Package bump: patch` line
and explains consumer-contract and operator-work impact. A PR with several edits
uses at least the highest-impact category. CI checks the numeric transition and
rejects a proposed version whose distribution tag already exists;
independent review checks whether the category is truthful. Tooling, research
and documentation outside the package do not bump or publish a package.

Task 9 declares stable `1.0.0` from experimental `0.1.0` with `Package bump: major`.
It adds an explicitly adopted protocol and this repository's automatic release
workflow; it preserves proportional-controls bytes and existing consumer authority.
After this stable declaration, major/minor/patch follows the shared contract.
An experimental producer elsewhere may choose a disclosed breaking `0.x` minor;
this repository's release cadence is not a requirement on its consumers.

Concurrent PRs retain category intent, reconcile onto current main before merge,
recompute the next version, and repeat exact-head checks/review after head changes.
No version reservation or multi-merge mechanism exists. For example, major then
patch from `1.95.0` yields `2.0.0` then `2.0.1`; two majors yield `2.0.0` then
`3.0.0`. Existing frozen content cannot be changed under the same version.
CI is evidence; the owner's independently reviewed merge is the publication
authorization for the version-bearing PR, never self-approval or consumer adoption.

## Frozen-package preparation

Before accepting a frozen package-source PR into main, prepare its actual public
`LICENSE`, aligned manifest metadata, approved redistribution rights, complete
public export inventory and source-time qualification. This producer retains its
accepted MIT license and notices; Task 45 makes no new rights decision. Export
qualification and the release-transition check run before merge. The publisher
verifies prepared source; it must not silently add missing files after merge.

The first independently accepted main integration freezes this identity and its
payload, even if there is no distribution tag, credential or publication service.
A later license, inventory, metadata or content correction needs a new version.
Candidate 3.0.0 adds these mandatory obligations under `Package bump: major`,
compared with accepted 2.7.0; its source and native projection are proposals until
independently accepted. Historical accepted source, receipts and tags stay intact.

An independently reviewed package-changing owner merge plus successful main push
CI continues to authorize the existing automatic publication below. Preparing
this candidate grants no merge or manual publication authority and adds no
second release permission. Task 53 proposes the shared-publisher cutover described
below; independent review and authorized integration remain separate.

The same unaccepted 3.0.0 candidate includes the owner-facing finding-report
clarification in Task Handoff and optional Independent Review. Aggregate impact
against accepted 2.7.0 remains MAJOR: new pre-merge preparation obligations and
explicit finding-report content refine mandatory operator behavior. Refining this
candidate before its first accepted main integration requires no 4.0.0 bump.
Frozen 2.7.0 and the existing post-accepted-merge publisher remain unchanged.

## Automatic publication and recovery

[Publish accepted package](../.github/workflows/publish.yml) runs after successful
Public candidate checks for a push to source main. It binds the accepted merge
or squash SHA (ordinary merge, rebase and eligible direct-main also work), checks
first-parent source-main membership and the version/payload transition, and
qualifies that exact accepted source. Unchanged packages skip. The candidate
caller delegates staging and publication to `./.github/workflows/vibe-publisher.yml`
from its own executing workflow revision, passing only the exact triggering
`source_sha` and its committed [producer binding](../vibe-publisher.json).
There is no independent producer-policy SHA or PR/integrator eligibility gate.

An unprivileged readiness job uses that same workflow revision's planner and checks the
producer's affirmative MIT redistribution acknowledgement for changed packages.
The accepted governance adapter already checks license bytes/metadata, exact
export inventory and the dependency-free passive contract; its early return
precedes tree-v1's generic rights acknowledgement. This small producer check
closes that integration gap without copying the publisher. Its reference is
the owner's original [public MIT bootstrap request](https://github.com/jresearchsoftware/codex-relay/issues/83#issuecomment-6037643777),
implemented by the accepted root/package LICENSE grant. It acknowledges existing
rights while applicable, creates no new rights and adds no per-release approval.
Unchanged packages skip before rights/CI/destination/native-tool work.
The explicit direct-Git destination is
[jrs-vibevm/org.jresearch.ai.development-governance](https://github.com/jrs-vibevm/org.jresearch.ai.development-governance).
There is no registry service. Source `publish=false` excludes workspace batch
enumeration; the explicit direct publisher supports it.

For a changed version, an existing tag is a successful no-op: no native publisher
invocation and no ref mutation. When absent, the pinned native publisher builds
the normal package release in a disposable bare copy of the distribution repo.
An ordinary atomic push of distribution main and the new tag, without force,
publishes it. A concurrent tag creation or divergent main rejects the entire
push. This bounded staging step addresses VibeVM 1.0.7's demonstrated ability to
replace existing tags, including the precheck race; it is not a release-control
subsystem. No global highest-version gate is imposed: distribution main means
last published payload and advances in Git history. Actual older maintenance
source lines remain deferred.

The Actions result and step summary show published, already-published, skipped
or failed/pending state and exact source SHA. A failure does not undo source
acceptance or imply publication. Recover the credential/network/concurrency
failure, then rerun the failed workflow or manually dispatch **Publish accepted
package** from main with that same full `source_sha`. Dispatch requires successful
push CI at that SHA and accepted first-parent membership; candidate side-branch
heads and unaccepted commits are rejected. Retry does not bump, overwrite or
silently publish current HEAD. Existing tags remain untouched after an ambiguous
transport result. A release defect is repaired in a new reviewed version.

Use the established `DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN` Actions secret through
its existing organization/repository access arrangement. The source repository's
ordinary `GITHUB_TOKEN` cannot write across repositories. Keep allowed writers
with authorized maintainers/workflows; changes to credential access are an
owner/account action, not inferred from GitHub admin access. New producers reuse
the shared secret instead of creating their own tokens.
The local reusable workflow receives the token only in finalization.
Task 58's [shared credential/provisioning implementation](shared-publisher.md#shared-credential-and-destination-provisioning)
uses it for bound destination API operations after native staging. The existing named
organization secret is shared with authorized producer repositories; do not
create project-specific tokens or assume another repository's secret is visible.
This caller follows accepted publisher changes centrally; external producers use
`@main` after their separately authorized migration. Readiness and reusable code
resolve their implementation from `job.workflow_sha`, independently of the exact
producer release source. No secret access is changed. The full-organization
visibility premise for missing destinations is documented in the shared contract.
The token is never placed
in a remote URL, persisted config, artifact or log. PR checks receive no publisher
secret. No environment approval gate or second release approval is added.

## Proportional controls and validation

The concrete risks are silent frozen-tag replacement, package changes reusing a
version, publication from an unaccepted head and implicit consumer authority
transfer. The cheap controls are source-transition CI, existing independent
review, first-parent/CI binding, remote-tag skip, atomic non-force Git publication,
and explicit conditional consumer routing. They reuse existing Git/Actions state;
there is no ledger, service, per-protocol activation registry or status synchronizer.

This package's dependency closure is empty and the passive export rejects an
undeclared dependency. If dependencies are admitted later, qualify the resolved
actually included graph's frozen metadata/tool hashes at release time, preserving
optional/dev exclusions and explicitly justified exceptions as in the shared
protocol. Do not silently enable dependencies by adding top-level ranges.

Routine reviewers assess the change, category, authority and available CI evidence.
They do not re-run native publication or recalculate every remote blob hash.
Pinned-tool publisher/consumer, transitive conflict/update and concurrency probes
are one-time integration qualification. Existing full integrity/incident probes
remain diagnostic tools. No recurring package-manager transport ritual is required.

## Task 53 cutover and older-source recovery

The migration PR changes the single publishing workflow in place. Until its
independent acceptance and separately authorized integration, the existing main
workflow remains the production path. Integrating the tooling/binding-only
change is a no-op for unchanged 3.0.0; do not create a test release. Candidate
fixtures use disposable local Git and unprivileged Actions. Actual new-main
CI/no-op and the next genuine accepted release need later live verification.

Retry post-cutover releases with the same full source SHA via the existing
workflow name. A pre-cutover source has no binding: rerun its original failed
workflow run using its original implementation, never today's binding injected
into old source. The retained package-release.py publication code supports those
historical fixtures/original-run recovery; the new workflow never invokes it for
publication. Its category/arithmetic and pre-merge tag-reuse CLI remains active.
All five recent production runs succeeded at migration discovery.

If later authorized, rollback is an ordinary reviewed revert of the caller and
integration changes. It does not undo accepted source, move public tags or
release an unchanged package. Recover failed releases using their original
source and implementation; repair package defects forward in a new version.
