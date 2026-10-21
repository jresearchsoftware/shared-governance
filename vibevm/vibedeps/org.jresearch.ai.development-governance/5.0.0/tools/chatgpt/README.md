# Source-controlled ChatGPT Instructions

These optional maintenance assets share the package's whole version. They are
ordinary files in the VibeVM materialized slot, with no boot hook, dependency,
native Skill or executable capability declaration. Installing this package
does not run Python, adopt a topic or change ChatGPT settings. Python 3.11+ and
Git are used only for deliberate maintenance; ordinary chats read accepted files.

The producer owns [base.md](base.md) and [project.py](project.py). Each consumer
owns one directory (for example `chatgpt/`) containing reviewed `binding.json`
and human-editable `custom.md`. The same tool combines them into canonical
generated `instructions.md` and `receipt.json` in that directory. Optional
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
Instructions/cache diffs, effective `CHANGED`/`NO_OP`, and
ownership-receipt changes separately (status schema 3; no `source_changes`). Check is read-only: exit 0 is current,
1 is stale/missing generated output or receipt, 2 is invalid/unavailable input.
It can be opted into consumer CI; this package imposes no universal gate.
Update validates the complete plan before writing. Existing generated files
must match the previous receipt; unknown or manually changed files are preserved
with an error. Reconcile useful edits into custom Markdown and recover the old
generated file from the project's ordinary Git history before regeneration.
Only verified previously owned cache files are removed when disabling cache.
There is no force/overwrite-unknown switch or recursive cleanup.

Binding schema 2 has exactly these fields:

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

Receipt schema 3 retains only `schema`, `generator`, `repository` and generated
`artifacts` hashes. This has one concrete purpose beyond Git: prevent `update`
from silently overwriting valuable local generated-file edits (or deleting a
modified cache on disable). It is not an acceptance record, source inventory or
live-settings receipt. A schema-2 receipt is read for the same ownership check and
replaced once during an intentional update, preserving unknown/modified files.
No source/tool/version/SHA metadata refresh is required when output is unchanged.
A substantive dependency upgrade is validated/regenerated in the same normal PR;
if Instructions remain identical, no receipt or settings action follows merely
because routes or main advanced. No stale historical source inventory survives
in schema 3 and no circular self-pin or recurring receipt-only commit is needed.

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
marker, not a UI installation receipt. The owner reviews and manually applies
and reads back changed text, preserving unknown live rules. When the Task includes
application, compare the accepted desired text with supported live evidence, surface
the **complete** replacement for manual application if different, and obtain
supported confirmation/readback before claiming application or Task closure.
Disclose unavailable live reads or uncertain confirmation; a supplied export alone
proves comparison, not UI currentness. If effective text is unchanged and no known
application gap remains, no manual settings action is needed. Generation-only
Tasks acquire no settings-application obligation. On demand:

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
