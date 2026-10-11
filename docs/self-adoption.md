# Automatic producer self-adoption

Task 22 replaces the fixed Task 6/10 proportional-controls projection and the
routes to editable package source with one automatic accepted-source selection.
This policy becomes active after independent source acceptance and owner merge.
It explicitly adopts proportional-controls, requirement-authority,
package-versioning and task-handoff for this producer. Their applicability and
all local Issue, execution, publication and review authority remain intact.
Other consumers still adopt under their own policies.

## Safe point and ordinary use

The human-owned root AGENTS route runs `python3 scripts/self-adopt.py` at the start
of work. The authoring boot routes to the same mechanism. The command fetches
canonical source main into a dedicated `refs/self-adoption/main` tracking
ref in its ignored local Git-object cache, reads the existing direct-Git distribution's version tags in a disposable
bare clone and selects the newest **first-parent source-main** revision with a
matching published package. This uses acceptance/publication order, not highest
SemVer or the distribution default branch. Proposed checkout bytes, PR branch
commits and side-branch commits inside a merge are excluded.

The existing accepted-main → successful push CI → immutable publication workflow
continues unchanged. Source merge alone cannot activate an unpublished update.
The first subsequent effort automatically selects the successful publication;
an already-running effort keeps its reported exact selection. There is no
additional owner-triggered adoption PR, post-merge source write, release ledger,
registry service, version bump, publication credential or workflow feedback loop.
An ordinary Git/Actions retry of publication at the same accepted source SHA
remains governed by [release policy](releases.md).

Selection compares the entire tag payload, including `DISTRIBUTION.json`, with
the existing deterministic export from that accepted Git commit. It binds full
source SHA, peeled release commit, version, file set and payload hashes. A tag
whose source receipt or bytes disagree is rejected; an active frozen release
whose commit changes is rejected even with identical payload. The direct
distribution and canonical source owners remain the existing trust boundary;
this does not cryptographically authenticate individual reviewers or CI.

The command materializes byte-identical passive package files into an ignored
`.vibe/accepted-governance/<source-sha>/` directory. All files are written before an atomic
`ACTIVE.json` selector replacement. It prints the absolute directory and exact
identity; read only relevant adopted protocols from that directory. The selector
is disposable local materialization, not an external status record. Hash checks
are automatic output of the existing exporter, not a reviewer transport ritual.
Git branches, the index, package source, global tool configuration and the
project Git database/user refs are preserved. The helper writes only its ignored
`.vibe/accepted-governance` cache, outside protected `.agents` instructions.
Public guidance inherits the workspace ACL; no host or existing ACL is repaired. Namespaced release refs retain verified Git publication objects
for offline provenance checks. No VibeVM executable is needed for ordinary work.

## Failure, repeat and rollback

- A new accepted version that has not yet published retains the latest eligible
  publication with a visible warning. Interrupted/failed publication cannot
  activate partial content.
- Network/registry failure, missing Git/tool support or invalid update payload
  retains the last verified projection and reports failure. Retry the same
  command after recovery; no owner approval is required for a previously accepted
  publication. If Python cannot run, use the last reported directory only when
  its verified identity is available; otherwise preserve work and recover.
- Without a cache, the committed [bootstrap pin](../.agents/self-adoption.json)
  reproduces accepted published `1.2.0` from source Git blobs. Normal full clones
  include these objects. A shallow clone missing the bootstrap history must
  obtain canonical source history before starting governed work; it cannot infer
  acceptance from checkout bytes. `--offline` uses this bootstrap or a verified
  retained projection, without network.
- Repeated selection and source-only changes leave the selector bytes untouched.
  A new major is eligible under this producer's explicitly adopted accepted-merge
  authority if the passive supported package shape and four adopted routes remain
  valid. An incompatible export/unknown capability fails visibly and retains the
  previous guidance. Added topics are not automatically adopted.
- `python3 scripts/self-adopt.py --rollback` selects the previous verified local
  projection. Use `--offline` for the current effort to retain that temporary
  rollback; the next ordinary refresh intentionally retries the latest eligible
  accepted publication. Permanent policy rollback is an independently reviewed
  source correction with a new immutable package version, never a moved old tag.
- Corrupt active bytes or a forged candidate selector are rejected. If no verified
  active guidance can be established, stop at that concrete boundary and preserve
  work. No cleanup, forced ref update or protected capability repair is automatic.

## Coverage and historical provenance

The bootstrap selects `73798b919efbd0d8b0ee1317bf84a6c48d7e99d1`, accepted source
after PR 21, published as `1.2.0`, with payload SHA-256
`23d2f2ea4b28c5aafb17007d5e875b78f4b472c36d89fd66a1549e79070d0349`.
It includes the full proportional-controls wrapper/procedure, attribution,
free-hardening exception and Task 19 authority/friction corrections; the
requirement-authority addition; adopted package-versioning; and complete
task-handoff with the [manual client binding](manual-task-handoff.md).
Root AGENTS owns the explicit conditional topic selection. Local producer release
cadence, Issue authority, Step allocation and Codex navigation remain local.
The binding supplies implementation details without repeating generic handoff
obligations or creating a second Task charter.

The obsolete historical active file/receipt are removed together with their
routes. Their original source, transformation and hashes remain reproducible
through `scripts/project-protocol.py`, the frozen `0.1.0` package, accepted Git
history and dated [Task 10 evidence](task-10/step-1/README.md). No frozen release
or historical report is rewritten. The new projection preserves every package
byte rather than selectively extracting paragraphs. The
[Task 22 evidence](task-22/step-1/README.md) compares the supported alternatives,
tests the boundary/recovery and separates CLI evidence from model traversal.
