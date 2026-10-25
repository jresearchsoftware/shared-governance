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
python3 scripts/test-self-adoption.py
```

The qualifier checks tracked bytes, local links, manifests, package passivity
and protocol/export consistency, including committed native producer state.
Stage intended new files before running it; commit the candidate before comparing
its exact-commit export. The retained first-release check verifies semantic
equivalence to the accepted Skill/procedure, with no native projection.
Later protocol changes use the admitted scope, semantic coverage argument and
whole-package version/release checks; candidate authoring never refreshes active
guidance. [Self-adoption](docs/self-adoption.md) binds ordinary work to accepted
source-main and reads committed native files without bootstrap or publication.
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
the intended compatibility category and mandatory operator-work impact in the
existing review/release decision, and recompute the manifest version against
current accepted main. CI derives the numeric step from versioned source; no
literal PR-description marker is required.
The reviewed owner merge admits automatic publication; consumer adoption remains
separately owned.
