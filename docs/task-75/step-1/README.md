# Task 75 Step 1 — Negative constraint provenance

Authority: [Task 75](https://github.com/jresearchsoftware/shared-governance/issues/75)
and its [admission Decision](https://github.com/jresearchsoftware/shared-governance/issues/75#issuecomment-6385454528).
Accepted guidance is frozen at `2361868c41a916871d687aa8eea8f14573e2c82e`.
The launch supplies Task 75, Step 1 and purpose “Implement Task 75: prevent
agent-invented binding prohibitions”; no client title tool is available to verify
the persisted thread title. Candidate guidance remains proposed.

Package bump: patch — Development Governance 5.1.0 to 5.1.1.

## Bounded baseline and coverage

The complete accepted Requirement Authority, Proportional Controls, Task Handoff,
Package Versioning and Self-Adoption protocols, together with the producer's
authoring, release and manual handoff bindings, supply the relevant baseline.
RA-002 already denies independent authority to agent-generated convenience and
defensive restrictions. RA-005 preserves canonical authority and requires its
existing mechanism for material conflicts. RA-006 already derives mandatory
outcomes, prerequisites and gates from owner intent/contracts/protected invariants,
while leaving routine delegated means to engineering judgment. PC-004/013 already
require owner authority for material workflow narrowing and prevent a proposed
defense from authorizing itself through a CR or next Step.

Only RA-006 gains normative prose: the existing provenance rule explicitly covers
prohibitions, ordinary necessary operations and discussion before publishing a
material new restriction as authority. PATCH is justified by contract preservation,
not by the small diff: this adds no reporting field, approval, review stage or
operator action beyond the accepted rules above. If it created such duties, PV-002
would require a different classification. All eight other protocol files, client
tools, conditional routing/adoption, accepted exceptions and publication contract
retain their meaning and payload bytes. Changelog and version metadata change;
normal native source/slot/lock/boot generation selects the candidate for this
producer without changing the frozen public Relay Skill.

## Focused scenario walks

These are rule-based checks of proposed guidance against the charter's supplied
incident facts, not fresh live GitHub investigation, model-behavior proof or
retrospective execution of either incident.

| Scenario | Application and expected disposition |
| --- | --- |
| [Task 68 manual Step 2](https://github.com/jresearchsoftware/shared-governance/issues/68#issuecomment-6382957292): owner wants effective investigation and salvage; assistant excludes privileged host forensics, permission repair, alternate recovery and other diagnostic means. | RA-006 rejects an assistant's blanket exclusions without owner/contract/protected-boundary provenance. Effective in-scope diagnostics and recovery are engineering means when authorized. This does not grant host privilege or permission repair: actual host, credential and execution boundaries still govern. Preserve Step 2 evidence; separate [Relay Task 189](https://github.com/jresearchsoftware/codex-relay/issues/189) owns the authorized end-to-end diagnosis and fixes. Task 75 does not edit Task 68, PR 72 or their history. |
| [Relay Task 182](https://github.com/jresearchsoftware/codex-relay/issues/182): requested change touches the frozen Relay Skill, but assistant inserts a no-publication ban to keep it small. | RA-006 prevents the Task/Decision/prompt writer from excluding normal versioned preparation/publication already covered by the owner outcome and accepted lifecycle. No special owner exception is needed for that ordinary workflow. Frozen bytes still cannot be rewritten. Where the ban has entered historical canonical authority, use the existing [corrective trusted Decision](https://github.com/jresearchsoftware/codex-relay/issues/182#issuecomment-6385074994) rather than silently deleting it; continue the existing PR under its own authority. |
| Genuine protected operation: an admitted local worker cannot use GitHub credentials, publish, alter production or inspect a credential store without authority. | RA-003/005/006 preserve those actual boundaries. The worker completes permitted source/version preparation, checks and commits, then reports unavailable proof or publication for the authorized actor. A broad owner outcome is not permission to cross an explicit execution, credential, production or cross-repository boundary. Independent acceptance remains bound to the exact reviewed head. |
| A CR or Decision writer proposes diagnosis-only, no recovery/in-scope fixes, a prohibited tool or an extra hold for a new hypothetical risk. | Separate a preference from an existing obligation. Discuss a material narrowing's rationale and consequences before publishing it as authority. Accepted restrictions remain until reconciled through the trusted Decision mechanism. Ordinary authorized fixes need no new permission prompt. A real unresolved protected risk retains its accepted hold/stop effect. |
| Another consumer adopts RA without Relay Task machinery. | The same provenance and protected-boundary rules use that project's existing owner/Decision mechanism. No new form, provenance registry, reviewer gate, permission ritual or Task state machine follows; installation alone adopts no topic. |

## Delivery and remaining boundaries

This Step prepares local source, generated state and ordinary commits only.
Independent exact-head assessment, Writer publication, owner integration and
verification of the normal accepted-source package-publication result remain
with their authorized actors. Successful local checks do not establish those
events or whole-Task completion. Consumers own later deliberate adoption; no
consumer migration, monitoring or unrelated active-work mutation is included.
Root/sudo-only installed-runtime proof belongs to native Exact-head CI after
Writer publication and is not attempted or claimed here.

## Local validation

- `git diff --check`: passed.
- `TMPDIR=/tmp python3 scripts/qualify.py --export-ref HEAD`: passed, including
  exact authored export, registry/slot/lock/routes and unchanged Relay Skill.
- `python3 scripts/test-release.py`: passed 11 tests; six optional one-time
  native publisher/resolver integration tests skipped. No publisher was invoked.
- `TMPDIR=/tmp python3 scripts/test-distribution.py`: all 50 tests passed.
- Existing release `transition` check with category `patch`: passed 5.1.0 to
  5.1.1 against the frozen accepted SHA. No remote tag availability claim is made.
- Pinned VibeVM 1.0.7 musl binary matched the toolchain SHA-256. Native mixed
  install in disposable staging selected 5.1.1 and retained Relay 3.0.0; only
  selected generated outputs were transferred, preserving historical slots.
- All eight other complete authored protocol files match the accepted baseline
  byte for byte. The scenario walks above assess the negative-constraint rule.
- `test-self-adoption.py` could not run its 16 test bodies: fixture setup's local
  clone exits 128 because Git detects dubious ownership of the shared checkout's
  `.git`. Repeating with `/tmp` confirmed the clone limitation. No Git configuration,
  ownership or permission repair was attempted. Direct exact-commit native
  qualification passed; the clone-based suite remains unavailable in this worker.

The default worker temporary directory is inside the checkout, so export tests
initially rejected their destination as designed; selecting external `/tmp`
resolved that issue. This environmental correction changes no source or policy.
