# Task 67 Step 1 — Thin VibeVM dependency packaging

Authority: [Task 67](https://github.com/jresearchsoftware/shared-governance/issues/67)
and its [Manual Codex Step 1 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/67#issuecomment-6381799296).
Accepted guidance is frozen at `ac85342bf9f9fdf3f414bdbfba284a76e50949a2`.
Candidate instructions remain proposals. This is a Direct correction of the
authorized native-dependency contract; independent exact-head review remains separate.

## Evidence and authority analysis

[Task 45's design](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6221085331)
required qualification of actually included frozen dependencies.
[Task 51](https://github.com/jresearchsoftware/shared-governance/issues/51)
authorized normal native dependency support and manifest/lock/slot evidence.
Its accepted implementation required that evidence to be in the public allowlist.
That implementation choice was not a separate owner mandate to vendor every
dependency. [Relay's blocked 2.0.0 result](https://github.com/jresearchsoftware/codex-relay/issues/169#issuecomment-6311243986)
and [2.0.1 workaround Decision](https://github.com/jresearchsoftware/codex-relay/issues/169#issuecomment-6314092881)
demonstrate the cost; that consumer-specific historical Decision is preserved.
Accepted PV-013 protects frozen/hash-qualified closure; PV-016 identifies generated
slots as consumer state and PV-017 retains native resolution/update. No shared
protocol wording or package-source change is needed to implement those semantics.

Pinned VibeVM source is `b6659978453f50e6d1d4d99626d70b980a2c5847`:

- [Publication orchestrator](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-publish/src/orchestrator.rs):
  `publish()` parses package metadata and delegates direct Git publication; no
  exported dependency-slot requirement.
- [Git publication](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-publish/src/git_publish.rs):
  copies the supplied source tree. It does not synthesize a vendored closure.
- [Native source composition](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-package-source/src/builder.rs),
  [registry walk](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-registry/src/multi_registry_resolver/walk.rs)
  and [Git source resolution](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-registry/src/multi_registry_resolver/sources.rs):
  consume manifest requirements through configured sources. Git identity and
  declared version checks remain native.
- [Native solver tests](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-resolver/src/resolvo_engine/tests.rs):
  `resolvo_pins_transitive_deps` exercises the resolved transitive graph.

The source checkout's exact revision and the Linux musl binary SHA-256 were
verified live. Binary hash:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
The native fixture below confirms behavior, beyond reading the implementation.

## Correction and compatibility

The publisher reads committed native evidence under the selected package root
at the selected source SHA, independently of its public allowlist. It follows
required manifest edges through the existing lock's selected identities, qualifies
their complete native slot inventories, frozen metadata and content hashes, and
also qualifies any explicitly exported slots. It does not select versions or solve
ranges. Exact constraints and explicit Git declarations are checked for disagreement
with lock evidence. Source evidence is neither copied to the release nor added to
its receipt/digest unless the producer explicitly includes it in `files`.

Explicit vendoring remains supported and is checked against exported bytes:
source evidence cannot fill an incomplete shipped slot. Unused source slots and
excluded optional/development declarations remain outside the closure; a deliberately
shipped slot is checked regardless of its label. The unchanged-package path still
exits before readiness. Dependency-free governance retains its existing adapter.

The operator still materializes and commits native evidence before source
acceptance, but can omit it from the public inventory. No new configuration field,
resolver, credential, registry service, approval or per-release native-install test
is added. Consumer acquisition uses its own configured sources and lock; a producer
lock is qualification evidence, not a promise to force the consumer's versions.
Thin packages require reachable dependency sources for cold acquisition. Offline
use retains native local-source/cache limitations. Deliberately self-contained
distribution remains a package/consumer-owned choice.

Historical frozen releases, Relay/DocReview and unrelated consumers are unchanged.
Removing shipped bytes from a previously frozen package would still require its
own new version and producer authority. This tooling/docs-only change creates no
Development Governance release and does not include Task 65's version-policy work.

## Qualification

The focused cold-consumer test fails against the accepted publisher with
`AUTHORIZATION_PENDING` instead of `PUBLISHED`; see [baseline reproduction](logs/before.log).
With the correction, the same test publishes a four-file thin package to a
disposable bare Git repository: `vibe.toml`, `README.md`, `LICENSE`, and generated
`DISTRIBUTION.json`. It separately publishes direct and transitive dependencies to
disposable Git repositories. A new consumer with isolated Vibe settings, no lock,
slots or cache acquires all three packages through direct Git plus its ordinary
configured Git registry. Repeated install and intentional native update to the
next thin root version verify lock identity, native inventory/hashes, frozen
closure and direct/transitive installed-byte equality.

The fixture uses a bare-path Git registry: native `file:` registry URLs designate
directory registries, while an explicit `--registry` overrides source composition.
The first attempted mixed fixture configuration failed for that reason and was
corrected using the documented native contract; no production workaround was added.
Native `update` has a different option set from `install` and uses the committed
consumer source declarations.

Additional cases reject missing/tampered source evidence, mutable thin closure,
stale exact requirements, incomplete vendoring and included mutable development
slots, while accepting unrelated mutable source slots excluded from a thin release.
The full publisher matrix retains vendored publication, excluded suggestions,
source/CI/version/rights checks, no-op/sibling isolation, initial publication,
immutable tags, races, atomic non-force writes and same-source retries.

Reproduction (Python 3.11+, Git, pinned Linux VibeVM; all distribution writes local):

```sh
python3 tooling/vibe-publisher/test_publisher.py --vibe /absolute/pinned/vibe -v
python3 scripts/test-release.py --vibe /absolute/pinned/vibe
python3 scripts/test-publication.py --vibe /absolute/pinned/vibe
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-distribution.py
python3 scripts/test-self-adoption.py
python3 scripts/test-chatgpt-projection.py
git diff --check ac85342bf9f9fdf3f414bdbfba284a76e50949a2 HEAD
```

Exact results/logs and final-head CI are recorded in the canonical PR Outcome.
Local fixtures establish cold native Git acquisition, not Internet publication or
availability of every producer's dependency source. No public release/tag write,
consumer migration, service/configuration change, merge or Task closure is performed.
VibeVM 1.0.7 still rejects literal `dev-requires` and inline `optional=true` syntax;
planning exclusion tests do not claim native publication of unsupported manifests.
