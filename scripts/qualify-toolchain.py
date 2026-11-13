#!/usr/bin/env python3
"""One-time pinned-tool mixed graph and recovery probes in disposable native clones."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    vibe = args.vibe.resolve()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    require(hashlib.sha256(vibe.read_bytes()).hexdigest() == pin["linux_x86_64_musl_binary"]["sha256"],
            "binary differs from pinned musl bytes")
    spec = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare-distribution.py")
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    revision = preparation.git("rev-parse", "HEAD").decode().strip()
    report = dict(source_revision=revision, tool_version=pin["version"],
                  binary_sha256=pin["linux_x86_64_musl_binary"]["sha256"], cases=[])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="toolchain-qualification-") as temporary:
        base = Path(temporary)
        work = base / "workspace"
        settings = base / "settings"
        settings.mkdir()
        home = base / "home"
        home.mkdir()
        trace = base / "git-trace.json"
        env = {k: v for k, v in os.environ.items() if k in {"PATH", "LANG", "LC_ALL", "TMPDIR"}}
        env.update(VIBE_SETTINGS=str(settings), VIBEVM_USER_CONFIG=str(settings / "config.toml"),
                   HOME=str(home), XDG_CACHE_HOME=str(home / ".cache"),
                   XDG_CONFIG_HOME=str(home / ".config"), GIT_TRACE2_EVENT=str(trace),
                   GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0",
                   GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                   GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")

        def git(path, *arguments):
            return subprocess.check_output(["git", "-c", "core.autocrlf=false", "-C", str(path),
                                            *arguments], env=env, stderr=subprocess.PIPE).decode().strip()

        def run(label, path, *arguments, success=True):
            result = subprocess.run([str(vibe), "--json", *arguments], cwd=path, env=env,
                                    capture_output=True, text=True, timeout=180)
            report["cases"].append(dict(label=label, arguments=list(arguments), exit=result.returncode,
                                        stdout=result.stdout, stderr=result.stderr))
            args.output.write_text(json.dumps(report, indent=2) + "\n")
            print(label + ": exit " + str(result.returncode), flush=True)
            require((result.returncode == 0) == success, "unexpected exit: " + label)
            return result

        def tree(path):
            # Lifecycle journals are operational evidence, outside the materialized project.
            return {p.relative_to(path).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest()
                    if p.is_file() else None) for p in path.rglob("*")
                    if not ({".git", ".vibe"} & set(p.relative_to(path).parts))}

        git(base, "clone", "-q", "--no-hardlinks", str(ROOT), str(work))
        original_lock = tomllib.loads((work / "vibe.lock").read_text())
        original_tree = tree(work)
        (settings / "registry.toml").write_text('[[registry]]\nname="producer-source"\nurl="'
                                               + (work / "vibevm/vibepacks").as_uri() + '"\nauth="none"\n')
        # Deliberate fresh resolution, retaining the original lock in the clone's Git.
        (work / "vibe.lock").unlink()
        for package in original_lock["package"]:
            installed = work / "vibevm/vibedeps" / (package["group"] + "." + package["name"]) / package["version"]
            require(installed.resolve().is_relative_to(work.resolve()), "slot escaped disposable clone")
            shutil.rmtree(installed)
        require(not any(home.iterdir()) and not (settings / "cache").exists(), "cold cache is not empty")
        trace.unlink(missing_ok=True)  # Exclude the local fixture clone from acquisition evidence.
        run("mixed cold resolution", work, "install", "--no-default-registry", "--no-prefer-local", "--assume-yes")
        commands = [event["argv"] for line in trace.read_text().splitlines()
                    if (event := json.loads(line)).get("event") == "start"]
        origin = "https://github.com/jrs-vibevm/org.jresearch.ai.codex-relay.git"
        clones = [argv for argv in commands if "clone" in argv and origin in argv]
        require(clones, "no cold Relay Git clone observed")
        require(not any("raw.githubusercontent.com" in arg for argv in commands for arg in argv),
                "Git acquisition was rewritten to a raw-file host")
        origins = [git(Path(argv[-1]), "config", "--get", "remote.origin.url") for argv in clones]
        require(all(url == origin for url in origins), "Relay cache origin changed")
        report["cold_acquisition"] = dict(isolated_empty_home=True, compatibility_remap=False,
                                          clone_commands=clones, actual_origins=origins)
        lock = tomllib.loads((work / "vibe.lock").read_text())
        selected = lambda data: {(p["group"], p["name"]): (p["version"], p["content_hash"])
                                 for p in data["package"]}
        require(selected(lock) == selected(original_lock), "selected package identities changed")
        require(lock["meta"]["generated_by"] == "vibe " + pin["version"], "wrong materializer version")
        report["selected"] = [dict(group=p["group"], name=p["name"], version=p["version"],
                                   content_hash=p["content_hash"], source_kind=p["source_kind"],
                                   source_ref=p.get("source_ref")) for p in lock["package"]]
        # Preserve only historical slots pruned by native install, without replacing selected output.
        selected_paths = {"vibevm/vibedeps/" + p["group"] + "." + p["name"] + "/" + p["version"]
                          for p in lock["package"]}
        historical = {str(Path(p).parents[0]).replace("\\", "/") for p in original_tree
                      if p.endswith("/.vibe-slot.toml") and p.count("/") == 4} - selected_paths
        for path in sorted(historical):
            git(work, "restore", "--source=" + revision, "--", path)
        listing = json.loads(run("native Skill listing", work, "skill", "list", "--offline").stdout)
        require("codex-relay" in json.dumps(listing), "Relay Skill missing")
        run("Skill projection dry run", work, "skill", "install", "--offline", "--skill", "codex-relay",
            "--agent", "codex", "--scope", "project", "--dry-run")
        run("Skill projection", work, "skill", "install", "--offline", "--skill", "codex-relay",
            "--agent", "codex", "--scope", "project", "--yes")
        preparation.verify_producer(revision, work)
        report["generated_diff"] = git(work, "diff", "--stat")
        # No frozen payload or effective Instructions text may change.
        generated_tree = tree(work)
        for path, digest in original_tree.items():
            if (path.startswith("packages/development-governance/") and path not in
                    {"packages/development-governance/" + p for p in preparation.SOURCE_ARTIFACTS}
                    or path.startswith("vibevm/vibepacks/") or path.startswith(".agents/skills/codex-relay/")
                    or path == "chatgpt/instructions.md" or any(path.startswith(h + "/") for h in historical)):
                require(generated_tree.get(path) == digest, "immutable or effective content changed: " + path)
        check = json.loads(run("mixed graph check", work, "check").stdout)
        require(check["summary"]["error"] == 0 and all(f["check"] == "lockfile_files"
                and f["severity"] == "warning" and f["path"] in historical
                and "orphan" in f["message"] for f in check["findings"]),
                "unexpected native check findings")
        report["historical_slots_retained"] = len(historical)
        report["historical_warnings"] = check["summary"]["warning"]
        # Change source bytes only in this disposable registry. Forced reinstall must refuse them.
        shared = [p for p in lock["package"]
                  if (p["group"], p["name"]) == ("org.jresearch.ai", "development-governance")]
        require(len(shared) == 1, "expected one selected governance source for the mismatch probe")
        source = (work / "vibevm/vibepacks" / shared[0]["group"] / shared[0]["name"]
                  / ("v" + shared[0]["version"]) / "README.md")
        source.write_bytes(source.read_bytes() + b"\nDisposable mismatch probe.\n")
        before = tree(work)
        refused = run("force reinstall source mismatch", work, "reinstall", "--force", "--offline",
                      "--assume-yes", str(work), success=False)
        require("lock_hash_mismatch" in refused.stdout + refused.stderr, "missing pinned-byte refusal")
        require(tree(work) == before, "refused reinstall changed project")
        git(work, "restore", "--source=" + revision, "--", ".")
        # New ignored boot receipts are disposable materializer output, not committed source.
        for path in ("vibevm/vibespecs/boot/.vibe-boot-artifacts.lock",
                     "packages/development-governance/vibevm/vibespecs/boot/.vibe-boot-artifacts.lock"):
            if path not in original_tree:
                (work / path).unlink(missing_ok=True)
        restored_tree = tree(work)
        require(restored_tree == original_tree, "Git restoration did not recover the complete project: "
                + repr([p for p in restored_tree.keys() | original_tree.keys()
                        if restored_tree.get(p) != original_tree.get(p)]))
        preparation.verify_producer(revision, work)
        run("retained-slot reinstall", work, "reinstall", "--offline", "--assume-yes", str(work))
        preparation.verify_producer(revision, work)

        # Reproduce upstream B-206's late static-compilation failure, after materialization starts.
        rollback = base / "rollback"
        rollback.mkdir()
        registry = base / "rollback-registry"
        for name, tail, boot in [
            ("kept", "", "# Kept\n\nkept rule.\n"),
            ("broken", 'format="normal"\n', '# Broken {#root}\n#use spec://org.example/ghost/boot/base#root\nBROKEN\n'),
            ("wrapper", '[requires.packages]\n"org.example/broken"={version="^1.0",link="static"}\n', '# Wrapper\n\nwrapper rule.\n')]:
            package = registry / "org.example" / name / "v1.0.0"
            (package / "vibevm/vibespecs/boot").mkdir(parents=True)
            (package / "vibe.toml").write_text('[package]\ngroup="org.example"\nname="' + name
                + '"\nkind="flow"\nversion="1.0.0"\n' + tail
                + '[boot_snippet]\nsource="vibevm/vibespecs/boot/' + name + '.md"\n')
            (package / ("vibevm/vibespecs/boot/" + name + ".md")).write_text(boot)
        (settings / "registry.toml").write_text('[[registry]]\nname="fixture"\nurl="' + registry.as_uri() + '"\n')
        (rollback / "vibe.toml").write_text('[project]\nname="rollback"\nversion="0.0.0"\nspec_format="xml"\n')
        (rollback / "AGENTS.md").write_text("Human-owned rollback overlay.\n")
        run("rollback baseline", rollback, "install", "org.example/kept", "--no-default-registry", "--assume-yes")
        before = tree(rollback)
        failed = run("late failed install rollback", rollback, "install", "org.example/wrapper",
                     "--no-default-registry", "--assume-yes", success=False)
        require("STATIC.xml" in failed.stdout + failed.stderr, "failure did not reach static compilation")
        require(tree(rollback) == before, "failed install did not restore manifest, lock, slots and boot")
        report["result"] = "PASS"
        args.output.write_text(json.dumps(report, indent=2) + "\n")
        print("Mixed graph, frozen payload, native projection, refusal, rollback and Git recovery: PASS")


if __name__ == "__main__":
    main()
