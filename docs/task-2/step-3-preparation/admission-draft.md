# Task 2 — Step 3 proposed owner admission

**DRAFT ONLY — awaiting explicit owner admission in the live Issue.**
This text is committed for review. No part is currently in effect; acceptance
or merge of this source documentation does not admit external execution.
It proposes a bounded first publication and disposable remote qualification,
not a new semantic source change or real consumer adoption.

## Proposed admission text

I admit **Step 3: first public distribution and disposable remote-consumer
qualification** for [Task #2](https://github.com/jresearchsoftware/shared-governance/issues/2)
under the following exact boundaries.

- Route: owner-launched manual Codex; model `gpt-6.1-sol`, effort `xhigh`,
  subagents allowed for independent subtasks. No Relay Writer/automatic route.
- Accepted semantic source: `jresearchsoftware/shared-governance` at
  `60704ce3e0f0243d157646989429c6e621fc8f04`, accepted through PR #4 and
  its separately authorized squash merge. Re-read live Issue and AGENTS.md.
  If source authority/head has changed, stop to reconcile before mutation.
- Package: `org.jresearch.ai/development-governance`, version `0.1.0`.
  Only the accepted passive payload and generated canonical receipt may ship.
  Preserve accepted bytes, attribution, MIT notice and `publish=false`.
- Publishing account: **`foal`**. Destination:
  **`jrs-vibevm/org.jresearch.ai.development-governance`**, public GitHub
  repository, URL
  **`https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git`**.
- Authorize creating this **one new empty public repository**, after confirming
  the target does not already exist under the account's effective access.
  No auto README, license, gitignore, template, import or initial source push.
  Creation permission and existing Git authentication must be verified in the
  execution environment. Stop at missing/interactive authentication; do not
  acquire, copy, expose or configure credentials or change permissions/settings.
- Authorize the hash-pinned VibeVM **1.0.7** musl direct-Git publisher solely
  to create initial **`refs/heads/main`** and annotated **`refs/tags/v0.1.0`**
  containing the faithful prepared package. Its internal lease/force flags
  are disclosed: this admission permits only unborn-ref creation, not replacing
  or moving any existing public ref. If any refs exist or concurrent state
  appears, stop. No public history rewrite or changed-content republish.
  The tool has no create-only enforcement: an outer empty-ref check leaves a
  race before the publisher takes its internal lease snapshot. This is an
  operator boundary, not an immutable-ref guarantee. If exclusive initial
  publishing conditions cannot be established, stop for a separate owner decision.
- Expected canonical payload-map SHA-256:
  `4b611bc0a6dc9500dd9e7b6cc11c23092ecf81d25d329ea2066ac9bca9471609`.
  Expected receipt SHA-256:
  `ce072ea1b991f2a1c22ff65cf62b057ecd07817b7f06a8a739cc09281f660b24`.
  Expected VibeVM tree hash including receipt:
  `sha256:9ee1caef5a62d56dc5bcc1890633e8395314f6a93ae9c85dfb8f47cf3d7a1af7`.
  Recompute them from the accepted source before publishing; a mismatch stops work.
- Authorize read-back of real initial refs, anonymous independent clone at the
  full peeled distribution SHA, canonical source/file verification, and a fresh
  **disposable anonymous remote consumer**. Use exact `=0.1.0`, the recorded full
  distribution SHA, this exact destination URL and `auth="none"`; empty isolated
  VibeVM settings/cache on native Linux. Verify complete slot/receipt/lock/hash,
  every declared native Skill and human AGENTS preservation; compare to exact-source
  Git/native export; repeat installation and canonical verification once.
  Treat GitHub full-SHA acquisition failure as a result, without silently changing
  to a tag-only requirement, patching VibeVM or weakening checks.
- Publication alone does not complete Step 3. Report exact source and real distribution
  identities, full verification results, expected/unexpected warnings and remote
  failures in one concise English canonical Outcome in this Issue.
  Stop for independent assessment; do not self-approve or close Issue #2.
- No GitHub Release, central registry registration, host deployment, new package
  capability, semantic policy edit, other-repository mutation, real consumer
  migration, deletion, or movement of public refs is admitted. If failure occurs
  after repository/ref creation, preserve remote state and report it; do not
  delete, retry a changed publication, or invent recovery authority.
  Source acceptance, publication, remote qualification and consumer adoption
  remain distinct gates. **Issue #2 stays OPEN / keep-open.**

## Future operator sequence — only after that admission

Use an existing approved Git-authenticated publisher environment. The local
fixture's environment deliberately disables ambient Git configuration and does
not prove this authentication. Do not reuse its configuration for a real push
without resolving this prerequisite through existing supported owner interfaces.

1. Re-read Issue/AGENTS, confirm the accepted source and owner account, exact target,
   current organization access and actual target absence. An HTTP 404 alone is
   insufficient if effective access is ambiguous. Create only the admitted empty target:

   ```sh
   gh repo create jrs-vibevm/org.jresearch.ai.development-governance --public
   ```

   Verify its canonical full name, owner, public visibility and effective push access.
   Inspect all remote refs successfully; empty output is meaningful only when
   `git ls-remote` succeeds. Any ref or access failure stops the initial publication.

2. Use the existing accepted-source preparer and exact hash-verified tool:

   ```sh
   source_sha=60704ce3e0f0243d157646989429c6e621fc8f04
   target_url=https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git
   # prepared must be a new empty path outside the authoring checkout.
   python3 scripts/prepare-distribution.py --source-ref "$source_sha" --destination "$prepared"
   python3 scripts/prepare-distribution.py --source-ref "$source_sha" --verify "$prepared"
   "$vibe" --json registry publish "$prepared" --path "$prepared" --repo-url "$target_url" --dry-run
   # Recheck successful empty remote-ref inspection immediately before actual publishing.
   "$vibe" --json registry publish "$prepared" --path "$prepared" --repo-url "$target_url"
   ```

   `publish=false` and dry-run are not external-authority or provenance gates.
   The exact musl binary SHA-256 is
   `20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
   The pinned publisher uses atomic ref push with internal `--force-with-lease`
   and `git tag -f`. Preflight/read-back are not atomic host-side protection;
   any unexpected remote race or ref movement must be reported and preserved.

3. Read back all refs and the peeled `v0.1.0` full commit. Confirm `main` and the
   tag identify the expected payload commit. Clone anonymously at that commit
   with separate read-only Git configuration, then verify:

   ```sh
   python3 scripts/prepare-distribution.py --source-ref "$source_sha" --verify "$independent_clone"
   ```

   Record actual public Git identities, tag object/peeled SHA, receipt/map/tree
   hashes and file set. The temporary local fixture commit is not usable here.

4. Create a separate empty native-Linux consumer and settings/cache directories.
   Keep its human-owned AGENTS sentinel and declare:

   ```toml
   [project]
   name = "disposable-consumer"
   version = "0.0.0"
   spec_format = "mixed"

   [requires.packages]
   "org.jresearch.ai/development-governance" = { version = "=0.1.0", git = "https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git", rev = "FULL_RECORDED_PUBLIC_DISTRIBUTION_SHA", auth = "none" }
   ```

   Run with fresh isolated `VIBE_SETTINGS`/`VIBEVM_USER_CONFIG`, anonymous read-only
   Git settings, no credential helpers/prompts, and no default registry:

   ```sh
   "$vibe" --json install --path "$consumer" --no-default-registry --assume-yes
   "$vibe" --json skill install --path "$consumer" --agent codex --scope project --skill proportional-controls --yes
   python3 scripts/prepare-distribution.py --source-ref "$source_sha" --verify-consumer "$consumer"
   "$vibe" --json check --path "$consumer"
   ```

   Assert the exact destination URL, full recorded public SHA and anonymous auth
   separately: the canonical consumer verifier trusts the URL/ref declaration
   when comparing it to the lock. Compare complete projected Skill bytes against
   exact-source native export and human AGENTS outside its one managed block.
   Inspect check JSON; exit 0 alone does not establish warning absence.
   Repeat the same install command once, reproject and repeat these checks to
   qualify remote idempotence; `reinstall` is a distinct upstream operation.

5. Publish the admitted English Outcome with actual PASS/FAIL, remaining limitations,
   warnings and preserved state. No claim of remote qualification follows merely
   from a successful publisher, local probe or source CI. Keep GNU/glibc, path-only,
   mutable tag/tool, lock-slot split, offline/cache and alpha limitations explicit.
   Any future real consumer adoption requires that consumer's separate reviewed Task.

The owner must explicitly admit this proposal in the live Issue before step 1
or any actual remote publisher/consumer execution. This document itself supplies
no publication, Issue-writing, review or closure authority.
