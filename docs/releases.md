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
second release permission. The shared publisher remains an unactivated alternative.

The same unaccepted 3.0.0 candidate includes the owner-facing finding-report
clarification in Task Handoff and optional Independent Review. Aggregate impact
against accepted 2.7.0 remains MAJOR: new pre-merge preparation obligations and
explicit finding-report content refine mandatory operator behavior. Refining this
candidate before its first accepted main integration requires no 4.0.0 bump.
Frozen 2.7.0 and the existing post-accepted-merge publisher remain unchanged.

## Automatic publication and recovery

[Publish accepted package](../.github/workflows/publish.yml) runs after successful
Public candidate checks for a push to source main. It binds the accepted merge
or squash SHA, checks first-parent source-main membership and the version/payload
transition, and qualifies that exact accepted source. Unchanged packages skip.
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

Configure repository secret `DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN` with an
authorized fine-grained token granting Contents write on the distribution
repository only. The source repository's ordinary `GITHUB_TOKEN` cannot write
across repositories. Keep allowed writers with authorized maintainers/workflows;
credential setup is an owner/account action, not inferred from GitHub admin access.
The token is used only by Git askpass in the publication step; it is never placed
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
