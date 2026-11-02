# Native Codex Relay Skill

[Task 57 Step 3 Decision](https://github.com/jresearchsoftware/shared-governance/issues/57#issuecomment-6367694493)
selects the native VibeVM path. This change remains proposed until independently
accepted. The separate [standalone PR 64](https://github.com/jresearchsoftware/shared-governance/pull/64)
stays Draft and unchanged; its later disposition is owner-controlled.

## Identity and routing

The root manifest retains the public immutable Git root for Relay 3.0.0 at
`325c96371783e2d628bfa9903b3244468c688fe6`. Development Governance 7.0.0 is
selected from this producer's exact authored in-tree registry through its normal
[self-adoption](self-adoption.md) procedure; it is not a claim that 7.0.0 has
been publicly published. Task 57's accepted public 5.0.0 pin remains historical
at `30a23f467c30c41fec918204cbbf2ecfffd7bef5`. Relay's annotated v3.0.0 tag is
`edd206aef4318a5f35b2353b221b2682e74bedb7`. Its public distribution receipt binds
accepted Relay source `ba99807bfc7e7d199ce9bf0e02be8e31416ddc95` and payload digest
`4322086611ebec9cc34bffe8fa650cf9c572a3c455da6484f68d1bba86c472ee`.
The selected Shared slot is identical to the exact authored export and has no
release-only `DISTRIBUTION.json`. Its native slot receipt and root lock bind that
content. The immutable Relay payload, public distribution receipt, native Skill
projection and inert dependency closure retain their accepted identity.
The in-tree producer registry and historical slots remain intact.

The generated root INDEX reads the authoring overlay, Shared 7.0.0 compact boot,
then Relay's conditional boot. Relevant Relay work reads its complete Skill and
triggered references. The [project Skill](../.agents/skills/codex-relay/SKILL.md)
is an exact native projection with its native receipt; ordinary use needs no
installation or network. Its `references/shared-protocols.md` selects the unique
Shared package from the consumer root lock and verifies that slot's identity.
All nine triggered Relay protocol references resolve inside the same 7.0.0 slot.
The producer's five project-wide topic adoptions and conditional self-adoption
remain unchanged. Relay's additional topics apply only to relevant Relay product
work. Manual Codex retains the [local Task binding](manual-task-handoff.md).
The new SI topic remains available but unadopted by the producer and Relay Skill;
this graph update does not activate its backlog scan.

Relay's nested frozen 4.0.0 lock/slot is inert publisher closure evidence. It is
neither an active root boot route nor a fallback protocol source. Historical
producer slots likewise remain unselected. Package acquisition, Skill discovery,
service eligibility, automatic routing and Writer Outcome success are distinct.
The existing workflows, publisher, CI, runner-group allowlist and services are
unchanged. A real separately admitted Task must verify automatic execution.

## Maintenance and rollback

Use the hash-checked Linux musl VibeVM 1.0.10 in [the toolchain pin](../toolchain/vibevm.json)
and the [published installation contract](../.agents/skills/codex-relay/references/installation.md).
Generate in a disposable native filesystem and review all outputs together:

```sh
export VIBE_REMAP="$PWD/toolchain/vibevm-git-compat.toml"
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

Deliberate Relay updates select reviewed immutable public roots, regenerate and
project in staging, and commit manifest, lock, selected slots, native receipt and
boot routes together. Shared source authoring uses the existing exporter/staging
procedure in [self-adoption](self-adoption.md): set its exact root requirement to
the new authored version without a Git override, stage the exact export and use
native registry resolution alongside the unchanged Relay root. Keep Relay's
public root available through its existing native cache or normal authorized
public acquisition; do not rewrite its payload or nested closure. Transfer only
the selected generated outputs and preserve historical slots.

For this mixed graph, VibeVM 1.0.10's `--registry` flag selects a local-only
resolver that omits manifest Git sources. Instead set `VIBE_SETTINGS` to an
isolated authoring directory with a `registry.toml` containing one `[[registry]]`
whose `name` is a local alias, `url` is `file:///absolute/staging/source/vibevm/vibepacks`
and `auth` is `none`. Run the install command above without `--registry` and
without `--offline` for public Git acquisition. This uses the native mixed
resolver without changing user registry configuration. The original lock may
be retained when intentionally changing Shared's exact version; preserve
historical slots pruned in disposable staging when transferring selected output.

Keep the compatibility variable in that isolated staging environment. VibeVM
1.0.10 otherwise applies its built-in raw-file mapping to the Relay Git clone,
causing a 404. The single [compatibility row](../toolchain/vibevm-git-compat.toml)
retains the existing origin; it adopts no remap package or global configuration.
See the [owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/87#issuecomment-6577910678)
and [qualification](task-87/step-1/README.md) before removing it in a later upgrade.

The offline qualifier checks both source forms: public packages retain their
immutable revision, content hash and distribution receipt; producer Shared
uses the authored version/content, local registry URL and native slot receipt.
No fabricated distribution revision or release receipt is needed for a candidate.
A changed package needs its own version and matching materialization, not reuse
of frozen public bytes. The Skill's actual lower-bound requirement permits this
producer selection, but resolver success does not qualify changed semantics or
an installed Relay. This does not adopt the change in Relay's own repository
or any other consumer.
Task 74 restores TH-029's intended effective-text reconciliation duty with an
explicit owner-selected PATCH exception despite the narrower published 5.2.0
workflow; see [release policy](releases.md). Relay's pinned Skill bytes are unchanged.

Task 65's 5.2.3 -> 6.0.0 change affects Package Versioning's compatibility and
release assessments. The Skill's used protocol paths and section names,
consumer-root lock/slot selection, local authority and supported execution
mechanisms remain available. Its existing deliberate-update guidance can apply
the new assessment without changing Relay's interfaces or immutable Skill bytes.
This producer updates its own reviewed source/lock/materialized state; it does
not release or migrate Relay. The retained nested 4.0.0 snapshot still belongs
to Relay's immutable release closure and is never a fallback policy source.

Task 84's 6.0.0 -> 7.0.0 change does affect the Skill's used closure semantics.
The target is native closing linkage for a genuinely completing `close-authorized`
PR and condition-verified later closure for `keep-open`. The pinned Skill and
runtime source still prescribe `closesTask=false`, neutral squash and separate
trusted closure requiring effective `close-authorized`. Keep those immutable
bytes and supported historical/admitted authority intact; do not claim the new
behavior from installing the Shared slot. The producer-local
[Task 84 transition](releases.md#task-84-closure-transition) records the exact
fallback scope, deprecation, owner-selected 60-calendar-day window from verified
publication of the first compatible Relay release, qualification limits and
post-publication Relay1 deliverable. Shared publication does not start the clock;
the exact event and derived deadline are recorded only once that Relay publication
is verified. Removal needs a separately accepted future Shared release no earlier
than window end. Source/native graph validation is separate
from qualification of that combination or deployment of a compatible Relay.
A new Relay release must implement/qualify its own adoption and raise its Skill
floor to the first published Shared version containing the new behavior.

Rollback uses ordinary Git revert of the complete integration (or checkout of
the accepted predecessor), restoring graph, slots, projection, receipts and
routing together. For native removal, use the documented `skill uninstall` in
staging and remove the Relay root/slot/routes together in the reviewed diff.
Preserve unrelated Skills and local overlays. No standalone projector owns this
native installation. Offline reading/projection from retained slots is supported;
cold offline acquisition without slots/cache is not promised.

The [Step 3 evidence](task-57/step-3/README.md) records scoped qualification and limits.
