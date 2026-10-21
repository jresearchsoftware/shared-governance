# Task 58 Step 2 — Restore existing-destination publication

Authority: the complete [Task 58 charter and Step 2 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/58#issuecomment-6315590037),
following the [Step 1 CR-1](https://github.com/jresearchsoftware/shared-governance/pull/59#issuecomment-6315578620).
Accepted source-main guidance remains frozen at
`99034dd708e5d0201060986b561ada4d2cffd453`; the reconciled Step 1 head was
`0132d79546130b094f52c1145779e34cf488aab9`. PR 59 was converted to Draft and
its identity/head/state read back before editing. Historical Outcome and review
remain untouched. This is Manual Codex implementation evidence, not acceptance.

## Correction and preserved boundaries

Stage first reads ordinary public Git refs. If accessible, it retains the tag
skip and normal bare clone/native stage path without constructing a REST client.
Finalize likewise uses Git refs, atomic non-force push and exact tag readback
without a REST precondition. REST 403, 429, 503 or transport failure can no longer
block an otherwise Git-accessible destination. There is no new operator action.

Only failed Git access to an exact source-bound `jrs-vibevm` destination enters
the existing REST fallback. An anonymous 404 permits disposable local staging;
it grants no creation authority. Finalization retains authenticated absence
proof, public identity checks, refreshed 404, create/readback reconciliation and
failure codes. Git access must succeed after provisioning before any push.
Forbidden/private/redirect/transient/ambiguous fallback evidence cannot authorize
creation. Source/CI/version/rights/export/dependency checks, no-op, immutable tags,
secret-free native staging and same-source retry remain intact. No workflow,
producer readiness or active publisher pin change was needed in Step 2.

## Qualification

Implementation/documentation commit:
`4b6b54de8147801f43bb37200ed21d7554ea4bba`. Tests ran on the same implementation
bytes in a disposable Debian native-filesystem clone with Python 3.11 and pinned
VibeVM 1.0.7 musl, SHA-256
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
Subsequent evidence commits do not change those implementation bytes.

| Command | Result / primary log |
| --- | --- |
| `python3 tooling/vibe-publisher/test_publisher.py --vibe /path/to/pinned/vibe -v` | [89 passed, no skips](logs/publisher-native.log) |
| `python3 scripts/test-release.py --vibe /path/to/pinned/vibe` | [17 passed, no skips](logs/release-native.log) |
| `python3 scripts/test-publication.py --vibe /path/to/pinned/vibe` | [11 passed, no skips](logs/publication-native.log) |
| `python3 scripts/test-distribution.py` | [48 passed](logs/distribution.log) |
| `python3 scripts/test-self-adoption.py` | [13 passed](logs/self-adoption.log) |
| `python3 scripts/test-chatgpt-projection.py` | [24 passed](logs/projection.log) |

Total: **202 passed, zero skips**. The new native regression couples stage and
finalize across successive source-qualified versions while a synthetic REST
client would return 403/429/503/transport failure. It asserts **zero REST calls**,
real native staging, real local atomic Git publication, exact tag-object readback,
finalize retry and stage retry skipping the existing tag. Its
[pre-correction run](logs/regression-before.log) on Step 1 reproduces CR-1:
403/429/503 stop staging. The first fixture's zero-status fake instead returned
200; that subcase detected unwanted REST calls. The final fake represents zero
literally, and the complete corrected suite passes.

The new failed-Git/ambiguous-REST regression verifies both stage and finalize
remain closed, with no POST or push. Retained native absent-destination tests
exercise staging before create, safe empty-repo first push, injected push failure
and same-source retry without another create, then Git-only retained-tag retry.
Private/masked-404, scope/membership/SSO, create race, failed create/readback,
source/CI/version/rights/dependency, no-op and sibling-isolation coverage remains.
API responses are simulated; local Git and native operations are real. No live
GitHub destination creation or publication is claimed. Exact-head qualification
and hosted Actions evidence are bound in the canonical Step 2 Outcome.

## Credential compatibility investigation

Read-only [organization-secret visibility metadata](logs/secret-visibility.log)
again confirms the established name is exposed to Shared Governance and Landscape.
This endpoint provides names, not the token type, identity, scopes, membership or
create capability. No secret value was accessed, extracted or used for a probe.
The current CLI identity is not substituted for the injected publication identity.

Accepted [producer release policy](../../releases.md) describes a fine-grained
Contents-write token for the existing distribution repository. That documents
the supported existing-publication setup; it does **not** establish the actual
current secret's type. Existing release success proves publication access, not
classic `repo` scope or destination-org owner membership. GitHub documents that
[private resources can be masked as 404](https://docs.github.com/en/rest/using-the-rest-api/troubleshooting-the-rest-api#404-not-found-for-an-existing-resource),
including when fine-grained credentials lack access to the affected repository.
Thus neither public Git access, secret visibility nor a create permission by
itself replaces the retained absence proof.

**Disposition:** actual compatibility with the active-owner/classic-`repo` proof
is **unverified**, not a second proven implementation defect. The Step 2 Git-first
correction restores existing public publication without that proof. Creation
retains the restriction and remains pending when it cannot be proven. Before
live creation, the unresolved owner question is whether supported non-secret
attestation establishes that the existing injected credential satisfies this
proof, or whether a separately authorized policy/capability design is needed for
the established credential. No new token, rotation/escalation, relaxed private-404
protection, secret visibility or organization setting change was attempted.

Development Governance 4.0.0 and native projections remain unchanged, so no
package bump is appropriate. Distribution main/tag at pre-handoff readback remain
`f14da40725cd35fb3117ae84a506256505340787` /
`52440f3edfb1a47e4b34a239469ca38f1f1ecc60`.
The known VibeVM 1.0.7 unsupported dependency-manifest syntax and historical
fixture-probe limit retain the disclosed meanings in [Step 1](../step-1/validation.md).
No merge, release, live destination write, activation, consumer migration,
settings/credential mutation or Task closure is authorized by this result.
The completed PR requires fresh independent exact-head review.
