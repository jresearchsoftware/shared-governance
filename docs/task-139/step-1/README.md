# Task 139 Step 1 qualification

[Task 139](https://github.com/jresearchsoftware/shared-governance/issues/139)
binds this work to independently accepted source
`f51fd0ab22ff61fab48bd1e5af96918d77af1ec6`. The exact-label Small Improvements
scan found no open candidates.

## Published identities

The [toolchain pin](../../../toolchain/vibevm.json) records the mutable VibeVM
[v1.0.12 release](https://github.com/vibevm/vibevm/releases/tag/v1.0.12),
its tagged commit, manifest asset and three selected assets. The complete
manifest's SHA-256 matched the charter and release API. Its five platform
rows matched the API's asset name, size and SHA-256 for all bootstraps and
bundles. The selected musl bootstrap, GNU bootstrap and GNU bundle were
individually verified as downloads. The initial GNU responses from the
unqualified browser URLs had different digests. Both a fresh request and the
asset-ID endpoint independently returned the expected bytes for each GNU asset.

| Landscape flow | Peeled distribution commit | Distribution payload SHA-256 |
| --- | --- | --- |
| [Model guidance v1.1.0](https://github.com/jrs-vibevm/org.jresearch.ai.landscape-model-guidance/tree/v1.1.0) | `a810317f87fb4378be19edb04506444553f60148` | `f91d17bdb391f194eabcf46d5318fb87023e0c7686e2f5a9b0d65becddfddba7` |
| [Subagents v1.1.0](https://github.com/jrs-vibevm/org.jresearch.ai.landscape-subagents/tree/v1.1.0) | `b3e9da5a10af2b258699e7d1667dc925d247ae8d` | `23db5fe37bad3cc4cd5705b7bf47ed7b5940b5f63d3e6dcc24a8df589c7d030d` |

Both annotated public tags peeled to the admitted commits. Verification
covered each receipt's complete file inventory, per-file SHA-256, aggregate
digest and package-local links. Cold native Git acquisition produced the
same bytes and the same content hashes independently calculated for the lock.

The flows retain frozen passive epoch-1 manifests, no dependencies or Skill
declarations, and their same conditional routes. Ordinary and complex new
recommendations start at GPT-6.2 Sol/medium. Higher efforts require a
specific need, and GPT-6.1 Sol/medium remains a consumer-selected fallback
for new work when GPT-6.2 is unavailable. Existing allowlists, model limits,
clients, explicit helper permission and admitted profiles still govern. With
Subagents Off or local permission absent, the subagent boot skips full policy.
Permitted substantial work follows the adopted policy and may use zero helpers
when delegation would add no value. Helpers supply evidence within their
assignment. The separate independent assessment still owns acceptance.

## Materializer and projection

- Removing `[hooks]` and the lifecycle JSON `hooks` field leaves the hook-free
  manifests and actual JSON readers compatible. Probe readers use exit status
  or fields such as `ok`, `findings`, `summary` and `skills`.
  [Upstream break 013](https://github.com/vibevm/vibevm/blob/v1.0.12/formats/breaks/013.md)
- The mixed graph remains in lock schema 7 and FLOW epoch 1. The generated
  lock now includes exact requirement text on all four root edges and an
  explicit resolved commit for each Git source. The producer qualifier binds
  these fields and requires Relay's sole Shared edge to select 12.5.0.
  Higher lock epochs serve other graph features.
  [Upstream lock writer](https://github.com/vibevm/vibevm/blob/v1.0.12/crates/vibe-core/src/manifest/lockfile/configuration.rs)
- The generated root router moved to the front and contains optional personal,
  override and memory routes, lane receipts and a quiet clause. The authored
  project scope governs all three root entrypoints and preserves the accepted
  project-only boot. Root install leaves the member's narrower route/index
  bytes intact. Both Landscape entries stay static in the index and their
  installed boot files still conditionally route to full policy.
  [Upstream router](https://github.com/vibevm/vibevm/blob/v1.0.12/crates/vibe-workspace/src/boot_artifacts/redirect/router.rs)
- Skill projection migrates the portable schema-1 receipt to local schema-4
  state with an absolute path under ignored `.vibe/`. Keep the verified
  portable seed with the projected Skill in Git to support fresh clones.
  Retain the local state within its disposable qualification workspace.
  [Upstream migration](https://github.com/vibevm/vibevm/blob/v1.0.12/crates/vibe-agent-projection/src/pkgskill/receipt/activation.rs)
- VibeVM-owned Git data checkouts now normalize bytes without the user's
  `autocrlf` or tree EOL conversion. The producer already tracks LF.
  This qualification ran on Linux. The Windows-specific behavior was inspected
  in source. [Upstream Git normalization](https://github.com/vibevm/vibevm/commit/6e9b1c8e5)

## Combined evidence

- `qualify-toolchain.py` used a clean clone and isolated home/settings. The
  native Git trace shows direct clones from all three pinned Git origins.
  Cold resolution matched the complete committed lock after accounting for the
  local registry path and generation time. Repeat install preserved generated
  bytes. The qualifier checked both indexes, all selected slots and receipts,
  the 13 Skill files and ten shared protocol routes. The three member
  entrypoints and 30 historical slots were preserved.
- Native Skill listing returned Codex Relay 10.0.0 as the single Skill. Dry run
  and apply used the existing portable seed, and repeat apply held the local
  receipt byte-for-byte. A separate blank projection on a disposable clone
  returned `would-create` then `created` and produced the same Skill bytes.
  The probe confirmed that an unowned existing target is refused.
- Native root check reported zero errors, 30 retained-slot orphan warnings
  and three `redirect_block` warnings. The latter name the existing member
  entrypoints, which downward-discovering clients may concatenate. Member check
  reported zero findings. Root boot scope remains project-only through its
  authored entrypoints. Retained-slot boot repair also reported stale AI-native
  specification authority in the fixture, with offline boot reconstruction
  verified independently.
- `qualify-distribution.py` exercised a local bare Git remote. Ordinary install
  held the verified bytes after a disposable tag was moved. Fresh acquisition
  of the drifted tag was rejected by the canonical verifier. With the origin
  unavailable, retained-slot repair and cached offline install both worked.
  Plain update refused the held direct-tag source after a deliberate version
  change. Fresh staging resolution installed the new exact tag and complete
  Git rollback restored the verified original. The registry fixture separately
  verified targeted update through `vibe update` and held-version refusal
  through ordinary install.
- Exact-commit export and the release transition check classified this as
  **no exported package impact**. Development Governance remains 12.5.0.
  Its authored/exported content, in-tree registry and installed slot are byte
  identical to the accepted baseline. Relay 10.0.0 and its portable projection
  are byte identical, including the nested inert publisher closure. Local
  publisher tests exercised idempotence, competing writes and tag collision
  using disposable remotes.
- The canonical ChatGPT projector reports `NO_OP`. The complete generated
  file has SHA-256
  `98ce5976b0e2a6500d5939e3f064a34563f1684e91f515441e59806ae141db3a`
  at accepted baseline and candidate. This change creates no live application
  duty. Historical live Settings remain unverified. A separate synthetic
  consumer proved installation and the versioned projector before and after
  fresh tag resolution with its authored customization preserved.

The runtime proof used unprivileged Linux x86_64 musl. The GNU bundle's
component and source archive digests matched the manifest. The GNU bootstrap
reported its version with a weak `GLIBC_2.39` diagnostic on glibc 2.36. Windows,
macOS, installed privileged runtime, live client boot and account/model
availability remain unverified. No global registry, live Settings or production
state was touched. Writer owns publication and native Ready transition, followed
by exact-head Direct assessment.
