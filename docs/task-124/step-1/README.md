# Task 124 Step 1 coverage

[Shared Governance #124](https://github.com/jresearchsoftware/shared-governance/issues/124)
supplies the charter. This comparison uses independently accepted source-main
`d3309e0e735e65264da887f913d7118531810587` and its Development Governance
12.2.0 slot. The producer's exact-label Small Improvements discovery found no
open candidates.

## Source comparison

[PC-014](../../../packages/development-governance/vibevm/vibespecs/protocols/proportional-controls.md#PC-014)
owns the system-responsibility rule. PC-002, PC-005 and PC-008 already required
a concrete risk or accepted invariant for imposing a control. PC-009 already
assessed unnecessary gates and coupling, and PC-010 already rejected repeat
proof without a distinct purpose. PC-014 makes component and contract ownership
explicit and describes how to handle provider results and genuinely missing
guarantees. PC-004, PC-012 and PC-013 retain their authority and protected-boundary
requirements.

[RA-006](../../../packages/development-governance/vibevm/vibespecs/protocols/requirement-authority.md#RA-006)
already bounded proof to the deliverable and accountable component. Its new
reference places Task authoring and acceptance under the same criterion when
assigning a cross-system obligation. Its required integration and proof
exceptions and RA-007's project authority remain in place.
[IR-009](../../../packages/development-governance/vibevm/vibespecs/protocols/independent-review.md#IR-009)
already routed applicable control assessments to Proportional Controls. The
reference makes control placement part of that assessment while IR-007 and
IR-010 still require evidence for actual claimed effects and coupled behavior.
Topic applicability, rule IDs and the existing Task Handoff lifecycle are
preserved. The broader design question remains with
[Shared Governance #122](https://github.com/jresearchsoftware/shared-governance/issues/122).

## Acceptance examples

These are source-based scenario walks. Local package checks qualify the authored
source and native projection, and these examples describe expected decisions
for the stated contracts.

| Scenario and contract | Expected decision |
| --- | --- |
| A GitHub wrapper proposes copying the ruleset evaluation before an ordinary push. GitHub applies the rulesets for the selected operation. | Validate the wrapper's own repository/ref inputs and authorized operation. Invoke the normal push. If GitHub refuses, retain its refusal and operation context. A mirrored policy decision adds a speculative gate and can drift from enforcement. |
| A privileged Writer accepts an admitted source SHA and authorized target from Relay. | Validate the request shape and bound source, target and publication authority at the privileged interface. Relay owns orchestration and uses the Writer's supported result. Each component tests its own obligations without mirroring the other's internal checks. |
| An admitted publisher owes immutable version tags, but the native tool can replace them and the selected target has no established equivalent protection. | Retain a non-overwrite boundary at the publishing layer. The actual ability to replace a frozen tag creates a risk even when a prior read saw no tag, since another publisher could create it before the push. The existing atomic non-force push enforces the publisher's obligation under concurrency. See the [release policy](../../releases.md#automatic-publication-and-recovery). |
| A producer generates workflow content that Distribution delivers. The supported submission interface responds with a receipt for accepted processing. | Qualify the workflow against the output contract and report accepted processing. Distribution owns delivery. Verify a later delivery effect only when required by the caller's accepted contract, using the supported result interface. |
| A database client validates a request and the engine returns a constraint error, or a network timeout leaves a write's effect unknown. | Report the actual engine refusal or the timeout and unknown write effect. Reconcile through the supported operation interface or retry when the contract makes replay safe. A prior health probe cannot establish either result. |
| A caller owes confirmation of an exact protected result and the API confirms only that it accepted a request. | Use the supported readback for the bound result. That readback supplies the caller's missing proof and preserves source/result identity. An unbound readback or a guessed completion cannot establish it. |

The public Relay #269 Outcomes record the two launch refusals and that the
Codex child never started in either attempt. In a new-branch path, first
establish which component owns branch creation and which starting-state identity
the admission contract binds. Evaluate each rejection against that path and
retain any control that protects a real invariant. The refusals alone establish
neither an inability to implement the engineering task nor a basis to remove
all admission controls.
[Starting state mismatch](https://github.com/jresearchsoftware/codex-relay/issues/269#issuecomment-7061904846)
[Task branch already exists](https://github.com/jresearchsoftware/codex-relay/issues/269#issuecomment-7078219374)

## Version and handoff

The candidate's **12.3.0 MINOR** matches the provisional forecast against
accepted 12.2.0. The explicit ownership guidance is a compatible addition under
PV-002–004. It applies inside existing decisions and protects accepted caller
requirements, product contracts and local authority. Speculative gates lacking
an accepted obligation already lack grounds under PC-002 and PC-008. There is
no new mandatory operator work, supported-path restriction or automatic consumer
adoption. Recompute the version against accepted main at integration.

Writer publication, independent assessment, owner integration and accepted
source publication remain subsequent governed actions. The generated ChatGPT
Project Instructions text and the separately pinned Relay and Landscape
packages stay the same in this candidate. The Task policy is `keep-open`.
