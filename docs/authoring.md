# Authoring and the bounded experiment

The root `vibe.toml` is a virtual authoring workspace with one independently
versioned member, `org.jresearch.ai/development-governance` v0.1.0. The root boot
file is an authoring-local pointer outside the exported shared package. The
member is `kind="flow"`,
`format="simple"`, `epoch=1`, and explicitly `publish=false`. It has no
dependencies or executable capability declarations. Repository scripts are
authoring/qualification utilities outside the package.

The package supports distinct passive native Skills declared in `vibe.toml`;
initially only `proportional-controls` is included. Its accepted instruction and
procedure bytes remain unchanged. There is one source for that detailed guidance:
`vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0/vibevm/vibespecs/skills/proportional-controls/references/protocol.md`.
Each declared Skill has its own directory and references, with the strict
`include = ["SKILL.md", "references/*.md"]` projection. Relative references stay
inside that directory so either export is self-contained. The one compact package
boot source, `vibevm/vibespecs/boot/development-governance.md`, routes to Skills;
it does not duplicate detailed policy. One package version covers the entire
declared Skill set. Later additions or changes require a new accepted package
version and explicit reviewed consumer maintenance, without adding a separate
VibeVM dependency for each rule group. Native skill discovery and JIT reading
are separate from VibeVM boot linkage; no context or time saving is claimed.

## Git/native-Skill baseline

Use a fresh clone and select a full source commit:

```sh
git clone https://github.com/jresearchsoftware/shared-governance.git
cd shared-governance
# For a local candidate check; consumers must select an independently accepted SHA.
source_sha="$(git rev-parse HEAD)"
git diff --check
python3 scripts/qualify.py --export-ref "$source_sha"
destination="$(mktemp -d)/proportional-controls"
python3 scripts/vendor-skill.py --ref "$source_sha" --skill proportional-controls --destination "$destination"
```

