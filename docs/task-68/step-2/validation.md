# Task 68 Step 2 — Qualification evidence

Implementation starts from accepted `414077e956aa47b18ddc436f68c3245b508baf46`
in a separate checkout for `run-40084979299`. The canonical checkout was clean
and normalized to `codex/task-68` at that head; its prior branch was preserved.
The independent checkout has its own Git object store and execution resources.

## Native generation

Authored package was committed before exact-source staging. Linux musl VibeVM
1.0.7 was downloaded to this run's disposable Debian WSL directory and matched
the committed toolchain SHA-256
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
No runtime/host permission or credential changes were made.

The original `--registry` local-only path could not resolve Relay's explicit Git
root. Pinned source inspection established its resolver selection; a task-isolated
`VIBE_SETTINGS/registry.toml` selected the native mixed resolver. With the staged
in-tree registry declared as a file URL, the ordinary command was:

```sh
VIBE_SETTINGS=<task-isolated-settings> vibe --json install \
  --no-default-registry --no-prefer-local --assume-yes
```

Native install completed, selecting exactly Shared 6.0.0 and Relay 3.0.0; it
materialized only Shared and regenerated root/member nodes. Generated lock order
is preserved; the integrity check compares root dependency identities regardless
of order while rejecting duplicates. No generated identity was hand-edited.

Shared native content hash:
`sha256:b9229252f755190953c138db9304a083fd1297b36ab655ed4b110ec6319045a0`.
Relay remains
`sha256:451ee21dbfd63abd7918f0aee979220fb57cb8a8dffde20009a25f11bf9071e7`.
Offline native Skill discovery found exactly one `codex-relay`; project install
dry-run returned `unchanged`. Only selected lock, slot and boot output was
transferred back; all accepted historical slots remain in the review candidate.

The source/projection qualifier and regression suites are run against committed
candidate bytes; exact final command results and head belong in the canonical
Writer Outcome and native PR checks. Scenario walks are source-guidance evidence,
not fresh model compliance or live Relay/DocReview behavior. Independent
acceptance, integration and public package publication remain separate.
