# Task 9 implementation and qualification (2026-10-10)

Authority is [Issue 9](https://github.com/jresearchsoftware/shared-governance/issues/9)
and the owner's manual full-implementation request. Starting accepted main was
`d6e369337c33df4b16e32ed229d9521d7cf3f3b3`. Latest owner directions supersede
historical first-publication blockers. This change declares stable `1.0.0` in
one package, with `Package bump: major`; the stable contract and source-publication
workflow are explicit, while existing proportional-controls semantics and consumer
authority are preserved. No independent package or maintenance line is introduced.

## Scope coverage

| Owner direction | Implementation |
| --- | --- |
| Stable source path, one whole-package version | Workspace member `packages/development-governance`; manifest version; commit-relative historical export discovery. Frozen 0.1.0 retained outside membership. |
| Reusable lifecycle rules, local cadence | One canonical package-versioning protocol, separate VibeVM implementation section, producer-owned `docs/releases.md`. |
| Governance compatibility and pre-1.0 | Mandatory behavior/authority/workflow classification; disclosed experimental breaking minors, explicit 1.0 stability declaration, patch-only/caret/exact windows. |
| Parallel tasks | Sequential category application against current main, numeric transition CI, changed-head re-review; no reservations, duplicated authoring trees or multi-merge subsystem. |
| New protocol versus local policy | Conditional boot requires project adoption of the topic. Package install/update preserves existing local policy; newly adopting project selects a human-owned route. |
| Automatic publication and safe retry | Successful source-main CI trigger, actual accepted first-parent SHA, source transition, fixed public destination, absent-tag publish, existing-tag no-op, same-SHA dispatch tied to successful push CI. |
| Immutable frozen coordinates | Pre-merge source/version and public-tag check, remote-tag skip, native publisher in disposable bare copy plus atomic non-force final push. Competing tag/main cannot be overwritten. |
| Transitive closure and conflicts | Shared policy checks actually included frozen/hash graph with precise optional/dev exclusions and justified exceptions; this dependency-free payload retains an empty closure. Synthetic installed graph tests exercise transitive snapshot and diamond conflict. |
| Proportional routine evidence | Existing CI/review/Actions/refs; no manual per-file remote hashes, duplicate publisher review, ledger, registry service, activation flags or second approval. |
| Durable documentation | Root/current package docs use stable facts and publication links; original frozen README wording remains historical. |

The proportional-controls canonical bytes, active snapshot and accepted-origin
receipt remain unchanged. Task 15's semantic-completeness guidance remains in
AGENTS/authoring; unresolved adjacent Relay extraction candidates remain owned
by their existing consumer decisions. This new lifecycle protocol is newly
authored shared content, not a claim to repair those omissions or migrate Relay.

## Reproducible validation

```sh
git diff --check origin/main HEAD
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
python3 scripts/test-release.py --vibe /absolute/path/to/pinned/vibe
python3 scripts/qualify-vibevm.py --vibe /absolute/path/to/pinned/vibe --materialize
python3 scripts/qualify-distribution.py --vibe /absolute/path/to/pinned/vibe --source-ref "$(git rev-parse HEAD)"
```

Source/export, 33 distribution regressions, 16 release regressions (10 ordinary
and 6 optional native integrations), stable workspace/member/materialization,
local publisher/cold consumer and patch update/rollback are the focused surfaces.
Actionlint validates both workflows. Final exact-head results and CI links are
recorded in the canonical Issue Outcome, avoiding a self-referential source SHA.

The integration fixtures demonstrate existing-tag skip before binary invocation,
absent-tag failure then same-source retry, atomic concurrent-tag rejection,
valid numerically lower new release after a higher tag, frozen transitive graph,
unsatisfiable diamond and explicit consumer lock change. Local-registry project
re-resolution uses `install --registry`; pinned `update --registry` is a global-app
option. Real direct-Git `vibe update` is covered by the distribution probe.

An installed consumer retaining local version policy and a newly adopting
consumer selecting a human AGENTS route both preserve human text through install.
These are CLI and routing-contract checks, not fresh Codex model-execution proof.
The consumer tests are disposable; no existing consumer's authority changes.

VibeVM's deliberate tag-drift/offline incident probes remain diagnostic evidence:
the canonical verifier rejects the known lock/retained-slot split; complete
materialized Git rollback works offline, cache-only reconstruction can fail.
They are not routine release rituals. The bounded no-force publication workaround
addresses the specific known tag-replacement capability of the pinned publisher.

## Deployment and review boundary

The source workflow is complete and tested with local Git transport. Actual
GitHub Actions publication executes after independently reviewed owner merge.
Repository-secret name inspection on 2026-10-10 found no publisher secret;
an authorized owner must configure `DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN` with
Contents write on the distribution repository, as documented in release policy.
Existing admin/push permission does not establish a scoped Actions credential
or exclusive write ownership. No credential is copied or provisioned by this task.

The exact frozen v0.1.0 annotated tag object observed before and after implementation
was `0098ff6f983bb02345b3c7d270497fc340006408`. No distribution refs are mutated
by this execution. Live post-merge GitHub publication and credential authentication
remain unexecuted evidence; local integration does not claim them. Keep Issue 9
open at handoff; no self-approval, merge, package release or consumer migration.
