# Task 32 — Step 1: cross-project ChatGPT bootstrap research

**Research complete; architecture selection, implementation and independent
acceptance pending.** Recommend qualifying a small common bootstrap with direct
GitHub retrieval first, using consumer-owned bindings and existing accepted
VibeVM materialization. Add deterministic projection only if repeated output or
maintenance failures justify it. Sources are optional convenience inputs; a Skill
is an optional later delivery adapter. This recommendation is proposed research,
not an owner Decision or an adopted workflow.

Authority: the complete [Task 32 chronology](https://github.com/jresearchsoftware/shared-governance/issues/32)
and [Step 1 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6172393644).
Accepted source-main and branch base, frozen throughout this effort:
`15e8191435a126e54b4d1739a73fab112e01c081`.
The Decision admits research/design, bounded evidence experiments and one
terminal Outcome, followed by independent substantive **non-approving**
Deliberative assessment and owner discussion. It does not select architecture.
The exact terminal commit/PR is recorded in the canonical Outcome, avoiding a
self-referential result SHA in source.

## What the first-hand evidence actually establishes

Both owner-supplied comments were fetched in full through the all-pages connected
GitHub Issue-comments API and read through their ending sections. The committed
[evidence snapshots](evidence/task-chronology.json) preserve the body, all three
comments, author/IDs/order and the owner's separate current-chat clarification.
Copied instructions are comparison evidence, not Task Decisions or new governing
instructions for this executor.

| Surface | Evidence and state |
| --- | --- |
| DocReview original | [Comment 6172309309](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6172309309): **9,740 Unicode characters**, ends under **Merge and closure**. This is the recovered intended original, not a fresh export/readback of the live field. |
| DocReview live field | The Decision reports truncation at 8,000. **Reported, not independently observed.** Local clipping of the recovered original reproduces the consequences below; it does not prove actual UI bytes or timing. |
| Relay supplied text | [Comment 6172323060](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6172323060): **7,884 characters**, ends under **Boundaries and profile**. Owner-supplied comparison text; present live-field equality remains **unverified**. |
| Shared Governance field | Owner's answer in this Codex chat, 2026-10-14: “нет отдельного поля” — **no separate Project Instructions field**. This is first-hand owner clarification, not a UI readback. No synthetic third settings text or settings diff is invented. |
| Older DocReview replacement | No independently identified export of a different recent replacement was supplied or verified. It cannot replace the recovered original/currentness gap or be promoted from memory to current settings. |
| This execution surface | A local Codex chat in Shared Governance, not a fresh ChatGPT Project experiment. The supplied exact title was set once and persisted readback matched. No live client setting or Source upload changed. |

The two original files contain similar task/review/publication themes, but their
semantic authority and supported flows differ. The [complete semantic map](semantic-map.md)
covers every supplied source section and every material qualifier identified in
the bounded repository slices. It distinguishes client mechanics, shared policy,
Relay contracts, DocReview specialist methods, other local choices and stale or
duplicative candidates. It supplies an explicit test of the 90% hypothesis; no
semantic-overlap percentage is claimed.

### Length and clipping experiment

The read-only [measurement helper](inspect-evidence.py) checks each snapshot
against the exact API body, character count and ending section. Applying the
reported `body[:8000]` boundary to the recovered DocReview original removes
**1,740 characters (17.86%)**. It cuts the legacy CR metadata sentence after
“Reviewed”, losing its head-SHA completion, the entire remediation launch-profile
rule, the remaining publication/profile clauses and
the entire Merge and closure section: reviewed-head validation, qualified squash
conditions, keep-open/closing-reference rules, typed completion/closure,
protected boundaries and verified native outcome reporting. These are material
obligations, not expendable length padding.

Relay has **116 characters** of headroom against the same owner-stated limit,
about 1.45% of capacity. A small wording addition can exceed it. These are
Unicode-code-point measurements of the supplied text; actual UI counting,
rejection/truncation behavior and the asserted 8,000 limit were not independently
tested. No shortest-string or truncation-based prompt repair is recommended.

The diagnostic character-sequence similarity is **16.31%** with Python
SequenceMatcher/autojunk disabled. This is a reproducible textual observation,
not a proxy for semantic overlap or a reason to reject the owner's common-core
hypothesis. Shared behavior must be assessed by obligations and qualifiers.

## Bounded accepted-source baseline and provenance

The [32-file inspection inventory](evidence/measurements.json) gives revisions,
paths, full-file identity and actual inspected scope; a full-file hash does not
claim full-file reading where only relevant slices were examined.
[Acceptance provenance](evidence/acceptance-provenance.json) records current
native PR/review metadata. Read-only fetches imported immutable objects into
this producer checkout; no consumer checkout, branch, remote or source was edited.

| Baseline | Selection and currentness |
| --- | --- |
| Shared Governance | Decision-bound `15e8191435a126e54b4d1739a73fab112e01c081`, also observed remote main and PR 31 merge commit. Read full accepted AGENTS, INDEX, authoring boot, 2.2.0 slot boot, applicable Task Handoff/Proportional Controls/Requirement Authority, manual binding, CONTRIBUTING and authoring/self-adoption docs. STATIC.md is absent. |
| Shared independent-review source | [2.2.0 protocol](https://github.com/jresearchsoftware/shared-governance/blob/15e8191435a126e54b4d1739a73fab112e01c081/packages/development-governance/vibevm/vibespecs/protocols/independent-review.md), read fully as research. The accepted root retains four topics plus producer self-adoption; package availability and Task Handoff's reference **do not adopt this additional topic**. Step 1's independent substantive assessment boundary already follows its Decision/Task Handoff. |
| Relay product/Skill | [PR 125](https://github.com/jresearchsoftware/codex-relay/pull/125), native independent APPROVE at `1c90c98f3df5e4a9bac0669ad4b37bd8d37c998b`, accepted squash `52bebbc9cafc1e82737943a6d37f00945ffadfef`. Read full AGENTS, canonical Skill, workflow/compatibility and ownership mapping, plus lock/index/package manifest. Relevant AGENTS/Skill/lock/index bytes are unchanged at observed main `ed2ec60e8096bd2a7477e9eac9e9f9d2603c0f20`. |
| DocReview | [PR 313](https://github.com/jresearchsoftware/docs-evolution-review/pull/313), native APPROVE at `3bb51aa3aa3e0d6b05352a6644f34a59182f5479`, accepted squash `6014e8e2c20faebfaa656ee1e8e6efb1dcd9d630`. Read full AGENTS/local consumer methodology, relevant PROJECT-RULES slices, gate-policy and review-finalization contracts. Relevant AGENTS/PROJECT-RULES/methodology bytes are unchanged at observed main `fd6b0c4eda5c6b5390cbdcdb8a26820f0e5d45c2`. |
| VibeVM | This producer's toolchain pins **1.0.7**, source `b6659978453f50e6d1d4d99626d70b980a2c5847`. Inspected Agent target enum, full boot WhenCondition parser/test source, bounded boot/static-zone logic. No VibeVM executable or upstream tests ran in Step 1. |

The relevant Relay [#101](https://github.com/jresearchsoftware/codex-relay/issues/101)
charter and [#59](https://github.com/jresearchsoftware/codex-relay/issues/59)
ChatGPT integration/ownership direction were consulted. They describe small
bootstrap + accepted GitHub/locked guidance + optional cache, real-client
qualification and manual settings application; they do not admit consumer work
here. [#91](https://github.com/jresearchsoftware/codex-relay/issues/91) was checked
against its later completion Decision and PR 125 acceptance rather than its
stale pre-execution body status. Its closed source-development result does not
prove external VPM publication, live consumer rollout or client activation.

The live [Task 30](https://github.com/jresearchsoftware/shared-governance/issues/30)
charter remains BACKLOG / not admitted: it owns deliberately initiated general
governance onboarding and GitHub configuration assessment. It has no execution
result to import here and this bootstrap research does not trigger its audit.
The live [Task 15](https://github.com/jresearchsoftware/shared-governance/issues/15)
accepted principle corroborates the semantic-completeness route already present
at this effort's frozen source-main; no old admission/profile is reused.

### Material compatibility and ownership conclusions

1. Shared Governance 2.2.0 is a passive seven-topic package. This producer's
   adopted routes differ from Relay's explicitly adopted **Proportional Controls
   and Requirement Authority only**. Carrying the rest of a dependency closure
   does not activate Task Handoff, Deliberative or independent-review policy.
2. Accepted Relay uses current **v4** stable charter/trusted Decisions/Writer
   admission, retaining exact already-admitted old-attempt compatibility. Its
   source Skill is **0.1.0**, with a pinned **2.1.0** shared dependency. Reuse
   those sources; do not make a new generic adapter re-author native schemas,
   identities, admission, Writer/Reviewer, replay or deployment semantics.
3. DocReview retains its accepted methodology pin
   `f77478a51e4aec5cee16174dc6f2be768ccae087`, separately from the source-reported
   installed identity `2cb84b4d0bd4bcbfbd0aa7d686c14aeaf59eba4a` / workflows-v2.
   Its per-Task legacy/typed-v3 opt-in and explicit task_complete continuation
   are not obsolete merely because Relay now offers v4. Installation claims are
   accepted-source statements, **not a new live deployment probe**.
4. Relay's supplied settings use automatic positive native publication/merge;
   DocReview's supplied text says “review PR” authorizes analysis and requires
   a first-verdict preview. Shared Governance's admitted research is Deliberative.
   These are material local permissions, not one universally deduplicable rule.
5. DocReview's corporate-source/read-only/remotes/security rules and
   source-precedence/profile/locked ruleset, rendered/source/link/completeness/
   reader questions, freshness, required confirmation and finite controller
   batch gates belong to its specialist owner. Generic “review fully” cannot
   replace them. Their complete JIT routes are required even though the
   original settings summarize rather than reproduce those methods.

Potential stale wording is identified in the semantic map for owner-reviewed
reconciliation, including Relay's overly narrow “Issue body” authority summary
relative to accepted v4, and the very small length margin. No live text is
declared obsolete and removed solely through this analysis.

## What must stay in the bootstrap, and what can be loaded JIT

The permanent instruction must **start the loader** and define its authority
limits. A bare GitHub URL or “follow AGENTS” lacks enough role, acceptance and
evidence routing to address the reported PR 27/31 failure. Conversely, copying
all AGENTS, transitive protocols and specialist methods repeats policy and
creates size/version conflicts.

| Concise live bootstrap responsibility | Referenced accepted material / live work evidence |
| --- | --- |
| Project identity and client role: discussion/orchestration/independent assessment versus executor; supported tool route | Repository accepted AGENTS and consumer's client binding, not a universal Relay-development profile |
| An unambiguous starting reference and accepted-source selection rule; freeze its exact revision for the effort; candidate/cached/copied text cannot accept itself | Owner-bound Task/review acceptance record, accepted AGENTS, committed lock/index/slot and product/local source references |
| Read applicable adopted routes at substantive task boundaries and relevant changes; retrieve primary result/check evidence before a verdict | Full relevant canonical policy slices; current complete Task/Decision/Request/CR as locally selected; actual PR diff/source, checks/annotations and warnings |
| Critical authorization, independence and protected-action boundary; missing authority/current-head/evidence cannot yield unsupported PASS | Local native publication/merge/closure permissions, stronger reviewer identity, specialist methods and operational rules |
| Cache status and honest limits; qualified read-only discussion may proceed from identified snapshots; settings remain owner-applied | Optional Sources identity/currentness and live canonical evidence when needed; no per-message poll/hash or startup installer |
| Project-local communication/output format and a small overlay route where required | Full replacement format/length policy; product or DocReview specialist reference; no universal model/effort/labels |

The proposed *common algorithm* is:

```text
At a substantive work boundary:
  resolve the project's role, tool route and accepted source selection;
  freeze that independently accepted revision for this effort;
  read accepted AGENTS and applicable explicitly adopted boot/slot/local routes;
  resolve the current canonical Task/Decision/PR under the local authority model;
  inspect the actual result and primary checks/warnings before assessment;
  perform only the next authorized action, or explain the concrete evidence gap.
```

This is a research sketch, not a shipped template, executable generator or
ready-to-apply settings replacement. It does not supersede each project's
selected Task authority or admit a protected action.

A stable navigation URL can avoid unnecessary reapplication when only a
referenced dependency changes. A moving URL alone is **not** acceptance:
the local selection contract must resolve current owner/review evidence to
an exact accepted commit before substantive use. For this producer the existing
explicit Task SHA binding already supplies that fact. An immutable SHA in live
settings is simpler to audit but changes the settings text whenever it changes;
that is a real update, never a claimed no-op. Follow-on qualification should
compare these two reference choices without creating another acceptance registry.

## Alternatives and proportional tradeoffs

| Alternative | Benefit | Cost / failure mode | Research disposition |
| --- | --- | --- | --- |
| Common static bootstrap + direct GitHub retrieval + small local binding | Smallest implementation; one loading method, live evidence and existing accepted canonical policy; no resolver/service/binary in conversation | ChatGPT must actually follow the route; connector/file/CI permissions and primary evidence availability vary; maintenance still needs owner review | **Recommended first baseline to qualify.** Keep actual consumer permissions and exceptions in the binding/references. |
| Small deterministic projection of the same template/binding | Reproducible full text, length checks, intelligible actual settings diff/no-op, easier multi-project maintenance | Tool/schema/output ownership, candidate-versus-accepted inputs, semantic mapping and tests; correct text still does not prove model application | Add only after the static baseline exposes material repeated drift or useful measured maintenance savings; no second resolver or policy source. |
| Purpose-built ChatGPT Skill/adapter | Task-specific discovery/explicit invocation, shared retrieval procedure and connected tools when client support is qualified | Skill packaging/version/install/discovery, external client availability and priority; can silently copy policy or miss invocation | Optional later adapter. General platform support does not prove this repository's Skill discovery or VibeVM-to-ChatGPT projection. |
| Optional Project Sources snapshot | Useful offline/reference convenience, fewer repeated large downloads where addressability works | Stale or partial snapshot, unclear retrieval/addressability/version, manual upload/update/removal; files can contain normative text without becoming active policy | Cache only, selected by measured usefulness in a real client; direct route remains supported when absent. |
| Concatenate full policies into live Instructions | Immediate visible text | Original already exceeds budget; repeated generic/product/local sources diverge; high maintenance burden and clipped critical clauses | Reject as the baseline. Compression alone cannot establish semantic completeness or actual review behavior. |
| Settings synchronizer, standing service, mandatory preflight/checklist or per-message integrity worker | Could force additional mechanical checks | Unsupported live surface, protected mutation, new persistent state/credentials/gates, recurring operator work; does not prove substantive judgment | Outside admission and disproportionate to demonstrated Step 1 evidence. |

The concrete harm is a weak/missing loader or clipped instructions allowing
unsupported approval, mutation or closure. Existing canonical authority,
independent assessment and exact-result evidence already protect those actions
when loaded. The cheapest proposed correction is explicit small routing plus
honest primary-evidence limits. A generator or cache is not a new security
permission, and no extra attestation/approval service is justified by this report.

## Client and VibeVM evidence: observed versus inferred

Current OpenAI documentation describes Project instructions across its chats
and shared uploaded/connected Sources. This establishes platform concepts,
not these projects' live text, file freshness or model compliance.
[Projects and chats](https://learn.chatgpt.com/docs/projects).

Current documentation also supports installed task Skills in ChatGPT/Work and
Codex with distinct invocation syntax. It does not establish that a repository
Codex Skill or VibeVM output is automatically available to a ChatGPT Project.
[Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins).

In this session the connected GitHub `fetch_file` retrieved the complete accepted
producer AGENTS at the explicit SHA. Its content and Git blob matched local
`git show` exactly; [connector evidence](evidence/connector-source.json) and
the measurement helper preserve the comparison. Complete Issue chronology,
native PR/review records and accepted object reads were also available.
This proves a present retrieval path in **this Codex surface**, not automatic
loading in a new ChatGPT Project or the downstream availability of every CI API.

At pinned VibeVM source:
[WhenCondition](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-core/src/manifest/package/when.rs)
has **OS and installed-package** predicates. The parser does not accept a
ChatGPT-versus-Codex role selector; installed predicates are resolved at
generation and OS remains at read time. The
[Agent enum](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-agent-projection/src/agents.rs)
lists six coding-agent targets including Codex, with no ChatGPT Project target.
The accepted Relay package explicitly projects its Skill to `agents=["codex"]`.
These inspected contracts do not provide a native live ChatGPT settings/Sources
projection. This is source evidence, not a new CLI execution or an exhaustive
claim about every unrelated VibeVM capability.

PR 125's independently accepted qualification documents VibeVM 1.0.7 ignoring
transitive **Git-table source** details and using an explicit immutable two-root
consumer manifest with a native exact dependency edge. The future common
mechanism must consume the **actually resolved and materialized closure**,
not assume a declared transitive source became locked or reimplement version
resolution. This Step did not repeat that already accepted integration probe.
The producer's current native 2.2.0 lock/index/slot and Relay's 2.1.0 closure
remain separate; neither instructs all consumers to update.

No qualified live Project Instructions edit API or Project Sources
enumeration/version/upload interface was established in the current tool
surface. Project/Space/Page metadata tools are not evidence of that capability.
No unsupported internal API, cookies, UI automation, upload or fresh chat was
used. All Sources addressing/currentness, new-project model traversal,
review compliance and reliability remain follow-on real-client questions.

## Evidence experiments and follow-on behavioral qualification

Step 1 observations are limited to full-source recovery, text clipping,
accepted-source retrieval/currentness and source-level capability inspection.
The following are **desk analyses/proposed experiments**, not observed model
results or PASS verdicts. They define useful distinguishing evidence without
introducing a mandatory global checklist.

| Case | Desk conclusion / required follow-on observation |
| --- | --- |
| Normal discussion | Small role/language binding should avoid eager whole-graph reads. Observe a fresh project conversation and actual loaded sources; do not infer JIT economy from text length. |
| New Task + Decision | Bootstrap routes to the complete live chronology/local authority model. Observe stable charter/Decision handling and no guessed Step/launch; distinguish Shared manual flow from Relay admission. |
| First PR review from a link | Resolve the linked Issue, acceptance strategy, accepted base and candidate head, then actual diff/source and primary CI. Observe the model taking that path rather than trusting the implementer's summary. |
| PR 27/31 negative case | Task 32 reports metadata/Outcome/check-summary substitution. In a controlled context with only those inputs, the model must withhold PASS/APPROVE and identify missing substantive evidence. No new review of PR 27/31 or failure reproduction is claimed here. |
| Full positive review | Supply authorized diff, accepted rules, complete Task authority and primary checks/warnings. Observe substantive findings/rationale at the exact head. Deliberative assessment still stops before formal approval and owner Decision. |
| Stale/missing/changed sources | Changed candidate or policy invalidates affected proof. Observe retrieval of correct accepted bytes and a specific gap when unavailable; missing optional cache must not block working direct GitHub retrieval. |
| Source dependency update | Observe VibeVM's real resolved closure and content at deliberate maintenance, plus source-to-output coverage. No moving-latest/runtime binary or silent topic adoption. |
| Changed versus unchanged settings | Compare complete actual output bytes. Changed pin/role/boundary text needs a visible settings diff; unchanged template/navigation requires no re-paste solely because a referenced dependency changed. Sources updates are a separate actual diff. |
| Relay overlay | Preserve v4/native identities/admission/exact old compatibility, manual Writer capability limits and local publication/merge rules. Observe correct source/tool selection; no unconditional shared Deliberative activation. |
| DocReview overlay | Preserve current per-Task authority pin, corporate restrictions, finite controller batches and specialist final rendered/source/reader gates. Observe actual final output and questions, not a generic review checkbox. |
| GitHub unavailable | An identified snapshot may support qualified read-only discussion; unknown head/authority prevents protected publication, new admission, approval, merge/closure. Observe the concrete boundary without global reinstallation or token requests. |
| Unsupported Sources/Skill access | Direct bootstrap remains usable where tools permit; disclose missing optional capability. No automatic settings mutation or claim that local AGENTS/native Skill changed the Project. |

A fresh real ChatGPT Project trial is needed because the current Codex context
already contains task/agent instructions and cannot isolate the proposed loader.
The owner must separately authorize any settings application or test setup that
changes the live surface. Useful observations should record the real input,
surface, source revisions, inspected evidence and actual output; a text preview,
script assertion or UI display alone is not compliance proof.

## Reviewable first-consumer plan and owner choices

1. **Independent research assessment now:** assess this exact report/semantic map,
   primary sources, alternatives, limits and omitted requirements without native
   APPROVE. Discuss whether to accept report quality and whether to select the
   minimal direct-loading baseline. Those decisions are separable.
2. **Later owner admission for producer implementation:** if selected, implement
   one common template and minimal binding, optionally a small deterministic
   emitter only if justified. Decide the accepted-reference strategy, explicit
   ChatGPT role/permissions and whether to adopt the available independent-review
   topic. Preserve the current root's conditional topic selection until then.
3. **Shared Governance first:** produce a reviewed ready-to-paste complete
   replacement from the selected accepted sources. There is no existing separate
   field to diff against; record that absence. Owner applies/reads back the live
   field and separately opts into any Sources. Test a fresh Project and primary
   evidence review before claiming activation.
4. **Practical maintenance:** during deliberate accepted input changes, compare
   complete resulting settings and optional Sources with their last accepted
   outputs. Hand off only actual differences/no-op. Consume native locked closure,
   retain previous accepted revision for ordinary rollback, and preserve live
   Project Sources/owner text; no synchronizer or per-message work.
5. **Consumer handoffs after accepted shared design:** Relay #101's owner decides
   its binding/adoption and any charter narrowing; reuse accepted #91 product
   artifacts instead of a competing generator. DocReview separately admits its
   local migration and complete specialist-policy coverage. Neither consumer was
   changed by Step 1; their current settings/authority remain untouched.
6. **Packaging only if needed:** this research changes no package/runtime/native
   projection and needs no gratuitous SemVer bump. If a later admitted reusable
   package change is selected, justify one whole-package bump against accepted
   main, preserve source/export/native consistency, obtain exact-head independent
   acceptance and separate publication/consumer adoption authority.

Remaining material owner choices: exact reference selection/maintenance contract,
consumer-specific review-publication permissions, topic adoption, whether a
generator/Skill/cache adds demonstrated value, and real-client test setup.
Reported truncation and supplied-text currentness must be verified at that later
owner-controlled settings boundary before publishing an actual replacement diff.

## Validation, warnings and terminal boundary

Research measurements reproduce with:

```powershell
python docs/task-32/step-1/inspect-evidence.py
```

For reproduction outside this checkout, first obtain the four pinned source
commits and the two observed main commits named in the helper using ordinary
read-only Git fetches; no consumer installation is needed. The helper's output
proves snapshot completeness, exact connector/source equality and bounded
currentness comparisons, **not semantic completeness or model enforcement**.

Required producer source/export/release/self-adoption checks, final diff/scope
inspection and exact-head CI are reported with actual results in the canonical
Outcome/native records. No failed or unrun check is inferred successful.
No upstream suite, live settings/Source workflow, native VibeVM execution,
new ChatGPT model experiment, consumer rollout or deployment was qualified.

Committed local evidence: [source/export qualification](logs/qualification.txt)
passed at the first research commit; [distribution](logs/distribution.txt)
passed **32/32**, [release](logs/release.txt) passed **10** with **6** explicit
optional native resolver/publisher integrations skipped, and
[self-adoption](logs/self-adoption.txt) passed **12/12**. The unchanged package
boundary was 2.2.0 to 2.2.0 with no bump. These suites exercise existing producer
mechanisms, not a proposed ChatGPT implementation. The final report edits add
upstream context and correct the clipping description; final-head source/export,
whitespace, scope and native CI evidence remain externally bound to the Outcome.

Material warning dispositions:

- **Reported DocReview truncation:** complete intended source is recovered;
  actual live bytes are unavailable. Clipping shows loss of critical rules.
  Keep the distinction visible; owner-controlled live verification and migration
  are follow-on, not a claim of Step 1 repair.
- **Relay near-limit/currentness:** original margin is 116 characters; live
  equality and client compliance are unverified. Follow-on baseline confirmation
  and small bootstrap qualification are needed.
- **Policy/version/adoption differences:** parameterize accepted routes, retain
  v3/legacy/v4 and specialist exceptions; no silent migration or automatic
  activation. Package presence alone does not satisfy this dependency.
- **VibeVM transitive source/target limitation:** use accepted resolved native
  closure and honest source-level capability statements; no bespoke resolver or
  claimed ChatGPT projection. The accepted PR 125 integration evidence was
  inspected, not rerun.
- **Real-client evidence gap:** current GitHub retrieval succeeds in Codex;
  Project loading/Sources/Skill addressability and substantive model review
  remain unqualified. This limits recommendation confidence, not the admitted
  ability to deliver research.
- **Shared Governance settings:** owner states no separate field; do not fabricate
  an existing bootstrap, no-op update or settings activation proof.

The only terminal Step result is this source-grounded research PR and its
supporting evidence. Its one canonical English Outcome belongs on that PR under
the accepted manual binding. Independent Deliberative review and owner Decision
remain pending. No self-approval, merge, package publication, live settings change,
consumer adoption, future execution or Task closure is authorized. **Task 32
stays OPEN.**
