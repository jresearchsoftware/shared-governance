# Task 52 Step 1 — preserve scope at review classification

Authority: [Task #52 and Step 1 Decision](https://github.com/jresearchsoftware/shared-governance/issues/52#issuecomment-6289901870).
Frozen independently accepted source-guidance baseline:
`e654d9e20a7c42c50cc05786dc83a4f7a16f84e4` (owner-integrated PR #55).
Strategy: Direct implementation of the owner-decided correction; independent
exact-head assessment remains pending. Candidate rules do not govern this effort.

## Bounded baseline and intended correction

Read the complete Task #52 charter/admission, its primary Task #9 / #45 / #51
records, and accepted native boot plus PC, RA, PV, TH, IR and SA protocols.
PC-004/PC-005/PC-009 already require owner authority and risk/cost assessment;
RA-002 distinguishes ratified requirements from engineering preferences;
IR-012–IR-015 already cover evidence, provenance and optional improvements.
The failure point is their application before a review finding becomes a
blocker or a proposed Task amendment. No publisher implementation changes belong
in this correction.

Planned semantic owners: new PC-013 for review-driven scope preservation;
IR-012–IR-015 for obligation binding, classification and owner-facing reporting.
Keep all existing IDs and conditional topic adoption. Keep specialist/local
rules, genuine security obligations and Task Handoff's authority, publication,
Step and readiness lifecycle. Use existing reports and canonical Decisions;
introduce no additional reviewer, checklist, ledger, service, approval or wait.

## Whole-package version intent

Package bump: major

Accepted 3.0.0 is frozen. The proposed 4.0.0 tightens mandatory report behavior
for existing PC/IR adopters: every blocking finding must explicitly identify
its binding obligation, and new requirements must be separately labeled before
negative publication or amendment discussion. Existing rules imply scope
discipline, but do not require that explicit obligation binding in each blocker.
This additional mandatory report content rules out PATCH; it changes existing
adopters' required behavior rather than merely offering a new optional topic,
so MINOR would also understate the change under PV-002. MAJOR is justified by
that concrete contract tightening, not the size or security label of the edit.
There is no additional approval event or per-PR owner reapproval. Consumer
migration remains separately authorized; this effort stays bound to 3.0.0.

## Semantic coverage and operational cost

| Task requirement | Candidate owner and preserved boundary |
| --- | --- |
| Review-driven scope preservation | PC-013: before blocker/amendment presentation, distinguish an existing obligation from a proposed defense; assess old/new supported behavior and quantify cost. PC-001–PC-012 remain byte-identical. |
| Obligation-bound blocker and evidence | IR-012: identify violated obligation, authoritative source and concrete evidence for every blocker; provenance/severity alone supplies no authority. |
| Classification before owner-facing negative report | IR-013: separate **PROPOSED REQUIREMENT / OPTIONAL CHANGE** before negative reporting or amendment discussion, retaining it in the published report and any locally required preview. No universal preview approval. |
| Four categories and important new risks | IR-014: existing-obligation violation, evidence gap, baseline debt and optional protection; important new risks go to explicit owner discussion/decision with evidence, severity, behavior, alternatives and cost. Existing-authority holds and stronger safety rules survive. |
| Prevent correction-Step scope laundering | IR-015 plus unchanged TH-003–TH-005/TH-013: a review cannot admit its recommendation; explicit later owner ratification binds future work without inventing a retrospective violation. |
| Active paths/version/native projection | Packaged README/CHANGELOG, producer authoring/release references and committed native 4.0.0 source/slot/lock/index. Topic adoption and seven other protocols unchanged. Client projection follows its existing content-neutral tool. |

Ordinary in-scope findings use the existing report: one explicit obligation/source
binding per blocker and a category separating any new proposal. New control
proposals additionally describe added actions, frequency, prerequisites and
maintenance/recovery cost; an honest qualitative bound is enough when timing is
unknown. There are zero new commands, services, credentials, mandatory reviewers,
approval events or waiting periods. New scope alone needs the existing canonical
owner Decision; ordinary authorized fixes and Direct acceptance need no new
owner reapproval. The cost is report preparation by existing reviewers, not an
extra operator workflow. Other consumers own separately admitted migration.

## Chronology-based regression scenario

Primary records, read in chronological context:

1. Task #9 [proportionality feedback](https://github.com/jresearchsoftware/shared-governance/issues/9#issuecomment-6096823784)
   rejects recurring duplicated publication proof; its
   [automatic-publication direction](https://github.com/jresearchsoftware/shared-governance/issues/9#issuecomment-6099047526)
   selects accepted-source/version/CI, immutable tags and safe same-source retry.
2. The [Task #45 charter](https://github.com/jresearchsoftware/shared-governance/issues/45)
   asks to share the existing working mechanism while preserving its behavior.
   Its [Step 1 review](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6221404259)
   proposes protection against a later accepted PR inheriting an earlier
   ineligible direct-main edit; it explicitly calls this prospective, without a
   demonstrated incident. It prescribes historical acceptance reconciliation.
3. The next [Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6223120222)
   explicitly ratifies that new guarantee. The
   [whole-solution review](https://github.com/jresearchsoftware/shared-governance/pull/46#issuecomment-6232868860)
   subsequently demands historical policy/inventory/CI handling under that
   amended implementation contract.
4. [Task #51](https://github.com/jresearchsoftware/shared-governance/issues/51)
   records late-onboarding `HISTORICAL_BINDING_UNRESOLVED` and explicitly removes
   ordinary historical replay, accepting reduced historical assurance while
   retaining current release safeguards. [Task #53 acceptance](https://github.com/jresearchsoftware/shared-governance/pull/55#issuecomment-6289829541)
   establishes the producer cutover candidate, not proof of a live new release.

**Counterfactual at record 2, under the proposed rules:** historical acceptance
replay is **PROPOSED REQUIREMENT / OPTIONAL CHANGE**, an unapproved architectural
control rather than a blocking implementation defect. Existing source-main/CI
qualification does not itself promise a history-wide acceptance replay. A proper
owner-facing report states the prospective scenario and uncertainty, compares the
working immediate-transition path with historical traversal, and discloses added
old PR/owner/CI/binding/inventory prerequisites and adoption/recovery burden.
Cost: bounded current-transition work becomes history-dependent lookups for
each earlier package transition; any missing pre-onboarding record can block
otherwise valid future releases. Exact latency is not established. Options:
retain the current boundary and accept the hypothetical risk; perform bounded
case-specific reconciliation; or explicitly select a broader historical audit.
Do not describe the original working publisher as missing required security.

**After record 3:** the actual explicit Owner Decision binds subsequent Task #45
implementation. This correction does not erase that Decision, absolve defects
against it, rewrite reviews or retroactively activate candidate guidance. Its
later revision belongs to Task #51's explicit authority. The new protocol fixes
classification before the owner chooses; it does not veto informed owner choices.

## Authoring regression walks

These are desk applications of the complete candidate PC/IR and accepted TH/RA
boundaries, not executable model tests or independent acceptance. PASS means
the written rules yield the stated disposition and reject the counterexample.
No new automated classifier or publication gate is introduced.

| Case / supplied facts | Expected report and action | Rejected counterexample / authoring result |
| --- | --- | --- |
| S1: Task #9 → initial Task #45 request; reviewer imagines inherited direct-main bytes and demands old acceptance replay. No such guarantee accepted yet. | **PROPOSED REQUIREMENT / OPTIONAL CHANGE**; prospective risk, old/new workflow and history cost disclosed before a negative report or amendment. Ask owner to choose any new scope; accepting risk is available. | Security label makes historical replay a blocking existing defect. PASS, PC-013/IR-012–IR-014. |
| S2: Same case; a negative review is copied into a correction Step without a new owner scope Decision. | Review supplies no execution/scope authority. Preserve current boundaries; seek canonical Decision before implementing the new control. | Change Request silently authorizes audit or a newly allocated Step. PASS, IR-015/TH-003–TH-005/TH-013. |
| S3: Actual subsequent Task #45 Step 2 Decision explicitly ratifies the inherited-delta guarantee. | New requirement binds admitted subsequent implementation. Earlier publisher is not retrospectively defective under it. Later Task #51 supersession is respected. | Ignore ratification as mere reviewer preference, or erase history. PASS, IR-015/RA-002/TH-004. |
| S4: Positive blocker control: publisher modification replaces atomic non-force tag push with forced replacement; disposable local Git demonstrates an existing frozen version tag moves. | **Demonstrated existing-contract security regression**; bind blocker to Task #45 immutable-tag requirement / adopted PV-011–PV-012, compare unchanged-tag baseline with moved-tag candidate, report silent irreversible release-integrity impact and require no-overwrite/race closure evidence. Equivalent safe repairs allowed; no new owner approval needed for the already-admitted repair. | Call a proven accepted immutable-release violation optional, or accept merely because a new control was not selected. PASS, IR-012/IR-014/IR-015. This is a scenario, not a discovered defect in the current publisher. |
| S5: Credible new out-of-scope risk: private producer operator demonstrates that an explicitly selected public Markdown file contains confidential customer text; exporter enforces file inventory, not semantic content review. No existing semantic scanner obligation is established. | Disclose concrete exposure risk, evidence/severity and affected public behavior; preserve private-data/publication boundaries and use a justified hold under current authority if needed. A proposed semantic scanner is **PROPOSED REQUIREMENT / OPTIONAL CHANGE**: assess human content review or removal versus scanner setup, false positives and recurring release work; ask owner for scope disposition. | Pretend a scanner was already required, publish known confidential content, or mandate a new scanner in the correction Step. PASS, PC-013/IR-014/IR-015; actual confidentiality duties remain binding independently of scanner choice. |
| S6: Required exact-source CI result inaccessible; no evidence of failed behavior. | **Evidence gap**; name required CI proof and missing access, use existing pending/hold without PASS or fabricated implementation defect. | Missing log means vulnerable code or optional required evidence. PASS, IR-014/IR-018. |
| S7: Baseline debt is unchanged and unrelated to current accepted boundary; introduction evidence missing. | **Pre-existing debt** when baseline proves it, otherwise undetermined origin with comparison gap; disclose dependency if material, no automatic remediation scope. | Label regression/P1 solely to obtain an unrelated architecture change. PASS, IR-012/IR-015. |
| S8: Separate consumer adopts IR but keeps its own control/specialist policy and no prepublication preview stage. | IR report binds blockers and separates proposals; PC-013 reference does not adopt PC. Existing specialist obligations and local publication path remain. | Add universal preview/owner wait, weaken stronger native review identity, or activate new topic through a link. PASS, IR-001/IR-002/IR-013/IR-020. |
| S9: Ordinary in-scope security fix already admitted; evidence and independent Direct assessment sufficient. | Keep existing checks and independent acceptance; no additional approval/owner reconfirmation. | Every finding, safe hardening or PR now needs owner reapproval. PASS, unchanged PC-003/TH-013/TH-022 plus PC-013. |

## Qualification

Executed source/export/native checks and their limits will be recorded in
[validation.md](validation.md) before the canonical Outcome. The walks above
do not establish fresh model adherence, live client settings, publication or
consumer migration. Implementer checks cannot supply independent acceptance.
