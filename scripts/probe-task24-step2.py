#!/usr/bin/env python3
"""Dated Task 24 Step 2 native dogfooding diagnostic; no production mutation."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = "96d26c51b6d05ee5ec4576a44f541b904f0f13fb"
PACKAGE = "org.jresearch.ai/development-governance"
SLOT = "vibevm/vibedeps/org.jresearch.ai.development-governance/1.2.0"
PROTOCOL = "vibevm/vibespecs/protocols/task-handoff.md"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    digest = hashlib.sha256(args.vibe.read_bytes()).hexdigest()
    if digest != pin["linux_x86_64_musl_binary"]["sha256"]:
        raise ValueError("requires pinned VibeVM 1.0.7 musl bytes")
    base = Path(tempfile.mkdtemp(prefix="task24-step2-native-"))
    env = {k: v for k, v in os.environ.items() if k in {"PATH", "LANG", "LC_ALL"}}
    env.update(GIT_AUTHOR_NAME="Disposable fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Disposable fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")
    cases, observations, generated = [], {}, {}

    def git(work, *argv):
        return subprocess.check_output(["git", "-c", "commit.gpgsign=false", "-c",
                                        "core.hooksPath=/nonexistent", *argv],
                                       cwd=work, env=env, text=True).strip()

    if git(args.upstream, "rev-parse", "HEAD") != pin["source_revision"]:
        raise ValueError("upstream checkout must match pinned source")

    def clone(source, name, revision=None):
        work = base / name
        git(base, "clone", "-q", "--no-hardlinks", str(source), str(work))
        if revision:
            git(work, "checkout", "-q", "--detach", revision)
        return work

    def run(work, label, command="install", registry=None, offline=True, no_prefer_local=False):
        settings = base / (work.name + "-settings")
        command_env = dict(env, VIBE_SETTINGS=str(settings),
                           VIBEVM_USER_CONFIG=str(settings / "config.toml"))
        argv = [str(args.vibe.resolve()), "--json", command, "--path", str(work)]
        if offline:
            argv += ["--offline"]
        if command == "install":
            argv += ["--no-default-registry", "--assume-yes"]
            if no_prefer_local:
                argv += ["--no-prefer-local"]
        elif command == "update":
            argv += ["--all", "--assume-yes"]
        if registry:
            argv += ["--registry", str(registry)]
        result = subprocess.run(argv, env=command_env, capture_output=True, text=True, timeout=120)
        cases.append(dict(label=label, argv=argv, exit=result.returncode,
                          stdout=result.stdout, stderr=result.stderr))
        return result

    def state(work, name):
        files = ["vibe.toml", "vibe.lock", "AGENTS.md", "vibevm/vibespecs/boot/INDEX.md",
                 "vibevm/vibespecs/boot/STATIC.md", SLOT + "/.vibe-slot.toml"]
        generated[name] = {p: (work / p).read_text() for p in files if (work / p).is_file()}

    upstream = clone(args.upstream, "upstream", pin["source_revision"])
    observations["upstream_checked_in_lock"] = (upstream / "vibe.lock").read_text()
    observations["upstream_declared_planning"] = tomllib.loads(
        (upstream / "vibe.toml").read_text())["requires"]["packages"][
            "flow:org.vibevm.world/multi-user-planning"]
    observations["upstream_retained_install_exit"] = run(
        upstream, "upstream retained checked-in lock", registry=upstream / "vibevm/vibepacks").returncode
    # Remove only these generated artifacts in our newly created disposable clone.
    for relative in ("vibevm/vibedeps", "vibe.lock", "vibevm/vibespecs/boot/INDEX.md",
                     "vibevm/vibespecs/boot/STATIC.md"):
        target = upstream / relative
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
    observations["upstream_cold_install_exit"] = run(
        upstream, "upstream cold actual root", registry=upstream / "vibevm/vibepacks").returncode
    observations["upstream_cold_lock"] = (upstream / "vibe.lock").read_text() if (
        upstream / "vibe.lock").exists() else None
    observations["upstream_generated_index"] = (upstream / "vibevm/vibespecs/boot/INDEX.md").read_text()

    spec = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare-distribution.py")
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    payload, receipt = preparation.snapshot(ACCEPTED)
    observations["canonical_export_receipt"] = receipt

    def manifest(work, mode="static-transitive", version="^1.2.0", requirement=None):
        text = ('[workspace]\nmembers = ["packages/development-governance"]\n'
                '[project]\nname = "task24-step2-fixture"\nversion = "0.0.0"\nspec_format = "mixed"\n')
        if requirement:
            text += '[requires.packages]\n"flow:' + PACKAGE + '" = ' + requirement + '\n'
        else:
            text += '[requires.packages."flow:' + PACKAGE + '"]\nversion = "' + version + '"\nlink = "' + mode + '"\n'
        (work / "vibe.toml").write_text(text)

    def producer(name, mode="static-transitive", version="^1.2.0"):
        work = clone(ROOT, name, ACCEPTED)
        (work / "AGENTS.md").write_text("Task 24 Step 2 human overlay.\n")
        # This representation tests ready native file routing, not the production helper.
        (work / "vibevm/vibespecs/boot/00-authoring.md").write_text(
            "Task 24 Step 2 public synthetic authoring overlay. Read applicable installed guidance.\n")
        registry = work / "vibevm/vibepacks"
        source = registry / PACKAGE / "v1.2.0"
        for relative, data in payload.items():
            target = source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        manifest(work, mode, version)
        return work, registry, source

    for mode in ("static-transitive", "dynamic"):
        work, registry, source = producer("producer-" + mode, mode)
        result = run(work, "producer cold " + mode, registry=registry)
        observations[mode + "_install_exit"] = result.returncode
        if result.returncode:
            raise ValueError("versioned registry adaptation failed: " + mode)
        preparation.verify(ACCEPTED, work / SLOT, installed=True)
        observations[mode + "_canonical_payload_verified"] = True
        observations[mode + "_overlay_preserved"] = re.sub(
            r"<vibevm>.*?</vibevm>", "", (work / "AGENTS.md").read_text(), flags=re.S
        ).strip() == "Task 24 Step 2 human overlay."
        state(work, "producer-" + mode)
        boot_path = (work / "vibevm/vibespecs/boot/STATIC.md") if mode == "static-transitive" else (work / SLOT / "vibevm/vibespecs/boot/development-governance.md")
        observations[mode + "_literal_relative_protocol_links_resolve"] = all(
            (boot_path.parent / p).is_file() for p in re.findall(r"\]\((\.\./protocols/[^)]+)\)", boot_path.read_text()))
    # Independent variation: typed path dependency with static-transitive link.
    path_work, _, _ = producer("typed-path-static")
    manifest(path_work, requirement='{ path = "packages/development-governance", version = "=1.2.0", link = "static-transitive" }')
    observations["typed_path_static_exit"] = run(path_work, "typed path static-transitive").returncode

    work = base / "producer-static-transitive"
    registry = work / "vibevm/vibepacks"
    first_lock = (work / "vibe.lock").read_bytes()
    run(work, "producer repeat", registry=registry)
    observations["repeat_lock_unchanged"] = (work / "vibe.lock").read_bytes() == first_lock
    first_identity = tomllib.loads(first_lock.decode())
    repeated_identity = tomllib.loads((work / "vibe.lock").read_text())
    for item in (first_identity, repeated_identity):
        item["meta"].pop("generated_at", None)
    observations["repeat_lock_identity_equal_except_timestamp"] = first_identity == repeated_identity
    git(work, "switch", "-q", "-c", "synthetic-ready")
    git(work, "add", "-A")
    git(work, "commit", "-qm", "Synthetic source and native projection together")
    first = git(work, "rev-parse", "HEAD")
    clean = clone(work, "clean-committed")
    preparation.verify(ACCEPTED, clean / SLOT, installed=True)
    observations["clean_clone_slot_and_index_readable_without_tools"] = (clean / "vibevm/vibespecs/boot/INDEX.md").is_file()

    # Moving removes the original recorded registry URI, without modifying the lock by hand.
    moved = base / "moved-producer"
    work.rename(moved)
    work = moved
    registry = work / "vibevm/vibepacks"
    observations["old_recorded_registry_exists"] = (base / "producer-static-transitive").exists()
    observations["moved_retained_install_exit"] = run(work, "moved retained install", registry=registry).returncode
    observations["moved_retained_update_exit"] = run(work, "moved retained update", "update", registry).returncode
    observations["move_lock_unchanged"] = (work / "vibe.lock").read_bytes() == first_lock
    state(work, "moved-retained")
    absent = clone(work, "moved-missing-slot")
    shutil.rmtree(absent / SLOT)
    observations["moved_missing_slot_install_exit"] = run(
        absent, "moved missing slot", registry=absent / "vibevm/vibepacks").returncode
    observations["moved_missing_slot_restored"] = (absent / SLOT / PROTOCOL).exists()
    if observations["moved_missing_slot_restored"]:
        preparation.verify(ACCEPTED, absent / SLOT, installed=True)
        observations["moved_missing_slot_canonical_verified"] = True
    state(absent, "moved-missing-slot-repaired")

    # A candidate source edit with a version advance, committed with its materialization.
    source = registry / PACKAGE / "v1.2.1"
    updated = dict(payload)
    updated["vibe.toml"] = updated["vibe.toml"].replace(b'1.2.0', b'1.2.1')
    updated[PROTOCOL] += b"\nTASK24_STEP2_CANDIDATE_SENTINEL\n"
    # This is synthetic source, not a forged production distribution receipt.
    updated.pop("DISTRIBUTION.json")
    for relative, data in updated.items():
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    package = work / "packages/development-governance"
    (package / "vibe.toml").write_bytes(updated["vibe.toml"])
    (package / PROTOCOL).write_bytes(updated[PROTOCOL])
    observations["caret_update_exit"] = run(work, "caret deliberate candidate update", "update", registry).returncode
    new_slot = work / SLOT.replace("1.2.0", "1.2.1")
    observations["caret_update_candidate_materialized"] = (new_slot / PROTOCOL).exists() and b"TASK24_STEP2_CANDIDATE_SENTINEL" in (new_slot / PROTOCOL).read_bytes()
    # Do not assume caret update advances a retained local-registry lock.
    manifest(work, version="=1.2.1")
    observations["exact_candidate_install_exit"] = run(work, "explicit exact candidate install", registry=registry).returncode
    if not (new_slot / PROTOCOL).exists():
        raise ValueError("explicit candidate materialization unavailable; retain fixture")
    git(work, "add", "-A")
    git(work, "commit", "-qm", "Synthetic candidate source and native projection together")
    second = git(work, "rev-parse", "HEAD")
    git(clean, "remote", "set-url", "origin", str(work))
    git(clean, "pull", "-q", "--ff-only")
    observations["pull_advances_source_and_projection"] = git(clean, "rev-parse", "HEAD") == second and (clean / new_slot.relative_to(work) / PROTOCOL).read_bytes() == updated[PROTOCOL]
    git(clean, "checkout", "-q", "--detach", first)
    preparation.verify(ACCEPTED, clean / SLOT, installed=True)
    observations["checkout_rollback_verified"] = not (clean / new_slot.relative_to(work)).exists()
    git(clean, "checkout", "-q", "--detach", second)
    observations["checkout_forward_verified"] = (clean / new_slot.relative_to(work) / PROTOCOL).read_bytes() == updated[PROTOCOL]
    observations["synthetic_commits"] = [first, second]
    state(work, "candidate-updated")

    integrity = base / "producer-dynamic"
    for damage in ("corrupt", "missing"):
        target = integrity / SLOT / PROTOCOL
        if damage == "corrupt":
            target.write_bytes(payload[PROTOCOL] + b"CORRUPTED\n")
        else:
            target.unlink()
        observations[damage + "_native_check_exit"] = run(integrity, damage + " native check", "check").returncode
        observations[damage + "_retry_exit"] = run(integrity, damage + " retry", registry=integrity / "vibevm/vibepacks").returncode
        try:
            preparation.verify(ACCEPTED, integrity / SLOT, installed=True)
            observations[damage + "_existing_exporter_error"] = None
        except ValueError as error:
            observations[damage + "_existing_exporter_error"] = str(error)
        target.write_bytes(payload[PROTOCOL])
    index = integrity / "vibevm/vibespecs/boot/INDEX.md"
    index.unlink()
    observations["missing_index_native_check_exit"] = run(integrity, "missing index check", "check").returncode
    observations["git_file_existence_detects_missing_index"] = not index.is_file()
    run(integrity, "missing index retry", registry=integrity / "vibevm/vibepacks")
    observations["missing_index_retry_restored"] = index.is_file()

    # Task 22 used a single-package Git export. Try the actual nested producer root.
    nested_source = clone(ROOT, "nested-source-mirror", ACCEPTED)
    git(nested_source, "tag", "fixture-accepted")
    for layout, repository in (("nested", nested_source), ("exported", base / "single-package-export")):
        if layout == "exported":
            repository.mkdir()
            for relative, data in payload.items():
                target = repository / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            git(repository, "init", "-q", "-b", "main")
            git(repository, "add", ".")
            git(repository, "commit", "-qm", "Disposable accepted-source export")
            git(repository, "tag", "v1.2.0")
        tag = "fixture-accepted" if layout == "nested" else "v1.2.0"
        direct = clone(ROOT, "direct-git-" + layout, ACCEPTED)
        (direct / "AGENTS.md").write_text("Task 24 direct Git disposable overlay.\n")
        if layout == "nested":
            manifest(direct, requirement='{ version = "=1.2.0", git = "' + repository.resolve().as_uri() + '", rev = "' + ACCEPTED + '", auth = "none" }')
            observations["direct_git_local_raw_sha_exit"] = run(
                direct, "direct Git local raw SHA preflight", no_prefer_local=True).returncode
        manifest(direct, requirement='{ version = "=1.2.0", git = "' + repository.resolve().as_uri() + '", tag = "' + tag + '", auth = "none", link = "dynamic" }')
        observations["direct_git_" + layout + "_exit"] = run(direct, "direct Git " + layout).returncode
        observations["direct_git_" + layout + "_initial_lock"] = (direct / "vibe.lock").read_text() if (direct / "vibe.lock").exists() else None
        # The actual producer also retains historical v0.1.0 under vibepacks.
        # Keep its initial precedence result, then isolate direct Git using the supported flag.
        for relative in ("vibe.lock", "vibevm/vibedeps"):
            target = direct / relative
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
        observations["direct_git_" + layout + "_no_local_exit"] = run(
            direct, "direct Git " + layout + " no-prefer-local", no_prefer_local=True).returncode
        observations["direct_git_" + layout + "_no_local_lock"] = (direct / "vibe.lock").read_text() if (direct / "vibe.lock").exists() else None
        if layout == "exported" and (direct / SLOT).exists():
            preparation.verify(ACCEPTED, direct / SLOT, installed=True)
            observations["direct_git_exported_verified"] = True
            state(direct, "direct-git-exported")
            for relative, data in updated.items():
                target = repository / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            (repository / "DISTRIBUTION.json").unlink()
            git(repository, "add", "-A")
            git(repository, "commit", "-qm", "Disposable candidate Git export")
            git(repository, "tag", "v1.2.1")
            # Update exposes no --no-prefer-local; remove only fixture-local historical precedence.
            (direct / "vibevm/vibepacks").rename(base / "direct-exported-retained-history")
            manifest(direct, requirement='{ version = "=1.2.1", git = "' + repository.resolve().as_uri() + '", tag = "v1.2.1", auth = "none", link = "dynamic" }')
            observations["direct_git_exported_update_exit"] = run(direct, "direct Git exported update", "update").returncode
            observations["direct_git_exported_update_payload_equal"] = (direct / new_slot.relative_to(work) / PROTOCOL).is_file() and (direct / new_slot.relative_to(work) / PROTOCOL).read_bytes() == updated[PROTOCOL]
            installed_files = {p.relative_to(direct / new_slot.relative_to(work)).as_posix(): p.read_bytes()
                               for p in (direct / new_slot.relative_to(work)).rglob("*") if p.is_file()
                               and p.name != ".vibe-slot.toml"}
            observations["direct_git_exported_update_complete_payload_equal"] = installed_files == updated
            state(direct, "direct-git-updated")
    result = dict(accepted_source_main=ACCEPTED, starting_candidate=git(ROOT, "rev-parse", "HEAD"),
                  vibevm_source=pin["source_revision"], binary_sha256=digest,
                  fixture=str(base), observations=observations, generated=generated, cases=cases,
                  scope="Disposable Linux fixture. No active helper replacement, publication, consumer change or independent acceptance.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in observations.items() if not isinstance(v, (dict, list)) and len(str(v)) < 400}, indent=2))


if __name__ == "__main__":
    main()
