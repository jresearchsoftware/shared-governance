# ChatGPT bootstrap projection (prototype, schema 1)

One [template](../templates/chatgpt-bootstrap.md) and one standard-library
[projector](../scripts/project-chatgpt.py) serve every binding. This is proposed
Task 32 tooling outside the governance package, not an adopted protocol or a live
settings synchronizer. Python 3.11+ and Git are maintenance tools; ordinary
ChatGPT conversations require neither executable.

The client starts with the accepted project AGENTS, follows its boot and local
routes and reads applicable adopted detail JIT. The template contains no topic,
package version, slot coordinate, consumer identity or Task-specific Decision.
Changing protocol names/counts/versions changes input data and receipts, never
common logic. OS/installed-package routing does not establish a ChatGPT role.

## Inputs and independent authority

Supply a local Git object store and a reviewed JSON binding. Fetch missing exact
objects through ordinary authorized Git separately; the projector never fetches,
installs, resolves dependencies, reads credentials or contacts a settings API.
Objects from another repository may reside in this store for read-only examples.

Establish repository identity, acceptance and the exact SHA from current owning
project Decisions/review and Git facts **before** invoking the tool. Pass that SHA
and authority URL separately as `--accepted-sha` and `--authority-anchor`.
The tool rejects a mismatching binding or moving ref, then reads only committed
blobs at that SHA, ignoring candidate checkout changes. Matching inputs and an
existing commit prove consistency, **not** independence, repository provenance
or acceptance. The tool cannot authenticate an owner Decision or detect two
matching fraudulent inputs. Keep external acceptance evidence in the existing
Task/PR. Do not make this schema a new authority registry.

Binding schema 1 has these data fields:

| Field | Meaning |
| --- | --- |
| `repository`, `accepted_sha`, `authority_anchor` | Owning repository and independently established source binding. |
| `mode`, `role`, `permissions` | ChatGPT client role. `orchestration-review` supports authorized lifecycle orchestration; `read-only-preview` permits discussion/assessment only. Capability names never grant permission. |
| `overlay` | Irreducible language, owner permissions and client-specific instructions. Reference canonical policy instead of duplicating it. Free text needs semantic review; the tool cannot certify its authority. |
| `native` | `materialized` consumes committed INDEX/lock/slots; `absent` supports projects without them and refuses to hide existing native state. |
| `local_sources` | Exact-revision local/product/specialist entry points that AGENTS alone cannot safely supply for this client. |
| `client_limits` | Genuine unsupported/unknown client surfaces, without inventing restrictive production policy. |
| `character_budget` | Owner-bound Unicode code-point budget, at most 8,000 for this prototype. Not an assertion about every platform's limit. Oversize text fails; nothing is clipped. |
| `cache_selection` | Optional explicitly reviewed repository paths, empty by default. Their absence does not block projection when cache export is disabled. |

The first-consumer and historical read-only bindings are in
[Step 4](task-32/step-4/README.md). They use identical common code/template.
Consumer migration and topic adoption remain project-owned.

## Reproduce and review

The same interface is used for every consumer (substitute independently checked
values, not moving branch names):

```text
python scripts/project-chatgpt.py --repository <object-store> --binding <binding.json> --accepted-sha <40-character-SHA> --authority-anchor <owner-acceptance-URL> --baseline-kind <assumed-empty|candidate|owner-export> --output <new-review-directory>
```

With `candidate` or `owner-export`, also pass `--baseline <complete-export.md>`.
The baseline contains the complete Instructions in exactly one `markdown` fence.
`assumed-empty` takes no baseline: its diff is an **unverified proposal against
assumed empty settings**, not a live delta. `owner-export` records the owner's
export provenance; the projector still cannot verify UI currentness/readback.
Unknown live rules must be reconciled before replacement.

Outputs are complete fenced `instructions.md`, `receipt.json`, `settings.diff`
(only actual inner settings text, without transport fences) and `maintenance.json`.
No-op is explicit. The new output directory must not exist; existing files are
preserved. Compare and intentionally reconcile task-owned artifacts after review.
There is no apply/upload/approve/merge action.

The receipt records source hashes and original ordered native entries/conditions,
not an adopted topic list or permission decision. During deliberate maintenance,
the projector consumes INDEX schema 1, lock schema 7 and slot-receipt schema 1
from the pinned native layout. It compares the materializer's recorded source
identity and per-file hashes and requires indexed slots to be locked. It never
solves ranges/edges, selects versions or claims fresh VibeVM runtime qualification.
Use accepted VibeVM tooling for resolution or unsupported materialization formats.
An unavailable indexed source is a concrete projection gap, including a conditional
route whose materialization is unavailable; this does not declare that condition
true. Conditions are preserved unevaluated, for accepted client/JIT interpretation.

## Maintenance and exact settings changes

Run after an independently accepted relevant source/lock/route/overlay/template
change or observed defect, not every message. Keep the old accepted binding for
an active effort. A new effort/reprojection needs a current independently checked
binding; changed main alone is insufficient.

Pass `--previous-receipt <receipt.json>` to report added/removed/changed source
paths separately from the exact Instructions diff. This covers materialized
direct/transitive files without copying policy into Instructions. A changed
payload can require JIT/source-cache attention without a new common algorithm.
With unchanged inputs/output, `settings_text: NO_OP` means no re-paste. A new
Outcome or Task with unchanged accepted settings also requires no re-paste.

This prototype deliberately uses an **immutable pin** for auditable acceptance.
Updating that pin changes actual Instructions even if AGENTS content is identical;
the diff honestly requests a reviewed owner update. It does not claim the no-op
benefit of a stable moving navigation URL. Retaining the old pin indefinitely is
not automatic source currency. A future accepted dynamic selection contract could
change this tradeoff; no such resolver/service is implemented here.

## Optional Sources: one selection/export method

Leave `cache_selection` empty and omit `--cache` unless a small snapshot adds
value. With an explicit selection, `--cache` produces schema-1
`sources-manifest.json` and one human-reviewable `sources.md` with exact canonical
links and selected bytes. No full governance export, dependency resolver, binary
download, upload API or mandatory cache is added. The historical Relay preview
demonstrates two small routing files; it is not a migration recommendation.

Review the exact selected content, manifest and old/new cache diff. The owner may
upload the snapshot through a supported UI and check whether the client can
actually address it; replace/remove only the identified old snapshot after
reconciling unrelated Sources. On accepted selection/revision/content change,
compare manifests and snapshots and hand off only actual cache changes. With no
cache change, upload nothing. Missing/stale/unsupported Sources fall back to
canonical GitHub reads; unavailable GitHub permits qualified read-only discussion
and stops unknown-head review/admission/protected actions. Upload, complete UI
enumeration, retrieval reliability, freshness and activation remain unqualified
until observed by the owner. This manifest is a cache receipt, never authority.

The fetched official [Projects and chats](https://learn.chatgpt.com/docs/projects?surface=app)
documentation describes project instructions and shared uploaded/connected
context. It does not establish this account's field readback, a complete Sources
API, automatic repository synchronization or model compliance. Those are distinct
integration claims and remain unverified here.

## Qualification limits

`python scripts/test-chatgpt-projection.py -v` exercises real Git blobs and CLI
failures in disposable synthetic repositories plus exact first-consumer output.
The [Step 4 evidence](task-32/step-4/evidence/validation.md) distinguishes these
checks, real accepted consumer projections, primary CI and unavailable runtime
behavior. Prompt text and refused CLI flags prove no model-level access enforcement.
Independent substantive review and owner-applied/read-back ongoing dogfooding
remain necessary before claiming acceptance or live activation.
