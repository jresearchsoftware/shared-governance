# Local qualification

All checks below ran on the committed implementation candidate in an owned,
clean Git-bundle checkout. The SHA is a candidate input for qualification, not
an independently accepted authority claim. Later changes only add this evidence.
The exact final head still requires independent assessment and native CI through
the trusted publication path.

| Check | Result |
| --- | --- |
| `git diff --check` | PASS |
| `python3 scripts/qualify.py --export-ref HEAD` | PASS: 1494 tracked files, 4048 local links; bounded credential-marker scan and exact public export/native projection |
| `python3 scripts/test-self-adoption.py` | PASS: 19 tests, including new Landscape corruption/removal, pin and route drift rejection/recovery |
| `python3 scripts/test-distribution.py` | PASS: 52 tests |
| `python3 scripts/test-release.py` | PASS: 20 executed; 6 optional native publisher integration tests skipped (no `--vibe`; this Task does not change publication) |
| Pinned native cold and repeat install in staging | PASS: four-package closure; repeat offline reuse |
| Pinned native offline `check` / `validate` in staging | PASS; zero findings / no executable contributions |
| Clean candidate with empty settings/cache, no install | PASS: native offline validate and check; clean Git worktree |
| Clean accepted source with no install | PASS: full native integrity/file reads, offline validate and check |
| Accepted versus delivered candidate native check | IDENTICAL: 0 errors, 14 historical-slot orphan warnings; intentionally retained under self-adoption, not deleted |
| Complete effective ChatGPT Instructions | PASS: `check` against committed candidate full SHA returned schema-4 `NO_OP`, no diffs; Sources disabled, `live_settings_verified=false` |
| Existing package source/slots/Skill and historical slots | Unchanged in the Task-owned diff; original Governance/Relay hashes and Relay revision preserved |
| Public tag/receipt identity | PASS: both tag/peeled commits, exact frozen manifests, complete inventory and canonical receipt digest |
| Conditional policy cases | Full-source scenario assessment in README; no runtime/subagent launch or profile-telemetry claim |

Exact projector invocation on the candidate:

```sh
python3 scripts/project-chatgpt.py check --repository . --binding chatgpt/binding.json --accepted-sha fff1afd49468fc5e7c6fc3225504f2a9670c3a47 --authority-anchor https://github.com/jresearchsoftware/shared-governance/issues/96
```

No effective Instructions bytes changed; no new full replacement/application is
needed for this integration. This is not live application evidence and does not
discharge earlier gaps. If accepted continuation changes generation inputs/text,
reconcile the full accepted replacement under the existing manual procedure.

Native host installed-runtime proof, PR/Outcome publication, independent acceptance
and authorized integration remain with trusted Writer/CI/reviewer continuation.
No privilege escalation, GitHub credential use or protected remote mutation occurred.
The original source checkout's collector-owned Git directory refused direct clone;
a local bundle supplied the owned clean fixture without permission/config changes.
Root export qualification also found its disposable destination inside the source
under the launch TMPDIR; running it in the nested owned fixture put generated
exports outside that fixture's source tree, satisfying the existing exporter rule.
Neither limitation was bypassed or misreported as a successful original command.

All useful task changes and selected evidence are committed. The pre-existing
untracked `.codex-sandbox/` contains launcher-owned state and this Step's isolated
fixtures. It remains outside the task commits; unrelated launcher content and
permissions are untouched. Disposable task fixtures are removed after final
qualification; useful qualification logs are preserved here.
