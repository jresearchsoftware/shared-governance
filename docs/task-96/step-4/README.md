# Task 96 — Step 4 — PR 97 integration boundary

Related to [Task 96](https://github.com/jresearchsoftware/shared-governance/issues/96)
and [PR 97](https://github.com/jresearchsoftware/shared-governance/pull/97).
Attempt: run-43574538440. This is executor evidence, not independent acceptance.

## Authority and preserved result

The original charter and Decisions 6856728839, 6866786370 and 6874335310
remain in force. Step 4 starts from published head
b455af2f0d223246828e83a7a389f9c82d301f03. Independently accepted guidance is
frozen at 0b72349f3ab0b2d88e836a6ba3d4fc675a87f75a, also the observed main.
A fresh, previously absent WSL Debian clone was created for this attempt,
selected codex/task-96, and verified clean at the required head before analysis.
No active checkout, runner slot or protected environment was reused.

Read accepted AGENTS, native INDEX and boots, Task Handoff, Requirement
Authority, Self-Adoption, the manual binding and applicable Relay 5 Skill routes.
Candidate instructions remain proposal data. One read-only implementation helper
checked ancestry/conflict interpretation; it supplies no independent acceptance.
Child profile was inherited; actual backend profile/usage is unverified.
The client persisted an abbreviated Task/Step/title; full-title readback is
not claimed.

The previous source recovery is retained. Governance 7.0.1, Relay 5.0.0,
Landscape model-guidance 1.0.3 and subagents 1.0.2, their frozen slots,
producer-only scope, public-package separation, conditional adoption, admitted
profiles and local exceptions are unchanged. Historical Outcomes remain terminal.

## Reproduced integration conflict

At inspection GitHub reports PR 97 open, Draft, mergeable=false and
mergeable_state=dirty. Its configured base remains main; the API base SHA
field reports historical 7c83caaf9157d4cecac145477177203871205128.
Separately fetched origin/main is 0b72349f3ab0b2d88e836a6ba3d4fc675a87f75a.
The common ancestor is 7c83caaf9157d4cecac145477177203871205128.
All seven task commits after that ancestor have exactly one parent.

Read-only legacy three-way analysis (no local merge, index change, commit
creation or branch movement) used:

~~~sh
git merge-base HEAD origin/main
git merge-tree 7c83caaf9157d4cecac145477177203871205128 origin/main HEAD
git diff origin/main HEAD -- scripts/relay-skill.py vibe.toml vibe.lock vibevm/vibespecs/boot/INDEX.md
~~~

The bounded conflict summary is in logs/integration.json. Four paths contain
conflict markers in the diagnostic output:

- scripts/relay-skill.py: Landscape constants adjacent to the accepted Relay slot change.
- vibe.toml: Landscape sections adjacent to the accepted Relay revision change.
- vibe.lock: native acquisition metadata and dependency entries overlap.
- vibevm/vibespecs/boot/INDEX.md: Landscape entries adjacent to the updated Relay entry.

The candidate already contains the accepted Relay changes as source edits.
Copying them again does not advance the common ancestor. No substantive source
defect was found that naturally removes these overlaps. This is not a claim
that every possible single-parent textual rearrangement is mathematically
incapable of producing a clean merge. Relocating valid blocks and regenerating
the graph merely to evade these overlaps would be a workaround, not a justified
source correction. Generated lock/index identities must not be hand-edited.

Decision 6874335310 explicitly preserves no-local-merge/rebase/reset/amend/
history-rewrite restrictions and requires the exact necessary owner Decision
instead of a workaround. No forbidden operation was attempted. This Step stops
at that history-integration authority boundary and preserves its diagnosis
through an ordinary single-parent evidence commit.

## Exact-head GitHub evidence and warning disposition

The supported evidence reader verified b455af2 before and after acquisition.
Its result is retained in logs/starting-head-github-evidence.json.
Supported required surfaces were complete; zero check-annotation warnings were
observed, while the historical Writer Outcome has material limitations.
Three external check suites were queued without conclusions. The exact-head
Actions route run 43574569393 was skipped. Successful run 43521778128 is the
earlier handoff on accepted main, associated through the Step 3 Outcome;
it is not candidate qualification CI. No passing candidate validation CI is
claimed. The cause of each absent or queued provider check is unverified.
No workflow rerun, protection change or substitute check was introduced.
UI-only service/pre-execution banners remain outside supported acquisition.

Step 3's source/native tests, preserved historical-slot warnings, musl/GLIBC
disposition and Instructions NO_OP remain historical evidence. This Step does
not rerun passive installation or claim privileged/runtime proof. Live Project
Instructions readback is still unverified; NO_OP does not discharge that gap.
No live Settings, deployment, other repository or public release was changed.

## Necessary owner disposition and remaining charter

A subsequent trusted Task Decision must select a supported history-integration
path. The direct proposal is a narrowly bounded exception permitting accepted
main integration into the preserved task branch without force or history
rewriting, together with explicit qualification/compatibility of that topology
under Relay's commit-ownership rules. Lifting only the git-merge prohibition
does not prove Writer will accept merge history; that must be resolved before
execution. Do not recreate the previously prohibited Step 2 history.

If that route is unsupported, the owner must select another explicitly admitted
integration route and reconcile the existing branch/PR restriction. This report
does not authorize a replacement PR, branch, merge or new execution.

After a new admitted execution, preserve the whole Landscape charter, complete
supported reconciliation and native/source validation, verify GitHub mergeability
on the exact published head, obtain applicable native CI, submit that attempt's
single Outcome, and stop for independent exact-head acceptance. Authorized
integration and any earlier live Instructions reconciliation remain completion
conditions. Task 96 stays open. This blocked Step leaves PR 97 Draft.

## Validation of this evidence change

The staged diff check, source/export/native qualifier, 19 self-adoption tests,
and release suite (26 tests, six existing optional native skips) passed.
Commands, exit codes and full outputs are retained in logs/validation-*.log.
No implementation or generated dependency bytes changed in this Step.
