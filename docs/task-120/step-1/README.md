# Task 120 Step 1 coverage

[Task #120](https://github.com/jresearchsoftware/shared-governance/issues/120)
authorizes the foreign-link clarification and includes
[Small Improvement #121](https://github.com/jresearchsoftware/shared-governance/issues/121)
under the producer's standing delegation. Both go through one candidate and one
independent assessment. Use both Issue links in the receiving PR and Outcome.

## Foreign project links

[RA-007](../../../packages/development-governance/vibevm/vibespecs/protocols/requirement-authority.md#RA-007)
owns the new first-response behavior.
[TH-001](../../../packages/development-governance/vibevm/vibespecs/protocols/task-handoff.md#TH-001)
routes bare result links to it and retains lifecycle ownership.
The [shared bootstrap](../../../packages/development-governance/tools/chatgpt/base.md)
places the early check before substantive inspection. The generated
[producer Instructions](../../../chatgpt/instructions.md) carry that check,
with the existing custom instructions and binding preserved.

These source-based scenario walks describe the expected result in a conversation
bound to Codex Relay, except where stated. They provide no live ChatGPT behavior
or Settings evidence.

| Input | First action and boundary |
| --- | --- |
| Standalone link to DocReview PR #347 | Determine ownership from the repository and accepted project scope. Reply once, for example, “That PR belongs to Docs Evolution Review. This conversation is bound to Codex Relay, so I’ll stop here.” Stop before reading the diff, CI, full discussion or other policy. Do not propose fixes, open a local Small Improvement or route work. |
| Standalone link to a Relay PR | Apply the ordinary local routing and existing result-authority checks. |
| “Compare this DocReview PR to our Relay workflow” | Read comparison-relevant evidence and identify external claims as such. The comparison grants no lifecycle authority. |
| “Create a proposal Issue in Shared Governance to clarify this rule” | Use the authorized ordinary proposal path under local implementer policy. Omit execution, approval and other lifecycle effects. |
| “Merge this DocReview PR” | Hand off to Docs Evolution Review with the canonical PR and minimum relevant evidence. The foreign URL leaves the current project binding intact. |
| A DocReview PR is supplied as relevant evidence for an authorized Relay Task | Read the relevant evidence proportionately and label its external source. |
| A link targets a second explicitly declared repository in the active project | Apply the local route and the existing local permissions. |
| A bare link has ownership that cannot be resolved from the URL | Check only the identity information needed against accepted scope. If unresolved, explain the gap and withhold dependent work. Similar names or common GitHub ownership do not settle scope. |

The [Task #98 coverage](../../task-98/step-1/README.md) remains applicable to
intentional discussion such as “please take care of it.” Any substantive foreign
reading still needs a requested or established purpose, and a request for foreign
lifecycle control still follows the handoff. The additional warning and stop is
specific to a bare link without a cross-project purpose.

## Package impact forecast

[PV-004](../../../packages/development-governance/vibevm/vibespecs/protocols/package-versioning.md#PV-004)
owns the advisory forecast and review reconciliation. Conditional package boot
routes adopted lifecycle work to it during ordinary planning and assessment.

| Scenario | Forecast or review disposition |
| --- | --- |
| Edit producer documentation outside the exported package | NONE when the shipped contract and bytes are expected to stay the same. |
| Correct a shipped example to match the existing contract | PATCH when the supported behavior stays the same. |
| Add an optional example or guide without changing required steps | MINOR when the addition is compatible. |
| Add a mandatory operator action to an existing supported workflow | MAJOR because routine operator work changes. |
| Forecast PATCH for a settings clarification, then review a result that actually implements an owner-authorized required per-setting choice | Report PATCH → MAJOR and name the new required choices in the ordinary owner-facing assessment. Apply the existing review and acceptance criteria. The difference alone requires neither a CR nor a hold. |
| Already authorized work has no forecast | Continue the authorized launch or execution and assess the actual impact in the existing review. No separate forecast field or approval is required. |

The combined 12.2.0 candidate matches the charter's MINOR forecast. The early
response is new guidance for an underspecified paste. Accepted RA-007 expressly
limited substantive foreign inspection to the owner's request and did not
establish inspection of an unqualified paste as a supported workflow. The
forecast adds advisory information and carries any changed estimate in the
existing classification rationale. Version arithmetic still uses then-current
accepted main at integration. The [release rationale](../../releases.md#contribution-and-integration)
records the compatibility judgment for independent review.

## Completion boundary

Independent acceptance of the exact published candidate, authorized integration
and verified publication of the exact accepted package are separate from worker
validation. The complete effective desired Instructions change, so
[TH-029](../../../packages/development-governance/vibevm/vibespecs/protocols/task-handoff.md#TH-029)
also requires owner reconciliation and attributable live readback after
acceptance and integration. The checked-in generated file contains the complete
desired text. Consumer projects own any separate adoption.
