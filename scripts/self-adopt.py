#!/usr/bin/env python3
"""Refresh this producer's accepted guidance; never publish or use checkout package bytes."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://github.com/jresearchsoftware/shared-governance.git"
DISTRIBUTION = "https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git"
BASELINE = "73798b919efbd0d8b0ee1317bf84a6c48d7e99d1"
BASELINE_RELEASE = "4e701dcb0c97bb7a220800a550eb2f668a8ab20b"
SPEC = importlib.util.spec_from_file_location("adoption_preparation", ROOT / "scripts/prepare-distribution.py")
PREPARATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARATION)


def git(root, *args):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    return subprocess.check_output(["git", "-c", "maintenance.auto=false", "-c", "gc.auto=0", *args],
                                   cwd=root, env=env, stderr=subprocess.PIPE, timeout=30)


def snapshot(root, revision):
    previous = PREPARATION.ROOT
    try:
        PREPARATION.ROOT = root
        return PREPARATION.snapshot(revision)
    finally:
        PREPARATION.ROOT = previous


def tree(root, revision):
    files = {}
    for entry in git(root, "ls-tree", "-rz", revision).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        if mode != "100644" or kind != "blob":
            raise ValueError("release contains non-ordinary files")
        files[name.decode()] = git(root, "cat-file", "blob", oid)
    return files


def baseline(root):
    pin = json.loads((root / ".agents/self-adoption.json").read_text())
    files, receipt = snapshot(root, BASELINE)
    if pin != {"source_revision": BASELINE, "release_commit": BASELINE_RELEASE,
               "payload_sha256": receipt["payload_sha256"], "version": receipt["version"]}:
        raise ValueError("bootstrap identity differs from accepted baseline")
    return files, {**receipt, "release_commit": BASELINE_RELEASE}


def verified(root, metadata):
    revision = metadata["source_revision"]
    accepted = BASELINE
    probe = subprocess.run(["git", "rev-parse", "--verify", "refs/self-adoption/main"],
                           cwd=root, capture_output=True, timeout=30)
    if not probe.returncode:
        accepted = probe.stdout.decode().strip()
    if revision not in git(root, "rev-list", "--first-parent", accepted).decode().splitlines():
        raise ValueError("active source is not accepted first-parent history")
    files, receipt = snapshot(root, metadata["source_revision"])
    if metadata != {**receipt, "release_commit": metadata["release_commit"]}:
        raise ValueError("active identity differs from accepted source")
    if revision == BASELINE:
        if metadata["release_commit"] != BASELINE_RELEASE:
            raise ValueError("bootstrap release identity differs")
    else:
        retained = git(root, "rev-parse", "refs/self-adoption/releases/v" + receipt["version"]).decode().strip()
        if retained != metadata["release_commit"] or tree(root, retained) != files:
            raise ValueError("active publication proof differs from accepted export")
    directory = root / ".agents/accepted" / metadata["source_revision"]
    if directory.is_symlink():
        raise ValueError("active directory is a symlink")
    actual = {p.relative_to(directory).as_posix(): p.read_bytes()
              for p in directory.rglob("*") if p.is_file() and not p.is_symlink()}
    if any(p.is_symlink() for p in directory.rglob("*")) or actual != files:
        raise ValueError("active files differ from accepted source")
    return files


def activate(root, files, metadata, current=None):
    cache = root / ".agents/accepted"
    cache.mkdir(parents=True, exist_ok=True)
    if cache.is_symlink():
        raise ValueError("active cache is a symlink")
    target = cache / metadata["source_revision"]
    if target.exists():
        verified(root, metadata)
    else:
        # Public guidance must inherit workspace access. TemporaryDirectory's
        # private Windows DACL survives rename and excludes sandbox readers.
        pending = cache / ("pending-" + uuid.uuid4().hex)
        pending.mkdir()
        for name, data in files.items():
            path = pending / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        os.rename(pending, target)
    state = {"current": metadata}
    if current and current != metadata:
        state["previous"] = current
    pointer = cache / "ACTIVE.json"
    if pointer.exists() and json.loads(pointer.read_text()).get("current") == metadata:
        return target
    # Only the small selector changes; an interrupted write leaves the old selector usable.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=cache, delete=False) as stream:
        json.dump(state, stream, indent=2, sort_keys=True)
        stream.write("\n")
        staging = Path(stream.name)
    try:
        os.replace(staging, pointer)
    finally:
        staging.unlink(missing_ok=True)
    return target


def select(root, distribution, main):
    ancestry = git(root, "rev-list", "--first-parent", main).decode().splitlines()
    ranks = {revision: rank for rank, revision in enumerate(ancestry)}
    candidates = []
    for tag in git(distribution, "tag", "--list", "v*").decode().splitlines():
        if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
            continue
        oid = git(distribution, "rev-parse", tag + "^{commit}").decode().strip()
        receipt = json.loads(git(distribution, "show", oid + ":DISTRIBUTION.json"))
        if not isinstance(receipt, dict):
            raise ValueError("published receipt must be an object")
        revision = receipt.get("source_revision")
        if revision in ranks and tag == "v" + receipt.get("version", ""):
            candidates.append((ranks[revision], oid, revision))
    if not candidates:
        raise ValueError("no published accepted source is available")
    _, oid, revision = min(candidates)
    files, receipt = snapshot(root, revision)
    if tree(distribution, oid) != files:
        raise ValueError("published tag differs from exact accepted export")
    # Docs/tool-only merges do not cause unnecessary activation or bumps.
    _, latest = snapshot(root, ancestry[0])
    warning = None
    if latest["payload_sha256"] != receipt["payload_sha256"]:
        warning = "New accepted package is not yet published; retaining latest eligible publication"
    return files, {**receipt, "release_commit": oid}, warning


def refresh(root=ROOT, *, offline=False, rollback=False, source=SOURCE, distribution=DISTRIBUTION):
    root = Path(root)
    warnings = []
    pointer = root / ".agents/accepted/ACTIVE.json"
    state = json.loads(pointer.read_text()) if pointer.exists() else {}
    if not isinstance(state, dict) or set(state) - {"current", "previous"}:
        raise ValueError("invalid active selector")
    current = state.get("current")
    if current:
        verified(root, current)
    else:
        files, current = baseline(root)
        activate(root, files, current)
    if rollback:
        previous = state.get("previous")
        if not previous:
            raise ValueError("no previous accepted version to roll back to")
        files = verified(root, previous)
        target = activate(root, files, previous, current)
        return result(previous, target, ["Temporary local rollback; use --offline for this effort until recovery"])
    if not offline:
        try:
            # A namespaced local tracking ref avoids races with a user's FETCH_HEAD.
            # No force, checkout, user branch or origin/main rewrite is required.
            git(root, "fetch", "--quiet", "--no-tags", "--", source,
                "refs/heads/main:refs/self-adoption/main")
            main = git(root, "rev-parse", "refs/self-adoption/main").decode().strip()
            with tempfile.TemporaryDirectory(prefix="governance-adoption-") as temporary:
                remote = Path(temporary) / "distribution.git"
                git(root, "clone", "--quiet", "--bare", "--", distribution, str(remote))
                files, selected, warning = select(root, remote, main)
                if selected["version"] == current["version"] and selected["release_commit"] != current["release_commit"]:
                    raise ValueError("frozen active release tag moved")
                # Retain normal Git publication objects for offline provenance checks.
                # A non-force namespaced ref also refuses replacement of a retained tag.
                release_ref = "refs/self-adoption/releases/v" + selected["version"]
                retained = subprocess.run(["git", "rev-parse", "--verify", release_ref],
                                          cwd=root, capture_output=True, timeout=30)
                if not retained.returncode and retained.stdout.decode().strip() != selected["release_commit"]:
                    raise ValueError("previously retained frozen release moved")
                git(root, "fetch", "--quiet", "--no-tags", "--", str(remote),
                    selected["release_commit"] + ":" + release_ref)
                target = activate(root, files, selected, current)
                current = selected
                if warning:
                    warnings.append(warning)
        except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
            # Avoid exposing transport stderr, remote credentials or command arguments.
            reason = str(error) if isinstance(error, ValueError) else type(error).__name__
            warnings.append("Update failed (" + reason + "); retained accepted guidance. Retry after recovery")
    target = root / ".agents/accepted" / current["source_revision"]
    verified(root, current)
    return result(current, target, warnings)


def result(metadata, target, warnings):
    return {"self_adoption": "RETAINED_WITH_WARNING" if warnings else "PASS",
            "version": metadata["version"], "source_revision": metadata["source_revision"],
            "release_commit": metadata["release_commit"], "payload_sha256": metadata["payload_sha256"],
            "directory": str(target.resolve()), "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="use the last verified accepted projection")
    parser.add_argument("--rollback", action="store_true", help="select the previous verified projection locally")
    args = parser.parse_args()
    try:
        print(json.dumps(refresh(offline=args.offline, rollback=args.rollback), indent=2))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        parser.exit(1, "No verified active guidance: " + type(error).__name__ + "; preserve work and recover\n")


if __name__ == "__main__":
    main()
