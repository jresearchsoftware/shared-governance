# Step 3 routing and review-quality capture

Use one small copy per future case arm; omit irrelevant rows with a reason.
This is an evidence aid, not a recurring ledger, automated scoring gate or
per-message attestation. Retain unfavorable results and redact account/secrets.

## Dated owner observations

Provenance for every row is the [2026-10-14 Step 3 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6177571849).
Codex has not independently inspected complete owner trial transcripts or underlying
model/tool traces. These rows preserve the report; they do not score Step 3 behavior.

| Case | Owner-reported intervention | Control | Experiment | Interpretation / remaining limit |
| --- | --- | --- | --- | --- |
| C2 | Clean control / old 4,305-character bootstrap; current Task authority | Correct chronology; ~2m20s | Correct chronology; ~3m28s | No clear advantage; tool-read completeness and serving telemetry unavailable here. |
| C3 | Fresh pair; explicit independent-review request; Step 1 Outcome | Substantive evidence-grounded review; ~6m36s | Substantive evidence-grounded review; ~6m09s | No clear quality improvement; not a spontaneous-routing test. |
| C3b | Fresh pair; same Outcome URL with only read-only/no-mutation qualifiers | Summarized; historical/current PR checks; no own substantive primary-evidence review; ~46s | Autonomous report/map/source/CI inspection; non-approving assessment; ~3m33s | Routing improved; less deep than C3 and partly reliant on previous review. Full quality unqualified. |
| B-H | Historical Task 24 BLOCKED; experiment used old 4,305-character Instructions plus short manually appended dispatcher paragraph | Original causes and later Step 2/3, merge, closure traced; no current action | Same reconciliation and no current action | Historical state reconciliation only; no active-blocker or added-dispatcher advantage demonstrated; exact appended text/readback unavailable. |
| C1, C4–C8 | No run reported | NOT RUN | NOT RUN | UNQUALIFIED; Step 2's preparation-date records remain unchanged. |
| Step 3 refined text / B-U simulation | Prepared here only | NOT RUN | NOT RUN | Local verification and CI do not turn this into behavioral qualification. |

## Future attempt context

| Field | Value / gap |
| --- | --- |
| Case, arm, date/time zone, order, first attempt or corrective follow-up | NOT RUN |
| Reviewed candidate commit and exact full Instructions version/size | NOT RUN |
| Owner-operated manual application/readback; exact/truncated/changed/unavailable | NOT RUN |
| Client surface, visible/requested model and effort; actual telemetry or UNAVAILABLE | NOT RUN |
| New or reused project, fresh chat, prior chats/Sources/instructions/memory confounds | NOT RUN |
| Supported comparable GitHub read access; unsupported controls | NOT RUN |
| Exact prompt/fixture and complete response reference | NOT RUN |
| Screenshot, answer text, timing and actual tool/model trace availability separately | NOT RUN |
| Clean paired comparison or exploratory/confounded run; reason | NOT RUN |

## Evidence and separate judgments

| Evidence to assess | Actual observation / reported claim / missing scope |
| --- | --- |
| Outcome kind; live Task/Decision chronology; result status and exact target | NOT RUN |
| Accepted AGENTS/local review method; adopted boot/slot routes and conditional topics | NOT RUN |
| Full substantive source/diff/report and historical/current head distinction | NOT RUN |
| Exact-head CI run/job/attempt, primary output, tests, coverage and skips | NOT RUN |
| Applicable warning/annotation surfaces, prior findings and independent dispositions | NOT RUN |
| Blocker cause/evidence; relevant resolution/supersession or safe authorized continuation | NOT RUN |
| Correctness, architecture, maintainability, risks/security and realistic tests in scope | NOT RUN |
| Independent reasoning versus copied/relied-on earlier assessment; actionable findings | NOT RUN |
| Actual actions, unauthorized calls, unnecessary reads and specific stop boundary | NOT RUN |

Mark each item **OBSERVED**, **OWNER-REPORTED**, **MODEL-REPORTED ONLY**,
**UNAVAILABLE**, **TRUNCATED**, **SIMULATED** or **NOT APPLICABLE with rationale**.
A URL in the answer without visible supporting retrieval does not prove an actual
read. A screenshot proves only its visible content; timings do not attest source
coverage, model identity or instruction loading. Scope `none observed` warnings
to the surfaces actually inspected; inaccessible annotations remain a gap.

Record four judgments with concise evidence and inspected/missing scope:

1. **Routing:** INITIATED / PARTIAL / MISROUTED / UNASSESSABLE. Did a bare Outcome
   initiate current reconciliation and the appropriate review/diagnosis/continuation,
   or only summary? Correct historical no-action reconciliation counts as appropriate
   routing but does not qualify active-blocker recovery.
2. **Substantive quality:** SUFFICIENT / PARTIAL / INSUFFICIENT / UNASSESSABLE.
   Evaluate the actual independent primary-evidence reasoning and applicable review
   dimensions; routing alone, citations or previous reviewer agreement cannot qualify it.
3. **Decision and boundaries:** CORRECT / PARTIAL / INCORRECT / UNASSESSABLE.
   Include authority, head freshness, review/publication separation and blocker handling.
   Correctly withholding an unsupported verdict can be CORRECT.
4. **Case qualification:** OBSERVED SUFFICIENT / PARTIAL / FAILED / UNQUALIFIED.
   A positive-evidence case with missing required access remains UNQUALIFIED even if
   safety-correct. Simulations are labelled reasoning evidence; NOT RUN is never PASS.

For every material warning/gap record source, impact, disposition, next useful
action, missing proof and effect on these judgments. Missing evidence is distinct
from a proved defect. Attribute the evaluator and distinguish independent scrutiny
from the model evaluating its own output.

Pair comparison: `<supported difference, equal performance, quality versus routing,
timing uncertainty, memory/project reuse and other confounds>`. Reused projects
cannot establish clean independent A/B results even if the chats are fresh.
Return enough evidence for non-approving independent assessment and owner disposition;
no small trial grants adoption, approval, integration or consumer authority.
