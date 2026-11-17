# Source-controlled ChatGPT Instructions

These optional maintenance assets share the package's whole version. They are
ordinary files in the VibeVM materialized slot, with no boot hook, dependency,
native Skill or executable capability declaration. Installing this package
does not run Python, adopt a topic or change ChatGPT settings. Python 3.11+ and
Git are used only for deliberate maintenance; ordinary chats read accepted files.

The producer owns [base.md](base.md) and [project.py](project.py). Each consumer
owns one directory (for example `chatgpt/`) containing reviewed `binding.json`
and human-editable `custom.md`. The same tool combines them into canonical
generated `instructions.md` in that directory. Optional
`sources.md` and `sources-manifest.json` share the same selection/update path.
Commit source/custom/generated changes together in the consumer's normal review.
Never edit generic code per project, edit generated text as policy, or keep
the canonical desired Instructions only in a transient bundle.

## One distribution and maintenance route

Under the consumer's own authority, deliberately update its existing VibeVM
requirement/lock to an accepted published package version, then use normal
`vibe update` / `vibe install` and review the materialization. For a direct Git
requirement the existing distribution repository is
`https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git`;
select the reviewed version/tag through the consumer's established manifest.
VibeVM owns resolution, direct/transitive closure, lock and file transport.
Do not assume a proposed producer version is published or accepted.

From the consumer root, invoke the version selected in its native lock, e.g.
`python vibevm/vibedeps/org.jresearch.ai.development-governance/2.3.0/tools/chatgpt/project.py`.
The path is an illustrative versioned slot, not a separate resolver. Append:

```text
check --repository . --binding chatgpt/binding.json --accepted-sha <independently-accepted-full-SHA> --authority-anchor <current-owner-or-review-URL>
```

Use `update` instead of `check` for an intentional local write. Both report exact
Instructions/cache diffs and effective `CHANGED`/`NO_OP` (status schema 4).
Check is read-only: exit 0 is current, 1 is stale/missing generated output or
cache pending removal, 2 is invalid/unavailable input. It can be opted into
consumer CI; this package imposes no universal gate.
Update validates local paths before writing and regenerates changed outputs,
including manually edited generated files. Review useful edits through custom
Markdown and ordinary Git review. Disabling cache removes only `sources.md` and
`sources-manifest.json` in the binding directory, including locally edited copies.
Unchanged bytes are not rewritten. No ownership registry or clean-worktree gate
is involved; no recursive cleanup is performed.

Binding schema 2 remains supported unchanged and has exactly these fields:

| Field | Meaning |
| --- | --- |
| `schema` | `2` (unsupported formats fail explicitly). |
| `repository`, `navigation_ref` | Project identity and stable discovery branch such as `main`; navigation never proves acceptance. |
| `mode`, `role`, `permissions` | `orchestration-review` or `read-only-preview`, human-readable ChatGPT role and capability names. Preview permits only `discussion`/`assessment`; names grant no authority. Other supported names: `orchestration`, `authorized-publication`, `authorized-integration`, `authorized-continuation`. |
| `native` | `materialized` consumes existing INDEX/lock/slots; `absent` refuses to hide existing native state. |
| `local_sources` | Additional accepted project/product/specialist entry paths; no inline generic policy. |
| `character_budget` | Positive Unicode code-point budget, at most 8000; output must be strictly below it. Oversize fails without clipping. This is an owner-bound budget, not universal UI qualification. |
| `cache_enabled`, `cache_selection` | Explicit boolean and unique accepted repository paths. Disabled is the default choice; enabled needs a nonempty selection. |

`custom.md` is ordinary reviewed Markdown, not opaque JSON prose. Keep local
language, role, permissions, client limits and necessary workflow routing here;
reference full accepted policy instead of copying rule lists. The common base
does not impose Task, Outcome, BLOCKED, Deliberative or review procedures on a
non-adopting project. Presence of package/INDEX adopts nothing. Free text still
needs semantic review; this tool cannot enforce model behavior or authenticate
the authority of arbitrary custom text.

