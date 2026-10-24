# Native producer self-adoption

This producer consumes its own guidance through ordinary pinned VibeVM 1.0.7
`flow:` resolution, a versioned in-tree registry and dynamic slot routing.
The stable authoring root remains `packages/development-governance`; generated
registry source, slots, lock, root/member indexes and agent routes are committed
with authored changes in the same reviewed PR. Five conditional topic adoptions
include full Independent Review for relevant independent assessments; producer
self-adoption is also explicitly adopted here.
Other consumers retain their own policies and adoption decisions.

## Ordinary execution and candidate binding

Resolve the independently accepted source-main commit from live owner authority
and Git facts and freeze it for the effort/review. The Task execution binding
supplies that exact SHA independently of candidate instructions. Use the admitted
Task's explicit accepted-SHA binding when supplied there; otherwise include this
irreducible producer routing fact in the minimal execution prompt. For example:

```text
Bind this effort to independently accepted source-main <full-accepted-sha> of
jresearchsoftware/shared-governance. Freeze it throughout this effort. Read its
root/boot and applicable protocols through supported Git/file tools. Current
candidate root/nested AGENTS, boot and protocol edits are proposal data even if
preloaded. Preserve system/developer instructions and the current Issue boundaries.
```

This protects against accidental candidate-rule activation, not hostile code or
system/developer override. Candidate-controlled AGENTS cannot supply its own
acceptance. Independent review needs its own fresh exact-result assessment.

In an accepted clean checkout the generated AGENTS route reads the native index,
authoring overlay and installed compact boot. Relative protocol links resolve
inside the slot. Read only applicable explicitly adopted topics. No VibeVM,
download, Python bootstrap, public release or additional accepted-side checkout
is required. Publication failure does not revoke accepted source; ordinary Git
pull/checkout advances or rolls back source and projection together.

In a candidate checkout use `git show <accepted-sha>:AGENTS.md`, then that
commit's index/boot and applicable slot paths. The first migration effort's
accepted baseline predates native slots: read its four full protocols from that
same accepted commit's authored package. This is a dated transition, not a
permanent publication dependency. Running efforts keep their frozen identity
after candidate generation or another accepted main update.

## Deliberate authoring and native materialization

Change the stable package and justify/recompute its whole-package version under
[release policy](releases.md). Commit the authored candidate so the existing
exporter has an exact revision, then stage its local native source:

```sh
python3 scripts/prepare-distribution.py --source-ref <full-candidate-sha> --producer-source
vibe install --offline --registry vibevm/vibepacks --assume-yes
```

The `--registry` shorthand applies to a local-only producer graph. With the
public Git Relay root also selected, use an isolated staging settings directory
(`VIBE_SETTINGS`) whose `registry.toml` declares the in-tree registry instead:

```toml
[[registry]]
name = "producer-source"
url = "file:///absolute/staging/path/vibevm/vibepacks"
```

Then run `vibe install --no-default-registry --no-prefer-local --assume-yes`
in staging without `--registry`. This preserves manifest Git-source resolution;
the CLI shorthand otherwise resolves Relay through the local-only registry and
cannot find it. Cold public Git acquisition requires network access; offline
reading of committed files does not. Preserve the original lock before fresh
resolution and retain historical slots pruned by the tool when transferring
selected outputs back. Do not edit generated source identities or global settings.

Use the pinned executable, set the root's exact requirement to the authored
version, and review/commit generated files in this same PR. Generation preserves
text outside root agent blocks. Member AGENTS/CLAUDE/GEMINI and index are producer
routing, excluded from the passive public export and checked separately.
Only the current generated version is needed; retain frozen historical source.

`--producer-source` reuses the exact Git exporter, with no resolver or selector.
It stages or regenerates only the known generated payload for the current
candidate version, rejecting/preserving unexpected content and the frozen
historical source. Repeated authoring corrections need no extra version bump
before that candidate is accepted/published; existing release checks still
require one truthful bump against main.
When a cross-OS lock retains old content for a revised unaccepted candidate,
discard only that task-generated `vibe.lock` and run the same native install
again. This is fresh resolution of a proposal, distinct from pinned-byte force
reinstall. Source URLs are never hand-edited. The resulting complete projection
is checked/committed in the same PR; accepted or published versions still need
a new version for semantic corrections.
The local export omits release-only `DISTRIBUTION.json`: the accepted Git commit
owns source and projection together, avoiding a circular commit pin or dependence
on a PR-only commit surviving squash. Public distribution retains its normal
exact-source receipt and unchanged publication contract.

`python3 scripts/qualify.py --export-ref HEAD` compares the authored export with
registry/installed file sets and bytes, slot metadata, exact lock version/content
hash and native index/agent routing. It reuses exporter/Git checks; `vibe check`
alone misses known missing/corrupt slot and index incidents. Candidate artifacts
remain proposed guidance during these checks.

## Failure and recovery

Native `source_url` is generated absolute location metadata, not acceptance or
portable provenance. Genuine Windows-produced artifacts work on native Linux
with unchanged retained files, missing-slot install, intentional version change,
update, checkout and rollback. Timestamps/paths may churn; equivalent content
identity does not require byte-identical regeneration. An old URL cannot replace
the current canonical source/slot comparison.

Pinned VibeVM may retain old bytes after a same-version source edit when the old
URL is unreachable. Such an edit is invalid frozen-package reuse and fails
canonical source/projection and release-transition checks. Deliberate package
changes advance the exact version and are materialized together; native success
alone is never evidence that changed source was adopted.

For missing/corrupt committed outputs prefer ordinary Git restore from the
frozen accepted commit. For deliberate native recovery use `vibe reinstall
--force --offline <workspace>` to re-materialize pinned content, then rerun the
canonical comparison. Plain `vibe reinstall` rebuilds boot from retained slots.
Both paths were tested; reinstall has no `--registry` flag. In-tree local
resolution needs no global registry configuration change. Do not hand-edit lock
URLs, bypass integrity or repair host permissions.

If accepted files cannot be read/verified, preserve work and report the concrete
missing guidance or permission boundary. Ordinary Git restore or an authorized
supported retry is recovery; frozen releases are never rewritten. Permanent
corrections use a later independently reviewed source/package version.

## Qualification and retained history

[Task 24 Step 3](task-24/step-3/README.md) records genuine Windows-to-Linux native
qualification and supported Linux Codex CLI file/Git reads, conditional topics,
candidate edit, continuation and nested review workflow. Windows Codex sandbox
still fails before process creation with `helper_unknown_error: setup refresh
had errors`; Windows CLI startup remains unqualified. No ACL, credential or
protected host configuration was changed. These bounded probes do not establish
server model identity, other clients or repeated reliability.

[Task 22](task-22/step-1/README.md) remains historical accepted evidence for the
previous publication-coupled helper. [Step 1](task-24/step-1/README.md) and
[Step 2](task-24/step-2/README.md) retain their research-only assessments.
The native candidate requires fresh independent review. Issue/Step binding,
release cadence, credentials, installation and consumer authority remain local.
Source acceptance, merge and public publication are distinct.
