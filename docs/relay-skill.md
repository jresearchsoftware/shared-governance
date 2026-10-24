# Native Codex Relay Skill

[Task 57 Step 3 Decision](https://github.com/jresearchsoftware/shared-governance/issues/57#issuecomment-6367694493)
selects the native VibeVM path. This change remains proposed until independently
accepted. The separate [standalone PR 64](https://github.com/jresearchsoftware/shared-governance/pull/64)
stays Draft and unchanged; its later disposition is owner-controlled.

## Identity and routing

The root manifest pins the public immutable Git root for Relay 3.0.0 at
`325c96371783e2d628bfa9903b3244468c688fe6` and the producer's authored
Development Governance 5.1.0 through its generated in-tree registry.
Relay's annotated v3.0.0 tag is
`edd206aef4318a5f35b2353b221b2682e74bedb7`. Its public distribution receipt binds
accepted Relay source `ba99807bfc7e7d199ce9bf0e02be8e31416ddc95` and payload digest
`4322086611ebec9cc34bffe8fa650cf9c572a3c455da6484f68d1bba86c472ee`.
The earlier public Shared 5.0.0 root at
`30a23f467c30c41fec918204cbbf2ecfffd7bef5` remains historical evidence. Native
producer authoring uses exact exported candidate bytes without a public
distribution receipt or a publication dependency. The integrity check verifies
the local Shared source/slot/lock against the exact authored export and retains
Relay's public-root, closure and native Skill receipt checks.

The generated root INDEX reads the authoring overlay, Shared 5.1.0 compact boot,
then Relay's conditional boot. Relevant Relay work reads its complete Skill and
triggered references. The [project Skill](../.agents/skills/codex-relay/SKILL.md)
is an exact native projection with its native receipt; ordinary use needs no
installation or network. Its `references/shared-protocols.md` selects the unique
Shared package from the consumer root lock and verifies that slot's identity.
All nine triggered Relay protocol references resolve inside the same 5.1.0 slot.
The producer's five project-wide topic adoptions and conditional self-adoption
remain unchanged. Relay's additional topics apply only to relevant Relay product
work. Manual Codex retains the [local Task binding](manual-task-handoff.md).
The new SI topic is available but not adopted by the producer or Relay Skill;
this graph update does not activate its backlog scan.

Relay's nested frozen 4.0.0 lock/slot is inert publisher closure evidence. It is
neither an active root boot route nor a fallback protocol source. Historical
producer slots likewise remain unselected. Package acquisition, Skill discovery,
service eligibility, automatic routing and Writer Outcome success are distinct.
The existing workflows, publisher, CI, runner-group allowlist and services are
unchanged. A real separately admitted Task must verify automatic execution.

## Maintenance and rollback

Use the hash-checked Linux musl VibeVM 1.0.7 in [the toolchain pin](../toolchain/vibevm.json)
and the [published installation contract](../.agents/skills/codex-relay/references/installation.md).
Generate in a disposable native filesystem and review all outputs together:

```sh
vibe --json install --no-default-registry --no-prefer-local --assume-yes
vibe --offline --json skill list
vibe --offline --json skill install --skill codex-relay --agent codex --scope project --dry-run
vibe --offline --json skill install --skill codex-relay --agent codex --scope project --yes
```

For initial transition, start fresh resolution in staging: preserve the old lock
and slots outside that disposable checkout before install. The first install
with the old lock reused its local Shared identity despite the new Git root.
Fresh resolution with `--no-prefer-local` selected both public roots. Do not edit
generated identity fields. VibeVM prunes historical orphan slots; retain those
accepted historical files when transferring the selected generated outputs back.
No special action is needed for ordinary file reading.

Deliberate updates select reviewed immutable roots, regenerate and project in
staging, and commit manifest, lock, selected slots, native receipt and boot routes
together. Shared source authoring still uses the existing exporter/staging
procedure in [self-adoption](self-adoption.md); a changed package needs its own
version and matching materialization, not reuse of these frozen public bytes.
Qualification must be updated for an intentionally selected new graph.
For mixed local Shared/public Relay regeneration, use that procedure's isolated
`registry.toml`, rather than the local-only `--registry` shortcut.

Rollback uses ordinary Git revert of the complete integration (or checkout of
the accepted predecessor), restoring graph, slots, projection, receipts and
routing together. For native removal, use the documented `skill uninstall` in
staging and remove the Relay root/slot/routes together in the reviewed diff.
Preserve unrelated Skills and local overlays. No standalone projector owns this
native installation. Offline reading/projection from retained slots is supported;
cold offline acquisition without slots/cache is not promised.

The [Step 3 evidence](task-57/step-3/README.md) records scoped qualification and limits.
