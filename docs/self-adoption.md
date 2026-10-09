# Repository self-adoption

[Task 6](https://github.com/jresearchsoftware/shared-governance/issues/6) adopts
`proportional-controls` for ordinary manual Codex work in this repository.
The active [Skill](../.agents/skills/proportional-controls/SKILL.md) and its
procedure are generated copies of the independently accepted package at
`fd609af8a1ea8ce015fda4652e5a8c444ca821c5`, the `main` commit after
[PR 5](https://github.com/jresearchsoftware/shared-governance/pull/5).
The [source receipt](../.agents/proportional-controls-source.json) records that
commit, canonical path and file hashes using the existing native exporter format.
The repository's MIT LICENSE covers the projection. The adjacent VibeVM receipt
records the two files owned by native projection; no other VibeVM state was
created or is needed.

Codex discovers `.agents/skills` at the repository root; `AGENTS.md` routes
applicable decisions to this active Skill. Detailed guidance remains in the
canonical package source, with no separately authored policy in the projection.
See the [official skill discovery documentation](https://learn.chatgpt.com/docs/build-skills).
VibeVM is unnecessary for ordinary sessions and source checks.

## Reproduce or update

Use a checkout of the full accepted source SHA above with the hash-verified
Linux x86_64 musl VibeVM 1.0.7 tool from [authoring](authoring.md), with `$vibe`
set to its absolute path. From that checkout's root, using disposable
`VIBE_SETTINGS` and `VIBEVM_USER_CONFIG`:

```sh
"$vibe" --offline --json skill list --path .
"$vibe" --offline --json skill install --path . --agent codex \
  --scope project --skill proportional-controls --yes
```

The workspace member is discovered natively and projected into the root's
`.agents/skills/proportional-controls`, rather than the member's nested directory.
The first install reports `created`; repeating it reports `unchanged`.
Human-owned `AGENTS.md` is preserved. There is no dependency installation,
path-only workaround, manifest edit, registry or publication step.

Copy the generated Skill directory and adjacent native receipt into the adoption
branch. Recreate the source receipt with the existing `scripts/vendor-skill.py`
at that full SHA into an empty temporary destination. Its `SKILL.md` and procedure
must match the projected files, and its LICENSE must match the root LICENSE;
copy only its `SOURCE.json` to `.agents/proportional-controls-source.json`.
From the adoption branch, run `python3 scripts/qualify.py --export-ref HEAD` and
`git diff --check`.
The existing candidate CI verifies the active file set, bytes and both receipts
against the pinned source independently of candidate authoring edits.

Authoring changes do not refresh active guidance. Do not edit the generated
Skill or project an unreviewed workspace into it. After a new package version
is independently accepted, a separately reviewed adoption change may reproduce
projection from that accepted commit and update both receipts together. Retain
the old snapshot while authoring or reviewing the proposed policy. Review the
exact adoption head before merge; rollback uses an ordinary reviewed Git revert.
This self-adoption does not publish a package or migrate another repository.

## Acceptance evidence

Local qualification on 2026-10-10 (Europe/Prague):

- Hash-verified VibeVM 1.0.7 discovered the workspace Skill at the root, installed
  it as `created`, then returned `unchanged`; the human-owned AGENTS bytes were
  identical before and after projection. Both projected files matched the pinned
  accepted Git blobs byte-for-byte. The disposable authoring qualifier also
  passed all six commands, with zero check errors, warnings or findings.
- Native Windows Codex CLI 0.154.0 `skills/list` returned `proportional-controls`
  with `scope=repo`, `enabled=true`, the root projection path and no skill errors.
  A fresh ephemeral read-only session saw it in startup metadata without directory
  discovery, read its Skill and procedure, and correctly distinguished secret-log
  hardening from an unauthorized platform/install/ledger requirement for prose.
  This is behavioral evidence, not independent review acceptance. The configured
  `gpt-6.1-sol` was rejected by that CLI before a turn; the successful probe used
  its advertised default `gpt-6-astra` without changing user configuration.
- Source/exact-commit export and all 42 existing distribution tests passed.
  A disposable boundary probe allowed an authoring-only procedure edit while
  retaining active bytes, and rejected edits to active guidance, origin metadata
  and the native receipt. No other consumer or external publication was exercised.
