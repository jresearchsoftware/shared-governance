# Task 62 — Step 1: generated desired state and settings application

Authority: [charter](https://github.com/jresearchsoftware/shared-governance/issues/62)
and [owner direction/joint admission](https://github.com/jresearchsoftware/shared-governance/issues/62#issuecomment-6319169919).
No earlier execution Step exists. This is Task 62 Step 1; Task 60 independently
retains [its Step 1 history and coverage](../../task-60/step-1/README.md).
Same frozen accepted guidance `61aa3444365b02a27c392d48aa9ea33e85c5d5d4`.

## Receipt decision and non-circular contract

Inspected common project.py/base.md/README, producer wrapper, projection/native
qualification tests, current binding/custom/generated receipt and bootstrap/manual
binding, plus Landscape Task 12 chronology and PR 14. Active repository consumers
of receipt provenance are the projector's status source_changes and projection
tests; native qualifier invokes the CLI but does not need that inventory. Public
consumer code cannot be exhaustively enumerated, so removal is a MAJOR contract
change, not a claim that private consumers have none.

Alternatives assessed: deleting receipt entirely loses the existing local-write
ownership check; replacing it with Git-clean checks would introduce a different
repository/worktree policy and complicate first generation. Keeping schema 2's
full SHA/tool/source inventory perpetuates duplicate audit state and needless
churn. Schema 3 therefore retains only generator/repository identity and output
hashes. Concrete harm avoided: a user edits generated instructions (or an optional
cache), then update/disable silently destroys those useful edits. The receipt
lets the tool refuse before **any** output write/delete, even when Git has no
clean committed output. It is not tamper-proof authority or settings evidence.

Schema-2 ownership hashes migrate once under the same complete-plan checks.
Thereafter a new main SHA, changed native routes or tool metadata with identical
output yields no receipt commit. Every generation/check still requires an exact
independently accepted source and authority anchor, verifies committed ordinary
files and native lock/slot/index integrity, and ignores dirty candidate guidance.
Git and normal invocation/PR evidence bind reviewed tool version, inputs, output
and exact assessment result; no self-containing SHA is persisted. Optional enabled
Sources remain explicit exact-source snapshots and keep their manifest provenance.
They are never a mandatory cache or closure requirement.

Regenerate after effective inputs/dependency changes in the same normal PR, review
both changed and unchanged output, then accept the exact result. Candidate generated
text remains proposed; its accepted-source input is not authority for candidate
custom text or a newly proposed generator. Source acceptance and independent
review remain external. No follow-up hash-only refresh after squash is prescribed.

## Reusable/client ownership and cases

TH-029 owns conditional Task completion when application is in scope. The optional
ChatGPT base/README supplies complete-text manual application and supported
comparison mechanics; local manual binding links that behavior. Generation alone
acquires no application duty. Same-change native materialization remains SA-006/007.

| Case | Result |
| --- | --- |
| Unrelated accepted main commit / same-output generator upgrade | Check/update NO_OP; no settings work or receipt churn. |
| Substantive native dependency upgrade | Validate exact new accepted native inventory; regenerate in same PR; unchanged output needs no settings action. |
| Effective custom/binding/base change | Check stale, diff complete desired text, safe update, review in normal PR. |
| Legacy inventory names old 2.7.0 source | Historical provenance is not live drift. One deliberate schema migration can remove duplicate inventory with normal adoption; no self-pin. |
| Application included and live differs | Present full accepted replacement, reconcile unknown live rules, owner applies, supported confirmation/readback before closure. |
| Application included, live unavailable | Disclose gap; never infer synchronization from source merge or receipt. |
| Unchanged text, no known application gap | No manual action. A previously unverified application remains an explicit gap. |
| Foreign receipt, modified outputs, bad source/lock/slot/route | Preserve files and refuse; simplification cannot bypass protection. |

## Landscape recovery recommendation, updated for current chronology

The charter called Task 12 open, but live chronology now shows it **closed** after
[owner confirmation](https://github.com/jresearchsoftware/codex-model-landscape/issues/12#issuecomment-6318415643).
The owner confirmed application of the complete accepted 5,830-character file;
context corroboration is disclosed, not independent Settings UI enumeration.
Respect that disposition: do not reopen, re-paste or invent another execution
solely for a historical receipt SHA. No current source/live drift is established.

If reconciliation is later needed, independently freeze then-current accepted
Landscape source, use its pinned 4.0.0 common projector check and compare the
complete accepted desired text with supported owner evidence. Review any real
content difference; supply the whole text for manual application only if needed.
Keep 4.0.0's historical receipt as disclosed provenance in the interim rather than
hand-editing it or requiring hash churn. A substantive upgrade may deliberately
refresh/qualify once against a pre-generation accepted snapshot; that anchor need
not equal the containing commit. Adoption of published 5.0.0, if separately admitted,
migrates schema 2 safely and regenerates/qualifies in that same ordinary PR.
No consumer-specific projector, consumer edit, settings edit, reopen or release
was executed by this upstream Step.

Qualification and limits: [validation](validation.md).
