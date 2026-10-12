#!/usr/bin/env python3
"""Task 24 Step 3: genuine Windows generation and native Linux consumption.

Only disposable clones/settings are mutated. Preserve native lock URLs as emitted.
"""
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
REGISTRY = "vibevm/vibepacks"
SOURCE = REGISTRY + "/" + PACKAGE + "/v1.2.0"
WINDOWS_SHA256 = "ceb0b8582e059dfab708ee0c5221e700c232c97912bdd5174dc0df1d03011b46"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", required=True, type=Path)
    parser.add_argument("--produce", action="store_true")
    parser.add_argument("--windows-fixture", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    digest = hashlib.sha256(args.vibe.read_bytes()).hexdigest()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    expected = WINDOWS_SHA256 if args.produce else pin["linux_x86_64_musl_binary"]["sha256"]
    if digest != expected or args.produce != (os.name == "nt"):
        raise ValueError("requires actual pinned Windows producer or native Linux consumer")
    spec = importlib.util.spec_from_file_location("exporter", ROOT / "scripts/prepare-distribution.py")
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    payload, receipt = exporter.snapshot(ACCEPTED)
    base = Path(tempfile.mkdtemp(prefix="task24-step3-native-", dir=ROOT / ".vibe")) if args.produce else Path(tempfile.mkdtemp(prefix="task24-step3-native-"))
    env = dict(os.environ)
    env.update(GIT_AUTHOR_NAME="Disposable fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Disposable fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    cases, observations, states = [], {}, {}
    result = dict(accepted_source_main=ACCEPTED, canonical_receipt=receipt, platform=os.name,
                  binary_sha256=digest, fixture=str(base), cases=cases,
                  observations=observations, states=states)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def save():
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    def git(work, *argv):
        return subprocess.check_output(["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
                                       "-c", "core.hooksPath=" + str(base / "no-hooks"), *argv], cwd=work, env=env, text=True).strip()

    def clone(source, name):
        work = base / name
        git(base, "clone", "-q", "--no-hardlinks", str(source), str(work))
        return work

    def state(work, label):
        paths = ["vibe.lock", "vibe.toml", "AGENTS.md", "vibevm/vibespecs/boot/INDEX.md", SLOT + "/.vibe-slot.toml"]
        states[label] = {p: (work / p).read_text(encoding="utf-8") for p in paths if (work / p).is_file()}
        save()

    def run(work, label, command="install", extra=(), settings=None):
        settings = settings or base / (work.name + "-settings")
        command_env = dict(env, VIBE_SETTINGS=str(settings), VIBEVM_USER_CONFIG=str(settings / "config.toml"))
        argv = [str(args.vibe.resolve()), "--json", command]
        if command in {"install", "update"}:
            argv += ["--path", str(work), "--registry", str(work / REGISTRY), "--offline", "--assume-yes"]
            argv += ["--no-default-registry"] if command == "install" else ["--all"]
        else:
            argv += [str(work), "--offline", "--assume-yes"]
        argv += list(extra)
        proc = subprocess.run(argv, env=command_env, capture_output=True, text=True, timeout=120)
        cases.append(dict(label=label, argv=argv, exit=proc.returncode, stdout=proc.stdout, stderr=proc.stderr))
        save()
        print(json.dumps(dict(label=label, exit=proc.returncode)), flush=True)
        return proc.returncode

    def verify(work, label):
        try:
            exporter.verify(ACCEPTED, work / SLOT, installed=True)
            observations[label] = "PASS"
        except (ValueError, OSError) as error:
            observations[label] = str(error)
        save()

    if args.produce:
        work = clone(ROOT, "windows-producer")
        git(work, "checkout", "-q", "--detach", ACCEPTED)
        (work / "AGENTS.md").write_text("Public disposable Task 24 Step 3 local overlay.\n", encoding="utf-8")
        (work / "vibevm/vibespecs/boot/00-authoring.md").write_text("Read applicable accepted protocols via the generated index.\n", encoding="utf-8")
        (work / "vibe.toml").write_text('[workspace]\nmembers=["packages/development-governance"]\n[project]\nname="task24-step3-fixture"\nversion="0.0.0"\nspec_format="mixed"\n[requires.packages."flow:' + PACKAGE + '"]\nversion="=1.2.0"\nlink="dynamic"\n', encoding="utf-8")
        for relative, data in payload.items():
            target = work / SOURCE / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        observations["windows_install_exit"] = run(work, "genuine Windows cold install")
        verify(work, "windows_slot_verified")
        state(work, "windows-produced")
        git(work, "add", "-A")
        git(work, "commit", "-qm", "Synthetic Windows native ready state")
        result["windows_fixture"] = str(work)
        result["windows_commit"] = git(work, "rev-parse", "HEAD")
        result["lock_blob"] = git(work, "rev-parse", "HEAD:vibe.lock")
        save()
        return

    if not args.windows_fixture:
        parser.error("--windows-fixture is required for Linux consumption")
    seed = clone(args.windows_fixture, "linux-seed")
    first = git(seed, "rev-parse", "HEAD")
    result["windows_commit"] = first
    result["windows_lock_blob"] = git(seed, "rev-parse", "HEAD:vibe.lock")
    state(seed, "linux-clean-Windows-artifacts")
    verify(seed, "clean_checkout_slot")
    observations["ready_index_without_bootstrap"] = (seed / "vibevm/vibespecs/boot/INDEX.md").is_file()
    old_url = tomllib.loads((seed / "vibe.lock").read_text())["package"][0]["source_url"]
    observations["unchanged_windows_source_url"] = old_url
    observations["old_url_unreachable_on_linux"] = not Path(old_url.removeprefix("file://")).exists()
    run(seed, "Linux retained Windows slots install")
    verify(seed, "retained_install_slot")
    run(seed, "Linux retained Windows slots update", "update")
    state(seed, "linux-retained")
    for name in ("missing-slot", "force-raw", "force-configured", "force-missing", "plain-index", "same-version-source", "version-change"):
        work = clone(args.windows_fixture, name)
        if name == "missing-slot":
            shutil.rmtree(work / SLOT)
            run(work, "Linux missing Windows slot install")
            verify(work, "missing_slot_restored")
        elif name.startswith("force"):
            if name == "force-missing":
                shutil.rmtree(work / SLOT)
            else:
                (work / SLOT / "vibevm/vibespecs/protocols/task-handoff.md").write_text("Disposable corruption\n")
            settings = base / (name + "-settings")
            if name == "force-configured":
                settings.mkdir()
                (settings / "registry.toml").write_text('[[registry]]\nname="fixture"\nurl="' + (work / REGISTRY).as_uri() + '"\n')
            run(work, name + " pinned restoration", "reinstall", ["--force"], settings)
            verify(work, name + "_restored")
        elif name == "plain-index":
            (work / "vibevm/vibespecs/boot/INDEX.md").unlink()
            run(work, "plain reinstall boot restoration", "reinstall")
            observations["plain_reinstall_index_restored"] = (work / "vibevm/vibespecs/boot/INDEX.md").is_file()
        elif name == "same-version-source":
            # A deliberate integrity incident, not an admissible frozen version edit.
            (work / SOURCE / "vibevm/vibespecs/protocols/task-handoff.md").write_text("Disposable source mutation\n")
            run(work, "old Windows URL deliberate same-version source edit install")
            run(work, "old Windows URL deliberate same-version source edit update", "update")
            verify(work, "same_version_retained_slot")
            observations["same_version_source_diff_detected_by_exporter"] = (work / SOURCE / "vibevm/vibespecs/protocols/task-handoff.md").read_bytes() != payload["vibevm/vibespecs/protocols/task-handoff.md"]
            run(work, "old Windows URL deliberate source edit forced install", extra=["--force"])
            observations["forced_install_reads_changed_source"] = (work / SLOT / "vibevm/vibespecs/protocols/task-handoff.md").read_text() == "Disposable source mutation\n"
        else:
            new_source = work / REGISTRY / PACKAGE / "v1.2.1"
            for relative, data in payload.items():
                if relative == exporter.RECEIPT:
                    continue
                if relative == "vibe.toml":
                    data = data.replace(b'1.2.0', b'1.2.1')
                if relative == "vibevm/vibespecs/protocols/task-handoff.md":
                    data += b'\nPublic disposable patch marker.\n'
                target = new_source / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                authored = work / "packages/development-governance" / relative
                authored.parent.mkdir(parents=True, exist_ok=True)
                authored.write_bytes(data)
            manifest = work / "vibe.toml"
            manifest.write_text(manifest.read_text().replace('=1.2.0', '=1.2.1'))
            run(work, "old Windows URL explicit version change update", "update")
            run(work, "old Windows URL explicit version change install")
            new_slot = work / SLOT.replace("1.2.0", "1.2.1")
            observations["meaningful_version_change_visible"] = new_slot.is_dir() and (new_slot / "vibevm/vibespecs/protocols/task-handoff.md").read_bytes().endswith(b'Public disposable patch marker.\n')
            git(work, "add", "-A")
            git(work, "commit", "-qm", "Synthetic Linux patch source and projection together")
            second = git(work, "rev-parse", "HEAD")
            exporter_root = exporter.ROOT
            exporter.ROOT = work
            exporter.verify(second, new_slot, installed=True, native=True)
            observations["version_change_source_slot_canonical"] = True
            exporter.ROOT = exporter_root
            pull = clone(args.windows_fixture, "pull-consumer")
            git(pull, "remote", "set-url", "origin", str(work))
            git(pull, "pull", "-q", "--ff-only", "origin", "HEAD")
            observations["pull_advances_source_and_slot"] = git(pull, "rev-parse", "HEAD") == second and (pull / SLOT.replace("1.2.0", "1.2.1")).is_dir()
            git(pull, "checkout", "-q", "--detach", first)
            verify(pull, "rollback_windows_slot")
            git(pull, "checkout", "-q", "--detach", second)
            observations["checkout_forward_slot"] = (pull / SLOT.replace("1.2.0", "1.2.1")).is_dir()
        state(work, name)
    save()


if __name__ == "__main__":
    main()
