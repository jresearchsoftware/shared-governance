# Task 100 Step 2: project-side Skill selection

Related to [Task 100](https://github.com/jresearchsoftware/shared-governance/issues/100).
This is the complete reviewable implementation/design evidence, not a replacement
for the original truncated Step 1 Outcome. The independently accepted baseline
for this cycle is `1aabc1b1131d6d73285f84d8dc8a8dd3725135a4`; current
[owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/100#issuecomment-6940639935)
selects a common discovery Skill with independent Project source bindings. No
native ChatGPT activation, live Settings reconciliation, release or external
product contribution is claimed here. The Task stays open for its actual
acceptance, product delivery and owner application/readback conditions.

## Delivered contract and compatibility

The optional [projector](../../../packages/development-governance/tools/chatgpt/project.py)
adds schema 3, with a separate explicit `skill_selection` consumer snapshot and
named native entries/shared routes. Maintenance uses the existing interface and
Git object store, validates both snapshots and generates exact selected Git links
and VibeVM lock identities. All complete product/shared semantics stay at those
canonical sources. No new resolver, native Skill payload, ZIP, Plugin, registry,
service, API, cache, installation receipt or source authority oracle is introduced.

Existing schema 2 remains supported with identical output, including this
producer's 7988-character complete Instructions. Its base/custom/binding and
Instructions remain unchanged. The candidate's whole-package classification is
**10.1.0 MINOR** against accepted 10.0.0: compatible opt-in tooling/guidance, no
new mandatory work for existing consumers, protocol changes or topic adoption.
Opting in changes effective desired text and retains existing TH-029 manual
application/readback. This cycle deliberately does not opt this producer or other
consumers in before source acceptance. Materialized candidate source is proposed;
the frozen accepted baseline continues to govern this execution.

The source pin is independent of the commit containing generated Instructions,
preventing circular SHA churn. Advancing a consumer lock does not silently advance
an explicit Project selection. An accepted change to the selection updates the
exact Project routes; a transport release does not. Current Task authority may
require reconciling an obsolete selection; the generator never silently blesses
it. Native missing/ambiguous/stale discovery discloses a limitation and retains
JIT fallback. Local maintenance refuses inconsistent selected source rather than
emitting false links; this is not a runtime installation preflight.

## Bounded semantic coverage

| Accepted baseline behavior / owner requirement | Candidate disposition and evidence |
| --- | --- |
| Project Instructions are desired text; Sources optional; no native registration claim | Preserved schema 2/base/CLI and native/live state separation in schema 3. |
| Freeze accepted Git and consume root VibeVM selection without resolving or adopting all declared Skills | Separate exact consumer SHA and explicit name/entry/shared selection; validates lock/slot bytes and native declaration. Other declared Skills omitted. |
| Common transport must not replace per-Project product/shared versions | Output routes to the Project snapshot/root lock, prohibits publisher/bundled/other-Project substitution; product transport remains external. |
| Preserve applicability, complete triggered reading, relative routes, authority, adoption and role | Canonical source content is linked rather than copied/re-authored. Existing base and all ten protocol bytes unchanged. |
| Missing Skill must not block unrelated work | JIT fallback/disclosure; only evidence/capability-dependent actions withheld. |
| Stable inputs, explicit updates/rollback, unknown live coexistence | No rewrite on unchanged bytes; separate source pin; Git rollback; complete owner settings reconciliation and native-object preservation guide. |
| Prove actual use rather than ZIP/metadata/model claims | Two-Project owner trial requires installed identity and actual retrieval evidence; no runtime success claimed from tests. |

The selected-source integrity checks use the existing committed lock/receipts,
not a new authority ledger or global preflight. They protect the concrete failure
of emitting a different/unlocked product or shared route. Invalid local input
is cheap to repair before generating text. Added cost is confined to deliberate
opt-in maintenance and actual owner-selected native trials. The cheaper alternative,
unchanged schema 2/JIT, stays supported without new commands or gates.

## Relay distribution compatibility and external handoff

The frozen root lock selects native Relay **5.0.0**, distribution commit
`5fc55231ffc2fee2d7dd4c399e85ef1d3b091bd9`, tree
`sha256:d78711a85f07e3d09eb95d9660e1c0ca4fc4efc0dece0dadfb4f2265340c0973`.
Its [native shared route](https://github.com/jresearchsoftware/shared-governance/blob/1aabc1b1131d6d73285f84d8dc8a8dd3725135a4/vibevm/vibedeps/org.jresearch.ai.codex-relay/5.0.0/skill/references/shared-protocols.md)
uses the consuming root's selected Shared slot, **10.0.0** here, and explicitly
rejects its nested publisher closure as fallback. This is usable unchanged for
accepted-Git/JIT reading with exact repository/revision context. A filesystem
projection alone is not a cloud ChatGPT installation.

The same Relay source's [standalone delivery](https://github.com/jresearchsoftware/codex-relay/blob/0aff32a6873262185f60364463f4e97ef330de89/guidance/artifacts/standalone/codex-relay/references/shared-protocols.md)
bundles Shared **5.0.0** by design. It is structurally portable, but its immutable
policy payload cannot act as the selected version for all Projects with different
locks. A wrapper does not remove that authority difference.

| Path | Existing Relay trees usable unchanged for owner-selected architecture? | Necessary product/publisher changes |
| --- | --- | --- |
| Native manual upload/shared Skill | Native tree requires consumer-root interpretation; standalone fixes Shared 5.0.0. Neither qualifies as the common source-neutral transport. | Relay-owned thin discovery/export, target-uploader packaging qualification, reviewed release/provenance. No third manually authored policy tree. |
| Manual Skill-only Plugin / Plugin Creator | Same payload limits; a Plugin manifest alone does not fix either. | Same accepted transport plus product-owned root manifest/name/version and `skills/` layout; manual installation and readback. No app/server needed solely for guidance. |
| GitHub marketplace | Same Skill limits; existing native VibeVM distribution is not a Plugin catalog. | Same transport/wrapper plus product-owner catalog or separate explicitly owned distribution repo, accepted immutable promotion and admin-managed GitHub access/sync. |
| VibeVM source/project Codex projection | Already functional as selected Git/JIT source and local Codex delivery; not ChatGPT activation. | No change needed for fallback. A ChatGPT export must preserve source/dependency context through the product's new route, not another resolver. |
| API/local-folder route | No verified cloud Project registration bridge; filesystem paths are not a cloud contract. | No Shared implementation justified. Qualify separately if the actual client supports it. |
| No native registration | Existing native accepted Git routes work with independently selected Shared; standalone only under its separate delivery contract. | No Relay release required for this fallback; optional Project selection can be adopted after Shared source acceptance. |

**Concrete external contribution handoff, for Relay's own project context:**

- Problem: common installed discovery currently cannot be inferred to defer to
  independently bound consumer Git/lock versions. Native consumer-root paths and
  fixed standalone closure must not be treated as a common policy payload.
- Proposed smallest deliverable: Relay owns one portable transport entry that
  discovers the acting Project's explicit accepted consumer snapshot, reads its
  selected Relay Skill and Shared root-lock routes JIT, and reports missing access
  or binding without choosing latest/defaults. It contains navigation semantics,
  not copied workflow/schema/protocol authority. Qualify actual tool access and
  product source routing; no new dependency resolution.
- Package it under Relay's existing authored/generation/provenance/release route.
  Native Skill upload needs the actual UI's confirmed archive requirements. If
  choosing a Plugin, use the documented portable root `plugin.json` Agent Plugins
  1.0 manifest, owner-selected name/version/description/license/publisher metadata,
  and `skills/<transport-name>/SKILL.md` with all referenced resources. No MCP/app
  or hooks required just for distribution. A catalog is optional, not needed for
  a one-time manual trial. Manifest/schema docs are linked in the shared guide.
- Acceptance there: no embedded policy overrides, missing-binding safe behavior,
  full source/schema JIT reads, two Projects retaining different locked versions,
  identity/provenance plus actual client readback and update/fallback behavior.
  Relay decides source edits/new version and any third generated delivery artifact.
  Shared does not execute or accept that work. No external Issue/PR was created.

This is a design inference from source and supported distribution primitives,
not proof that a global transport's instructions win in every ChatGPT runtime.
Until product qualification and the owner trial succeed, **NO_CHANGE/JIT is the
functional baseline**. Native manual installation is the simplest optional next
trial after the product export exists. Marketplace automation is unnecessary for
a reasonable one-time manual action.

## Evidence, owner procedure and remaining limits

The reusable [owner guide and comparison](../../../packages/development-governance/tools/chatgpt/README.md#optional-named-skill-selection-binding-schema-3)
contains setup, scope/permissions, version pinning, refresh/removal/rollback,
unknown live objects, two-Project readback and fallback. Research checked current
official documentation on **2026-11-17**, using the openai-docs skill and a bounded
read-only helper. A second helper supplied local behavioral tests; neither helper
provides independent governance acceptance.

The currently exposed Plugin Creator contract was inspected without invoking
mutations. Creation chooses active-workspace scope when present, otherwise
personal; private visibility is not personal scope. Guarded updates require the
observed release ID, overlay omitted files, reject lower versions and bump an
unchanged version. Therefore a repeated upload is not an idempotent no-op and a
historical download is not rollback. Available metadata/file/history inspection
cannot by itself prove conversation activation. No intended live object ID or
eligible disposable workspace was supplied, and no installation/settings action
was authorized. No native install, upgrade, removal, exact-byte identity,
existing-chat refresh or two-Project runtime test was performed.

The exact native Skill ZIP nesting/limits and duplicate/version replacement rules
remain target-UI questions. Project-scoped native versions and cross-workspace
availability remain unverified. No connected Platform API was treated as ChatGPT
administration. The owner must separately select/authorize the transport artifact
and its wider installation scope, apply each accepted Project selection and supply
attributable installed/identity/use readback before claiming the architecture works.
Those conditions remain on Task 100; this source candidate needs independent
exact-result assessment, with no self-approval, publication or closure.

Small-improvement discovery found open #105 and #106. #105 concerns GitHub settings
choices; #106 concerns chat-to-Work handoff feasibility and an unresolved owner
disposition. Neither is included or implemented. Both remain with their original
Issues; this Task adds no discretionary Work handoff or client routing control.

## Local validation

Checks completed locally against the committed package candidate and contained
clean Git clone:

| Check | Result |
| --- | --- |
| `scripts/qualify.py --export-ref HEAD` | PASS: exact passive export/native projection, local links and bounded credential markers. |
| `scripts/test-chatgpt-projection.py` | 37 PASS, including eight added source-selection tests: different repositories and separate Project directories for one repository, real accepted Relay/shared slots, exported CLI, explicit selection, unchanged schema 2, no implicit Skill, dirty-source isolation, no-op mtime, upgrade/rollback and invalid selected state without partial writes. |
| `scripts/test-distribution.py` | 52 PASS. |
| `scripts/test-self-adoption.py` | 19 PASS. |
| `scripts/test-release.py` | 20 PASS; six optional one-time native publisher/resolver cases skipped by the ordinary suite. |
| `scripts/test-publication.py` | 11 PASS; one optional native publisher case skipped. |
| `scripts/test-publication-dispatch.py` | 7 PASS. |
| `scripts/package-release.py` against the frozen baseline | PASS: 10.0.0 → 10.1.0 MINOR. |
| Producer `project-chatgpt.py check` against the frozen accepted baseline | PASS: Instructions NO_OP, Sources DISABLED, live settings unverified. |
| `git diff --check` | PASS. |

Pinned VibeVM 1.0.11 was downloaded into the contained task fixture, matched the
recorded SHA-256, and generated 10.1.0 source/slot/lock/routes in isolated staging.
Its native install returned success; Relay 5.0.0 and both Landscape pins stayed
unchanged. Only known current generation outputs were transferred; historical
slots stayed intact. This is local materialization evidence, not ChatGPT activation
or a root/sudo installed-service proof. Native exact-head CI remains separate.

The launcher's temporary directory lies inside the authoring checkout, while the
existing exporter intentionally requires a destination outside its authoring root.
An isolated clean clone from a local Git bundle let unchanged tests use a sibling
temporary directory entirely inside this execution's contained workspace. The
initial direct export test refusal exercised that existing path boundary; no source
or host-permission relaxation was needed. A credential-free isolated local clone
attempt also hit Git ownership checking; archive/bundle staging avoided reliance
on that clone path without changing ownership or global Git configuration.

Source/export/fixture checks prove selection mechanics, not model compliance or UI
activation. Protocols, base and producer desired Instructions are unchanged against
the accepted baseline. Existing unknown live settings gaps remain unresolved.
The pre-existing untracked `.codex-sandbox/` is launcher-owned; only this effort's
identified isolated fixtures/downloads are removed after checks. No GitHub
credentials or mutation are used for handoff. Useful changes are committed on the
admitted Task branch for trusted Writer; publication and independent acceptance
remain separate.