## Accepted source, changes and no-op

Before maintenance independently establish repository identity, source acceptance
and exact revision using current project authority and Git facts. Supply the
SHA and evidence URL explicitly. The tool reads committed blobs at that SHA,
ignoring dirty candidate guidance. `--source-repository` optionally identifies a
separate read-only Git object store; the default is `--repository`. A matching
object/URL proves consistency, not repository provenance or owner acceptance.
There is no fetch, authority oracle or latest-version lookup.

The generated Instructions use stable discovery links such as `main`; each effort
establishes/freeze its independently accepted exact revision. That SHA is an
invocation/provenance anchor, never the containing commit of the generated file.
Git records reviewed generator version, binding/custom inputs and output together;
record exact invocation/source/authority evidence in the normal Task/PR as needed.
The projector still validates committed native inputs at the explicit accepted SHA,
even if the effective output is unchanged. Candidate guidance cannot accept itself.

There is no ChatGPT projection receipt. When adopting this interface from an
older version, remove the consumer's tracked `chatgpt/receipt.json` in its normal
adoption PR. The tool does not read, migrate, generate or delete legacy receipts.
Status schema 4 removes `maintenance_evidence` as well as the former
`source_changes` inventory. Git and normal invocation/review evidence own
provenance; native VibeVM `.vibe-slot.toml` receipts remain a separate contract.
A substantive dependency upgrade is validated/regenerated in the same normal PR;
if Instructions remain identical, no settings action follows merely because
routes or main advanced. No circular self-pin or recurring metadata commit is needed.

Regenerate/check after effective base, custom, binding, relevant accepted guidance
or materialization changes and review the output in the same normal PR. A pinned
new generator plus accepted-source validation can qualify unchanged output. Active
efforts retain their frozen authority; Git preserves historical provenance. An
explicitly enabled cache remains a versioned exact-source snapshot and changes
when its selected snapshot/identity changes; it is optional, not a closure gate.
Do not poll each message or add periodic live checks. Unchanged bytes are not rewritten.

Native support is bounded to INDEX schema 1, lock schema 7 and slot receipt
schema 1. Each INDEX path inside a materialized locked slot must be declared
by that exact slot's receipt, with the existing lock identity, ordinary committed
file and hash checks. This does not require receipts to list unreferenced extra
files throughout the slot. Original order/conditions remain unevaluated; OS/package predicates
do not choose client roles or topic adoption. Missing indexed files fail
maintenance even if condition applicability is unknown. Use VibeVM to resolve
unsupported formats; this tool neither solves ranges/edges nor installs files.

## Owner-controlled settings and optional Sources

Generated raw `instructions.md` is complete desired text, including its generated
marker, not a UI installation receipt. For projects intentionally using generated
Project Instructions and adopting TH-029, a task changing the complete effective
text includes live reconciliation even without an explicit application clause.
Generate/validate the desired text in the ordinary reviewable change. After
acceptance/integration, compare accepted full text with supported live evidence.
If different or unconfirmed current, present the **entire raw Markdown replacement**
in one complete copyable `markdown` fence, without clipping, a patch or fragments.
The owner manually reviews/applies it, preserving/reconciling unknown live rules.
Obtain supported readback or sufficiently attributable owner-confirmed live content
before claiming a match or closing the task. Inaccessible live Settings or uncertain
confirmation remains an evidence gap and completion hold, including after merge.
An owner export alone proves the comparison, not UI currentness.

Unchanged effective text, cache-only, dependency/binding changes with identical
output and SHA-only changes create no new application or receipt upkeep duty.
Retain earlier unresolved mismatches/verification gaps; a later generation NO_OP
does not discharge an earlier changed-text obligation. The CLI's `application`
field explains these boundaries; it cannot identify whole-task change history,
determine topic adoption, verify live Settings or judge closure. `live_settings_verified`
remains false, including after an exact owner-export comparison. Once accepted
integration, required reconciliation and other real obligations are verified,
already-authorized closure needs no further discretionary owner prompt. No automatic
Settings write, daemon, external verification service or new approval loop is added.
Another project's release does not adopt or apply anything for this consumer.
On demand:

