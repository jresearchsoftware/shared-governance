# Package authoring

The root virtual workspace has one stable member,
`packages/development-governance`. Its manifest owns the whole-package version;
a routine bump changes that value without moving the authoring tree. Frozen
`0.1.0` remains at its historical path as retained source, outside membership.
Historical exports discover the path from the selected commit's workspace.
The current passive flow contains three ordinary protocols and no native Skills,
capabilities or dependencies. Proportional-controls preserves its accepted
baseline and adds the scoped Task 19 existing-proof and friction corrections;
requirement-authority is conditionally read interpretive guidance, while
package-versioning has explicit consumer-adoption applicability.

[Release policy](releases.md) separates this producer's cadence from reusable
policy and documents automatic publication, exact-source retry and credentials.
[Distribution](distribution.md) describes the generated source receipt and
one-time integration tests. The authoring boot is outside the exported package.
The active proportional-controls snapshot and its source receipt remain pinned
as described in [self-adoption](self-adoption.md); candidate bytes cannot refresh it.

## Semantic completeness

[Task 15](https://github.com/jresearchsoftware/shared-governance/issues/15)
establishes the accepted invariant for future governance extraction, package
adaptation and consumer adoption: preserve the complete accepted reusable
semantics when moving policy ownership. Working behavior supplied by leftover
consumer instructions does not prove successful extraction.

Before moving ownership, read all relevant current canonical policy slices,
their project integrations and outcome/correction evidence. Where earlier splits
or adaptations matter, consult accepted source history and original instructions.
Bound this baseline to the domain's decisions and behaviors; one current
paragraph or like-named file is not necessarily its complete contract.

Explain source-to-shared coverage of each material obligation, trigger, qualifier,
exception, cost/authority boundary, operator flow and agent-routing condition in
the existing Task/PR/review evidence. Distinguish exact preservation,
meaning-preserving reformulation, explicitly accepted semantic change,
omission/weakening, and genuinely consumer-specific binding. Map obligations,
not strings; byte equality alone cannot establish completeness of the baseline.

An omitted or weakened reusable requirement is a producer migration defect.
Repair canonical shared source and independently accept a new package version
before relying on it for that behavior; do not rewrite or republish frozen
`development-governance@0.1.0`. Product-owned contracts and deliberate local
overlays remain local only with an explicit, defensible ownership rationale.
Record material omissions and owner dispositions rather than silently relying
on the old consumer to supply missing shared semantics.

Exercise the shared guidance in at least one other plausible consumer or
scenario without the old project's residual rules, and assess the original
consumer after replacing its reusable duplicates. Prove loading and application
where possible. Separate file/text evidence, CLI behavior and actual model
behavior; identify unavailable evidence instead of claiming it passed. A
scenario supports the coverage argument, not an always-on global test gate.

Under each consumer's separately admitted migration, adopt pinned reviewed
content and remove the genuinely duplicated canonical local guidance in the
same reviewed change. Preserve documented product bindings and verified local
overlays, checking for missing, weakened or doubly authoritative rules. Use
normal independent exact-head review and ordinary Git rollback. Source
acceptance alone transfers no consumer authority.

Scale this argument to the material change. Trivial editorial edits need no
exhaustive manual mapping; this procedure adds no standing ledger, rigid global
checklist, service or extra owner step. Assess any proposed new gate using
[proportional controls](../.agents/protocols/proportional-controls.md).
Task 15's first demonstration compares the frozen `proportional-controls` flow
with its [Relay provenance](provenance.md) in Task/PR evidence. Unresolved
producer findings and consumer-owned verification belong in the handoff to
[Relay Task 97](https://github.com/jresearchsoftware/codex-relay/issues/97);
the separate [routing investigation, Task 99](https://github.com/jresearchsoftware/codex-relay/issues/99),
does not accept or repair semantic migration gaps.

## Source and pinned-tool checks

Python 3.11+ and Git suffice for ordinary source/export checks:

```sh
git diff --check
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
python3 scripts/test-release.py
```

Stage new files and commit before checking exact-commit export. It selects the
stable or historical root from that commit, validates passive payload shape and
writes `DISTRIBUTION.json` outside the checkout. The receipt binds source SHA,
path, version and generated payload hashes. These hashes are tool output, not
a recurring manual reviewer exercise. Historical native-Skill exports remain
available through `vendor-skill.py`; current flow commits declare none.

For a changed integration, use the pinned Linux x86_64 musl VibeVM 1.0.7 binary
in a disposable native filesystem. Its SHA-256 is recorded in
[toolchain/vibevm.json](../toolchain/vibevm.json):

```sh
python3 scripts/qualify-vibevm.py --vibe /absolute/path/to/vibe --materialize
python3 scripts/qualify-distribution.py --vibe /absolute/path/to/vibe --source-ref "$(git rev-parse HEAD)"
python3 scripts/test-release.py --vibe /absolute/path/to/vibe
```

The authoring probe checks stable workspace/member loading and isolated registry
installation. Distribution's integration probe covers cold/repeat install,
lock/slot/route integrity, a deliberate disposable mutable-tag incident, offline
retained-slot behavior, synthetic patch update and complete Git rollback.
Release integration covers the guarded native publisher, competing writers,
transitive frozen closure, diamond conflict and intentional lock update.
No real consumer is migrated. These are focused integration/incident probes,
not mandatory per-release requalification of package-manager file transport.

Pinned VibeVM emits a static INDEX entry despite authored dynamic linkage;
the installed compact boot performs conditional protocol routing. It also has
known path-only `empty world / ORDER-LAW`, GNU `GLIBC_2.39` and cache-only offline
recovery limitations. No general platform restriction or model cost claim is
inferred. Task 10's [model evidence](task-10/step-1/README.md) is historical;
this task's consumer applicability scenarios establish routing contract and CLI
behavior without claiming fresh model execution.
