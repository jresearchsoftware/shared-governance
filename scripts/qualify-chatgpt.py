"""Optional pinned-VibeVM install/update proof in a disposable external consumer."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", type=Path, required=True)
    parser.add_argument("--source-ref", required=True)
    args = parser.parse_args()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    if hashlib.sha256(args.vibe.read_bytes()).hexdigest() != pin["linux_x86_64_musl_binary"]["sha256"]:
        raise ValueError("Use the exact pinned musl binary")
    spec = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare-distribution.py")
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    with tempfile.TemporaryDirectory(prefix="chatgpt-native-") as temporary:
        fixture = Path(temporary)
        env = {k: v for k, v in os.environ.items() if k in {"PATH", "LANG", "LC_ALL", "TMPDIR"}}
        env.update(VIBE_SETTINGS=str(fixture / "settings"), VIBEVM_USER_CONFIG=str(fixture / "settings/config.toml"),
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
                   GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                   GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                   PYTHONDONTWRITEBYTECODE="1")

        def run(command, cwd, expected=0):
            result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
            if result.returncode != expected:
                raise ValueError("Fixture command failed: " + str(command) + "\n" + result.stdout + result.stderr)
            return result.stdout

        def native(command):
            # VibeVM emits a JSON event stream followed by its final result.
            remaining = run(command, consumer).lstrip()
            decoder = json.JSONDecoder()
            while remaining:
                report, end = decoder.raw_decode(remaining)
                remaining = remaining[end:].lstrip()
            return report

        _, receipt = preparation.snapshot(args.source_ref)
        version = receipt["version"]
        registry = fixture / "registry"
        source = registry / preparation.COORDINATE / ("v" + version)
        preparation.prepare(args.source_ref, source)
        remote = fixture / "distribution.git"
        run(["git", "init", "--bare", "-q", "-b", "main", str(remote)], fixture)
        run([str(args.vibe), "--json", "registry", "publish", str(source), "--repo-url", remote.as_uri()], source)
        consumer = fixture / "consumer"
        consumer.mkdir()
        manifest = consumer / "vibe.toml"
        manifest.write_text('[project]\nname="ordinary-consumer"\nversion="0.0.0"\nspec_format="mixed"\n'
                            '[requires.packages."org.jresearch.ai/development-governance"]\n'
                            f'version="={version}"\ngit="{remote.as_uri()}"\ntag="v{version}"\nauth="none"\n')
        (consumer / "AGENTS.md").write_text("# Ordinary garden project\nNo shared governance topics adopted.\n")
        install = native([str(args.vibe), "--json", "install", "--path", str(consumer),
                          "--no-default-registry", "--assume-yes"])
        slot = consumer / preparation.slot(version)
        preparation.verify(args.source_ref, slot, installed=True)
        custom = consumer / "chatgpt/custom.md"
        custom.parent.mkdir()
        custom.write_text("Speak English. Discuss planting. No external mutations.\n")
        binding = {"schema": 2, "repository": "fixture/garden", "navigation_ref": "main",
                   "mode": "read-only-preview", "role": "Garden discussion", "permissions": ["discussion"],
                   "native": "materialized", "local_sources": [], "character_budget": 8000,
                   "cache_enabled": True, "cache_selection": ["AGENTS.md"]}
        (custom.parent / "binding.json").write_text(json.dumps(binding))
        run(["git", "init", "-q"], consumer)
        run(["git", "add", "."], consumer)
        run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic accepted consumer"], consumer)

        def project(action, installed_slot):
            sha = run(["git", "rev-parse", "HEAD"], consumer).strip()
            return json.loads(run([sys.executable, str(installed_slot / "tools/chatgpt/project.py"), action,
                                   "--repository", str(consumer), "--binding", "chatgpt/binding.json",
                                   "--accepted-sha", sha, "--authority-anchor",
                                   "https://github.com/fixture/garden/issues/1"], consumer))

        first = project("update", slot)
        same = project("check", slot)
        assert first["effective_content"] == "CHANGED" and same["effective_content"] == "NO_OP"
        original_custom = custom.read_bytes()
        generated = custom.parent / "instructions.md"
        assert not any(w in generated.read_text() for w in ("Task", "Outcome", "BLOCKED", "Deliberative"))
        # Synthetic upgrade uses the normal materializer, never a copied consumer generator.
        major, minor, patch = map(int, version.split("."))
        next_version = f"{major}.{minor}.{patch + 1}"
        upgraded_source = registry / preparation.COORDINATE / ("v" + next_version)
        shutil.copytree(source, upgraded_source)
        (upgraded_source / "DISTRIBUTION.json").unlink()  # No false canonical receipt for synthetic content.
        package_manifest = upgraded_source / "vibe.toml"
        package_manifest.write_text(package_manifest.read_text().replace(f'version = "{version}"', f'version = "{next_version}"'))
        base = upgraded_source / "tools/chatgpt/base.md"
        base.write_text(base.read_text() + "\nSynthetic compatible client-mechanics addition.\n")
        run([str(args.vibe), "--json", "registry", "publish", str(upgraded_source),
             "--repo-url", remote.as_uri()], upgraded_source)
        manifest.write_text(manifest.read_text().replace("=" + version, "=" + next_version)
                            .replace('tag="v' + version + '"', 'tag="v' + next_version + '"'))
        update = native([str(args.vibe), "--json", "update", "--path", str(consumer), "--all",
                         "--assume-yes"])
        upgraded_slot = consumer / preparation.slot(next_version)
        assert upgraded_slot.is_dir() and not slot.exists()
        run(["git", "add", "."], consumer)
        run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic dependency upgrade"], consumer)
        changed = project("update", upgraded_slot)
        assert changed["instructions"] == "CHANGED" and changed["sources"] == "CHANGED"
        assert project("check", upgraded_slot)["effective_content"] == "NO_OP"
        assert custom.read_bytes() == original_custom
        assert "Synthetic compatible" in generated.read_text()
        print(json.dumps({"native_chatgpt_lifecycle": "PASS", "source_ref": args.source_ref,
                          "version": version, "synthetic_upgrade": next_version,
                          "install_ok": install["ok"], "update_ok": update["ok"],
                          "invocation": "same tool from native versioned slot before/after VibeVM update",
                          "custom_preserved": True, "non_adopting_negative": "PASS",
                          "cache_export": "PASS; no upload", "scope": "disposable synthetic consumer only"}))


if __name__ == "__main__":
    main()
