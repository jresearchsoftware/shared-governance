#!/usr/bin/env python3
"""Qualify fresh native resolution of a revised unaccepted same-version proposal."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    if hashlib.sha256(args.vibe.read_bytes()).hexdigest() != pin["linux_x86_64_musl_binary"]["sha256"]:
        raise ValueError("requires pinned native Linux VibeVM")
    base = Path(tempfile.mkdtemp(prefix="task24-step3-candidate-regenerate-"))
    work = base / "candidate"
    env = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
               GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
               VIBE_SETTINGS=str(base / "settings"), VIBEVM_USER_CONFIG=str(base / "settings/config.toml"))
    subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "--no-hardlinks", str(ROOT), str(work)], env=env, check=True)

    def git(*argv):
        return subprocess.check_output(["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
                                        "-c", "core.hooksPath=/nonexistent", *argv], cwd=work, env=env, text=True).strip()

    spec = importlib.util.spec_from_file_location("exporter", ROOT / "scripts/prepare-distribution.py")
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    exporter.ROOT = work
    protocol = work / exporter.PACKAGE / exporter.HANDOFF
    protocol.write_bytes(protocol.read_bytes() + b"\nDisposable unaccepted candidate correction.\n")
    git("add", exporter.PACKAGE)
    git("commit", "-qm", "Disposable candidate correction without changing candidate version")
    revision = git("rev-parse", "HEAD")
    exporter.stage_producer(revision, work)
    lock = work / "vibe.lock"
    old_lock = lock.read_text()
    lock.unlink()  # Only this newly created disposable proposal's generated lock.
    argv = [str(args.vibe.resolve()), "--json", "install", "--path", str(work), "--registry",
            str(work / "vibevm/vibepacks"), "--offline", "--no-default-registry", "--assume-yes"]
    process = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=120)
    try:
        exporter.verify_producer(revision, work)
        verified = "PASS"
    except (ValueError, OSError) as error:
        verified = str(error)
    result = dict(scope="disposable unaccepted same-version proposal; frozen releases untouched",
                  revision=revision, argv=argv, exit=process.returncode, stdout=process.stdout,
                  stderr=process.stderr, old_windows_lock=old_lock, new_lock=lock.read_text(),
                  canonical_producer=verified, operation="discard only proposal lock; native fresh resolve, no URL editing")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(exit=process.returncode, canonical_producer=verified)))


if __name__ == "__main__":
    main()
