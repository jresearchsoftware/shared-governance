# Task 13 — Step 1 — Workflow-aware GitHub repository governance

This dated authoring evidence supports the source proposal for [Task 13](https://github.com/jresearchsoftware/shared-governance/issues/13)
under its [Step 1 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/13#issuecomment-6143460763).
The Issue body, [workflow-mode clarification](https://github.com/jresearchsoftware/shared-governance/issues/13#issuecomment-6097019681)
and both comments were read in full. The Decision supersedes backlog admission
only; all semantic scope, exceptions and external-mutation exclusions remain.

## Authority and provenance

Frozen independently accepted source-main:
`1b97f0aadcc769c04415d8f4855098cee35b9f3a`. Startup fetch matched live main and
PR 27's squash commit. Its root AGENTS, native authoring/package boot, all five
applicable protocols, CONTRIBUTING, authoring, manual handoff, release and
self-adoption bindings were read through Git. Candidate files are proposal data.
Task 9's accepted compatibility/adoption and release decisions inform the
version; Relay Task 90 confirms the separate product-provisioning boundary.

The protocol is new synthesis from Task 13's complete public charter and owner
clarification, constrained by accepted proportional-controls and the five
existing protocols. It does not extract or transfer a consumer's canonical
policy. The reference example uses the public Issue's description; private
consumer content and identity evidence are not exported into this public PR.

Current primary GitHub documentation was inspected on 2026-10-13:

- [Protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): feature availability, ordinary force/deletion restrictions, admin exceptions, native checks/reviews and merge compatibility.
- [Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): branch/tag targeting, permissions, inheritance/layering and enforcement state.
- [Rules REST API](https://docs.github.com/en/rest/repos/rules) and [protection REST API](https://docs.github.com/en/rest/branches/branch-protection): read surfaces, pagination, active-rules scope and concealed bypass details.
- [Merge methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github) and [automatic deletion](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches): independent options and retained-branch exceptions.

These document product capability, not owner choices. Policy recommendations and
cadence are the candidate's reasoning, not facts asserted by GitHub. Links are
provided inside the shipped passive protocol so later owners can verify their
host/version and plan rather than treat the dated investigation as permanent.

[Read-only public GitHub observations](logs/github-observations.json) bind the
source/distribution examples and the 2.0.0 published source receipt. Merge
options match the charter. Empty API-visible rulesets/active branch rules and
classic-protection 404s do not prove complete protection absence or qualify an
enforced workflow. No destructive experiment or configuration change occurred.

## Recommendations and credible alternatives

| Choice | Candidate recommendation / rationale | Alternative and tradeoff |
| --- | --- | --- |
| Important branch history | Recommend force/deletion prevention where available at justified cost, while retaining ordinary authorized non-force pushes. Silent loss propagates; current non-force practice helps but cannot enforce other writers. | Accepted procedural practice/recovery evidence can suffice where risk permits or capability is unavailable. Mandatory plan upgrades and unconditional locks add cost and can break legitimate updates. |
| Governed development | Retain task/PR traceability, substantive exact-result independent acceptance and meaningful checks without requiring Relay. Prefer a compatible PR route; native count/identity gates need a concrete local decision. | Blanket distinct-account approvals add unavailable reviewer/credential prerequisites in manual projects. Pure checks alone cannot establish independent policy acceptance. |
| PR integration / cleanup | Squash-only plus auto-delete is the starting candidate for disposable PR branches. Small operator cost prevents accidental merge-style choices and stale task branches. | Merge/rebase or auto-delete off remains appropriate for meaningful commit topology, retained integration branches and supported tooling. Direct-main projects need not spend effort on unused merge settings. |
| Reference materiality | Routine dated factual updates retain direct-main; material recommendation/contract effects warrant independent evidence assessment and owner adoption through the accepted path. | PRs for every refresh create repeated friction; treating a policy change as routine evidence can silently change obligations. A durable non-PR review path can suffice. |
| Verification cadence | Onboarding/first adoption once; relevant changes or suspected drift recheck affected surfaces; meaningful changes get relevant source/assessment checks. | Per-session settings checks and periodic audits without risk evidence repeat proof and add maintenance. Never rechecking after a relevant change permits unnoticed drift. |
| Distribution/hybrid | Reuse accepted release/no-overwrite boundaries and inspect writer/bypass scope; retain distinct source, direct-main and publication paths. | Universal PR-only distribution blocks supported atomic publication. Broad publisher bypass risks weakening unrelated history/tag protections. |

These are recommendations awaiting **Deliberative** independent assessment and
owner selection, not ratified defaults. No material open question prevents a
coherent reviewable candidate. Remaining owner choices are whether to accept
this recommended protection floor, PR merge defaults/exceptions, materiality
escalation and event-driven cadence, or request a different proposal. Adoption
or actual settings in each consumer requires that consumer's own authority.

## Semantic coverage and ownership

| Canonical Task obligation / boundary | Candidate coverage |
| --- | --- |
| Actual workflow, manual governed baseline, Relay not defining criterion | Working-model table and manual PR walk; product schemas/provisioning remain local. |
| Routine reference direct-main plus material guidance distinction | Materiality examples, reference walk and cadence; no compulsory Task Request/blanket PR. |
| Distribution role, immutable publication, Task 9 coordination | Publication section and walk defer release policy; no second cadence or frozen-release edits. |
| Mixed paths, real writers, supported exceptions | Hybrid walk, scoped bypass analysis and retained-branch handling. |
| Minimal main/history protections, merge/review/check alternatives | Proportional selection table compares current protection, costs and alternatives; stronger local rules retained. |
| Plan/permissions, UI/API verification, unavailable capability | Effective-setting section and optional GET examples; no 404 absence inference or privilege workaround. |
| Onboarding, relevant-change recheck, per-change validation | Cadence table and five-step new/existing checklist; no periodic audit or state service. |
| Passive guidance and separate consumer adoption | Opening applicability plus explicitly conditional boot; no producer adoption of the added topic. |
| Whole-package lifecycle and complete projection | 2.1.0 manifest/dependency, exporter file-set rules, generated registry/slot/lock/boot and integrity regressions. |

All five accepted protocol files are preserved byte-for-byte. Availability of
the sixth topic does not automatically activate it, alter their triggers,
introduce a Skill/capability/dependency or supersede local authority. Root's
five adopted topics remain intact. No reusable Task obligation was knowingly
omitted or left to a consumer residual duplicate. Local GitHub/Relay provisioning,
native authority schemas, installed consumers, protected operations and future
package splitting remain with their existing owners.

**Package bump: minor — 2.0.0 to 2.1.0.** The addition is compatible precisely
because newly available normative guidance requires explicit project adoption.
Existing consumers' mandatory behavior, local authority, supported workflows
and all five protocols are unchanged. Adoption of cost-bearing controls is
separate. A new file alone would not justify minor; automatic activation would
require major. Recompute this intent against then-current main before integration.

## Qualification scope

[Semantic walks](scenarios.md) exercise PR, direct-main, publication, hybrid,
existing/new consumer and unavailable-evidence paths without residual local
consumer rules. They are desk-based application evidence, not GitHub enforcement
or model compliance. Source/export/native consistency and existing regressions
are exercised separately; complete receipts are in `logs/`.

The first distribution run failed all 31 cases during fixture setup: the test
copied the six-topic source but relabeled it 1.3.0, whose accepted shape has five
topics. [Initial log](logs/distribution-initial.txt) is retained. The fixture's
version, slot, tag and negative substitutions now consistently use 2.1.0; the
accepted 2.0.0 five-topic export remains a separate historical regression.
No passivity/integrity guard was weakened. An earlier malformed full-SHA staging
invocation was rejected before mutation; staging with the resolved full commit
then passed. These in-Step corrections do not change package content or bump
intent and require no separate execution admission.

No live settings/protections, release refs, credentials, existing consumer
installation, Relay workflow or package publication is exercised. Existing
native transport/Windows-to-Linux and loader qualification is reused; routine
source addition does not justify repeating unchanged package-manager incident
or client-startup integration. Optional native integration tests remain explicitly
skipped when the pinned Linux tool is not supplied, not counted as passes.
The accepted Windows Codex CLI startup gap remains unqualified; no ACL/sandbox
or host repair is attempted. CLI/file/projection checks do not prove model behavior.

One result PR owns this source and supporting evidence. The canonical terminal
Codex Outcome belongs as one top-level comment on that PR, linked to Task 13.
The implementer stops for substantive independent exact-head non-approving
assessment, then owner discussion/Decision under Deliberative. No formal APPROVE,
approval-driven merge, release or Task closure follows from this report.
