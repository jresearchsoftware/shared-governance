# Task 24 — Step 3 — Native self-adoption qualification and implementation

This is the separately attributable Step 3 candidate under the current
[owner admission](https://github.com/jresearchsoftware/shared-governance/issues/24).
It continues [PR 25](https://github.com/jresearchsoftware/shared-governance/pull/25)
and preserves the Step 1/2 commits, Outcomes and research-only assessments.
Implementation evidence supplies no independent acceptance, merge, publication,
consumer installation or Task closure authority.

## Frozen authority and reused evidence

The clean starting branch/PR head was `521e9eef8c6e4190f342cb5a5e02e4eb6e2a3bc9`.
Live source-main is `96d26c51b6d05ee5ec4576a44f541b904f0f13fb`, independently assessed
under Task 22 and merged by its owner through PR 23. The owner completion record
and live merged PR were read. That SHA is frozen for this whole production effort.
Its four protocol bytes equal the independently accepted/published 1.2.0 source
`73798b919efbd0d8b0ee1317bf84a6c48d7e99d1`. Initial helper selection passed without
warnings: release `4e701dcb0c97bb7a220800a550eb2f668a8ab20b`, payload SHA-256
`23d2f2ea4b28c5aafb17007d5e875b78f4b472c36d89fd66a1549e79070d0349`.
Candidate root/nested/boot/protocol instructions remain proposals for this effort.

The [Step 1 Outcome](https://github.com/jresearchsoftware/shared-governance/issues/24#issuecomment-6120052165),
[Step 2 Outcome](https://github.com/jresearchsoftware/shared-governance/issues/24#issuecomment-6123279371)
and [Step 2 assessment](https://github.com/jresearchsoftware/shared-governance/pull/25#pullrequestreview-5490198249)
were read. Their path ORDER-LAW, typed registry/static/dynamic comparisons,
relative-link explanation, no-tool conflicts/continuation and basic integrity
failures are reused. This Step tests the missing cross-OS and real file-tool
scenarios, then implements the owner-selected design.

## Genuine Windows to native Linux qualification

[Reproducible diagnostic](../../../scripts/probe-task24-step3-native.py) ran pinned
Windows VibeVM 1.0.7, not a Linux-generated surrogate. Its official release
[fragment](logs/windows-fragment.json), ZIP and executable digests were checked;
Windows executable SHA-256 is
`ceb0b8582e059dfab708ee0c5221e700c232c97912bdd5174dc0df1d03011b46`.
Native Linux musl SHA-256 remains
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Windows produced/co-committed a genuine lock, slots, index and agent routing at
synthetic commit `fef8ac65b9eed9edad30a5b66a7d833c485be557`, lock blob
`7d4925088a9b8c4f22027942fe9f922026443eb0`. Native Linux clones consumed that exact
commit/blob without changing URLs. These fixture commits are test data, not
production acceptance.

| Scenario | Observed behavior |
| --- | --- |
| Clean checkout / ordinary startup | Committed slot/index readable and canonical without bootstrap/install. |
| Linux retained-slot install and update | PASS; Windows URL can remain unchanged and unreachable. |
| Linux missing-slot install | Restores pinned canonical bytes from the clone's own in-tree registry. |
| Deliberate exact version change | New source/slot selected; old Windows URL does not suppress the meaningful change. |
| Pull / checkout rollback / forward | Source and committed projection advance/restore together. |
| Corrupt and missing slots, `reinstall --force --offline` | Canonical exporter verification PASS with fresh fixture-local settings; no `--registry` assumption. |
| Plain reinstall with removed index | Index regenerated. |
| Same-version source mutation incident | Native install/update retain old slot; canonical source comparison detects the change. Frozen same-version edits also fail release transition. |
| Lock churn | Timestamp may change; retained identity/hash and URL are distinguished from exact lock bytes. |

Complete [Windows](logs/windows-native.json) and [Linux](logs/linux-native.json)
command/state evidence is retained. An initial harness wrote a nonexistent
`registries` field into disposable user config: it failed visibly; the
[initial record](logs/linux-native-initial.json) is preserved. The corrected
configured case uses the documented fixture-local `registry.toml`; the simpler
unconfigured in-tree path also passes. No protected/global host config was edited.
Absolute URLs are native location metadata. Accepted Git plus canonical
source/slot/lock/index checks supply provenance; a native exit/check alone does not.

## Actual supported Codex file-tool qualification

[Parameterized diagnostic](../../../scripts/probe-task24-step3-codex.py) supplies
only an exact accepted SHA and routing instructions, never full protocol text.
The Windows real-tool attempt still fails before PowerShell process creation:
`helper_unknown_error: setup refresh had errors`. It was not retried or repaired;
[Windows record](logs/windows-codex.json) cannot qualify Windows CLI startup.

WSL's inherited Windows npm wrapper lacked a Linux optional executable. A matching
0.162.1 Linux executable was unpacked under disposable `/tmp`; existing WSL
ChatGPT authentication was used without copying/altering credentials or config.
The default WSL gpt-5.4 was rejected before tools; its [initial record](logs/linux-codex-initial.json)
is preserved. The owner explicitly authorized gpt-6.1-sol for these one-off
launches only. No server-side model identity or silent model replacement is claimed.
The supported workspace-write/read-only sandboxes were retained.

[Linux events](logs/linux-codex.json) demonstrate accepted root/boot/protocol reads
through actual `git show`, a harmless candidate edit with bytes verified,
conditional applicable topics and skipped package-versioning, continuation after
candidate AGENTS change with the SHA retained, a fresh nested review-oriented
launch with proposals treated as data, and an unrelated translation skipping all
four protocols. Review workflow qualification is not independent assessment.

[Final ready-checkout probe](../../../scripts/probe-task24-step3-ready.py) consumes
the real Windows-generated candidate at `f324d69d1227bc83c4bb3ba8fd6c3d960282c91a`
in a clean native Linux clone. [Events and recovery](logs/ready-startup.json) show
actual root/index/authoring/slot boot and five applicable protocol reads through
Git, with relative links resolved inside committed slots, no installation or
bootstrap. This intentionally tests a hypothetical future accepted candidate in
isolation, while the production effort retains accepted `96d26c51…` authority.
Corrupt and missing final 1.3.0 slots are restored to exact canonical bytes through
supported native force reinstall. Only after this successful gate was the old
helper/selector retired. A release-doc sentence exposed by this probe was corrected
from publication-coupled activation to accepted source-main reading.

## Smallest implemented producer layout and semantic coverage

The root pins `flow:org.jresearch.ai/development-governance` at `=1.3.0`, dynamic.
The stable authored package, one current generated versioned registry copy,
versioned slot, native lock, root/member indexes and AGENTS/CLAUDE/GEMINI routes
are committed in this same PR. Temporary native synchronization locks are ignored.
The existing exporter stages/verifies native files; no new resolver, manager,
service, accepted-side checkout, tool patch, upgrade or public registry is added.

Local native export omits release-only `DISTRIBUTION.json`; the accepted Git
commit owns source/projection together. This avoids a self-referential commit
receipt and a dependency on unaccepted PR commits surviving squash. The normal
public export still includes the exact-source receipt. Generated member routing
is checked as producer state and excluded from the passive public package.
The root's existing owner/Issue/review/consumer/protected-boundary overlays are
preserved outside VibeVM's block. The accepted four protocol files remain byte
identical, including attribution, applicability, exceptions and free hardening.

The reviewed protocol draft is now proposed package content in
[self-adoption](../../../packages/development-governance/vibevm/vibespecs/protocols/self-adoption.md).
Coverage of canonical Issue semantics is explicit:

| Obligation | Implemented coverage |
| --- | --- |
| Conditional producer applicability and local authority | Explicit adoption only; other repositories/topics skip it; no transferred Task/review/release powers. |
| Accepted source distinct from publication | Exact source-main binding frozen per effort; committed files readable during publication outage. |
| Candidates remain proposals | Explicit external task binding covers root/nested/generated text; isolated future-guidance tests disclose scope and client limits. |
| Prefer supported native tools / preserve overlays | Typed in-tree VibeVM, existing Git exporter, root overlays, dynamic relative routes. |
| Source-controlled ready state / same reviewed PR | Generated source/slots/index/agents committed with source; no post-publication adoption PR or startup bootstrap. |
| Integrity and rollback | Existing canonical exporter extended to native state; changed/missing source/slot/hash/routes fail; ordinary Git recovery. |
| Independent exact-result assessment | Fresh review of final head remains pending; old research acceptance and CLI checks do not approve implementation. |

Package bump: **minor**, 1.2.0 → 1.3.0. The shared protocol is explicitly conditional
and additive. Existing consumers' mandatory behavior/local authority and all four
existing protocol bytes remain intact. Producer startup changes are separately
owner-admitted in Step 3; frozen releases, public release workflow, credentials
and consumers remain unchanged. The isolated future producer is also the
applicability scenario without a residual bespoke helper; no consumer migration
or claim about other client loading behavior is made.

## Validation and review boundary

Native mismatch/recovery regressions cover ready checkout, registry/slot corruption
and missing files, forged slot metadata, lock hash/version/source-kind, moved
source URL/timestamp, missing/wrong index, member route, root overlay preservation,
manifest range/link mismatch and stale committed/uncommitted source behind an old
URL. Distribution/release regressions retain historical exports and passivity.
[Validation logs](logs/) identify tested source and individual results. Final
head-associated CI and publication read-back belong to the separate canonical
Step 3 Outcome; local logs are not CI or independent acceptance.

No merge, release, consumer/Relay installation, GitHub settings, protected host
configuration/ACL/credential change or Task closure was performed. Stop for fresh
independent exact-head review of PR 25.
