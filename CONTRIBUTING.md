# Contributing

Open an Issue for a proposed shared principle or a focused PR for a bounded
correction. Explain the problem, semantic owner, likely consumers, preserved
qualifiers and final behavior. Source changes are independently reviewed before
merge. A successful check is validation evidence, not review acceptance.

Ordinary contributions need no Relay installation, VibeVM registry account,
publication credentials or Task/Step machinery. Bootstrap authority remains
[Relay Task 83](https://github.com/jresearchsoftware/codex-relay/issues/83);
later substantive work uses repository-local Issues.

Use Python 3.11 or newer and Git for source and exact-commit flow export:

```sh
git diff --check
python3 scripts/qualify.py --export-ref HEAD
python3 scripts/test-release.py
```

The qualifier checks tracked bytes, local links, manifests, package passivity
and protocol/export consistency, including the accepted-origin active snapshot.
Stage intended new files before running it; commit the candidate before comparing
its exact-commit export. The first-release check also verifies semantic equivalence
to the accepted Skill/procedure, with no native projection.
Its credential scan reports paths only and covers bounded markers; it cannot
prove absence of all secrets or private knowledge. Inspect the complete diff.

For VibeVM behavior, use the exact pinned tool and disposable fixture in
[docs/authoring.md](docs/authoring.md). A VibeVM tool is unnecessary to read the
source or export the native skill. Do not add another mandatory dependency merely
for ordinary prose edits.

Governance changes should preserve examples and exceptions, distinguish generic
principles from product mechanisms, and state material behavior changes. Compare
new findings with the starting state before calling them regressions. Use a
focused behavioral check when it adds evidence, rather than tests that repeat
wording. Package-changing PRs follow [release policy](docs/releases.md): justify
one `Package bump: major|minor|patch` category and recompute against current main.
The reviewed owner merge admits automatic publication; consumer adoption remains
separately owned.
