# This producer's release policy

This repository adopts the [package-versioning protocol](../packages/development-governance/vibevm/vibespecs/protocols/package-versioning.md)
for its package lifecycle. It owns one package at the stable
`packages/development-governance` path. `[package].version` is the sole authored
whole-package version. Frozen `0.1.0`, historical receipts and the active
proportional-controls snapshot are retained unchanged. Package splitting,
parallel major maintenance lines and consumer migration need separate decisions.

## Contribution and integration

Each independently accepted package-changing PR increments the whole-package
version once against current accepted `main`. Its English description contains
one `Package bump: major`, `Package bump: minor` or `Package bump: patch` line
and explains consumer-contract and operator-work impact. A PR with several edits
uses at least the highest-impact category. CI checks the numeric transition;
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
