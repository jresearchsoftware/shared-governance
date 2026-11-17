# Task 113 Step 1: Chat-to-Work control evidence

Historical Step 1 report. The owner subsequently selected Option A and rejected
B. See [Step 2 verification](../step-2/chat-work-verification.md) for the current
Decision, evidence limits and continuation request; the A/B request below is
retained as history, not a pending choice.

Evidence checked on **2026-11-17 UTC**. Related to [Task #113](https://github.com/jresearchsoftware/shared-governance/issues/113) and [source Issue #106](https://github.com/jresearchsoftware/shared-governance/issues/106). This is a bounded research result and proposed owner decision, not an implementation, independent acceptance, live-settings readback or authorization to transfer a conversation.

The independently accepted source baseline remains `f8d77b16ab9e92b31ae9a9390acabd9be9e962a7`. Accepted root AGENTS/native boot, Requirement Authority, Proportional Controls, Task Handoff (including TH-029), the manual binding and authoring/contribution guidance were read from that commit. The installed `openai-docs` skill directed inspection of current official product guides and the changelog. No candidate instruction was treated as accepted authority.

## Finding and unresolved boundary

The owner requires **no transfer of interaction/control away from the existing Chat conversation**. Asking first, preferring Chat, sharing history, or keeping a Work conversation inside the same Project does not satisfy that requirement.

Official documentation establishes a supported **Work access-denial route for eligible managed workspaces**. It does not establish that this route is available to the originating owner's client, or explicitly guarantee that it suppresses every transfer prompt, navigation or attempted platform-mandated handoff. No supported per-Project non-transfer enforcement setting was established in the bounded sources inspected. This is an evidence limitation, not a claim that every possible control is impossible or that an undocumented control cannot exist.

Consequently, **#106's absolute requirement is not proved implemented**. Changing source instructions alone would not prove it. Preserve that requirement unless the owner explicitly chooses an alternative through Task #113's Decision chronology. Safe independent #105 work can continue.

## Supported controls and their limits

| Layer | Primary supported evidence | What the evidence establishes; limit |
| --- | --- | --- |
| User chooses Chat or Work | [Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt.md), “Choose how you want to work”; [Get started with Work](https://learn.chatgpt.com/docs/get-started-with-work.md), “What to try first” | The user can select Chat, Work or Codex; the Work guide begins by switching to Work. Selection describes how to start/use an experience. Neither guide promises an immutable Chat-only conversation or a prohibition on later routing. |
| Workspace/member Work access | [ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex), “Configure Work access for your workspace” | Owners/admins manage Work Cloud and Work Local in **Workspace settings → Permissions & roles**, for the default and custom roles. Cloud covers supported hosted surfaces; Local alone still permits local desktop Work. The article states: “Chat remains available in every configuration.” It also says the member can see that Work is unavailable and request access. This establishes product access denial, not an explicit guarantee that every handoff UI or attempted transfer disappears. |
| Effective role permissions | [Managing feature access with RBAC](https://help.openai.com/en/articles/11750701-managing-feature-access-with-role-based-access-control-in-chatgpt), “Availability,” “Before you begin,” “Check a member's effective access” | RBAC is available on Enterprise, Edu, Healthcare and Teachers plans. Workspace Owners can manage defaults and create/assign roles; Admin authority is more limited. Ordinary roles combine additively: one granting role can retain access despite another being Off. Inspect all direct/group roles and eligibility; changes can take up to five minutes. A single Off role is insufficient proof. |
| Local/cloud distinction and rollout | [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions.md), “Review Work Local and Work Cloud permissions” | Some workspaces expose independent local Work/Codex controls; others expose **Allow members to use Codex and Work Locally** together. The combined control affects both products. Cloud browser/network controls are separate from Work entitlement. Inspect the actual layout rather than assuming labels or independence. |
| Starting defaults | [Enterprise admin quickstart](https://help.openai.com/en/articles/20001264-chatgpt-enterprise-admin-quickstart), section 5 | Model, reasoning, speed and new-chat defaults configure a starting experience. They do not themselves determine all effective availability. No documented Chat-only enforcement guarantee follows from a starting default. |
| Project instructions and inherited controls | [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), “Add project instructions,” “Workspace-level feature controls”; [Projects and chats](https://learn.chatgpt.com/docs/projects.md), web sections | Project settings hold instructions that override global custom instructions. Projects inherit workspace restrictions. Project creation/sharing permissions are documented; the same Project may contain Chat and Work chats. These facts do not establish a Project-level routing veto. The inspected pages give no explicit exhaustive statement that such a veto cannot exist. |
| Account/client preferences | [Desktop settings](https://learn.chatgpt.com/docs/reference/settings.md) | The documented preferences include follow-up behavior, personalization, browser permissions and Computer Use. None of the inspected settings descriptions establishes a Chat-to-Work prohibition. This reference is not proof that every account or client exposes exactly the same settings. |
| Runtime versus access control | [Work admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq.md), “Governance”; [Work Overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview), “Network access and external destinations” | Runtime policy and workspace access are separate layers. Disabling public shell internet access does not disable apps, search or the cloud browser. Disabling only local-computer access or one tool is not evidence that Work itself is unavailable. |

The dated official [Model Spec, 2025-12-18](https://model-spec.openai.com/2025-12-18.html#follow-all-applicable-instructions), orders instruction authority and excludes instructions conflicting with higher authority. This supports the hierarchy limitation; it does not specify every current ChatGPT routing rule or provide an enforcement setting. The public document also cautions that published behavior guidance is not an exact account of every production detail. Source or Project Instructions cannot establish that a conflicting platform requirement has been disabled.

## What the documented platform limits mean

The public sources describe materially different capability surfaces:

- [Computer Use](https://learn.chatgpt.com/docs/computer-use.md), “Set up Computer Use,” documents switching to Work or Codex for supported desktop GUI operation. Keeping ordinary Chat does not establish availability of this workflow.
- [Browser](https://learn.chatgpt.com/docs/browser.md), “Computer Use in the browser,” identifies desktop browser operation by Work or Codex. Ordinary web search is not the same capability.
- [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer.md) describes generated-file workflows in web Work and file creation in CLI/IDE, with different preview interfaces. It does not prove that every file operation requires transferring an existing Chat.
- [Code review](https://learn.chatgpt.com/docs/code-review.md), “Ask questions about the change,” describes a new Codex review chat and use of an existing adjacent chat. It does not establish that all PR discussion or every independent review must move to Work.

These are documented feature/surface limits, **not an exhaustive public routing algorithm**. Issue #106 records that higher-priority runtime requirements may mandate Work for particular operations. This research neither verifies every example as universally mandatory nor substitutes a broad task-category rule for the actual applicable runtime instruction. A mandatory exception, if encountered, remains governed by that instruction. Disclose the particular operation and supported alternative without presenting an optional handoff as compulsory.

The [current changelog](https://learn.chatgpt.com/docs/changelog) and [What's new](https://learn.chatgpt.com/docs/whats-new) were inspected for client changes. The July 2026 desktop changes bring Chat and Work histories/Projects together. Shared presentation/history does not establish preservation of the existing Chat as the control surface. Search results about Local/Worktree or host handoff concern different operations and do not answer #106.

## Conditional managed-workspace route for an owner to consider

This route is **not authorized for execution in this Step** and is not yet qualified as satisfying the absolute requirement. It follows the access controls above; the readback below is the evidence needed to evaluate this particular proposed solution, not a new standing workflow.

1. Identify the originating Chat's account, active workspace, plan, client/version, relevant member and actual permission layout through supported owner/admin evidence. The automatic Relay worker's configuration proves none of these facts.
2. If eligible, an authorized workspace administrator can review denying **both Work Cloud and Work Local** for the intended member through defaults/applicable roles. An Owner must perform any required role creation/assignment. Check all grants rather than only one role. If the local permission is combined with Codex, disclose the additional effect before choosing this route.
3. This denial applies to the member/workspace capability, not solely this Project. It can remove useful Work workflows in other Projects. It neither transfers an existing conversation nor supplies missing Chat tools. This broader operational cost requires the owner's explicit choice; do not infer it from #106's narrower desired outcome.
4. After an authorized change, read back the actual workspace/member, both effective access states, relevant role assignments and applicable delay. Verify on the intended supported client that Chat remains usable and Work is unavailable. Reopening settings or citing source text alone is insufficient.
5. To claim the **absolute no-transfer guarantee**, also obtain supported evidence of the client's behavior for an attempted or mandatory handoff while denied, or an authoritative OpenAI statement covering that behavior. No such test, transfer or settings mutation was performed here. If verification would initiate the prohibited transfer, do not run it under this research authorization; obtain an agreed safe verification method first.

Denial is a credible supported access-control candidate. Its applicability and exact effect on interaction/control transfer remain unverified. A changed role label, starting model, network restriction or unavailable execution alone cannot be reported as proof of every part of the owner requirement.

## Current evidence and capability bounds

This investigation used read-only Git/GitHub authority, official web documentation and advertised tool metadata. It wrote only this report. No live settings, credentials, roles, browser/client state, chat identity or conversation were changed; no handoff was initiated.

The available tool inventory did not advertise a tool that reads or changes Work role entitlements or ChatGPT Project Instructions. Plugin permission tools concern plugin/app permissions; document-session tools concern connected document surfaces. Their availability does not prove access to client settings. The worker is an automatic Relay execution environment, not a readback of the originating ChatGPT account, workspace, subscription, admin role or product toggle. Unknown live Project Instructions and any higher-priority rules remain unknown.

No live original-Chat reproduction, effective role readback, support confirmation or adversarial routing test was available. Public search absence cannot establish a universal negative. Documentation can change after this dated check. New supported controls or owner-provided attributable evidence should reopen the precise feasibility question rather than repeat an unqualified “impossible” claim.

## Proposed explicit owner Decision

**The owner must choose the disposition; neither option is implied by accepting this report or completing #105.** Recommended next request in Task #113's chronology:

> For #106, choose either **A: retain the absolute no-transfer requirement and pursue the conditional managed-workspace control plus supported applicability/behavior verification**, leaving #106 open until proved or separately disposed; or **B: explicitly replace that absolute requirement with the narrower fallback below**, accepting the possibility of platform-mandated exceptions. No answer leaves the absolute requirement unresolved.

Proposed fallback for **B**, not adopted or implemented:

> Keep the existing Chat as the interaction/control surface whenever the platform permits. Use supported capabilities available in that Chat. Do not initiate a discretionary Work handoff because work is complex, lengthy or convenient to delegate; asking first does not convert such a handoff into the default workflow. Identify any particular operation that higher-priority platform/runtime instructions require to use Work, explain the limitation and any supported in-chat alternative, and disclose the mandated exception while following the applicable higher-priority instruction. Do not claim these instructions disable platform routing or guarantee absolute non-transfer.

This is a **material weakening of the original absolute requirement**, so it requires explicit owner disposition before implementation. Acceptance of the report's quality is distinct from choosing this fallback. Retaining A is valid even if the eventual result is that some operations cannot be completed under the requested surface constraint; no automatic transfer or requirement downgrade follows.

If a later accepted change modifies this producer's complete effective Project Instructions, [accepted TH-029](https://github.com/jresearchsoftware/shared-governance/blob/f8d77b16ab9e92b31ae9a9390acabd9be9e962a7/vibevm/vibedeps/org.jresearch.ai.development-governance/11.0.0/vibevm/vibespecs/protocols/task-handoff.md#TH-029) and the [manual binding](https://github.com/jresearchsoftware/shared-governance/blob/f8d77b16ab9e92b31ae9a9390acabd9be9e962a7/docs/manual-task-handoff.md) require the complete accepted text, owner manual application and attributable live readback after acceptance/integration. Unknown live rules must be reconciled. Unchanged effective text creates no new application duty and discharges no earlier unresolved gap. This report changes no effective Instructions and supplies no live-setting proof.

#106 should remain open with its `small-improvement` label until its own requirement is satisfied or the owner explicitly disposes of the infeasible remainder. Task #113 retains the owner's keep-open conditions. This bounded research can be assessed with the combined result while those whole-Task obligations remain.
