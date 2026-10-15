# Independent review methodology and evidence

Apply to independent assessment only when the owning project explicitly adopts
this topic. Installing/updating the package or reading a reference does not
activate it or replace local review policy. Use the project's canonical authority,
acceptance criteria, artifact-specific methods and authorized publication path.
This contract works manually, including for research and results without a PR.
It grants no execution, approval, merge, release, adoption or closure permission.

Where adopted, [task-handoff](task-handoff.md) owns result identity, Task/Step,
Decisions, Outcome routing and Direct/Deliberative acceptance. This protocol
substantiates the assessment; it creates no parallel acceptance authority.
Preserve stronger project-owned reviewer identity, checks and protected boundaries.

## Establish what is being assessed

Identify the complete actual result and its comparison baseline: exact commit
and substantive diff for a source PR, or the actual deliverable and identifiable
revision/evidence for a report, deployment, qualification or no-change result.
Do not invent a PR or SHA for a non-repository artifact. Refresh current canonical
requirements, authorized Decisions and applicable change requests. Independently
reconcile the result with the full goals, constraints and acceptance criteria,
including material omissions; the candidate's manifest or summary cannot decide
which requirements or source areas exist.

Inspect primary artifacts and relevant changed behavior. PR metadata, changed-file
names, an implementer's Outcome, an earlier PASS or green check summary are
navigation and claims, not proof that the substantive result was reviewed.
Read the complete substantive diff and affected source, generated output,
interfaces or analogous primary evidence needed to assess the result. For an
artifact consumed through a rendered or operational surface, inspect that surface
when it is part of the accepted contract; source shape alone cannot prove its
usability or observed behavior. Research review examines the actual argument,
source support, alternatives, tradeoffs and limitations against canonical goals.

Bound investigation to the result and its material dependencies and risks.
Complete review does not mean reading every unrelated repository file or running
every possible experiment. Explain material uninspected or inaccessible surfaces
and how they limit the assessment; never describe a partial review as complete.

## Verify evidence and affected behavior

Verify material validation through the primary records applicable to the exact
result: relevant test scope and outcomes, CI run/job/check identity and output,
annotations, artifact evidence or environment observations. Distinguish what was
independently inspected, rerun, reported by the implementer or unavailable.
Green but skipped, incomplete, stale or unrelated checks do not prove coverage.
Existing sufficient proof need not be rerun solely to be independent: inspect
its binding and substance. Required checks and human/owner confirmation remain
required; a deterministic validator proves only its mechanically checked facts.

Inspect applicable supported primary warning surfaces, including the Outcome
and execution/job/check/runtime annotations when those belong to the binding.
A log search for `warning` does not replace them. For every known material
warning retain source, impact, scope, disposition, next action and evidence gaps.
Unavailable required evidence is a gap, not absence of warnings. Unsupported
UI-only or pre-execution banners need no new acquisition workaround; that access
limit alone is not a defect, but a known material warning still needs disposition.

Assess correctness, omissions, security, compatibility, regressions and the
required user/operator workflow. Compare material old/new behavior in each
changed surface with authorized requirements; implementation or reviewer
preference cannot retroactively authorize a changed contract. An unauthorized
material delta requires the owning project's decision before acceptance.
For controls and operator-work changes, apply adopted
[proportional-controls](proportional-controls.md), including the simplest
authorized black-box path and unnecessary friction. Do not prescribe a protected
live action outside authority merely to obtain review evidence.

Follow coupled changes across relevant validators, consumers, alternate
entrypoints, generated projections, post-checks, regression coverage and active
operator guidance. Changed identifiers, endpoints or execution representations
need bounded active-reference closure, preserving valid alternate forms and
historical evidence. For cross-layer or lifecycle-sensitive behavior, trace
process/ownership boundaries and terminal or durable effects; helper ordering
alone is insufficient proof of the required end-to-end effect. Use appropriate
observations or explicitly identify the missing proof. This is risk-directed
analysis, not an unrelated cleanup or universal full-suite requirement.

## Findings and review after correction