```text
compare --repository . --binding chatgpt/binding.json --live-export <owner-export.md> --live-format raw
```

`fenced` accepts one complete `markdown` fence instead. Comparison is exact and
read-only, including whitespace; it reports diff/no-op and owner-export provenance,
never verified UI currentness. No actual field is read or mutated. A returned
replacement is full raw Markdown in one fence, not a patch or fragment.

Optional Sources use explicitly selected exact Git/materialized files, canonical
links and hashes. The owner may separately upload identified snapshots and
verify addressability/currentness through supported surfaces. No automatic
upload, enumeration, sync or cache requirement exists. Missing caches do not
block canonical GitHub reads. Without required live evidence, qualify analysis
and stop dependent actions. Static text/CLI tests prove no ChatGPT compliance,
freshness, role enforcement, Source access or live-settings application.


## Optional named Skill selection (binding schema 3)

Opt in only under the consumer's own accepted authority. Schema 3 retains every
schema-2 field and adds exactly one `skill_selection` object. Existing schema-2
bindings and generated Instructions are unchanged. This selects **source routes**,
not an installed ChatGPT Skill version. One shared transport Skill can be used
across Projects while each Project keeps its own accepted consumer snapshot and
root lock. Project-only native Skill version installation is unverified.

For example, add the following object and change `schema` to `3` in an otherwise
complete binding. This real source example identifies the Task 100 research
baseline; it is not an instruction to adopt it in another consumer:

```json
"skill_selection": {
  "accepted_sha": "1aabc1b1131d6d73285f84d8dc8a8dd3725135a4",
  "authority_anchor": "https://github.com/jresearchsoftware/shared-governance/issues/100#issuecomment-6940639935",
  "skills": [{
    "name": "codex-relay",
    "entry": "vibevm/vibedeps/org.jresearch.ai.codex-relay/5.0.0/skill/SKILL.md",
    "shared": ["vibevm/vibedeps/org.jresearch.ai.development-governance/10.0.0/vibevm/vibespecs/boot/development-governance.md"]
  }]
}
```

Use the existing `check`/`update` commands. `--accepted-sha` still validates the
maintenance effort's independently established source; `skill_selection.accepted_sha`
is the separate, deliberately frozen consumer snapshot for the named sources.
Both live in the supplied Git object store; neither is inferred from current HEAD,
main, a generated file or a Plugin's version. Independently verify repository
provenance and acceptance for both. The tool checks consistency, not authority.
The selected snapshot must contain AGENTS, native INDEX/schema-7 lock and intact
slot receipts. Each entry/shared route must be receipt-listed in a locked slot;
the Skill name/entry must match that package's native `[[skill]]` declaration.
`shared` identifies the explicitly selected shared entry routes, not duplicate
policy or a new adoption list. Read their applicable complete protocols normally.
This uses VibeVM's existing selection; it does not interpret requirements, resolve
closure, install files or automatically select every declared Skill.

The output identifies the consumer SHA, exact Skill/shared links and locked
package versions/content hashes. Follow lock source refs and package provenance
for upstream identities; local registry paths are transport metadata. The
project's source acceptance/adoption remains independently owned. Selection is
stable when maintenance HEAD advances: no containing-commit self-pin or recurring
SHA-only update is needed. On an accepted product/shared upgrade, deliberately
change this selection to the accepted consumer snapshot and matching routes,
regenerate and review the complete diff. Rollback restores the previously
accepted binding/custom/output through ordinary Git, preserving any stronger
current authority and unresolved live application gap. Retain old Git objects.
Unchanged inputs do not rewrite files or require reinstalling a common Skill.

