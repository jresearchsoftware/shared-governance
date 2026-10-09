#!/usr/bin/env python3
"""Exercise the pinned VibeVM only in a disposable local authoring fixture."""
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
    parser.add_argument("--vibe", required=True, type=Path, help="downloaded pinned Linux x86_64 v1.0.7 binary")
    parser.add_argument("--materialize", action="store_true", help="also probe local dependency installation (alpha behavior)")
    parser.add_argument("--path-source", action="store_true", help="reproduce the known v1.0.7 path-only dependency limitation")
    args = parser.parse_args()
    vibe = args.vibe.resolve()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text(encoding="utf-8"))
    allowed = {pin[name]["sha256"] for name in ("linux_x86_64_gnu_binary", "linux_x86_64_musl_binary")}
    if hashlib.sha256(vibe.read_bytes()).hexdigest() not in allowed:
        parser.exit(1, "VibeVM binary digest differs from the pinned release bytes\n")
    tracked = [name for name in subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0") if name]
    with tempfile.TemporaryDirectory(prefix="shared-governance-vibe-") as temporary:
        fixture_root = Path(temporary)
        workspace = fixture_root / "workspace"
        workspace.mkdir()
        for name in tracked:
            source = ROOT / name
            if source.is_symlink():
                parser.exit(1, "Fixture only copies ordinary tracked files\n")
            target = workspace / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        env = {key: value for key, value in os.environ.items() if key in {"PATH", "LANG", "LC_ALL", "TMPDIR"}}
        env["VIBE_SETTINGS"] = str(fixture_root / "settings")
        env["VIBEVM_USER_CONFIG"] = str(fixture_root / "settings/config.toml")
        commands = []

        def run(*arguments):
            result = subprocess.run([str(vibe), *arguments], cwd=workspace, env=env,
                                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            commands.append({"arguments": list(arguments), "exit": result.returncode})
            if result.returncode:
                print(result.stdout)
                print(result.stderr)
                raise RuntimeError("VibeVM command failed: " + " ".join(arguments))
            print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip())
            if "check" in arguments:
                report = json.loads(result.stdout)
                if report["summary"]["error"] or report["summary"]["warning"] or report["findings"]:
                    raise RuntimeError("VibeVM check reported findings")
            return result.stdout

        run("--version")
        run("--offline", "--json", "validate", "--path", str(workspace), "--no-default-registry")
        run("--json", "check", "--path", str(workspace))
        member_relative = tomllib.loads((workspace / "vibe.toml").read_text(encoding="utf-8"))["workspace"]["members"][0]
        member = workspace / member_relative
        skills = tomllib.loads((member / "vibe.toml").read_text(encoding="utf-8"))["skill"]
        # Validate/projection may already have written state; only source-tracked bytes are payload.
        prefix = member_relative + "/"
        payload = {name.removeprefix(prefix): (workspace / name).read_bytes()
                   for name in tracked if name.startswith(prefix)}
        # Keep native projection receipts out of the source-tree registry transport.
        registry = fixture_root / "registry"
        registry_member = registry / Path(member_relative).relative_to("vibevm/vibepacks")
        for relative, data in payload.items():
            target = registry_member / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        run("--json", "check", "--path", str(member))
        agents_before = (workspace / "AGENTS.md").read_bytes()
        for declaration in skills:
            run("--offline", "--json", "skill", "install", "--path", str(member),
                "--agent", "codex", "--scope", "project", "--skill", declaration["name"], "--yes")
            skill = member / declaration["path"]
            projected = member / ".agents/skills" / declaration["name"]
            expected = {path.relative_to(skill).as_posix() for path in skill.rglob("*") if path.is_file()}
            actual = {path.relative_to(projected).as_posix() for path in projected.rglob("*") if path.is_file()}
            if actual != expected:
                raise RuntimeError("VibeVM skill projection file set differs from canonical skill")
            for source in skill.rglob("*"):
                if source.is_file() and (projected / source.relative_to(skill)).read_bytes() != source.read_bytes():
                    raise RuntimeError("VibeVM projection differs from canonical skill bytes")
        if (workspace / "AGENTS.md").read_bytes() != agents_before:
            raise RuntimeError("member skill projection changed root AGENTS.md")
        run("--json", "check", "--path", str(workspace))
        if args.materialize:
            # This temporary project is an authoring probe, never a consumer migration.
            requirement = ('{ path = "' + member_relative + '", version = "=0.1.0", link = "dynamic" }'
                           if args.path_source else '"=0.1.0"')
            with (workspace / "vibe.toml").open("a", encoding="utf-8") as manifest:
                manifest.write('\n[project]\nname = "authoring-fixture"\nversion = "0.0.0"\nspec_format = "mixed"\n'
                               '\n[requires.packages]\n"org.jresearch.ai/development-governance" = '
                               + requirement + '\n')
            run("--offline", "--json", "install", "--path", str(workspace), "--registry",
                str(registry), "--no-default-registry", "--assume-yes")
            installed = workspace / "vibevm/vibedeps/org.jresearch.ai.development-governance/0.1.0"
            actual = {path.relative_to(installed).as_posix() for path in installed.rglob("*") if path.is_file()}
            if actual != set(payload) | {".vibe-slot.toml"}:
                raise RuntimeError("materialized payload file set differs from authored source; missing="
                                   + repr(sorted(set(payload) - actual)) + "; extra="
                                   + repr(sorted(actual - set(payload) - {".vibe-slot.toml"})))
            for relative, data in payload.items():
                if (installed / relative).read_bytes() != data:
                    raise RuntimeError("materialized payload differs from authored source bytes")
            agents_after = (workspace / "AGENTS.md").read_bytes()
            blocks = re.findall(rb"<vibevm>.*?</vibevm>", agents_after, flags=re.S)
            outside = re.sub(rb"<vibevm>.*?</vibevm>", b"", agents_after, flags=re.S).rstrip()
            if len(blocks) != 1 or outside != agents_before.rstrip():
                raise RuntimeError("dependency install modified human-owned AGENTS.md content")
        print(json.dumps({"vibevm_qualification": "PASS", "version": pin["version"],
                          "commands": len(commands), "native_skill_bytes": "identical",
                          "dependency_install": "PASS" if args.materialize else "not requested",
                          "fixture": "disposable local paths; no package publication or consumer writes"}))


if __name__ == "__main__":
    main()
