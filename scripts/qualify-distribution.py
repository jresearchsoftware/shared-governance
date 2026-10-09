#!/usr/bin/env python3
"""Probe package preparation and pinned VibeVM Git acquisition in disposable Linux fixtures."""
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
SOURCE = "aa1e18085dee2aa59e19c5939e882cd8084eea00"
COORDINATE = "org.jresearch.governance/proportional-controls"
SLOT = "vibevm/vibedeps/org.jresearch.governance.proportional-controls/0.1.0"
SKILL = "vibevm/vibespecs/skills/proportional-controls"


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", type=Path, required=True, help="exact pinned Linux x86_64 musl binary")
    parser.add_argument("--source-ref", default=SOURCE, help="full canonical package source commit")
    args = parser.parse_args()
    vibe = args.vibe.resolve()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    require(hashlib.sha256(vibe.read_bytes()).hexdigest() == pin["linux_x86_64_musl_binary"]["sha256"],
            "VibeVM binary differs from pinned musl bytes")
    preparation = module("preparation", "prepare-distribution.py")
    vendor = module("vendor", "vendor-skill.py")
    with tempfile.TemporaryDirectory(prefix="shared-governance-distribution-") as temporary:
        fixture = Path(temporary)
        env = {key: value for key, value in os.environ.items() if key in {"PATH", "LANG", "LC_ALL", "TMPDIR"}}
        env.update(VIBE_SETTINGS=str(fixture / "settings"),
                   VIBEVM_USER_CONFIG=str(fixture / "settings/config.toml"),
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null", GIT_TERMINAL_PROMPT="0",
                   GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                   GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
        commands = []

        def git(path, *arguments):
            result = subprocess.run(["git", "-C", str(path), *arguments], env=env,
                                    capture_output=True, text=True, timeout=30, check=True)
            return result.stdout.strip()

        def run(path, *arguments, success=True, settings=None):
            command_env = dict(env)
            if settings:
                command_env.update(VIBE_SETTINGS=str(settings), VIBEVM_USER_CONFIG=str(settings / "config.toml"))
            target = [str(path)] if arguments[0] == "reinstall" else ["--path", str(path)]
            result = subprocess.run([str(vibe), "--json", *arguments, *target],
                                    env=command_env, capture_output=True, text=True, timeout=120)
            commands.append({"arguments": list(arguments), "exit": result.returncode})
            print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip())
            require((result.returncode == 0) == success, "unexpected VibeVM result: " + " ".join(arguments))
            if arguments[0] == "check" and success:
                report = json.loads(result.stdout)
                require(report["summary"]["error"] == 0 and report["summary"]["warning"] == 0
                        and not report["findings"], "VibeVM check reported findings")
            return result

        distribution = fixture / "distribution"
        receipt = preparation.prepare(args.source_ref, distribution)
        remote = fixture / "distribution.git"
        git(fixture, "init", "--bare", "-b", "main", str(remote))
        preparation.verify(args.source_ref, distribution)
        run(distribution, "registry", "publish", str(distribution), "--repo-url", remote.as_uri(), "--dry-run")
        require(not git(remote, "for-each-ref"), "dry-run mutated remote refs")
        run(distribution, "registry", "publish", str(distribution), "--repo-url", remote.as_uri())
        revision = git(remote, "rev-parse", "v0.1.0^{commit}")
        refs = git(remote, "for-each-ref")
        run(distribution, "registry", "publish", str(distribution), "--repo-url", remote.as_uri())
        require(git(remote, "for-each-ref") == refs, "identical republish changed refs")

        def consumer(name):
            path = fixture / name
            path.mkdir()
            (path / "vibe.toml").write_text('[project]\nname = "disposable-consumer"\nversion = "0.0.0"\nspec_format = "mixed"\n'
                + '\n[requires.packages]\n"' + COORDINATE + '" = { version = "=0.1.0", git = "'
                + remote.as_uri() + '", tag = "v0.1.0", auth = "none" }\n')
            (path / "AGENTS.md").write_text("Human-owned fixture instructions.\n")
            return path

        first = consumer("consumer")
        run(first, "install", "--no-default-registry", "--assume-yes")
        preparation.verify(args.source_ref, first / SLOT, installed=True)
        lock = tomllib.loads((first / "vibe.lock").read_text())
        expected_hash = preparation.vibe_hash(preparation.snapshot(args.source_ref)[0])
        require(lock["package"][0]["content_hash"] == expected_hash, "lock hash differs from canonical package")
        run(first, "install", "--no-default-registry", "--assume-yes")
        preparation.verify(args.source_ref, first / SLOT, installed=True)
        run(first, "skill", "install", "--agent", "codex", "--scope", "project",
            "--skill", "proportional-controls", "--yes")
        baseline = fixture / "native-skill"
        vendor.export(args.source_ref, baseline)
        projected = first / ".agents/skills/proportional-controls"
        expected = {p.relative_to(distribution / SKILL).as_posix() for p in (distribution / SKILL).rglob("*") if p.is_file()}
        actual = {p.relative_to(projected).as_posix() for p in projected.rglob("*") if p.is_file()}
        require(expected == actual, "native VibeVM file set differs")
        for relative in expected:
            require((projected / relative).read_bytes() == (baseline / relative).read_bytes(), "native skill bytes differ")
        agents = (first / "AGENTS.md").read_bytes()
        require(len(re.findall(rb"<vibevm>.*?</vibevm>", agents, flags=re.S)) == 1,
                "expected one managed AGENTS block")
        require(re.sub(rb"<vibevm>.*?</vibevm>", b"", agents, flags=re.S).strip() == b"Human-owned fixture instructions.",
                "human-owned AGENTS content changed")
        run(first, "check")
        preparation.verify_consumer(args.source_ref, first)
        git(first, "init", "-b", "main")
        git(first, "add", "AGENTS.md", "vibe.toml", "vibe.lock", "vibevm", ".agents")
        git(first, "commit", "-m", "Disposable complete materialized baseline")
        baseline_revision = git(first, "rev-parse", "HEAD")
        second = consumer("independent-consumer")
        cold_settings = fixture / "independent-settings"
        run(second, "install", "--no-default-registry", "--assume-yes", settings=cold_settings)
        run(second, "skill", "install", "--agent", "codex", "--scope", "project",
            "--skill", "proportional-controls", "--yes", settings=cold_settings)
        preparation.verify_consumer(args.source_ref, second)

        # Default file:// Git archive does not serve arbitrary commit IDs.
        by_revision = consumer("revision-consumer")
        manifest = by_revision / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('tag = "v0.1.0"', 'rev = "' + revision + '"'))
        failure = run(by_revision, "install", "--no-default-registry", "--assume-yes", success=False)
        require("git archive" in failure.stderr and "no such ref" in failure.stderr,
                "file Git revision failure differs from the known transport restriction")

        unavailable = fixture / "unavailable.git"
        remote.rename(unavailable)
        try:
            run(first, "reinstall", "--offline")
            preparation.verify_consumer(args.source_ref, first)
            failure = run(second, "install", "--offline", "--no-default-registry", "--assume-yes",
                          success=False, settings=cold_settings)
            require("remote repository `vibe.toml` not found" in failure.stderr,
                    "offline install failure differs from the remote-manifest limitation")
            run(second, "clean", "--offline", settings=cold_settings)
            failure = run(second, "reinstall", "--offline", success=False, settings=cold_settings)
            require("tree is incomplete" in failure.stderr and "slot missing" in failure.stderr,
                    "offline reinstall failure differs from the missing-slot limitation")
            failure = run(second, "reinstall", "--offline", "--force", success=False, settings=cold_settings)
            require("remote repository `vibe.toml` not found" in failure.stderr,
                    "forced offline reinstall failure differs from the remote-manifest limitation")
        finally:
            unavailable.rename(remote)

        # Deliberately drift a disposable tag. This is an upstream failure probe,
        # never a permitted change to an actual public package/version.
        readme = distribution / "README.md"
        original_readme = readme.read_bytes()
        readme.write_bytes(original_readme + b"\nDisposable tag-drift probe.\n")
        try:
            preparation.verify(args.source_ref, distribution)
        except ValueError:
            pass
        else:
            raise ValueError("prepublication verifier accepted changed bytes")
        run(distribution, "registry", "publish", str(distribution), "--repo-url", remote.as_uri())
        require(git(remote, "rev-parse", "v0.1.0^{commit}") != revision, "tag drift was not exercised")
        run(first, "install", "--no-default-registry", "--assume-yes")
        drift_lock = tomllib.loads((first / "vibe.lock").read_text())["package"][0]
        require(drift_lock["content_hash"] != expected_hash, "expected upstream lock drift was not observed")
        preparation.verify(args.source_ref, first / SLOT, installed=True)  # Slot still has old bytes.
        try:
            preparation.verify_consumer(args.source_ref, first)
        except ValueError:
            pass
        else:
            raise ValueError("canonical consumer verifier accepted lock/slot split")
        run(first, "check")  # Check does not detect the demonstrated split.
        drifted = consumer("drifted-consumer")
        run(drifted, "install", "--no-default-registry", "--assume-yes", settings=fixture / "drift-settings")
        try:
            preparation.verify(args.source_ref, drifted / SLOT, installed=True)
        except ValueError:
            pass
        else:
            raise ValueError("canonical verifier accepted freshly acquired drifted content")

        # Only temporary version metadata changes: no second authored package.
        readme.write_bytes(original_readme)
        package_manifest = distribution / "vibe.toml"
        package_manifest.write_text(package_manifest.read_text().replace('version = "0.1.0"', 'version = "0.1.1"'))
        run(distribution, "registry", "publish", str(distribution), "--repo-url", remote.as_uri())
        manifest = first / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('=0.1.0', '=0.1.1').replace('v0.1.0', 'v0.1.1'))
        run(first, "update", "--all", "--assume-yes")
        upgraded = first / SLOT.replace("0.1.0", "0.1.1")
        require(upgraded.is_dir() and not (first / SLOT).exists(), "synthetic update/pruning failed")
        require(tomllib.loads((upgraded / "vibe.toml").read_text())["package"]["version"] == "0.1.1",
                "synthetic update installed wrong version")
        for relative in expected:
            require((upgraded / SKILL / relative).read_bytes() == (baseline / relative).read_bytes(),
                    "version-only update changed canonical skill bytes")
        run(first, "skill", "install", "--agent", "codex", "--scope", "project",
            "--skill", "proportional-controls", "--yes")
        # Rollback restores the entire reviewed/materialized consumer state.
        git(first, "restore", "--source=" + baseline_revision, "--staged", "--worktree", "--", ".")
        shutil.rmtree(upgraded)
        remote.rename(unavailable)
        try:
            run(first, "reinstall", "--offline")
            preparation.verify_consumer(args.source_ref, first)
        finally:
            unavailable.rename(remote)
        print(json.dumps({"distribution_qualification": "PASS", "source_revision": args.source_ref,
                          "payload_sha256": receipt["payload_sha256"], "distribution_revision": revision,
                          "vibevm_content_hash": expected_hash,
                          "commands": len(commands), "native_skill_bytes": "identical",
                          "local_publish_and_idempotence": "PASS", "independent_cold_consumer": "PASS",
                          "tag_drift": "upstream lock/slot split reproduced; canonical verifier rejects",
                          "offline": "existing slots and complete Git rollback PASS; cache-only recovery FAIL",
                          "update": "synthetic version-only declaration change PASS",
                          "scope": "disposable local Git transport; remote publication not qualified"}))


if __name__ == "__main__":
    main()
