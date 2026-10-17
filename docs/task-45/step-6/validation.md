# Task 45 Step 6 qualification

Authority: [Step 6 Owner Decision](https://github.com/jresearchsoftware/shared-governance/issues/45#issuecomment-6238437956).
Frozen independently accepted source-main: `ec048fb39ae28cf2d747101466a603ddd062b1b0`.
Starting PR #46 head: `6c8df4197a2b6980a0d314cc0cba236d57c7b5b9`.
The canonical terminal Outcome on PR #46 binds the final exact head and primary
CI evidence. [Coverage and scenarios](coverage.md) describe the full affected
publisher path, semantic ownership, breaking/adoption implications and local limits.

## Observed source and regression results

The integrated implementation is `2b6fe8871fd1c304f7357780cdbd732309ecad80`;
native generation is committed at `8a2e62dc4b0d70e42de4f4344d28e27aedbab421`.
All ordinary suites ran in a clean native Debian WSL clone of the latter:

| Check | Observed result and primary record |
| --- | --- |
| Source/exact export/native integrity | PASS, 681 tracked files, 1,080 local links, bounded credential-marker scan; [log](logs/source.txt). |
| Distribution | 46 passed, zero skips; changelog inclusion/missing/empty/historical-version rejection, address collision/broken/misdirected links, insertion-stable anchors and legacy headings; [log](logs/distribution.txt). |
| Release | 17 total: 11 passed, six optional native transport/dependency cases skipped; [log](logs/release.txt). |
| Self-adoption | 12 passed, zero skips; current installed changelog/rules, source/slot/receipt/lock/INDEX and recovery, full review-topic local route; [log](logs/self-adoption.txt). |
| ChatGPT | 24 passed, zero skips, including non-adopting consumer and reproduced complete Instructions/receipt; [log](logs/chatgpt.txt). |
| Shared publisher | 50 total: 44 passed, six optional native transport cases skipped; [log](logs/publisher.txt). The temporal suite has 17 passing tests, including three new coupled cases. |
| Whole-package transition | PASS: accepted 2.7.0 → same candidate 3.0.0, `Package bump: major`; no 4.0.0. |
| Whitespace and immutable history | PASS; exact Git comparison preserves all retained 0.1.0/2.5.0/2.6.0/2.7.0 source and slots. |

The [before-fix regression run](logs/regression-before.txt) deliberately loads
the original Step 5 publisher at `6c8df4197a2b6980a0d314cc0cba236d57c7b5b9`.
Exactly the historical-incomplete factual no-op case fails at its intended
invariant (`AUTHORIZATION_PENDING` instead of `NO_PACKAGE_CHANGE`); the paired
changed/incomplete negative and bounded candidate/production contract cases pass.
This expected failure proves N1, not a failure of the corrected result. The new
publisher passes all three and the complete suite. Fixtures have real Git
chronology and synthetic PR/CI evidence; they assert no live publication incident
or substantive independent acceptance.

Six unchanged protocols plus the two addressed operator guides compare exactly
with accepted 2.7.0 after stripping address annotations. All accepted protocol
headings remain. Meaningful changes to Task Handoff/Independent Review and the
retained preparation changes are assessed through the bounded coverage map;
tests cannot attest that methodology was followed by a model.

## Pinned-native payload qualification

VibeVM 1.0.7 Linux x86_64 musl binary digest was independently checked against
`toolchain/vibevm.json`:
`20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240`.
The existing exporter staged exactly 20 payload files (public release receipt
is additional; local producer source intentionally omits it). Payload digest:
`380043aa5c23ab5425615efc5c7cbc5a09ad60779fccaf3a33170ebe04a15d8a`.

In a disposable clone of `2b6fe8871fd1c304f7357780cdbd732309ecad80`, refresh of
only the task-generated candidate lock and ordinary offline native install
regenerated source/slot/receipt/hash. Exact `--verify-producer` passed. Actual
installed CHANGELOG, IR-005 and TH-006 were opened and checked; canonical
comparison covers every file byte and address. Only current 3.0.0 outputs and
the generated lock were copied back, preserving all historical source/slots.

The ordinary native installer prunes old unclaimed slots in that disposable
fixture. Its tracked inventory was reconciled only there, then the unchanged
`qualify-vibevm.py --materialize` passed seven native commands, zero findings,
dependency installation, complete payload equality and human overlay preservation;
[primary log](logs/native-authoring.txt). This is fresh materialization evidence
for the changed package, not a real distribution publication or consumer migration.

For the actual retained inventory, [native check](logs/native-retained-inventory.json)
reports **zero errors and three warnings**: deliberately retained installed
2.5.0/2.6.0/2.7.0 slots have no current lock entry. Their impact is native
orphan-slot reporting/pruning on deliberate install, not a source/slot mismatch
of current 3.0.0. Preserve this history; ordinary execution reads the current
accepted route and needs no install. Canonical exporter/lock/slot checks pass;
the zero-finding authoring fixture above is separate. No zero-warning claim is
made for the retained inventory and no historical slot was removed from this PR.

## Projection, evidence reuse and remaining limits

The existing projector regenerated complete desired Instructions and receipt,
with 6,135 Unicode characters against the 8,000 budget; update was CHANGED and
subsequent check NO_OP. Sources are DISABLED. Authority inputs retain frozen
accepted `ec048fb39ae28cf2d747101466a603ddd062b1b0`; the receipt names the current
owner Decision and is consistency evidence, not acceptance. Shared generator/base
bytes and local binding remain unchanged. Root explicitly adopts IR for this
producer; the ChatGPT publication restriction is confined to local custom and
generated Instructions. No live Instructions/Sources were read/applied or model
compliance established; manual owner application/readback remains necessary.
The supported title tool and listing confirmed `Task 45 — Step 6 — Publisher and review`.

Git comparison with the starting head confirms both shared-publisher workflows,
staging/finalization mechanics, credential handling, example binding/probe,
existing production release entrypoint and shared ChatGPT tools are unchanged.
Existing sufficient Step 2/4 native atomicity/race/retry and transport proof is
reused for these unchanged invariants. Optional native transport skips above
are explicitly skips, not new passes. No gratuitous remote publication was run.

The production audit still checks inherited acceptance. Owner-disposed N2 is
documented/tested as a narrower offline candidate contract; no new approval/API
gate was introduced. The fresh independent reviewer must correct/supersede the
unsupported earlier blocking classification; the executor cannot self-approve.

The unprivileged Actions fixture does not execute production planning,
publication or the production summary; focused shell tests exercise the actual
no-code fallback. Real private caller permissions, destination credentials,
remote public publication, producer activation, Landscape integration, consumer
adoption and Windows/macOS shared-publisher operation remain unqualified and
outside this Step. Known squash-only portability and VibeVM path/cache/static
INDEX limitations retain their documented scope. CI/checks, source acceptance,
merge, public publication, consumer adoption and Task closure remain distinct.
