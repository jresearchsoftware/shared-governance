# Task 58 Step 1 — Shared credential and bound repository creation

Authority: [Task 58](https://github.com/jresearchsoftware/shared-governance/issues/58)
and the owner's explicit Manual Codex Step 1 execution prompt on 2026-10-21.
The Issue had no comments at start or the prepublication refresh. Accepted source
guidance and starting main are frozen at
`99034dd708e5d0201060986b561ada4d2cffd453` (accepted Task 52 / PR 56).
Read its root/native routing, proportional controls, requirement authority,
Task Handoff, package versioning and producer/manual contributor bindings.
Reconciled linked Tasks 45, 51 and 53 and their relevant implementation,
independent review and integration records. Candidate files cannot repin authority.

## Result and workflow impact

The shared reusable workflow accepts the established named organization secret.
Its old `publish_token` input remains compatible; the named input takes precedence.
The unprivileged Actions fixture passes a public synthetic marker through the new
named input and checks isolation before source planning/staging. No new token,
inherit-all-secrets arrangement or producer-specific credential setup is added.

The exact source-bound destination alone selects the repository. Only canonical
HTTPS URLs under `jrs-vibevm` enter automatic provisioning; existing destinations
outside that namespace retain the old path. Source-main/CI, changed version,
rights/license, approved export and included dependency gates precede staging.
Successful credential-free pinned native staging precedes remote creation.
An absent public destination uses an empty local bare repository with main HEAD;
the first atomic non-force main/tag push needs no initialization commit or extra
push. Existing repositories receive no metadata/create request. No-op and retained
version tags cannot create anything.

Required ambiguity handling: GitHub can mask an inaccessible private repository
as 404. The implementation proves visibility only for the absent case using an
active organization owner membership and classic `repo` scope, then refreshes the
404. An unproven/limited credential, SSO restriction, 403, redirect or transient
GET fails closed. This is one bounded proof for Task 58's explicit inaccessible-
private-resource requirement, not a claim that every repo-create credential can
establish absence. Existing public publication needs no org-owner proof. The
additional requests occur only when a changed, natively staged release needs an
absent destination; there is no recurring approval, inventory ledger, new service,
credential rotation or automatic escalation. API creation and readback use the
same finalization-only secret already supplied to Git askpass.

Create requests fix public visibility and disable auto-init. A create/name race
or ambiguous POST result is reconciled by exact public repository readback; no
blind POST retry occurs. A created empty repository remains reusable after a
failed push. Tag collisions, divergent main and ambiguous Git push still use the
existing atomic no-force/readback rules. Raw API responses/errors and credentials
are not emitted to reports/logs; provisioning failures have an allowlisted code.

## Executed qualification

Implementation/documentation revision:
`484223da01b524ab37c6d24a75fdfc56f68a2f90`. Tests ran in a disposable Debian
native-filesystem Git clone with Python 3.11 and the pinned VibeVM 1.0.7 musl
binary. Verified SHA-256:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Later evidence-only commits retain the same tested implementation bytes.

| Command | Result / primary log |
| --- | --- |
| `python3 tooling/vibe-publisher/test_publisher.py --vibe /path/to/pinned/vibe -v` | [87 passed, no skips](logs/publisher-native.log) |
| `python3 scripts/test-release.py --vibe /path/to/pinned/vibe` | [17 passed, no skips](logs/release-native.log) |
| `python3 scripts/test-publication.py --vibe /path/to/pinned/vibe` | [11 passed, no skips](logs/publication-native.log) |
| `python3 scripts/test-distribution.py` | [48 passed](logs/distribution.log) |
| `python3 scripts/test-self-adoption.py` | [13 passed](logs/self-adoption.log) |
| `python3 scripts/test-chatgpt-projection.py` | [24 passed](logs/projection.log) |
| `python3 scripts/qualify.py --export-ref HEAD` | [PASS at implementation revision](logs/qualify.log) |

The 200 passing tests include absent/existing/forbidden/transient/private/racing
destinations, failed create/readback, ambiguous create transport, repeated
finalization, credential/error redaction, no-op and unchanged publication.
Actual native tests stage before any remote creation, then create a disposable
local bare destination, inject a failed push, retry without a second creation,
atomically publish main/tag and confirm the exact tag object. Failed native
staging cannot provision. The existing suite exercises main/tag races, immutable
tags, same-source partial retries, supported source integration routes, frozen
dependency closure and explicit initial publication. API/credential observations
in these fixtures are synthetic; Git/native publication runs are real local Git.

The first run of the two new native fixtures reported AUTHORIZATION_PENDING:
their fixture changed destination mapping in the same source transition. The
accepted mapping-change guard correctly rejected it. The fixture now establishes
its mapping in the prior commit and tests a normal changed new-version release;
the guard was preserved. A later complete run passed, as retained above.

## Current access evidence and limitations

Read-only `repos/{producer}/actions/organization-secrets` metadata confirms the
existing named organization secret is visible to both Shared Governance and
Landscape. [Retained metadata](logs/secret-visibility.log) includes only names and
counts. No secret value was requested, read, copied or changed. Organization-wide
secret administration listing was unavailable to the current CLI identity; the
per-repository visibility endpoint resolved the relevant access question.
This metadata does not prove the secret's actual scopes, organization membership,
create permission or live publication. If its injected token cannot prove absence,
automatic creation remains pending for owner disposition; no replacement token
or settings mutation is attempted. Private callers, real remote create/readback
and protected live publication remain unexecuted under this Step's boundaries.

The pre-existing VibeVM 1.0.7 `dev-requires` / inline `optional=true` native syntax
limitation remains; its negative test is not evidence of support. The historical
fixture-probe limitation documented in Task 53 is unchanged. Current candidate
Actions results and exact final head belong in the canonical Outcome.

Development Governance 4.0.0 payload/native slots and the active producer caller
pin remain unchanged. This tooling-only result needs no package bump. Before
handoff, remote source main remained the accepted binding; distribution main was
`f14da40725cd35fb3117ae84a506256505340787` and v4.0.0 tag object was
`52440f3edfb1a47e4b34a239469ca38f1f1ecc60`. No distribution write, merge, release,
activation, consumer edit, secret/settings change or Task closure was performed.
One PR result receives one attributable canonical Outcome, followed by verified
Ready state and a stop for independent exact-head review.
