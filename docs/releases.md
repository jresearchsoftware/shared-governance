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

Task 65 prepares **6.0.0 MAJOR** against accepted 5.2.3. Package Versioning's
existing cadence/actual-compatibility rules now require explicit floor and
constraint justification and distinguish the authority used by resolved and
bundled delivery. This tightens adopters' lifecycle assessment; it adds no new
topic, approval stage or universal compatibility matrix. The installed changelog
states the consumer/operator impact, and [Step 1 coverage](task-65/step-1/README.md)
traces the change and bounded scenarios. The Task 74 PATCH exception below does
not apply. Independent acceptance and then-current-main reconciliation remain
required; no source acceptance, external release or consumer adoption is claimed.

An upstream dependency release alone does not require a dependent release here
or in another producer. The dependent product's actual contract and shipped
immutable bytes determine its change and classification, while existing rights,
manifest, included-closure and publication obligations remain binding. This
producer's reusable flow still has an empty dependency closure; its authoring
workspace's unchanged Relay Skill is a separate dependency consumer, not a new
dependency of the public governance package.

Task 74's [superseding owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/74#issuecomment-6386467528)
selects one PATCH, 5.2.0 -> 5.2.1, for restoring the originally intended TH-029
effective-Instructions reconciliation requirement narrowed in Task 62/PR 63.
Accepted 5.2.0 expressly documented application only when included in Task scope;
the correction changes that published workflow obligation and would ordinarily
be MAJOR under PV-002. This is an explicit single-task exception, not unchanged
consumer-facing behavior or a revision of general PV-002. The unaccepted 6.0.0
candidate is superseded, not a release. Frozen releases, historical acceptance and
separate consumer update/adoption authority remain intact. Recompute one PATCH
against current accepted main before integration; see [Step 2 evidence](task-74/step-2/README.md).

Task 52 proposes 4.0.0 against frozen accepted 3.0.0: explicit per-blocker
obligation binding and prepublication proposed-requirement classification tighten
mandatory PC/IR report content. This is a concrete MAJOR contract change, without
an additional approval or publication stage. See the installed changelog and
[coverage/scenarios](task-52/step-1/README.md). Earlier references here to an
unaccepted 3.0.0 candidate retain Task 45's historical context; 3.0.0 is now the
accepted baseline and cannot be refined in place.

Each independently accepted package-changing PR increments the whole-package
version once against current accepted `main`. CI compares the actual package
payload and canonical `[package].version` at those exact source commits. A changed
payload must advance by exactly one numeric major, minor or patch step with the
required resets; unchanged packages need no bump. Candidate CI also rejects a
proposed version whose distribution tag already exists. PR descriptions are not
release-check input: absent, duplicate or contradictory `Package bump` lines
neither fail the check nor override versioned source. Automatic Relay Writer
descriptions require no producer-specific field or metadata update.

Under accepted shared PV-002–004, explain the intended compatibility category and
mandatory operator-work impact in the existing PR review or release decision,
supported where useful by the versioned changelog. Independent review assesses
that rationale against the actual consumer-contract changes; numeric arithmetic
alone does not establish semantic compatibility. A PR with several edits uses at
least the highest-impact category. This requires no additional PR field, form or
release ritual. Tooling, research and documentation outside the package do not
bump or publish a package.

Task 9 declares stable `1.0.0` from experimental `0.1.0` as a MAJOR transition.
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

## Codex Relay compatibility transition

When a Shared Governance behavior change needs a corresponding incompatible
Codex Relay implementation, this producer may publish the agreed Shared contract
before that Relay release through an explicit owner-selected transition. This
producer-local exception applies only to Codex Relay integration; other Shared
rule changes and other projects have no mandatory grace period. Preserve Relay's
existing [installed and retained-attempt compatibility contract](../.agents/skills/codex-relay/references/compatibility.md).

Use the behavior-change Task and existing release/review rationale to define
the transition, without a registry, feature switch or additional approval ritual:

1. Identify the affected rule and the **first Shared Governance package version
   containing it**. Describe the new behavior, the old Relay behavior and the
   narrow temporary fallback explicitly permitted by the accepted change. Name
   the older Relay versions, selected Shared versions, affected workflows and
   limits actually qualified together, with supporting compatibility evidence.
   This lets a consumer deliberately update Shared while retaining that Relay's
   old behavior for the identified rule during the supported window. Neither a
   successful install nor an open-ended constraint proves this compatibility;
   unqualified combinations and unknown future versions gain no support claim.
2. Require a linked implementation Issue in
   [jresearchsoftware/codex-relay](https://github.com/jresearchsoftware/codex-relay/issues)
   as part of that Shared behavior-change Task's completion/continuation. Record
   the introducing Shared version, desired Relay behavior, superseded old
   behavior, compatibility checks and how Relay's release will update its
   declared floor; link back to the Shared Task. For the imminent Task Closure
   change, create this Issue **after that Shared change is independently accepted,
   merged and published**. Creating it belongs to that behavior-change Task's
   continuation, not this instruction-only Task.
3. Until Relay implements the linked Issue, retain the older version's declared
   compatibility floor (currently `>=2.5.0` for Relay Skill 3.0.0), with transition
   support limited to versions and behaviors actually qualified under the
   fallback. Relay owns its implementation and release: once accepted and
   released, the new Relay version must declare compatibility starting at the
   first Shared version supplying the behavior it now requires, supported by
   the linked Issue's checks. Previously published Relay artifacts and their
   pins remain immutable. An unchanged lower bound is never a promise that all
   later Shared versions work.
4. Explicitly deprecate the legacy behavior. Before relying on the fallback,
   record the owner's bounded transition window and its reference event,
   preferably verified publication of the compatible Relay release, with a
   finite duration or deadline. Plan removal separately in a future Shared
   release, subject to independent acceptance and no earlier than the agreed
   window's end. There is no universal duration, automatic deletion or silent
   early withdrawal; released artifacts retain their historical content.

Keep source acceptance, immutable package publication, the consumer's deliberate
lock update and policy adoption, and qualification of its installed Relay
distinct. The fallback permits only the stated old behavior; it does not load an
old Shared snapshot in place of the selected package or waive native Relay trust
boundaries. Publishing this local instruction changes no active Relay behavior,
consumer dependency, closure policy or installed setting. Documentation outside
the exported package needs no package release.

Classify each actual Shared behavior change and later fallback removal under
PV-002/004 for the whole package, preserving the highest-impact category and
mandatory operator-work disclosure. A narrow Relay fallback cannot disguise an
otherwise breaking contract as PATCH or MINOR or extend Task 74's separate
single-task exception.

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
Candidate 3.0.0 adds these mandatory obligations as a MAJOR change,
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
