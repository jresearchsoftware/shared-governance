# Draft Relay incident — trusted worktree observation after worker execution

This is bounded evidence for a separately authorized Relay investigation, not a
Relay change or a recovery authorization.

Affected attempt: Shared Governance Task 68 Step 1,
[run-40082446961](https://github.com/jresearchsoftware/shared-governance/actions/runs/40082446961),
starting head `414077e956aa47b18ddc436f68c3245b508baf46`.
Native logs identify installed Relay `c3ac51525d92edb6d8b8a8c5a2c5bc242df7b873`
and execution slot `pool-4`.

## Confirmed evidence

- Trusted progress collection failed after contained execution:
  `TRUSTED_GIT_FAILED / GIT_LOCAL_FAILURE`, operation `worktree-observation`,
  syscall `open`, OS code `EACCES`, path context `checkout`.
- Runtime reports containment `reaped`, cleanup `complete`, stored diagnostics
  and no published head. GitHub artifacts are absent; the native job annotation
  supplies only exit code 1.
- The [immutable Step 1 Outcome](https://github.com/jresearchsoftware/shared-governance/issues/68#issuecomment-6382711491)
  reports the worker's claim of completed implementation/commit and untracked
  launcher-owned `.codex-sandbox/`. Neither exact candidate SHA nor original
  validation is verified by that claim.
- Step 2 used the accepted workflow's read-only `inspect` operation with original
  run/attempt identity. [Inspection run 40085261897](https://github.com/jresearchsoftware/shared-governance/actions/runs/40085261897)
  succeeded and returned `publicationIntent:null`, `publishedHead:null`,
  `authorizationBody:null`, the same installed revision and original slot.
  It supplied no candidate identity.
- Without a known exact retained candidate head, `inspect-prepublication` cannot
  be invoked faithfully. No recovery publication, original-worker replay,
  protected host inspection, credentials/permission repair or Outcome rewrite
  was performed. Retained server work was left intact. The newly admitted
  Step 2 implements from the accepted source under its explicit fallback scope.

## Mechanism and root-cause limits

The installed [trusted collector](https://github.com/jresearchsoftware/codex-relay/blob/c3ac51525d92edb6d8b8a8c5a2c5bc242df7b873/controller/src/trusted-git.mjs#L222)
walks checkout entries except top-level `.git`, honors ignored untracked paths,
and opens other regular files through guarded read/copy operations. Its guarded
open uses `O_RDONLY | O_NOFOLLOW | O_NONBLOCK`; there is no explicit
`.codex-sandbox/` exclusion. Unreadable nonignored launcher residue is plausible,
but no public evidence identifies the failed inode, creator, owner/group/mode,
collector identity or sandbox involvement. This is not a confirmed root cause.

[Relay Task 171 / PR 172](https://github.com/jresearchsoftware/codex-relay/pull/172)
is a comparison lead about renamed-tree primary-group access. Its merged fix is
an ancestor of the installed revision, four commits earlier. This evidence does
not establish recurrence or verify the installed configuration. Do not report
the old fix as absent or infer an ACL remedy from categorical `EACCES` alone.

## Reproduction and proportionate next investigation

No faithful reproduction is possible from available categorical evidence alone.
Obtain exact retained candidate identity and bounded failing-object metadata
through an explicitly authorized diagnostic channel. Reproduce the actual
worker/collector identities and launcher residue in isolated TEST; compare the
failing operation with clean task files and ignored/nonignored runtime residue.
Check primary-group behavior only against actual installed ownership evidence.

Fix the demonstrated owning boundary in a separate Relay Task. Preserve failure
for unreadable task source, private-file protections, actor separation and
historical diagnostics. Avoid broad privileges, blanket exclusions, recursive
permission repair or routine manual recovery based on the current hypothesis.

Impact: useful work may remain retained, but its identity, original validation
and publication provenance are unverified. Step 1 remains terminal `BLOCKED`.
The missing capability is bounded access to retained candidate/failing-object
evidence; an owner-authorized diagnostic/recovery route must supply it before
original-result recovery can proceed.