A changed opt-in block counts as effective Instructions text under the existing
TH-029 application procedure above. If it exceeds the owner's budget, revise
reviewable custom text/routing within authority; never clip or raise the 8000
ceiling. No automatic opt-in or reduction of existing custom rules occurs.
Separate binding directories can serve separate Projects, including Projects
using different snapshots of one repository. The owner must reconcile each
complete desired text with that specific live Project; a repository name alone
does not authenticate which ChatGPT Project is active.

## Native discovery and owner-controlled distribution

Keep four states separate: accepted Git `SKILL.md` reading; VibeVM's native Codex
`.agents/skills` projection; a Skill actually installed/discoverable in ChatGPT;
and Project Instructions/optional Sources. None proves another. Missing, stale,
unavailable or ambiguous native registration leaves accepted-Git/JIT reading
usable. Disclose the discovery limitation and continue unrelated work; stop only
operations lacking their required evidence, authority or capability. Do not turn
installation into a mandatory per-chat preflight or poll each message.

The simplest current path is this project-side binding plus JIT fallback. A
**separately accepted product-owned transport export** can add optional native
discovery later. It should only route to the acting Project's explicit selection,
without embedded product/shared policy overriding that selection, dependency
resolution, guessed local disk paths or a default project. Shared Governance
supplies no Relay product Skill or Plugin in this package. Relay owns that export,
its identity, license, compatibility, review and release; consumers own adoption.
A wrapper around an incompatible payload does not make it portable.

Documented alternatives, checked 2026-11-17; availability is not live proof:

| Path | Scope, owner setup and permissions | Pinning, maintenance and cost |
| --- | --- | --- |
| Native Skill upload/shared Skill | Eligible workspace user uses the Skills page, subject to role controls and scanning; wider than a Project. Review access and installation scope first. | Keep accepted artifact/hash and attributable client identity. Exact archive/update/rollback behavior needs target-UI qualification. Lowest optional distribution overhead. |
| Manual Skill-only Plugin / Plugin Creator | A Plugin can carry Skills without an app. Owner separately authorizes private creation/upload and installation in the intended personal/workspace scope. It is a distinct product object. | Root `plugin.json` plus `skills/<name>/SKILL.md` and resources; product publisher owns versioned wrapper and payload. More packaging work; no new service required. |
| GitHub workspace marketplace | Workspace admin imports a catalog with GitHub read authorization; workspace policy controls availability. This is not Project-local registration. | Select an accepted immutable commit for deliberate promotion; a moving branch can sync future entries. Catalog/sync administration adds ongoing cost. |
| VibeVM / standalone source | Consumer chooses reviewed package/lock and materialization; Codex projection remains local to Codex. | Trusted export input, not a ChatGPT installer. Native consumer-root routes need a qualified portable delivery; standalone bundled closure may differ. |
| Platform API / local-folder client | Platform credentials and local client configuration belong to their separate owners. | No verified bridge to cloud Project installation. Do not create an API key, disk-path bridge or sync service for this bootstrap. |
| No native registration | Owner maintains Project Instructions and optional Sources through the established procedure. | Exact accepted Git/locked JIT remains functional; no new install credentials or native version maintenance. |

### Manual owner trial and readback

This procedure is for a later explicitly authorized trial, not permission to run
it. Check the intended account/workspace and client surface, allowed upload/use/
share/install roles, existing same-name Skills/Plugins, and actual access scope.
Preserve unknown installed objects and live Instructions. Obtain explicit consent
for scope beyond one Project; common ownership does not prove account-wide or
cross-workspace availability.

1. Select the accepted **transport** artifact from its product owner. Record its
   source commit/version, complete file list, provenance, archive hash, publisher
   and intended access separately from each Project's Relay/shared selections.
   Do not upload the native Codex projection as if its filesystem routes worked
   in ChatGPT. Native Skill archive requirements must be confirmed in the target
   uploader; a generic ZIP candidate alone is not importer qualification.
