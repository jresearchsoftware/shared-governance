#!/usr/bin/env python3
"""One-time pinned-tool comparison of workspace and published-style self-consumption."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare-distribution.py")
PREPARATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARATION)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", required=True, type=Path)
    args = parser.parse_args()
    vibe = args.vibe.resolve()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    if hashlib.sha256(vibe.read_bytes()).hexdigest() != pin["linux_x86_64_musl_binary"]["sha256"]:
        raise ValueError("probe requires the pinned musl binary")
    # Preserve this diagnostic's historical accepted input after helper retirement.
    files, _ = PREPARATION.snapshot("73798b919efbd0d8b0ee1317bf84a6c48d7e99d1")
    files.pop("DISTRIBUTION.json")
    with tempfile.TemporaryDirectory(prefix="self-consumption-vibe-") as temporary:
        base = Path(temporary)
        workspace = base / "workspace"
        registry = base / "registry"
        package = workspace / "packages/development-governance"
        accepted = registry / "org.jresearch.ai/development-governance/v1.2.0"
        for directory in (package, accepted):
            for name, data in files.items():
                target = directory / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        (package / PREPARATION.PROTOCOL).write_bytes(
            files[PREPARATION.PROTOCOL] + b"\nLOCAL CANDIDATE SENTINEL\n")
        manifest = ('[workspace]\nmembers = ["packages/development-governance"]\n'
                    '[project]\nname = "self-adoption-probe"\nversion = "0.0.0"\nspec_format = "mixed"\n'
                    '[requires.packages]\n"org.jresearch.ai/development-governance" = "^1.2.0"\n')
        (workspace / "vibe.toml").write_text(manifest)
        (workspace / "AGENTS.md").write_text("Human instructions remain owned by the project.\n")
        env = {k: v for k, v in os.environ.items() if k in {"PATH", "LANG", "LC_ALL", "TMPDIR"}}
        env.update(VIBE_SETTINGS=str(base / "settings"), VIBEVM_USER_CONFIG=str(base / "settings/config.toml"))
        commands = []

        def run(command):
            options = ["--all"] if command == "update" else ["--no-default-registry"]
            result = subprocess.run([str(vibe), "--offline", "--json", command, "--path", str(workspace),
                                     "--registry", str(registry), "--assume-yes", *options],
                                    env=env, capture_output=True, text=True, timeout=90)
            commands.append({"command": command, "exit": result.returncode,
                             "stdout": result.stdout, "stderr": result.stderr})
            return result

        first = run("install")
        if first.returncode:
            raise ValueError("native workspace install failed")
        slot = workspace / "vibevm/vibedeps/org.jresearch.ai.development-governance/1.2.0"
        shadowed = b"LOCAL CANDIDATE SENTINEL" in (slot / PREPARATION.PROTOCOL).read_bytes()
        index = (workspace / "vibevm/vibespecs/boot/INDEX.md").read_text()
        boot_targets = "LOCAL CANDIDATE SENTINEL" in "\n".join(
            p.read_text() for p in workspace.rglob("*.md") if "packages" not in p.parts)
        before = (workspace / "vibe.lock").read_bytes()
        newer = registry / "org.jresearch.ai/development-governance/v1.2.1"
        for name, data in files.items():
            target = newer / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name == "vibe.toml":
                data = data.replace(b'version = "1.2.0"', b'version = "1.2.1"')
            target.write_bytes(data)
        update = run("update")
        after = (workspace / "vibe.lock").read_bytes()
        # A direct-Git published dependency, as used by this producer's release flow.
        distribution = base / "published"
        distribution.mkdir()
        git_env = dict(env, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                       GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                       GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null")

        def git(*arguments):
            subprocess.run(["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/nonexistent",
                            *arguments], cwd=distribution, env=git_env, capture_output=True, check=True)

        git("init", "-q", "-b", "main")
        for version in ("1.2.0", "1.2.1"):
            for name, data in files.items():
                target = distribution / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if name == "vibe.toml":
                    data = data.replace(b'1.2.0', version.encode())
                target.write_bytes(data)
            git("add", ".")
            git("commit", "-qm", "Disposable published payload")
            git("tag", "v" + version)
        git_requirement = '{ version = "=1.2.0", git = "' + distribution.as_uri() + '", tag = "v1.2.0", auth = "none" }'
        git_manifest = manifest.replace('"^1.2.0"', git_requirement)
        (workspace / "vibe.toml").write_text(git_manifest)
        direct_install = run("install")
        (workspace / "vibe.toml").write_text(git_manifest.replace("1.2.0", "1.2.1"))
        direct_update = run("update")
        direct_lock = (workspace / "vibe.lock").read_text()
        # A path-only member is independently assessed; no registry transport is allowed.
        path_workspace = base / "path-workspace"
        path_workspace.mkdir()
        import shutil
        shutil.copytree(package, path_workspace / "packages/development-governance")
        (path_workspace / "vibe.toml").write_text(manifest.replace('"^1.2.0"',
            '{ path = "packages/development-governance", version = "=1.2.0", link = "dynamic" }'))
        path_only = subprocess.run([str(vibe), "--offline", "--json", "install", "--path", str(path_workspace),
                                    "--no-default-registry", "--assume-yes"], env=env,
                                   capture_output=True, text=True, timeout=90)
        report = {"vibevm": pin["version"], "binary_sha256": pin["linux_x86_64_musl_binary"]["sha256"],
                  "workspace_member_shadows_registry": shadowed,
                  "candidate_present_in_materialized_boot_tree": boot_targets,
                  "index": index, "update_exit": update.returncode, "update_changed_lock": before != after,
                  "lock_before": before.decode(), "lock_after": after.decode(),
                  "direct_git_install_exit": direct_install.returncode,
                  "direct_git_update_exit": direct_update.returncode,
                  "direct_git_update_selected_new_version": 'version = "1.2.1"' in direct_lock,
                  "direct_git_lock": direct_lock,
                  "path_only_exit": path_only.returncode, "path_only_stdout": path_only.stdout,
                  "path_only_stderr": path_only.stderr, "commands": commands}
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
