# Task 113 Step 2: Option A feasibility and verification boundary

Checked **2026-11-17 UTC** for [Task #113](https://github.com/jresearchsoftware/shared-governance/issues/113), [PR #114](https://github.com/jresearchsoftware/shared-governance/pull/114) and [source Issue #106](https://github.com/jresearchsoftware/shared-governance/issues/106).

## Current decision and result

The trusted [Option A Decision](https://github.com/jresearchsoftware/shared-governance/issues/113#issuecomment-6955937179) retains the absolute requirement. The assistant must not initiate, suggest as a continuation, or route an existing Chat conversation into Work. If the current Chat lacks a capability and a higher-priority rule requires Work, explain the particular limitation and stop that affected Chat operation; continue independent supported work. An owner independently starting a separate Work conversation supplies no permission to transfer the original Chat. This is the selected Task behavior, not proof of a platform enforcement control.

The earlier [Step 1 research](../step-1/chat-work-research.md) and its proposed A/B request are historical. **B was rejected. Do not request that same policy choice again or implement its platform-mandated-transfer fallback.** The [Step 2 continuation Decision](https://github.com/jresearchsoftware/shared-governance/issues/113#issuecomment-6955955642) keeps the existing branch, PR and one 12.0.0 candidate.

**No effective complete non-transfer control has been established for the originating owner's permitted configuration.** Documentation still supports a conditional Work access-denial candidate, but does not establish the originating account's eligibility, its effective permissions, or an absolute guarantee against transfer of interaction/control. This is an inconclusive verification result, not evidence that every possible control is impossible. #106 remains open; report acceptance and #105 integration cannot resolve it by implication.

## Refreshed primary evidence

These are public supported descriptions, not readback of the owner's settings. The cited sections were inspected again in this Step.

| Surface / source | Supported fact and limit for #106 |
| --- | --- |
| [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex), “Configure Work access for your workspace” and “Where Work and Codex are available” | Eligible workspace administrators manage Work Cloud and Work Local under Workspace settings → Permissions & roles. Cloud denial alone leaves local Work possible. Chat stays available when Work access is denied; members can still encounter product-unavailable/access-request UI. Choosing Chat or Work starts the selected experience, including inside a Project. The article gives no guarantee that denied Work removes every transfer attempt or preserves an existing Chat's control surface in every routing case. |
| [Managing feature access with RBAC](https://help.openai.com/en/articles/11750701-managing-feature-access-with-role-based-access-control-in-chatgpt), “Availability,” “Before you begin,” “Understand workspace defaults and custom roles,” and “Check a member's effective access” | Custom RBAC is documented for Enterprise, Edu, Healthcare and Teachers. Owners control defaults and role assignment; Admins have narrower powers. Ordinary direct and group roles combine grants, so one Off setting is insufficient. Plan/seat eligibility and restrictions also matter; changes can take up to five minutes. This is feature-access evidence, not a Chat routing guarantee. |
| [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions.md), “Review Work Local and Work Cloud permissions” | Some layouts separate Work Local and Codex Local; others combine them under Allow members to use Codex and Work Locally. Disabling the combined control also affects Codex. Cloud browser and shell network capabilities are separate from Work entitlement. The actual layout must be identified before proposing a scoped change. |
| [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), “Add project instructions” and “Workspace-level feature controls”; [Projects and chats](https://learn.chatgpt.com/docs/projects.md), web sections | Project Instructions customize responses; Projects inherit workspace controls and can contain both Chat and Work conversations. Neither inspected description establishes a Project-specific veto on Chat-to-Work routing. Keeping both chats in one Project does not prove retention of the original interaction surface. |
| [Settings](https://learn.chatgpt.com/docs/reference/settings.md), complete preferences reference | Follow-up behavior governs steering versus queuing; browser and Computer Use controls govern tool permissions. No inspected preference documents a prohibition on Chat-to-Work transfer. This bounded reference is not an exhaustive inventory of the owner's client. |
| [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration.md), introduction and “Understand policy scope and precedence” | Admin requirements constrain supported runtime behavior, and defaults select starting values. Scope varies by client and execution environment; local requirements do not automatically govern Work cloud computers. The inspected policy guidance does not establish a Chat routing veto. A local sandbox, disabled tool or network denial cannot substitute for proof that transfer is disabled. |
| [Work admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq.md), “Work across devices” | Local computer access with Work Cloud is a distinct opt-in under Work Cloud. Disabling that local-access feature or enforcing residency does not itself disable Work Cloud. Local execution policy and cloud execution policy remain distinct. Therefore, a local-only restriction is not a complete solution. |

The [Computer Use setup](https://learn.chatgpt.com/docs/computer-use.md) describes desktop GUI operation in Work or Codex. The [Browser guide](https://learn.chatgpt.com/docs/browser.md#browser-use) describes desktop browser operation in those experiences. These establish particular feature/surface limits; they do not prove that every browser task, file operation or review requires transfer of an existing Chat. Available structured tools and ordinary web search must be assessed separately. Under Option A, an actually unavailable operation stops instead of initiating a handoff.

The dated [Model Spec authority rule](https://model-spec.openai.com/2025-12-18.html#follow-all-applicable-instructions) supports the instruction-hierarchy limitation. It does not disclose the complete production routing algorithm. Repository or Project text cannot prove that a conflicting platform rule has been disabled.

The [current changelog](https://learn.chatgpt.com/docs/changelog) and official-site searches for Chat/Work handoff controls did not establish an additional enforcing setting. Search hits about [remote-host handoff](https://learn.chatgpt.com/docs/remote-connections) and Local/Worktree concern Codex execution locations, not the requested Chat-to-Work boundary. Absence from a search is not proof of absence from the product.

## Actual configuration: known and missing

The admitted automatic worker is a repository execution resource. Its model, permissions, tools and filesystem do not identify the originating ChatGPT account, active workspace, plan, member role, client/version, Project or effective Work entitlements. No such attributable owner/admin readback was supplied in the Task chronology inspected in this Step.

Advertised connected capabilities were inspected. Plugin Management's permission reader is expressly for one plugin's permissions, not workspace RBAC or product entitlements. Pages/Spaces and Document Control address documents; they are not Project Settings or a Work entitlement reader. No advertised tool establishes the missing originating-client state. Unrelated service accounts or this worker's private runtime configuration cannot safely stand in for it. No account identifiers, secrets or arbitrary configuration files were probed.

Live Project Instructions remain unknown. The source-controlled desired text is unchanged. This result neither changes settings nor claims live compliance, and creates no new TH-029 application duty. Any earlier unverified live state remains unverified. A later authorized effective-text change must follow accepted TH-029: independent source acceptance/integration, complete raw Markdown for owner manual application, and attributable live readback preserving unknown rules.

## Conditional control and consequences before any change

The candidate is **effective denial of both Work Cloud and Work Local for the intended member in the originating managed workspace**, where supported. The documented administrative entrypoint is Workspace settings → Permissions & roles; available defaults/custom roles and exact labels depend on the workspace. An authorized Owner must perform any required role creation or assignment; limited Admin access is not presumed sufficient.

This is a member/workspace feature restriction, not a Project-only setting. Changing defaults may affect many members; changing a shared role may affect its other assigned people/groups. Denial can remove useful Work workflows across Projects and cloud-task viewing, and a combined local control can remove local Codex access. Work Cloud's local-computer-access path also needs consideration. The effect on already-running tasks and every navigation/transfer case has not been established here. Do not experiment on them or infer consent to these wider effects from Option A.

Even correctly denied access does not by itself prove the full requirement: documented unavailability and access-request UI leave the exact routing/control behavior unverified. No entitlement, role, default, local policy, Project Instructions or client setting was changed, and no prohibited handoff or live reproduction was attempted.

## Precise continuation request for the current Task chronology

The policy decision is complete; the next input is **read-only configuration evidence**, not another A/B question and not permission to mutate settings. Trusted Writer/owner continuation should request:

> Retain Option A. Please identify the originating client/surface and version, whether the Chat is in a personal or managed workspace, the plan and relevant administrative capability. For an eligible managed workspace, supply attributable read-only evidence of the actual Work Cloud/Work Local permission layout, defaults and all applicable direct/group grants for the intended member, including any combined Codex control and Work Cloud local-computer access. Avoid credentials and unrelated member data. If these controls are unavailable, report that fact. No settings changes or transfer tests are requested.

That evidence decides applicability and the smallest scope. If it supports a potentially usable denial route, present the actual affected member/group scope and losses for **distinct owner authorization before any change**, then read back effective permissions after propagation and verify Chat availability through a method that does not initiate a transfer. Do not change settings merely to make a hypothetical route testable.

For the remaining platform guarantee, the owner can obtain an authoritative OpenAI answer for that specific configuration without sending this worker credentials. Suggested support question:

> For this client/version and workspace permission layout, does denying all effective Work Cloud and Work Local access prevent an existing Chat conversation from being transferred into Work, including platform-initiated routing? What supported setting, if any, enforces this per Project while retaining Work access elsewhere? Please distinguish prevention of task execution from preservation of the original Chat interaction/control surface, and identify a verification method that does not initiate the prohibited transfer.

No support message was sent. A safe supported verification method or attributable product confirmation can reopen this precise question. If none can establish the absolute guarantee, return the documented limitation for later explicit owner disposition; retain Option A and stop affected operations in the meantime. Do not re-offer the rejected B as an assumed solution. #106 stays `small-improvement` labeled and open until effective proof or an explicit later disposition. #105 can proceed independently through exact-head acceptance, integration and publication.

## Source-based qualification of the selected behavior

These are reasoning scenarios against the trusted Decision and cited documentation, not live model/client tests or new shared package rules.

| Case | Required treatment and evidence limit |
| --- | --- |
| Chat exposes a supported read/search/integration capability | Use it within authority and keep the existing Chat. Complexity alone supplies no transfer permission. This Step used public documentation and unauthenticated GitHub reads without switching a conversation. |
| A particular operation lacks a Chat capability and an applicable higher-priority rule requires Work | Explain that specific unavailable operation and stop it; continue independent supported work. No transfer request, continuation suggestion or attempt. No live conflict was provoked to exercise this case. |
| Owner independently opens a separate Work chat | Do not treat it as permission to move/control the original Chat. No such conversation was created here. |
| Only Work Cloud or only Work Local is Off; another role grants access | Do not claim complete denial or non-transfer. Inspect all applicable paths/grants before proposing a change. |
| Both permissions appear Off | Still require configuration eligibility/effective-access evidence and supported non-transfer behavior proof; a settings screenshot alone cannot establish the absolute claim. |
| Personal/ineligible workspace or missing readback | Report unavailable/unverified applicability. Do not claim an enterprise control is usable or create roles, change plans, switch workspaces or rewrite Instructions to simulate enforcement. |
| Unknown live Instructions, rejected B, or #105 source acceptance | Preserve unknown higher-priority rules; none supplies a routing override, a new fallback choice or #106 closure. |

Disposition: completed bounded research with a specific capability/evidence boundary for live verification. No demonstrated new package defect was found. The required whole-Task outcome of proven absolute non-transfer remains unmet and discoverable in #106 and #113; the next trigger is the read-only originating-client evidence or supported product confirmation above. Independent assessment of this report's quality remains separate from proof of the original requirement.
