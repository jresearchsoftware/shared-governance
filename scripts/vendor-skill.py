#!/usr/bin/env python3
"""Export the instruction-only baseline from an exact local Git commit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "vibevm/vibepacks/org.jresearch.governance/proportional-controls/v0.1.0"
SKILL = PACKAGE + "/vibevm/vibespecs/skills/proportional-controls"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def export(ref, destination):
    revision = git("rev-parse", "--verify", ref + "^{commit}").decode().strip()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("destination must be absent or empty; existing skills are not overwritten")
    blobs = []
    for entry in git("ls-tree", "-rz", revision, "--", SKILL).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        path = name.decode("utf-8")
        relative = Path(path).relative_to(SKILL)
        if mode != "100644" or kind != "blob":
            raise ValueError("skill export only supports ordinary instruction files")
        blobs.append((relative, git("cat-file", "blob", oid)))
    if not blobs or not any(str(path) == "SKILL.md" for path, _ in blobs):
        raise ValueError("the selected commit has no proportional-controls skill")
    license_bytes = git("show", revision + ":" + PACKAGE + "/LICENSE")
    destination.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for relative, data in blobs:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        hashes[relative.as_posix()] = hashlib.sha256(data).hexdigest()
    (destination / "LICENSE").write_bytes(license_bytes)
    hashes["LICENSE"] = hashlib.sha256(license_bytes).hexdigest()
    provenance = {"repository": "https://github.com/jresearchsoftware/shared-governance",
                  "revision": revision, "source_path": SKILL, "sha256": hashes}
    (destination / "SOURCE.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="reviewed local commit or ref, resolved to a full commit SHA")
    parser.add_argument("--destination", required=True, type=Path, help="new/empty skill directory")
    args = parser.parse_args()
    try:
        result = export(args.ref, args.destination)
    except (ValueError, subprocess.CalledProcessError, OSError) as error:
        parser.exit(1, "Export failed: " + str(error) + "\n")
    print(json.dumps({"export": "PASS", "revision": result["revision"], "files": len(result["sha256"])}))


if __name__ == "__main__":
    main()
