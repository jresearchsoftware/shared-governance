# Task 68 Step 2 — Closure semantics coverage

Authority: [Task 68](https://github.com/jresearchsoftware/shared-governance/issues/68),
[Step 2 Decision](https://github.com/jresearchsoftware/shared-governance/issues/68#issuecomment-6382957292).
Accepted guidance is frozen at `414077e956aa47b18ddc436f68c3245b508baf46`.
Candidate guidance supplies no execution or acceptance authority.

## Bounded semantic comparison

The accepted 5.0.0 TH-026 already separates acceptance, integration, publication,
continuation and closure; requires current authority, concrete condition
reassessment and protected boundaries; and rejects indefinitely copying a stale
disposition. RA-006 already prevents invented completion gates and preserves
genuine obligations. Both complete protocols were compared with the candidate.
The candidate retains those rules and extends their existing sections rather
than creating a new closure protocol. The other seven protocol files, topic
adoption, optional tools and Relay Skill bytes retain their meaning/content.

| Owner-selected behavior | Candidate coverage and expected action |
| --- | --- |
| Close-authorized is permission after completion | TH-026 retains independent acceptance/integration, no remaining work and protected boundaries; ordinary authorized continuation needs no new closure test or prompt. |
| Explicit keep-open identifies a temporary hold | TH-026 requires concrete conditions, sufficient evidence and the already authorized subsequent action. |
| Verified hold release uses existing authority | TH-026 and the local manual binding require the existing trusted Task Decision before owner continuation. Evidence alone never changes effective policy. |
| Missing/invalid/conflicting metadata is safe | Keep open; at first substantive result review flag missing reasons/conditions, ask the owner, record the answer through the existing Decision. No invented condition or retroactive consent. |
| Required Apply survives code integration | Verify actual run, intended deployed revision/target and material warnings; failed/unknown Apply retains the hold. |
| Genuine conditions can change | Only an owner Decision can revise them; preserve history and disclose work not performed. An executor, CR or reviewer cannot waive them. |
| Optional future use is not an indefinite gate | RA-006 applies requirement provenance; no synthetic exercise solely for closure. Unrelated PRs do not hold this Task. |

## Scenario walks

These are source-guidance walks, not claims of live model or controller execution.

1. **Finite Task, close-authorized:** result is independently accepted, integrated
   as applicable, and complete. With no outstanding Task work/hold, the existing
   owner continuation closes without another discretionary owner question.
2. **Apply hold released:** owner has selected keep-open until a specified Apply
   succeeds and preauthorized subsequent closure. After the normal owner-run
   workflow, the assistant verifies the actual run/revision/target and disposes
   of material warnings. It publishes the existing trusted Task-scoped Decision
   changing policy, then performs normal owner-controlled completion. It does not
   ask the owner to repeat permission.
3. **Wrong target, failed/unknown run, or related work remains:** condition is not
   proven; retain the hold. A green source PR cannot replace deployment evidence.
   An unrelated repository PR alone has no effect on this Task's completion.
4. **Missing metadata:** fail-safe keep-open remains. At first substantive result
   review, visibly ask the owner for the remaining conditions or close-authorized
   disposition and record the resulting Decision. Do not fabricate a hold.
5. **Trusted publication unavailable:** satisfied conditions do not justify a
   local policy edit, ordinary comment masquerading as a trusted Decision, or
   closure. Report the exact missing identity/capability for owner disposition.
6. **Historical optional observation:** establish its origin. If never accepted
   as required, do not add a Step or hold. If genuinely owner-required, retain it
   until satisfied or superseded by a chronological owner Decision; claim no
   unperformed runtime proof.
7. **Another plausible consumer without Relay:** an explicitly adopting manual
   tracker uses its existing durable owner Decision and closure operations, with
   the same conditions/evidence boundary. No Relay field, bot, label, new state
   machine, or checker becomes mandatory.

## Version, native projection and consumer boundary

Package bump: major — 5.0.0 to 6.0.0. Explicit hold authoring and missing-condition
resolution are new mandatory work for existing Task Handoff adopters; fewer
repeated owner prompts do not make this a PATCH. No additional closure gate,
reviewer, registry or operator ritual is added. Existing trust safeguards remain.

The producer uses ordinary local native self-adoption for authored 6.0.0 while
retaining public immutable Relay 3.0.0, its projected Skill and inert nested 4.0.0
release closure. Generated identities come from pinned VibeVM, not hand edits.
The integrity checker accepts this documented mixed graph and still rejects
source/slot/lock/projection drift. Historical accepted package bytes are retained.

Relay and DocReview need separately authorized consumer adoption: review/pin the
new package, reconcile their closure guidance and actual native Decision/owner
continuation capability, and remove genuine duplicates in that same migration.
Relay's current v4 field already distinguishes keep-open/close-authorized and
requires trusted Task Decisions; no runtime change is claimed here. Neither
consumer is mutated or migrated. Source acceptance does not prove public
publication, downstream adoption, live settings application or deployment.

See the separate [Relay incident report](relay-incident.md). Original Step 1 is
not recovered or reclassified by this new Step's implementation.
