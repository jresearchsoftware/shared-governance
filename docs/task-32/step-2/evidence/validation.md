# Step 2 validation evidence

This record covers local preparation facts, not real ChatGPT model observations.
Exact final result/head, CI run/job/annotations and publication readback belong
to the canonical Step 2 Outcome on PR 33. Step 1 evidence remains historical.

## Text and source checks

`python docs/task-32/step-2/verify-text.py` passed during preparation. The complete
Instructions contain **4,305 Unicode characters** inside the sole `markdown`
fence, including the final LF. They exactly equal the common static template
with the Shared Governance binding substituted; no placeholders or clipping.
Unchanged inputs reproduce identical output. The 8,000 budget is an experimental
text constraint; the actual UI counting/limit behavior remains untested.

Connected GitHub AGENTS content/blob and all four Task comments were obtained.
The accepted AGENTS and both supplied original bodies matched canonical Git/
Step 1 snapshots exactly. The local verifier also confirms accepted native/local
routes and frozen consumer-example path existence. These checks do not prove
semantic completeness, consumer currentness, live settings equality or model reads.

Step 1 files and accepted package/native/root instructions are preserved. Full
staged diff inspection, whitespace and source/export qualification will be
reported here after the prototype commit and applicable checks.

## Repository checks

Pending execution at this initial prototype commit:

- `python scripts/qualify.py --export-ref HEAD`
- `python scripts/test-distribution.py`
- `python scripts/test-release.py`
- `python scripts/test-self-adoption.py`
- Whole-package boundary against the frozen accepted main and `git diff --check`
- Final exact-head Public candidate checks and primary warning inspection

All future behavioral C1–C8 results remain **NOT RUN / UNQUALIFIED**.
No native VibeVM/runtime, live project setup, Source upload, consumer installation,
protected action or independent acceptance is established by local checks or CI.