The first assessment covers the complete result. Aggregate reasonably
discoverable material findings rather than stopping at the first easy blocker.
If access prevents completing that assessment, report both obtained findings
and the remaining scope. Do not claim exhaustive defect discovery.

For an actionable finding identify the candidate/comparison, affected surface,
problem, impact/severity, evidence, required correction or invariant and acceptance
evidence. Compare material failures, including failed checks, with the starting
or reviewed baseline and classify their provenance:

- introduced by this implementation or remediation;
- pre-existing on the baseline;
- pre-existing but newly exposed or made blocking by changed behavior/validation;
- undetermined, with the missing comparison evidence stated.

Call a defect a regression only when introduction is supported. Baseline debt
does not automatically enter remediation: explain current authority or a material
dependency/changed acceptance boundary. Discovering it expands no Task scope.
Give proportional remediation guidance for non-local findings: the invariant,
coupled surfaces and useful correction sequence. Distinguish mandatory constraints
and acceptance evidence from suggested implementation choices; an equivalent
authorized solution is acceptable. New architecture or scope requires its owner.

On rereview, separately assess closure of prior findings, remediation-changed
behavior, adjacent coupled risks and genuinely new findings. A surviving blocker
needs an explanation of the invariant missed by prior review/remediation or an
explicit remaining evidence gap before another correction is prescribed; do not
invent a cause. Preserve useful finding history in existing review records.
Changed artifacts stale affected tests and assessments. Reuse sufficient evidence
for unchanged invariants with an explained applicability/binding; obtain fresh
applicable evidence for changed ones. Old-head acceptance does not accept a new
head. Do not regenerate unchanged history or add ceremonial review rounds.

## Judgment, independence and publication

Record the evaluator/role or review context, exact result and baseline, inspected
scope and primary inputs, substantive rationale/findings, material warnings,
unresolved evidence and their effect on the verdict. Distinguish exploratory,
pre-fix, stale and final evidence, and explain changes since prior assessment.
A generic PASS, another chat, model label, script or publication identity proves
neither sufficient review substance nor independence from implementation.
Use a genuinely separate evaluator or substantively separate review context as
allowed by project policy, with an honest independence rationale. Implementer
self-checks and helpers remain implementation evidence. If independent evaluation
is unavailable, leave independent acceptance pending.

If evidence is insufficient to justify a positive conclusion, do not publish
PASS/APPROVE. Name the specific missing evidence and use the project's pending,
inconclusive or blocking disposition, with the next useful action. Distinguish
an access/assessment gap from an established defect; do not manufacture findings
or a Change Request merely to delay merge. Justified nonblocking gaps or exceptions
need explicit rationale under applicable authority; required evidence cannot be
silently waived. Absence of discovered defects alone does not justify PASS.

A sufficiently evidenced Direct result may receive the locally authorized
positive verdict. A Deliberative result first receives substantive non-approving
assessment, even when its quality is good; preserve Task Handoff's owner
discussion/Decision before formal approval. Acceptance of report quality does
not adopt its recommendation. For later authorized acceptance of an unchanged
result, recheck current result/authority and reuse sufficient review evidence;
a changed result needs fresh applicable assessment.

Publish only through the owning project's authorized mechanism and verify the
record. An independent assessment copied through one owner account must name
its actual evaluator and publisher; it supplies no distinct authenticated native
reviewer identity, native GitHub APPROVE or branch-protection satisfaction.
Retain any stronger local requirement. Relay Reviewer/Writer, typed verdicts,
admission, schemas, check APIs and merge gates stay product-owned. Specialist
reader/source-completeness, code/test, environment and client methods stay with
their owners; they may strengthen this contract without replacing its substance.

Keep evidence in existing Task/artifact/review records. This contract requires
substantive judgment, not a rigid universal checklist, packet, per-file attestation,
new service or technical publication gate. Optional aids cannot prove that review
occurred. Any proposed additional mandatory control needs its own unmet invariant,
risk/cost assessment and owner authority under applicable proportional guidance.