2. If native upload is exposed, open Plugins → Skills → Create → Upload from your
   computer, or install the explicitly selected shared Skill. Review scan results
   and any Needs Review/Blocked disposition under workspace policy. Read back its
   actual name, owner, access and Installed state. This is a workspace Skill flow,
   not a project-only version selector. [Native Skill controls and upload](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).
3. Alternatively, if a reviewed Skill-only Plugin is chosen, use the supported
   Plugin ZIP upload flow (workspace admin: Admin console → Plugins → Add → Upload
   plugin), inspect its included Skills/apps, then complete installation where
   prompted. No app is needed for instruction-only packaging; GitHub access still
   needs its existing supported connection. Manual uploads expose Upload new
   version to eligible editors; source-managed Plugins update from their source.
   Do not create a second object to bypass policy. [Plugin operations](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).
4. After accepted source integration, apply each Project's complete Instructions
   under TH-029, preserving unknown rules, and obtain attributable live text
   confirmation. In fresh chats in two opted-in Projects with different accepted
   locks, select the same installed Skill/Plugin through the client's actual
   selector when offered. Ask it to identify the acting Project, consumer commit,
   selected Relay/shared entries and fetch a relevant complete read-only reference.
   Inspect actual retrieval/tool evidence and exact paths; no lifecycle mutation
   is needed. Then repeat without native selection to exercise JIT fallback.
5. Keep attributable UI/owner readback, transport identity and any available
   downloaded-file comparison with the trial evidence, date and target Projects.
   Record what each client really exposes; an absent selector/version/file readback
   is an explicit evidence gap. Model self-report, source hashes, an Installed row
   alone or generation success cannot establish project isolation or actual use.
   Do not claim existing-chat refresh from a fresh-chat test. [Plugin session guidance](https://learn.chatgpt.com/docs/plugins).

For update/removal, use only controls offered to the authorized owner on that
surface. Compare unchanged payloads before uploading; generation NO_OP is not
live readback and does not justify a new native release. Preserve the known-good
archive and previous Project selections. A retrieved historical release is not
a restored installation; lower-version replacement, duplicate handling, native
Skill uninstall/rollback and installed byte identity remain unqualified until
observed. If replacement/removal cannot be safely qualified, retain or disable
only the owner's identified object through supported controls, disclose the gap
and use accepted-source fallback. Never delete unrelated Skills or rewrite a
frozen release. Recheck the two-Project read-only behavior after a transport update;
changing one Project's product selection should not require a transport update.

For a deliberately chosen GitHub marketplace, the admin imports the repository
and root path at an accepted commit, reviews per-entry results and workspace
availability. The catalog belongs at `.agents/plugins/marketplace.json`; a local
entry points to a Plugin directory, while cross-repository entries support exact
SHAs. Sync now and daily synchronization are documented; invalid updates retain
the last working copy. Removing a catalog entry can leave a workspace copy;
deleting the marketplace deletes its imported Plugins. Inspect the actual result,
not just a green sync summary. A pinned catalog commit must be deliberately
promoted; do not assume a one-click rollback or project-level versions. [GitHub import lifecycle](https://learn.chatgpt.com/docs/enterprise/plugin-management).

A portable Plugin uses root `plugin.json` with the Agent Plugins manifest schema,
name and owner-selected release metadata, plus complete `skills/` contents;
`.codex-plugin/plugin.json` is a documented compatibility layout. No MCP server,
app, hook, marketplace or public submission is necessary just to package a Skill.
Public directory publication is another explicit publisher-owned operation.
[Portable packaging](https://developers.openai.com/plugins/build/plugins).
[Workspace versus filesystem Skill ownership](https://learn.chatgpt.com/docs/enterprise/skills).
[Separate Platform Skills API](https://developers.openai.com/api/docs/guides/tools-skills).

This source change tests local selection/generation only. It establishes no
ChatGPT eligibility, importer acceptance, native activation, refresh, rollback,
installed bytes, runtime policy compliance or live settings synchronization.
