# Task 68 Step 3 — Compatible closure guidance

Authority: [CR-68-001](https://github.com/jresearchsoftware/shared-governance/pull/72#pullrequestreview-5638289203),
starting head `9d42e494ee7ee36485b5cb74d5e44e0eb457aba2`.
Accepted guidance remains frozen at `414077e956aa47b18ddc436f68c3245b508baf46`.
This corrects Step 2's major rationale; its incident and execution evidence stay
historical. Candidate guidance does not govern its own authoring or acceptance.

Package bump: minor — Development Governance 5.0.0 to 5.1.0 under PV-002.

## Contract comparison

The complete accepted TH and RA protocols and PV-002 were compared with the
candidate. The two possible incompatible additions were a universal hold
authoring structure and a newly mandatory first-result-review action. TH-026 now
presents those as compatible guidance within existing reassessment and locally
selected timing/mechanisms. This producer retains the owner's concrete selection
in its manual binding; that selection does not bind other consumers.

| Area | Accepted 5.0.0 contract | Compatible 5.1.0 addition |
| --- | --- | --- |
| Completion | TH-026 requires actual completion, applicable checks/acceptance and protected boundaries. | Explains close-authorized permission after completion; no extra closure test. |
| Holds | TH-026 reassesses concrete conditions, remaining work and holds at meaningful transitions. | Shows how an owner-selected temporary keep-open can express conditions, sufficient evidence and authorized follow-up. No universal new authoring field. |
| Permission | Already authorized actions need no ceremonial reconfirmation; new scope needs its owner. | Verified preauthorized hold release uses the existing trusted Task Decision and owner continuation, with no repeated permission prompt. |
| Metadata gap | TH-026 permits only currently authorized continuation; RA-006 prohibits invented gates. | Retains the project's fail-safe keep-open and illustrates resolution through existing review/Decision, preserving local timing. No scheduled review duty. |
| Apply | Accepted source does not prove deployment/release; genuine obligations remain binding. | Example checks the actual owner-run workflow, intended revision/target and material warnings; failed/unknown Apply retains the hold. |
| Optional use | RA-006 distinguishes unratified suggestions from binding obligations. | Applies that distinction to future observation; unrelated PRs alone do not block this Task. |

RA-006's addition applies its existing authority rule to closure and explicitly
does not adopt Task Handoff elsewhere. All other rules, the other seven protocol
files, topic applicability, tools and publication contract retain their bytes.
No Relay controller, Writer state machine or consumer runtime is changed.

## Focused scenario walks

These assess authored guidance, not live agent/controller behavior.

1. A finite close-authorized Task is complete, independently accepted and
   integrated as applicable, with no hold. Existing owner continuation can close
   without another permission request or closure-specific test.
2. The owner selects keep-open until a specified Apply and preauthorizes release.
   The owner runs the normal workflow; the assistant verifies the actual run,
   intended revision/target and material warnings. If no related Task work/PR
   remains, it uses the existing trusted Task-scoped Decision, then the ordinary
   owner-controlled completion/closure path. Evidence alone does not mutate policy.
3. A failed, unknown or wrong-target Apply, or outstanding related Task work,
   retains the hold. An unrelated repository PR alone creates no blocker.
4. This producer's selected binding flags absent reasons/conditions at the first
   substantive completed/result-producing Task review, asks the owner for the
   missing disposition and records the Decision. Missing/invalid/conflicting
   metadata stays keep-open; no invented condition or retroactive consent.
5. A manual tracker without these labels keeps its accepted local reassessment
   timing and durable owner records. Installing 5.1.0 imposes neither Relay fields
   nor a new authoring structure, review event, checker or completion gate.
6. Verified conditions with unavailable trusted Decision capability do not permit
   a local policy edit or closure. Report the exact gap; an Outcome/CR/reviewer
   cannot replace owner authority or waive a genuine condition.
7. An optional future observation creates no synthetic exercise or indefinite
   hold. A genuine owner-required condition stays binding until satisfied or
   explicitly revised by its owner, without claiming omitted proof occurred.

The original [Step 1 incident](../step-2/relay-incident.md) remains terminal
BLOCKED and separate. Frozen 5.0.0 and earlier payloads, immutable public Relay
Skill 3.0.0 and its inert nested closure remain unchanged. Native producer
self-adoption selects authored 5.1.0; public publication and Relay/DocReview
consumer adoption require their own accepted paths. Independent exact-head
review, integration and Task closure remain separate boundaries.