The bootstrap was independently accepted and squash-merged as
`aa1e18085dee2aa59e19c5939e882cd8084eea00` through
[PR 1](https://github.com/jresearchsoftware/shared-governance/pull/1).
For a new candidate check, select its exact PR head explicitly; this does not
make that candidate an accepted consumer source.
The exporter resolves the supplied local Git ref to a full commit, copies only
ordinary skill files plus MIT LICENSE, and writes `SOURCE.json` with source SHA,
path and per-file hashes. It refuses to overwrite a nonempty destination. It
uses no network or credentials. The receipt is generated metadata, not another
editable policy source.

`--skill` selects one declared passive Skill and defaults to
`proportional-controls`. The exporter also supports accepted historical
old-coordinate source commits for this unchanged baseline; the current
distribution preparer requires the new package coordinate at the selected full
SHA. Historical export does not authorize publication under the old coordinate.

No real consumer is modified by this example. A later consumer may export into
its project-local `.agents/skills/proportional-controls` under its own approved
migration, review the source/projection diff, and commit the source identity and
materialized bytes together. A rejected update retains the previous consumer
commit; rollback uses the consumer's ordinary reviewed Git revert. These are
baseline mechanics, not a consumer adoption qualification in this Task.

## Pinned VibeVM probe

Run on Linux x86_64. Python 3.11+, Git and curl are sufficient to prepare the
probe. Download the musl binary into a temporary directory, verify its pinned
SHA-256, and invoke it by absolute path. No global installation, `vibe init`,
user skill installation, registry service or package publication is needed.

```sh
tool_tmp="$(mktemp -d)"
curl --fail --location --output "$tool_tmp/vibe" \
  https://github.com/vibevm/vibevm/releases/download/v1.0.7/vibe-bootstrap-x86_64-unknown-linux-musl
printf '%s  %s\n' \
  20d111df02eb28040ef4cb766bfcb0bde8ff4427b031f88f33eacb3711c3e240 \
  "$tool_tmp/vibe" | sha256sum --check
chmod u+x "$tool_tmp/vibe"
python3 scripts/qualify-vibevm.py --vibe "$tool_tmp/vibe" --materialize
```

The probe copies tracked candidate bytes to a disposable native temporary
directory. It relocates VibeVM settings/cache through `VIBE_SETTINGS` and
`VIBEVM_USER_CONFIG`, without changing the user's home or global configuration.
It verifies the downloaded binary digest before execution, then:

1. Validates the virtual workspace and checks both root and member.
2. Projects every declared member Skill for `codex` with `scope=project`, only
   inside the disposable member; compares each complete file set and file's bytes.
3. Checks that member projection preserves root human-owned AGENTS.md.
4. For `--materialize`, adds a temporary project and an exact `"=0.1.0"`
   requirement, then installs from a clean tracked-byte copy in the explicit
   local source-tree registry (excluding generated native projections/receipts),
   offline with default registry disabled. No registry index is created.
5. Confirms installation preserves human-owned AGENTS.md outside VibeVM's
   single managed block. The source checkout itself is never materialized.

All command JSON, including check findings, is printed. `check` exit 0 alone
does not establish absence of warnings. The normal probe without `--materialize`
qualifies workspace/skill authoring only. It does not qualify dependency install.

The local source-tree registry is a transport test, not publication of the
workspace or proof that a remote consumer can address nested members using one
monorepo Git URL. A later publishing Task must qualify its exact distribution
path and lock/content identity independently.

## Observed evidence and limitations

Historical bootstrap probes on 2026-10-07 used the old-coordinate package,
Debian WSL on its native temporary filesystem, ordinary UID 1000, Python 3.11
and the hash-verified musl VibeVM `1.0.7` binary.
Workspace `validate`, root/member `check`, actual project-scope skill projection,
byte/file-set comparison and local-registry dependency installation succeeded.
Inspected VibeVM check JSON contained zero errors and warnings. The comparison
uses identical canonical prose; it does not invoke a model or qualify automatic
client skill selection. Two read-only reasoning probes distinguished free
secret-log hardening from an unauthorized expensive Markdown gate.

Material limits remain:

- The GNU binary requires `GLIBC_2.39` and failed to start on this Debian system.
  The same release's pinned musl artifact worked; this is tool/platform evidence,
  not a new mandatory consumer platform rule.
- A path-only requirement failed before materialization with `empty world /
  ORDER-LAW`. Pinned upstream's
  [empty-world predicate](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-orchestrator/src/install/mod.rs#L290)
  and [planner root union](https://github.com/vibevm/vibevm/blob/b6659978453f50e6d1d4d99626d70b980a2c5847/crates/vibe-install/src/plan.rs#L225)
  omit `path_packages`. This is pre-existing upstream behavior, not introduced
  by this source. The supported local-registry requirement succeeded. Reproduce
  the unsuccessful path form with `--materialize --path-source`; it is expected
  to return a failing exit status. No upstream workaround or tool patch is shipped.
- Virtual workspace `check` requires a root boot directory even without a
  project. A small authoring-local pointer satisfies it without adopting the
  upstream initializer's default hierarchy or WAL scaffolding.
- `validate` writes lease/lifecycle state, so the probe runs on copies. Install
  adds a managed AGENTS block in its fixture; this does not authorize generating
  or replacing a consumer's instructions.
- VibeVM is closed alpha without compatibility promises. Release/tag mutability
  requires verified content identity; a version string alone is insufficient.
- No remote package publication, update/rollback, warmed-cache/offline consumer
  maintenance, transitive-package review, real consumer adoption, automatic
  native client discovery, or measured context/operating-cost saving is proven.

The fresh-clone requirement here covers public source, ordinary source checks,
exact-commit native export and disposable local authoring probes. It does not
imply that a new consumer is already governed by the package.

## Comparison and next decision

| Property | Git/native Skill | VibeVM authoring experiment |
| --- | --- | --- |
| Semantic source | One reviewed Git commit and procedure | The same authoring source and procedure |
| Native payload | Exact skill bytes, LICENSE, source/hash receipt | Same skill bytes through native projection |
| Extra tooling | Git and Python standard library | Pinned VibeVM binary, manifest and transient state |
| Dependency transport | Local exact-commit export | Exact local-registry requirement works; path-only fails |
| Startup/detail split | Skill discovery plus local detail | Boot pointer plus the same native skill; prompt-load saving unmeasured |
| Consumer authority | Separate reviewed adoption | Separate reviewed adoption; graph grants no permissions |

This evidence supports continuing a bounded experiment. Choose a separate
repository-local publishing Task only when a real consumer and its desired
distribution path justify it; qualify immutable content and alpha recovery
there. The first consumer migration belongs to that consumer's own Task and
must remove the former canonical duplicate in the same reviewed transition.
The Git/native-Skill baseline already provides a simpler viable alternative.

[Task 2 distribution preparation](distribution.md) records accepted Step 1
disposable direct-Git publishing/consumer probes, integrity rejection and
bounded update/offline/rollback results. Step 2's source identity and declared
Skill set were independently accepted through
[PR 4](https://github.com/jresearchsoftware/shared-governance/pull/4) and
squash-merged as `60704ce3e0f0243d157646989429c6e621fc8f04`.
The [Step 3 preparation packet](task-2/step-3-preparation/README.md) provides
fresh local evidence for that accepted SHA and the proposed `jrs-vibevm`
publication boundary. Actual remote publication remains unqualified and
requires separate explicit admission in the live Issue.
