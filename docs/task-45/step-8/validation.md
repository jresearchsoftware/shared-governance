# Task 45 Step 8 — post-squash CI regression

Authority: [Step 8 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6240256563)
and [owner confirmation](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6240303514).
Finding: [independent Step 7 Change Request](https://github.com/jresearchsoftware/shared-governance/pull/46#issuecomment-6239384970).
Frozen accepted source-main: `ec048fb39ae28cf2d747101466a603ddd062b1b0`.
Starting PR #46 head: `af9ee28dc0c631ea51ce1c082250953e277fafa7`.
Before substantive editing, the manual executor changed this same open PR from
Ready to Draft and read back its exact head, number and native Draft state.
The client title was set and persisted-title readback confirmed Task 45 / Step 8.

## Correction and preserved invariants

The P1 history dependency was introduced in Step 7's readiness test. It queried
an unmerged Step 6 candidate object which need not exist after squash integration.
The corrected test reads a small committed structural fixture instead. Fixture
provenance identifies Step 6 without querying that commit at runtime or treating
it as accepted authority. During this correction its complete 27 TH anchors and
eight headings were compared exactly with the original Step 6 Markdown.

The test still requires exactly TH-001–TH-027 plus TH-028, preserves all previous
headings, assigns TH-028 only to Task Handoff, checks installed-payload README
and changelog references and excludes producer CLI commands from shared guidance.
Existing collision, link, semantic-preservation, source/export/registry/slot/lock
and manual-route checks remain unchanged. A full copied protocol or resolver is
unnecessary: the fixture preserves precisely the historical structural contract
the existing test asserted.

No package, manifest, protocol, README/CHANGELOG, historical slot, lock, index,
publisher or workflow bytes change in Step 8. This remains the same unaccepted
3.0.0 MAJOR candidate against accepted 2.7.0, with `Package bump: major`.

## Reproducible isolated-history proof

[qualify-squash.py](qualify-squash.py) is a one-time qualification helper, not a
new standing CI gate. Run with Python 3.11+, Git and the repository's accepted
ancestry available locally; the tests use disposable native Linux filesystems:

```sh
python3 docs/task-45/step-8/qualify-squash.py --source-ref af9ee28dc0c631ea51ce1c082250953e277fafa7 --focused-only
python3 docs/task-45/step-8/qualify-squash.py --source-ref HEAD
```

The first command intentionally fails at the old finding. The second qualifies
the committed candidate. The helper initializes an empty independent repository,
fetches **only the accepted main SHA and its ancestry**, and replaces its tracked
tree with an archive of the selected candidate. One synthetic commit on `main`
has the accepted SHA as its sole parent. Tree-object equality verifies all
candidate bytes and modes. There are no task refs, clone hardlinks or object
alternates. `git cat-file -e` must fail for **both** the Step 6 object and original
candidate commit before tests execute. This is not a same-branch clone with
hidden access to PR objects.

The helper's post-squash checks are the actual `candidate.yml` main-push commands,
including the exact before SHA for release and whitespace checks. Its ordinary
tests still use durable accepted historical commits where needed; the required
fetch-depth remains unchanged. No transient PR object is fetched to make them pass.

## Observed results

Correction/helper revision: `a95bb67db7d4ee5b204295bceaf6f82d1e9bd1cc`.
The later evidence commit adds only this qualification text and primary logs.
The canonical Outcome binds final head, fresh Actions and final-head rerun.

| Check | Result and primary record |
| --- | --- |
| Before-fix negative control | [Old candidate tree](logs/before-fix.txt), synthetic squash `58a812985e0175f2762408dc8c73667f7aab18d0`: candidate and Step 6 objects absent; the original readiness test fails specifically on its `git show` call, exit 128. |
| Corrected whole main-push path | [Synthetic main log](logs/synthetic-main.txt): tree equals correction revision; both PR-only objects absent; exact-export/source/native integrity, all 47 distribution, 13 self-adoption and 24 ChatGPT tests pass. Release: 17 total, 11 pass / six optional native skips. Main-push version comparison accepts 2.7.0 → 3.0.0; whitespace passes. |
| Native retained inventory | [Pinned VibeVM check](logs/native-retained-inventory.txt): musl 1.0.7 digest verified against toolchain; zero errors, three known orphan-slot warnings for retained 2.5.0/2.6.0/2.7.0. |

The native warnings concern deliberately retained history outside the current
lock; deliberate native install prunes those slots. They do not establish a
current 3.0.0 source/slot mismatch. Preserve this history and use ordinary accepted
file reading; no install or materialization change is needed for a test-only fix.
The existing exporter/native consistency checks and self-adoption tests verify
the current installed package and local routing. No zero-warning claim is made.

`publish.yml` depends on successful Public candidate checks for a main push.
The complete synthetic main-push path now succeeds without the missing object,
so this specific regression no longer prevents that prerequisite. This is a
local history-boundary qualification, not an actual main integration, GitHub
push event, automatic publication run or grant of publication authority.

## Evidence reuse, limits and handoff

Unchanged Step 2/4 native atomic publication/race/retry and Step 7 materialization
evidence remains sufficient for those unchanged invariants. Native transport
skips remain skips; no new full publisher transport suite or remote publication
is performed. Actual new-head Actions and primary logs are identified in the
single canonical Outcome. Synthetic histories do not prove independent review,
owner integration or live permissions. Private caller/destination credentials,
publisher activation, Windows/macOS native publication, Landscape integration,
consumer adoption and live ChatGPT settings remain unqualified and outside scope.

The complete result is solely existing PR #46. Ordinary non-force push and exact
head reconciliation precede one attributable Step 8 Outcome on that PR. Successful
durable Outcome readback precedes Ready transition and same-PR/head/state readback;
that subsequent state evidence requires neither another Outcome nor a source
commit. Stop for fresh independent exact-head review under Direct. No self-approval,
merge, package/distribution publication, credentials/settings change, consumer
migration, Task closure or subsequent execution Step is authorized.
