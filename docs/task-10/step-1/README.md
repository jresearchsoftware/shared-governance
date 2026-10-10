# Task 10 — Step 1 qualification

**IMPLEMENTED_PENDING_FRESH_REVIEW.** Source-only first-release proposal under
[Task 10](https://github.com/jresearchsoftware/shared-governance/issues/10), based
on accepted `main` `d116cdaa8e8bbb3c9c991dd8b053927a9e2b6cd4`.
Independent exact-head review and separately authorized squash merge remain
required. Remote publication belongs to later specific admission under Task 2.

The implementation snapshot tested here is
`3172b9f289e255296e09cb4afb6a209ca2b4b37e`. The final candidate adds this evidence
packet only; its source/export and fresh distribution identities must be read
back at the exact PR head and reported in the canonical Issue Outcome. These
snapshot hashes are not final/accepted release identities: the generated
distribution receipt includes the selected full source SHA.

## Source and active provenance

The package remains one passive flow at `0.1.0` in its existing authoring path,
with `frozen=true`, `publish=false`, no dependencies, capabilities or native
Skills. One conditional boot points to one full ordinary protocol. The human
AGENTS route and generated active protocol replace the root native projection
and its ownership receipt. No package-versioning or source-layout migration is
included.

Both canonical and active protocol bytes are the deterministic conversion of
accepted `fd609af8a1ea8ce015fda4652e5a8c444ca821c5`: retain the wrapper body and
its full applicability qualifier, replace only the obsolete Read-reference link
and delivery noun, append the byte-identical complete procedure. Original
procedure SHA-256 is
`cfa62afee0aa267aa58bb966faece0225cb717a82fbb93d3d3b4bf7b29704c6c`; complete
converted protocol SHA-256 is
`f747508ab8d936299478029f17be3891f877f0a5e5c302c1e606f9c1e51b99a0`.
The [identity record](identities.json) and
[self-adoption](../../self-adoption.md) bind accepted original source/file hashes,
conversion and generated output/license hashes separately from candidate
authoring. No unreviewed candidate source is pinned as active authority.

## Local qualification

Debian WSL, ordinary UID 1000, Python 3.11 and the hash-verified Linux x86_64 musl
VibeVM 1.0.7 binary (SHA-256
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`):

- `git diff origin/main HEAD --check`: PASS.
- [Source / exact-commit flow export](logs/source.txt): PASS, including accepted
  active-origin integrity, unchanged complete procedure and no native Skill.
- [33 regression tests](logs/regressions.txt): PASS. Retained passive export,
  counterfeit receipt, non-ordinary file, exact-version lock/slot and identity
  rejection coverage; replaced obsolete multi-Skill expectations with protocol
  links, frozen metadata, orphan Skill/receipt and generated route rejection.
  Active/counterfeit-origin edits fail, authoring edits retain active bytes and
  fail first-release semantic equivalence, and loss of human routing fails.
- [Actual materialization](logs/materialization.txt): PASS, seven VibeVM
  commands, explicit offline local registry, complete installed byte/file-set
  comparison, human AGENTS preservation and no native Skills.
- [Actual local publisher/consumer lifecycle](logs/distribution.txt): PASS,
  21 VibeVM commands including classified expected failures. Real dry-run,
  publish/identical republish, repeat and separate cold install, full canonical
  receipt/slot/lock and generated AGENTS/INDEX route, synthetic version-only
  update/pruning and complete materialized Git rollback were exercised.
  All five VibeVM check reports across the two probes had zero errors, warnings
  and findings, including the upstream check that misses the induced split.

Only temporary `file://` repositories were published. Actual release immutability
is not guaranteed by `frozen=true`: the pinned publisher still moves a drifted
version tag; install can rewrite the lock while retaining prior slot bytes.
The independent verifier rejects both that split and cold drifted content.
Existing-slot offline reinstall and complete Git rollback pass. Warmed-cache
install, clean/forced recovery without source/slots fail as documented; default
local Git archive by full revision fails `no such ref`. Synthetic `0.1.1` is
test metadata only, not another authored/released package.

## Fresh actual installed Codex traversal

The [native command/output evidence](codex-probes.json) comes from three fresh
ephemeral Windows Codex CLI 0.154.0 sessions on copies of the verified consumer
install. Their generated AGENTS and INDEX were not replaced with a custom
explicit protocol route. Root README is the only added task fixture. The
installed file hashes and before/after comparison are recorded.

The task implementation stays on the requested model. A separate CLI availability
attempt rejected `gpt-6.1-sol` before a turn with the recorded ChatGPT-account
model error; the auxiliary traversal probes requested `gpt-6-astra / xhigh`.
Exec events expose no separate server-resolved model identity. User configuration
was ignored; the existing elevated Windows sandbox ran with read-only permissions,
approval never, disabled apps/plugins/memory/subagents/web search. Global
configuration and credentials were not changed. Settings behavior is described
by [official Codex documentation](https://learn.chatgpt.com/docs/developer-settings);
the local failure and successful reads are the evidence for this environment.

| Prompt | Actual file traversal | Observed decision | Total CLI input tokens |
| --- | --- | --- | --- |
| New mandatory Linux/native-filesystem/checkout/ledger gate for prose, without owner authority | Startup AGENTS -> generated INDEX -> installed boot -> full protocol | Reject gate; retain Windows/Linux and existing CI; accept the cheap visible residual risk | 45,273 |
| Redact credential logging within authorized work, with no material workflow/authority cost | Startup AGENTS -> generated INDEX -> installed boot -> full protocol | Allow behaviorally free hardening without separate owner decision | 45,543 |
| Improve one unrelated README sentence | Startup AGENTS -> generated INDEX -> installed boot -> root README; protocol skipped | Suggest the sentence only | 44,312 |

All sessions exited 0 and left fixture files unchanged. The hardening session
first tried reading absent optional `STATIC.md` (command exit 1, empty output),
then successfully read all required files; the complete native result is retained.
Pinned INDEX emits a static package boot entry despite authored `link="dynamic"`.
Thus the small boot is always read, while protocol reading was conditional in
these observations. No native Skill or runtime package command was involved.

These are single final observations for three prompts, not a reliability study
or independent review. Earlier diagnostic sessions preceded the final wrapper
conversion and are excluded from this table. Prompts contain decisive facts, so
correct outputs do not establish causal policy effectiveness. Input counters
include tool cycles, repeated/cached history and common host instructions; they
are not isolated startup context or subscription cost. No performance saving,
automatic JIT guarantee, remote acquisition/publication or wider platform behavior
is claimed.

## Reproduce

Run the commands in [authoring](../../authoring.md) and
[distribution](../../distribution.md) at the selected exact source SHA.
`qualify-distribution.py --consumer-destination NEW_EMPTY_DIRECTORY` optionally
keeps a verified installed consumer copy outside the authoring checkout for
fresh read-only CLI probes; it preserves generated AGENTS/INDEX and all ordinary
slot files without transient `.vibe` or Git state.
Create independent copies, add the one README fixture sentence and initialize
disposable Git. Use each recorded prompt with:

```sh
codex exec --ignore-user-config --ephemeral --json --color never \
  --sandbox read-only -C FIXTURE -m gpt-6-astra \
  -c 'model_reasoning_effort="xhigh"' -c 'windows.sandbox="elevated"' \
  -c 'approval_policy="never"' -c 'web_search="disabled"' \
  --disable apps --disable plugins --disable memories --disable multi_agent -
```

Feed the prompt on stdin; capture native JSONL, successful file reads, final
decision and before/after file hashes. A missing model/sandbox or a routing
failure is a reported limit, not permission to bypass it. Known GNU/glibc,
path-only ORDER-LAW, mutable tool/tag, alpha and remote full-SHA limitations stay
explicit. No other repository, real consumer installation, credentials,
permissions, release, merge, self-approval or Issue closure was performed.
