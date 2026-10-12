#!/usr/bin/env python3
"""Bounded Task 24 investigation; writes only disposable Linux fixtures and a report."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    vibe = args.vibe.resolve()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    digest = hashlib.sha256(vibe.read_bytes()).hexdigest()
    if digest != pin["linux_x86_64_musl_binary"]["sha256"]:
        raise ValueError("requires the pinned Linux musl VibeVM 1.0.7")
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    base = Path(tempfile.mkdtemp(prefix="task24-self-adoption-"))
    env = {k: v for k, v in os.environ.items() if k in {"PATH", "LANG", "LC_ALL", "TMPDIR"}}
    env.update(GIT_AUTHOR_NAME="Disposable fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Disposable fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")
    cases = []

    def git(work, *arguments):
        return subprocess.check_output(["git", "-c", "commit.gpgsign=false", "-c",
                                        "core.hooksPath=/nonexistent", *arguments],
                                       cwd=work, env=env, text=True).strip()

    def clone(name):
        work = base / name
        subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(ROOT), str(work)],
                       env=env, check=True, capture_output=True)
        git(work, "checkout", "-q", "--detach", revision)
        # Public synthetic overlay, with no production helper or authority claim.
        (work / "AGENTS.md").write_text("Task 24 disposable overlay.\n")
        return work

    def manifest(work, requirement):
        (work / "vibe.toml").write_text(
            '[workspace]\nmembers = ["packages/development-governance"]\n'
            '[project]\nname = "task24-fixture"\nversion = "0.0.0"\nspec_format = "mixed"\n'
            '[requires.packages]\n"org.jresearch.ai/development-governance" = ' + requirement + '\n')

    def run(work, command="install", registry=None, solver="resolvo"):
        settings = base / (work.name + "-settings")
        command_env = dict(env, VIBE_SETTINGS=str(settings), VIBEVM_USER_CONFIG=str(settings / "config.toml"))
        argv = [str(vibe), "--offline", "--json", command, "--path", str(work)]
        if command == "install":
            argv += ["--no-default-registry", "--assume-yes", "--solver", solver]
        if command == "update":
            argv += ["--all", "--assume-yes"]
        if registry:
            argv += ["--registry", str(registry)]
        result = subprocess.run(argv, env=command_env, capture_output=True, text=True, timeout=120)
        record = {"command": command, "solver": solver, "exit": result.returncode,
                  "stdout": result.stdout, "stderr": result.stderr}
        cases.append({"fixture": work.name, **record})
        return result

    for solver in ("resolvo", "naive", "sat"):
        work = clone("path-" + solver)
        manifest(work, '{ path = "packages/development-governance", version = "=1.2.0", link = "dynamic" }')
        (work / "packages/development-governance/vibevm/vibespecs/protocols/task-handoff.md").open("a").write(
            "\nTASK24_LOCAL_CANDIDATE_SENTINEL\n")
        result = run(work, solver=solver)
        if result.returncode == 0 or "ORDER-LAW" not in result.stderr:
            raise ValueError("pinned path-only limitation changed; reassess the design")

    work = clone("stable-tree-registry")
    manifest(work, '"=1.2.0"')
    if run(work, registry=work / "packages").returncode == 0:
        raise ValueError("stable-tree registry unexpectedly works; reassess the design")

    work = clone("registry-materialization")
    package = work / "packages/development-governance"
    registry = base / "registry"
    source_files = [Path(name).relative_to("packages/development-governance")
                    for name in git(work, "ls-files", "packages/development-governance").splitlines()]

    def seed(version):
        destination = registry / "org.jresearch.ai/development-governance" / ("v" + version)
        for relative in source_files:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(package / relative, target)
        return destination

    seed("1.2.0")
    manifest(work, '"=1.2.0"')
    if run(work, registry=registry).returncode:
        raise ValueError("ordinary local registry materialization failed")
    slot = work / "vibevm/vibedeps/org.jresearch.ai.development-governance/1.2.0"
    payload = {p.as_posix(): (package / p).read_bytes() for p in source_files}
    actual = {p.relative_to(slot).as_posix(): p.read_bytes() for p in slot.rglob("*") if p.is_file()}
    byte_equal = {k: v for k, v in actual.items() if k != ".vibe-slot.toml"} == payload
    if not byte_equal:
        raise ValueError("registry install altered the package payload")
    overlay_preserved = re.sub(r"<vibevm>.*?</vibevm>", "", (work / "AGENTS.md").read_text(),
                               flags=re.S).strip() == "Task 24 disposable overlay."
    initial_lock = (work / "vibe.lock").read_text()
    if run(work, registry=registry).returncode or (work / "vibe.lock").read_text() != initial_lock:
        raise ValueError("repeat install changed the lock or failed")
    git(work, "switch", "-q", "-c", "synthetic-ready-state")
    git(work, "add", "-A")
    git(work, "commit", "-qm", "Synthetic source and materialization together")
    first = git(work, "rev-parse", "HEAD")
    clean = base / "clean-committed-clone"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(work), str(clean)], env=env, check=True,
                   capture_output=True)
    clone_payload = {p.relative_to(clean / slot.relative_to(work)).as_posix(): p.read_bytes()
                     for p in (clean / slot.relative_to(work)).rglob("*") if p.is_file()}
    clean_ready = clone_payload == actual and (clean / "vibevm/vibespecs/boot/INDEX.md").is_file()
    if not clean_ready:
        raise ValueError("committed projection does not survive clean clone")

    # A compatible synthetic fixture update, never a public release/version mutation.
    source_manifest = package / "vibe.toml"
    source_manifest.write_text(source_manifest.read_text().replace('version = "1.2.0"', 'version = "1.2.1"'))
    protocol = package / "vibevm/vibespecs/protocols/task-handoff.md"
    protocol.write_text(protocol.read_text() + "\nTASK24_LOCAL_CANDIDATE_SENTINEL\n")
    seed("1.2.1")
    manifest(work, '"=1.2.1"')
    if run(work, registry=registry).returncode:
        raise ValueError("synthetic candidate update failed")
    new_slot = work / "vibevm/vibedeps/org.jresearch.ai.development-governance/1.2.1"
    candidate_materialized = b"TASK24_LOCAL_CANDIDATE_SENTINEL" in (
        new_slot / "vibevm/vibespecs/protocols/task-handoff.md").read_bytes()
    git(work, "add", "-A")
    git(work, "commit", "-qm", "Synthetic candidate source and projection together")
    second = git(work, "rev-parse", "HEAD")
    git(clean, "pull", "-q", "--ff-only")
    pull_together = git(clean, "rev-parse", "HEAD") == second and (
        clean / new_slot.relative_to(work) / "vibevm/vibespecs/protocols/task-handoff.md").read_bytes() == (
        new_slot / "vibevm/vibespecs/protocols/task-handoff.md").read_bytes()
    git(clean, "checkout", "-q", "--detach", first)
    rollback = (clean / slot.relative_to(work)).is_dir() and not (clean / new_slot.relative_to(work)).exists()
    git(clean, "checkout", "-q", "--detach", second)
    switch_forward = (clean / new_slot.relative_to(work)).is_dir() and not (clean / slot.relative_to(work)).exists()

    # Native check is evidence only; record actual mismatch detection and repair.
    installed_protocol = new_slot / "vibevm/vibespecs/protocols/task-handoff.md"
    original = installed_protocol.read_bytes()
    installed_protocol.write_bytes(original + b"CORRUPTED SLOT\n")
    corrupt_check = run(work, "check")
    corrupt_repair = run(work, registry=registry)
    corrupt_repaired = installed_protocol.read_bytes() == original
    installed_protocol.unlink()
    missing_check = run(work, "check")
    missing_repair = run(work, registry=registry)
    missing_repaired = installed_protocol.is_file() and installed_protocol.read_bytes() == original
    git(work, "restore", ".")
    index = work / "vibevm/vibespecs/boot/INDEX.md"
    index.unlink()
    missing_index_check = run(work, "check")
    index_retry = run(work, registry=registry)
    index_restored = index.is_file()
    lock = tomllib.loads(initial_lock)
    result = {"source_revision": revision, "vibevm_revision": pin["source_revision"],
              "binary_sha256": digest, "fixtures": str(base), "cases": cases,
              "observations": {"path_only_install": "BLOCKED on all three solvers",
                  "stable_source_as_registry": "BLOCKED", "registry_payload_byte_equal": byte_equal,
                  "human_overlay_preserved": overlay_preserved, "repeat_lock_unchanged": True,
                  "committed_clean_clone_readable_without_tools": clean_ready,
                  "candidate_materialized": candidate_materialized, "git_pull_moves_source_and_projection": pull_together,
                  "git_checkout_rollback": rollback, "git_checkout_forward": switch_forward,
                  "corrupt_slot_check_exit": corrupt_check.returncode, "corrupt_slot_retry_exit": corrupt_repair.returncode,
                  "corrupt_slot_repaired": corrupt_repaired, "missing_slot_check_exit": missing_check.returncode,
                  "missing_slot_retry_exit": missing_repair.returncode, "missing_slot_repaired": missing_repaired,
                  "missing_index_check_exit": missing_index_check.returncode, "missing_index_retry_exit": index_retry.returncode,
                  "missing_index_restored": index_restored,
                  "lock_package_provenance": lock["package"],
                  "synthetic_commits": [first, second]},
              "disposition": "Investigation only. No active implementation replacement or package/consumer publication."}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["observations"], indent=2))


if __name__ == "__main__":
    main()
