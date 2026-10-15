# Task 35 Step 1: contract and decision maintenance

[Task 35](https://github.com/jresearchsoftware/shared-governance/issues/35) and its
[sole admission Decision](https://github.com/jresearchsoftware/shared-governance/issues/35#issuecomment-6195904711)
authorize one integrated Manual Codex implementation/test/correction cycle and
one PR, including the regression formerly tracked in
[Issue 34](https://github.com/jresearchsoftware/shared-governance/issues/34).
The accepted producer baseline is frozen at
`bff65a38f61e7fc618ef86260a291637bf3477d1`; live main matched at execution start.
The accepted root, INDEX, authoring boot and materialized 2.3.0 slot supplied
applicable authority. STATIC is absent. Candidate guidance remains proposed data.

The full Task 35 chronology, Issue 34 and the linked Task 32 body/nine comments,
PR 33 body/six Outcomes/six COMMENTED reviews (no inline comments) were read.
The [Task 32 owner acceptance](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6195156746)
accepted final candidate `97a1f6a1758b65d9fc1894245129c0e3a5816748`, integrated by
squash as the frozen baseline. It deferred real-client qualification rather than
claiming runtime/settings/Sources proof. Post-squash
[push CI](https://github.com/jresearchsoftware/shared-governance/actions/runs/38756363934)
failed on the missing PR-only test revision; the
[publication workflow](https://github.com/jresearchsoftware/shared-governance/actions/runs/38756441064)
was skipped. Source 2.3.0 is accepted, unpublished; Issue 34's closure only
consolidated tracking. This work neither backfills that publication nor edits history.

## Bounded source and semantic ownership

The comparison evidence is Relay
`f6431d612d464c511fdda97e7dea64ace7f03ac7`, specifically the complete
[AGENTS contract-change and minimum-ceremony sections](https://github.com/jresearchsoftware/codex-relay/blob/f6431d612d464c511fdda97e7dea64ace7f03ac7/AGENTS.md),
[CONTRIBUTING documentation-maintenance section](https://github.com/jresearchsoftware/codex-relay/blob/f6431d612d464c511fdda97e7dea64ace7f03ac7/CONTRIBUTING.md),
and [ownership mapping](https://github.com/jresearchsoftware/codex-relay/blob/f6431d612d464c511fdda97e7dea64ace7f03ac7/docs/relay-guidance-ownership.md).
These supply extraction evidence, not authority to change Relay. The shared
comparison includes all seven accepted protocols and producer-specific
exceptions, [semantic completeness](../../authoring.md#semantic-completeness),
[manual binding](../../manual-task-handoff.md), [self-adoption](../../self-adoption.md)
and [release policy](../../releases.md), read at the frozen producer commit.

In this table PC = proportional-controls, RA = requirement-authority,
TH = task-handoff, IR = independent-review. The classification describes
**accepted 2.3.0 coverage**, before this candidate. New lifecycle text lives in
[contract and decision maintenance](../../../packages/development-governance/vibevm/vibespecs/protocols/contract-and-decision-maintenance.md).

| Source obligation / operational meaning | Accepted coverage | Candidate owner or remaining product binding |
| --- | --- | --- |
| Materially removing/replacing/renaming/disabling supported capabilities requires explicit canonical owner authority before implementation | Partially covered: RA protects observable contracts; TH bounds new workflow obligations; PC covers control changes | New topic supplies the broad proactive trigger, independently of a control/provenance question |
| Commands/entrypoints, inputs, visible behavior, responsibilities, manual/automatic transitions, extra actions, status/Outcome/recovery and supported client paths are material surfaces | Missing common invariant: no complete general surface definition | New topic preserves all portable categories; specific ChatGPT/GitHub interfaces remain local |
| Implementation/security/test/reviewer preference is not independent authority | Already complete: RA origin/ratification, PC risk versus preference, TH scoped execution | New topic connects that rule to its broader trigger without another authority hierarchy |
| Preserve established behavior where safe, otherwise stop for owner decision; equivalent observable internal refactoring needs no new permission | Partially covered: TH stops/RA reconciliation; PC free-hardening exception has a narrower trigger | New topic states both alternatives and the general refactoring exception |
| Independent assessment compares every materially changed old/new surface and functional/security requirements; unauthorized delta blocks acceptance until actual owner disposition | Already complete in IR; TH supplies general assessment semantics | New topic retains this narrow contract duty for projects using local review, routing assessment methods to separately adopted IR |
| Executable Task authority changes become canonical owner authority before related implementation | Already complete: TH stable charter/chronological Decisions | New topic connects promotion to the existing owner Decision mechanism without reproducing chronology or Step rules |
| Accepted reusable architecture/process/governance/security/qualification/operational decisions cannot stay chat-only; promote into existing appropriate durable contract | Missing common invariant | New topic owns promotion through a suitable authorized bounded change, without waiting on unrelated backlog |
| Distinguish durable policy, task-local, temporary/experimental and rejected material when later work depends on it | Partially covered: RA acceptance/origin; TH preliminary thoughts | New topic preserves useful classifications and excludes casual observations, unaccepted speculation and diagnostic facts |
| No decision ledger, chat scraper or ceremony-only Task; no gratuitous repeated proof | Already complete for proportional ceremony/proof; promotion-specific exceptions partly missing | PC retains proof/cost method; new topic preserves explicit promotion exceptions |
| Actual visible or Task/review/authorization workflow change, including remediation, updates affected human docs/examples in same Task/PR or explains why none are needed | Missing common invariant: IR checks guidance but does not own same-change maintenance | New topic supplies maintenance duty; implementation/contracts and supported legacy behavior must agree |
| No separate docs approval, CI gate, policy registry or paperwork cycle | Already complete general proportionality; source qualifier retained | New topic explicitly keeps docs within existing change/review |
| Native `OWNER_DECISION_REQUIRED`, Writer/Reviewer actors, CRs, v3/v4/legacy authority, schemas, admission snapshots, checks, TEST/PROD and client operations | Relay-only binding | Remain Relay-owned; shared guidance imports no keyword, parser, native actor, automation or deployment authority |
| Native CI summaries, diagnostics/hooks and exact Outcome publication mechanics in the surrounding minimum-ceremony section | Relay-only binding plus already complete PC/TH evidence and handoff semantics | No hook, repeated PASS comment, universal CI command set or product publication route is added |

One new conditional topic is smaller and safer than widening four existing
protocols. RA explicitly does not implement contract review; PC's trigger is
controls. TH already owns Task decisions and IR assessment methods. Extending
those adopted topics with the complete new lifecycle would add obligations to
existing consumers. The new topic supplies its essential duties with ordinary
local authority/review even without TH/IR adoption; cross-references activate none.
All seven earlier protocols and the shared ChatGPT tools remain byte-identical.

**Package bump: minor** — accepted source 2.3.0 to candidate 2.4.0. Compatibility
rests on explicit topic adoption and unchanged existing mandatory behavior,
exceptions, environments and local authority, not merely on adding a file.
Root/custom bindings retain the producer's four topics plus self-adoption;
this change does not adopt the new topic, IR or repository-governance here or in
another consumer. Ordinary reviewed source integration and automatic publication
remain separately authorized later; published/frozen content is not rewritten.

## Semantic walkthroughs without residual Relay rules

These are manual text/contract assessments of the candidate, not model trials,
runtime enforcement or consumer migration. A hypothetical project explicitly
adopts only the new topic and uses its own owner/change/review mechanisms.

| Scenario | Expected application and assessed result |
| --- | --- |
| A backup CLI's security fix replaces synchronous completion with a ticket and requires a manual poll | Entrypoint result, transition and extra action are material. Locate owner scope first; security preference alone is insufficient. Preserve safe existing completion or stop for owner decision. No Relay status keyword or schema is needed. |
| Internal parser rewrite preserves commands, accepted inputs, visible results and recovery | Equivalent observable refactoring needs no new owner permission. Existing tests/review remain governed locally; the topic adds no gate. |
| Owner accepts a reusable rule that recovery must remain available offline | Before related implementation, put any authority amendment into the canonical owner Decision. Promote the reusable rule to the existing recovery runbook in an authorized bounded change. Acceptance in chat alone does not provide later executors a durable contract. |
| A task-local exception permits one test fixture to use temporary credentials | Record its actual task-local scope when later work could mistake it for policy. Do not promote it to a universal credential rule or invent a ledger/extra Task. Real credential boundaries remain protected. |
| A diagnostic experiment suggests a faster architecture, without owner acceptance | Keep it experimental; do not turn speculation or a one-off diagnostic observation into durable policy or executable authority. |
| Remediation renames a user command but leaves old examples and a supported legacy client path | Same Task/PR updates guidance/examples and qualifies both supported paths, or explains why none are affected. Review checks old/new behavior against authority. Green CI or reviewer preference cannot approve an unauthorized rename. No separate docs cycle. |
| A package update reaches a consumer that adopted only PC and RA | New topic stays inactive; unchanged seven protocols preserve existing semantics. That consumer's local broader contract gate remains authoritative until a separately reviewed migration reconciles duplicates. |
| Relay later adopts the new topic under separate authority | Portable clauses can route to the shared topic while schemas, native actors, exact status, admission/CR/legacy mechanics, existing protections and operator paths remain local. This is a prospective ownership assessment, not an executed migration. Residual Relay text is not used to conceal a shared omission. |

## Qualification and handoff

The regression repair uses a source-grounded preservation baseline rather than
requiring a transient PR commit to survive squash. It retains historical Task 32
evidence and accepted protocol invariants. Existing distribution checks exercise
the eight-topic export, historical shapes, version boundary and malformed payload
rejection. Existing source/export/native checks bind generated registry, locked
slot, boot and tools to the exact candidate. Materialized outputs use the accepted
pinned VibeVM workflow, not hand-edited source URLs or a new validator.

Final validation, clean/squash-compatible regression evidence, exact PR head/CI,
annotations and material warnings are recorded in the canonical PR Outcome.
All executor/helper assessments are implementation self-check evidence.
Independent substantive exact-head **NON-APPROVING Deliberative review** and
owner disposition remain pending. No self-approval, merge, release, closure,
consumer migration, live settings/Sources edit, credential or PROD change is
authorized. Static scenarios/tests do not prove model behavior, runtime adoption,
live Instructions application, Sources access/freshness or reliability.
