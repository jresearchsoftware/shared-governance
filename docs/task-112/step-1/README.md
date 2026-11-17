# Task 112 — Step 1 — Human command interaction

Related to [Task #112](https://github.com/jresearchsoftware/shared-governance/issues/112).
This is implementation/qualification evidence, not independent acceptance or
publication. The automatic worker returns local committed work to trusted Writer;
GitHub publication, PR state, independent review, integration and closure remain
with their trusted actors. Issue closure policy stays **keep-open**.

## Authority and canonical baseline

The admitted starting head and independently accepted source baseline are
`e7b3769cf06755c305f832fda8fc8e73edfe147f` (12.0.0). Accepted root/boot/locked
protocols are frozen there for this effort. Candidate instructions and generated
12.1.0 files are proposals. The supplied launch is Task 112, Step 1; no Step
history was reconstructed and no external execution or publication was launched.

The bounded semantic baseline is the admitted owner charter's five intended
behaviors and scope/completion requirements, plus accepted PC-001/006/010,
PV-001–009/015, RA-001–007 and the producer's explicit topic-adoption boundaries.
The linked DocReview inventory at `2865b797a7eba744283ff9cd5933c331d9c9ff5a`
and PR #343 supply origin/context only. They are neither an accepted shared
contract nor authority to edit that consumer. This is authoring a new reusable
topic, not claiming extraction/adoption of every DocReview local rule.

## Placement and compatibility

The canonical owner is the new [Human Command Interaction protocol](../../../packages/development-governance/vibevm/vibespecs/protocols/human-command-interaction.md),
with [worked examples](../../../packages/development-governance/vibevm/vibespecs/guides/human-command-interaction.md)
and an explicitly conditional package boot route.

| Possible home | Decision and preserved ownership |
| --- | --- |
| Proportional Controls | PC-001 applies to proposed controls. PC-006 assesses friction's effect on control effectiveness; PC-010 avoids redundant proof/ceremony. Neither governs all ordinary human diagnostics/setup. Preserve their complete bytes and applicability, and link their overlap from HC-003 rather than creating a second action/copyback rule there. |
| Task Handoff | Governs adopted execution/result/continuation lifecycles, not ordinary administration. Preserve its complete bytes; no artificial Step or Outcome for each human interaction. |
| Context Loading / Contract Maintenance | Own relevant-context selection and contract-change/decision maintenance respectively, not shell action/copyback. Preserve their complete bytes. |
| Separate Human Command Interaction | Concise, explicitly adopted, platform-independent semantic owner. Shell-specific examples remain illustrative rather than prescribing a fixed command count, universal formatter or tool. Autonomous tool calls remain outside this human workflow. |

**12.1.0 MINOR** is a compatible addition to 12.0.0 under PV-002–004. It changes
no existing topic's mandatory behavior or adoption. Newly adopting projects accept
HC-001–003 deliberately; existing local rules stay canonical until their own
reviewed migration reconciles duplicates. The producer also retains its existing
six adoptions; making this topic available does not adopt it locally. No hooks,
capabilities, dependencies, new operator prerequisite, gate or interaction ledger
are added. Both files are in the passive export/native slot inventory. The normal
reviewed merge/publication path remains, with current-main version reconciliation
before integration. All ten old protocols, license and ChatGPT tool bytes remain
unchanged. Relay/Landscape pins remain stable; no consumer is migrated.

## Semantic coverage and scenarios

| Required behavior | Canonical coverage and assessed behavior |
| --- | --- |
| One action/input/result, not one shell statement | HC-002; each diagnostic example is one pasted block with three independent checks and one BEGIN/END report. No command-count cap. |
| Batch safe deterministic work | HC-002; Bash aggregates independent exit statuses, PowerShell collects/formats independent results. Bounded fields avoid a full environment/log dump. Deterministic optional-path checks can remain internal. |
| Interpretation, choice, permission and safety dependencies | HC-002; staged service example below. Batching never grants privileges, disruption, credentials, production access or a local-boundary exception. |
| Shell-specific output and failures | HC-003; Bash combines standard error/output and retains each command status and aggregate exit. PowerShell scopes helpers/preferences, catches cmdlet failures, retains partial output and emits one formatted string with explicit OVERALL. Native status requires immediate `$LASTEXITCODE` capture; no universal `Out-String` rule. |
| No simultaneous homework or repeated manual invocation | HC-002; each interaction requests only the next applicable action or choice and its one return. Neither example asks for separate replies per diagnostic. |
| Generic applicability and preserved adoption | HC-001 and conditional boot; ordinary shell/admin work can adopt it without governed Tasks. Installing/updating the package or adopting Task Handoff does not activate HC. |

The protected workflow is assessed as a conversation, not just a script:

| Conversation boundary | One currently requested human action/result | Withheld action and reason |
| --- | --- | --- |
| Operator requests printing diagnosis | Paste the read-only service block; return its one report. | No restart command or simultaneous permission homework. Diagnosis alone authorizes no disruption. |
| Report is missing/error/ambiguous | Ask the next interpretation/clarification needed for the actual evidence. | No inferred repair; a missing service is not permission to create/restart one. |
| Evidence supports a restart, permission absent | Explain impact and ask whether restart is authorized now under the local procedure; receive one Yes/No choice. | The restart instruction waits. A choice is one input; it is not a script that silently defaults to Yes. |
| Operator says No | End this proposed restart path and follow the actual chosen diagnostic direction. | No restart. |
| Operator says Yes but required production/change/admin authority is unresolved | Resolve that genuine boundary through the existing procedure. | A chat answer grants no privilege or local-policy exception. |
| Evidence, permission and local authority are sufficient | Then supply a concrete environment-appropriate restart/verify block and request one report. | No generic restart command was supplied with the initial diagnosis. This Task performs no actual service mutation. |

This scenario applies equally to a Bash daemon investigation. Safe batching is
preferred where facts/conditions are deterministic within an authorized action;
human interpretation and protected changes are true staged boundaries. The
conversation assessment is modeled; it proves no actual assistant compliance,
Windows service behavior or administrative operation.

## Small Improvements and authority warning

The exact-label open-Issue scan returned [#106](https://github.com/jresearchsoftware/shared-governance/issues/106).
The accepted baseline's Task 113 reports retain its absolute Chat-to-Work
non-transfer request with an unresolved owner/client disposition. The current
live Task also has [ordinary comment 6957332189](https://github.com/jresearchsoftware/shared-governance/issues/112#issuecomment-6957332189)
asking for normative implementation instead of feasibility work and transferring
that remainder to #112. This launch supplies **no active trusted Task Decisions**.
Under accepted Relay's “Authority, actors and capabilities,” ordinary comments
are evidence; only trusted active native Decisions amend this automatic admission.
The worker cannot promote the live comment to trusted authority or reconcile
that material operator-contract choice on its own. SI-004/006 preserve owner
holds, native admission and trust boundaries.

Disposition: #106 is not implemented in this admitted candidate. Preserve it open,
labeled and discoverable; no tracker mutation was attempted. Trusted Writer/owner
must reconcile that comment through the supported native Decision/admission path
before the normative #106 work depends on it. This is an authority warning for
the next boundary, not a missing Bash/PowerShell implementation or a technical
feasibility investigation. The independent admitted #112 deliverable continues.
If the comment is established as effective expanded authority, the combined Task
remainder is still outstanding and must not be reported complete by this result.

## Qualification and remaining boundaries

The runnable behavioral check is `python3 scripts/test-human-command-interaction.py
--pwsh <local-pwsh>`. It extracts the actual published Markdown code blocks;
fixtures stay local and never operate a real service. Tests cover real Linux
diagnostics, several failures/missing command, later independent success, child
exit/parent-shell survival, PowerShell cmdlet failure and partial native output,
one-string formatting/scoped preferences, and service Running/Stopped/Missing
fixture results without any restart.

Runtime used: Bash on Linux and PowerShell **7.4.6 Linux x64**, downloaded into
the contained ignored tool directory and verified against Microsoft's official
`hashes.sha256` (archive SHA-256
`6f6015203c47806c5cc444c19d8ed019695e610fbd948154264bf9ca8e157561`).
Windows PowerShell 5.1 syntax compatibility is source-assessed; native Windows
execution and actual service/admin behavior are unavailable here and are not
claimed. The native-executable adaptation fixture proves explicit status handling
on Linux, not every PowerShell version's standard-error behavior.

Final package/native/regression check results are recorded below after execution.
Independent exact-head review, owner integration and successful publication of
the exact accepted version remain trusted continuation work. DocReview's local
L12 wording belongs to a separate, independently reviewed consumer adoption after
publication; that consumer follow-up is not a producer completion prerequisite.
This candidate changes no complete effective Project Instructions text, so it
adds no new manual application action. Existing live-setting evidence gaps remain.

The pre-existing untracked `.codex-sandbox/` is supplied runtime content (owner
`nobody`, group `codex-relay-codex-work`, top directory mode 2770), including
private inputs/configuration. It is neither committed nor removed or permission
widened. Task-created tools/fixtures use ignored `.vibe/`; useful source/evidence
is committed explicitly. No credentials, settings, external repositories or
host services are changed.
