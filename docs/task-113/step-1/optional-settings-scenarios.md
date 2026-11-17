# Task 113 Step 1 — optional GitHub setting decisions

Source candidate: [Issue 105](https://github.com/jresearchsoftware/shared-governance/issues/105).
Receiving authority: [Task 113](https://github.com/jresearchsoftware/shared-governance/issues/113),
Step 1. This authoring effort remains bound to independently accepted source-main
`f8d77b16ab9e92b31ae9a9390acabd9be9e962a7` throughout. Candidate instructions
are proposed content. These are implementation self-checks, not independent
acceptance, actual consumer onboarding or live GitHub qualification.

## Bounded baseline and change

Read the accepted root/native routes and full GH, RA, PC and PV protocols from
that commit's Development Governance 11.0.0 slot, then compare the canonical
authored GH protocol and onboarding procedure/examples as proposed content.
GH-005 already recommended squash-only/disposable-head cleanup while preserving
topology, direct-main, generated/publication and retained-branch exceptions.
GH-008–GH-011 separated observed effective settings, access limits and compatible
working paths. GH-012/013 and ON-005/006 covered onboarding and verification,
but did not require an explicit per-setting binary owner answer before choice
resolution. A matching preconfigured value therefore could be mistaken for a
selected profile.

The Task explicitly admits the material correction. New GH-014 owns it; ON-005,
ON-006 and ON-007 route planning, verification and reporting to that one owner.
GH-012/013 integrate it into the existing timing/checklist. Worked examples
show operator behavior without adding another normative policy source.

| Contract slice | Proposed behavior and preservation |
| --- | --- |
| Relevant optional setting disclosure | Show actual observed value, dated evidence/scope or unknown, recommendation and practical impact. Cover merge commits and merged-head deletion at minimum; include other relevant optional settings. |
| Owner choice | Ask a separate Yes/No question for each named setting, with Yes meaning enable and No disable. A consolidated presentation is sufficient; there is no approval per routine implementation detail. |
| Temporal/attribution boundary | Record attributable answer, date and setting in the existing Task/Decision chronology before reporting the choice resolved or applying it. Reuse still-applicable explicit prior choices. Current values, defaults and generic onboarding approval are insufficient. |
| Unanswered item | Keep explicitly unresolved and do not mutate it or infer an answer. Continue independent authorized work and scope readiness honestly. |
| Decision versus actual configuration | An answer may resolve intent with configuration still unknown or unapplied. No access, settings permission or enforcement is inferred. |
| GH-001–007 applicability and exceptions | Topic adoption remains deliberate. Recommended profile remains optional. Both Yes and No are valid. Source assessment, merge authority, direct-main, topology, retained branches, publication and frozen identity retain their accepted owners. |
| GH-008–012 access and timing | No broader credentials, plan upgrade, destructive test, periodic/per-session/per-Task audit or installation-triggered questionnaire. Existing admitted application plus permission suffices; use normal readback afterward. |
| Local/consumer boundary | No new tracker schema/service, automatic mutation, consumer migration or historical Decision rewrite. Onboarding retains local procedures when GH is not adopted. |

The added questions/recording are mandatory work for adopters of the changed
workflow: this is a MAJOR whole-package change under PV-002, despite optional
resulting setting values. Cost is one bounded decision presentation at relevant
onboarding/settings events, stored in existing chronology; no recurring query
or new approval system. It prevents attributing an unchosen operational policy
to the owner. Already sufficient choices/authorization are reused. Package
classification, generation and combined qualification are recorded by the
receiving Task's integrated evidence; this document does not claim them passed.

## Behavioral walks

All projects, answers, dates and observations below are invented scenario inputs.
The tables are compact views of the existing Task chronology, not a new required
record form. No API call or settings mutation is performed by these walks.

### A. Fresh repository, no settings yet

Larch's owner authorizes a manual PR library plan before the repository exists.
There is no source commit or configuration to inspect. The operator records
that absence and presents these individual questions on 2026-11-16:

| Question / setting | Observed value | Recommendation and consequence | Owner Mara's answer, recorded in Decision L2 |
| --- | --- | --- | --- |
| Allow merge commits? Yes or No / `allow_merge_commit` | unknown; repository not created | No: prefer a squash task history; Yes can preserve topology. | No |
| Allow squash merging? Yes or No / `allow_squash_merge` | unknown; repository not created | Yes: supply the intended ordinary method. | Yes |
| Allow rebase merging? Yes or No / `allow_rebase_merge` | unknown; repository not created | No: not needed by this path; Yes would retain individual commits. | No |
| Automatically delete merged PR head branches? Yes or No / `delete_branch_on_merge` | unknown; repository not created | Yes: remove disposable task heads; No means keeping/manual cleanup. | No |

The owner rejects recommended cleanup, and that No is accepted without pressure
or enabling deletion. Answers are recorded before intent is marked resolved.
No guessed GitHub default fills an observation. Creation/settings application
are not admitted in this planning-only scenario. The operator completes file
and permission planning; configuration and workflow execution remain unverified.
A missing repository does not prevent useful discovery or authorize creating it.

### B. Existing repository, matching preconfiguration, partial answer

Moss's fictional General-settings read on 2026-11-16 shows the same tuple used
as context in Issue 105: merge commits false, squash true, rebase false, automatic
deletion true. The initial owner instruction is only “complete onboarding.”
That supplies neither a prior per-setting answer nor settings application power.

| Question | Observed value | Recommendation and impact presented to owner |
| --- | --- | --- |
| Allow merge commits? Yes or No | false | No: retain squash-oriented history; topology would justify Yes. |
| Allow squash merging? Yes or No | true | Yes: retain the proposed ordinary integration method. |
| Allow rebase merging? Yes or No | false | No: avoid an unused method; preserve it if individual commits become required. |
| Automatically delete merged PR head branches? Yes or No | true | Yes: remove disposable heads; No keeps them for manual management. |

Trace the real decision boundary:

1. Before any answer, all four choices are explicitly unresolved, even though
   the observations match the recommendation. No application is attempted.
2. Owner Mara answers No to merge commits, Yes to squash and No to rebase in
   Decision M3. The operator records those attributable answers/date and only
   then reports those three choices resolved. The still-enabled auto-delete
   setting remains an unanswered/unresolved item; it is not “accepted default.”
3. File/routing discovery proceeds. The report may call that separate manual
   path ready when proved, but discloses the unresolved choice and does not
   call the whole optional-settings decision scope complete.
4. Mara later answers No to automatic deletion in Decision M4. The operator
   records it before resolution. Intent is now resolved as false while observed
   configuration remains true. There is no settings-mutation authority, so the
   report hands the selected delta to the responsible admin and preserves the
   mismatch. It does not mark the configuration applied or silently keep Yes.

This walk distinguishes an observed value, recommendation, explicit owner
choice and applied value without four independent state systems or new forms.

### C. Yes with existing application authority

Pine uses disposable PR heads and explicitly admits setting application by an
authorized operator. General-settings evidence dated 2026-11-16 shows
`allow_merge_commit=true`, `allow_squash_merge=true`, `allow_rebase_merge=false`
and `delete_branch_on_merge=false`. The operator asks all four setting questions
with the same PR-path impacts as A; recommends No, Yes, No and Yes respectively.
Owner Ivo explicitly answers No, Yes, No and Yes in existing Decision P2.

The supported sequence is disclosure/questions → attributable answer record →
authority/permission and compatibility check → authorized application → readback.
The operator can reuse the unchanged squash/rebase values as observations and
make only necessary authorized changes. No second “approve application” ceremony
is invented when P2 plus existing admission already cover it. The scenario's
expected readback is false/true/false/true, but the walk itself performs no write
and supplies no live evidence. A failed/unknown real readback would remain an
application gap rather than invalidating the already recorded owner answer.

On a later unrelated source PR, reuse P2 and sufficient unchanged evidence;
do not ask those questions or inspect all settings again absent a relevant
change, suspected drift or denied operation.

### D. Missing evidence and missing answer are different

Ash's General-settings fields and protection details are inaccessible through
existing authorized access. All setting observations are unknown. The operator
still presents all four binary questions, with their PR-path recommendations
and consequences, rather than treating an absent field as false. Owner Ivo
answers No/Yes/No for merge/squash/rebase but does not answer automatic deletion.
Those three answers are recorded before resolution. Configuration remains
unverified for all four, while only auto-delete's choice is unresolved.

The operator prepares routing and gathers available ordinary-check evidence.
No broader token, alternative identity, plan upgrade or mutation is used to
“verify” a default. Later authorized UI evidence can resolve observation gaps
without asking the three unchanged answered choices again. That evidence alone
cannot resolve the still-unanswered auto-delete choice. Overall enforced-profile
readiness still depends on sufficient effective protection evidence; unrelated
planning is not stalled by that gap.

### E. Retained merged head, topology and coupled rules

Rowan merges a same-repository `release/1.x` head into main for release sync and
must retain it afterward. Evidence establishes that actual intended merged-head
usage; a retained branch's existence alone would not establish auto-delete risk.
Current settings are merge true, squash true, rebase false and auto-delete true.
After inspecting relevant protections, the operator asks the four separate
questions with these recommendations and practical consequences:

| Setting/question | Recommendation | Attributed owner Nia's Decision R2 |
| --- | --- | --- |
| Allow merge commits? Yes or No | Yes: release-sync needs supported topology; check linear-history compatibility. | Yes |
| Allow squash merging? Yes or No | Yes: preserve disposable task-PR integration. | Yes |
| Allow rebase merging? Yes or No | No: this workflow does not use it. | No |
| Automatically delete merged PR head branches? Yes or No | No while the retained merged head lacks compatible deletion protection; otherwise the intended branch is exposed. | No |

Keep the current observations distinct from R2; auto-delete's observed true still
requires authorized reconciliation/readback to meet the chosen retained-head
contract. The optional No is a valid answer. If Nia instead chooses Yes after
the same disclosure, record Yes and reconcile compatible retained-head protection
under existing authority before claiming the path safe; an answer does not waive
the accepted retained-branch obligation. Likewise a linear-history rule can make
merge commits unusable even when the repository option is true. Report that
coupling and seek the genuine policy disposition rather than silently disabling
the stronger rule or claiming the setting alone proves ordinary-path readiness.
No deletion/overwrite test is used.

### F. Direct-main evidence and generated publication exceptions

Willow's accepted routine evidence refreshes and generated publication push
directly without PRs. The operator discloses merge true and auto-delete false
from dated General-settings evidence, explains their little ordinary-path
effect, recommends retaining each, and separately asks “Allow merge commits?
Yes or No” and “Automatically delete merged PR head branches? Yes or No.”
Owner Nia answers Yes and No in Decision W2; those answers are recorded before
resolution. Squash/rebase changes have no relevant selected PR path and are not
proposed. There is no mandatory squash-only profile or reason to manufacture PRs.

Existing force-push/deletion protection, authorized non-force writers and frozen
tag identity remain in force. A PR-only proposal cannot erase these supported
direct paths; a publisher bypass is examined for its actual layered effects.
An unavailable essential publication protection remains a real gap regardless
of answered merge settings. Release authority, source acceptance and consumer
adoption do not follow from W2 or a successful settings read.

### G. Existing explicit answers, conflict, failed record and non-trigger

| Input | Expected result and why |
| --- | --- |
| Current owner Decision explicitly answers each named setting, date/attribution are present, and relevant paths have not changed. | Link/reuse it. Do not force another questionnaire or second approval. Reobserve only affected mutable facts when the event requires it. |
| A current value, screenshot of settings, recommendation, generic “approved” or silence is the only purported answer. | Keep choice unresolved and ask the binary question; none identifies the owner's Yes/No for that setting. A generic answer can count only when it unambiguously answers each already-presented question under current authority. |
| Owner explicitly selects No to auto-delete and an operator prefers cleanup. | Record No as valid. No enabling, corrective override or review defect arises solely from declining the recommendation. Accepted retained-branch/history obligations still apply. |
| Owner selects a value conflicting with a stronger accepted policy. | Record the answer without pretending it waives policy. Reconcile the actual conflict through current authority before dependent application/readiness; continue independent permitted work. |
| Owner answers, but the existing authoritative record cannot be saved. | Preserve the available evidence, state the record gap and do not apply or report resolution ahead of the required record. Continue unrelated work; invent no parallel service or broader publication authority. |
| Package install/update, ordinary source PR or session startup without a relevant event. | No new questionnaire, settings query, topic adoption or profile mutation follows. |
| GitHub governance is not adopted, or the project uses a non-GitHub host. | Retain the accepted local configuration procedure; do not impose GH-014 or GitHub APIs through the onboarding aid. |

## Original incident and verification limits

Issue 105's reported deployment settings are historical context, not a live
observation taken here and not proof of the original owner's decision. These
changes neither rewrite Deployment Task 12's Decisions/qualification nor change
that repository's settings. A future deployment adoption/decision belongs to
that separately governed project. Task 113 admits reusable source correction,
not retroactive client migration or settings application.

The walks check each decision boundary and the coupled workflows against the
proposed canonical protocol, using fresh and preconfigured repositories, Yes,
No, unavailable evidence, unanswered choices, permitted application ordering and
no-mutation paths. They support semantic coverage and operator usability. They
do not prove runtime enforcement, actual model behavior, independent acceptance,
GitHub settings readback, publication or consumer adoption. Integrated source,
export and native-tool checks belong to the receiving Task's combined evidence.
