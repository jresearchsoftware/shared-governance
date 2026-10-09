#!/usr/bin/env python3
"""Export the instruction-only baseline from an exact local Git commit."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0"
LEGACY_PACKAGE = "vibevm/vibepacks/org.jresearch.governance/proportional-controls/v0.1.0"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def export(ref, destination, skill="proportional-controls"):
    revision = git("rev-parse", "--verify", ref + "^{commit}").decode().strip()
    if not isinstance(skill, str) or len(skill) > 64 or not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", skill):
        raise ValueError("select a safe declared native Skill name")
    # Resolve the layout from this exact commit; historical baseline exports remain supported.
    members = tomllib.loads(git("show", revision + ":vibe.toml").decode())["workspace"]["members"]
    if len(members) != 1 or members[0] not in {PACKAGE, LEGACY_PACKAGE}:
        raise ValueError("the selected commit has no supported governance package")
    package = members[0]
    skill_path = "vibevm/vibespecs/skills/" + skill
    declarations = tomllib.loads(git("show", revision + ":" + package + "/vibe.toml").decode()).get("skill", [])
    selected = [entry for entry in declarations if entry.get("name") == skill]
    if selected != [{"name": skill, "path": skill_path, "include": ["SKILL.md", "references/*.md"]}]:
        raise ValueError("the selected commit has no unique passive Skill declaration")
    source_path = package + "/" + skill_path
    if destination.is_symlink():
        raise ValueError("skill destination must not be a symlink")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("destination must be absent or empty; existing skills are not overwritten")
    blobs = []
    for entry in git("ls-tree", "-rz", revision, "--", source_path).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        path = name.decode("utf-8")
        relative = Path(path).relative_to(source_path)
        if mode != "100644" or kind != "blob":
            raise ValueError("skill export only supports ordinary instruction files")
        if relative.as_posix() != "SKILL.md" and not re.fullmatch(r"references/[^/\\]+\.md", relative.as_posix()):
            raise ValueError("skill export only supports declared passive instruction/reference files")
        data = git("cat-file", "blob", oid)
        text = data.decode()
        if relative.as_posix() == "SKILL.md" and not re.match(
                r"---\nname: " + re.escape(skill) + r"\ndescription: [^\n]*\S[^\n]*\n---\n", text):
            raise ValueError("Skill discovery frontmatter differs from its declaration")
        blobs.append((relative, data))
    if not blobs or not any(str(path) == "SKILL.md" for path, _ in blobs):
        raise ValueError("the selected commit has no " + skill + " skill")
    if not any(path.as_posix().startswith("references/") for path, _ in blobs):
        raise ValueError("the selected Skill has no passive references")
    spec = importlib.util.spec_from_file_location("preparation", Path(__file__).with_name("prepare-distribution.py"))
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    preparation.validate_skill_links({skill_path + "/" + path.as_posix(): data for path, data in blobs}, skill_path)
    license_bytes = git("show", revision + ":" + package + "/LICENSE")
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
                  "revision": revision, "source_path": source_path, "sha256": hashes}
    (destination / "SOURCE.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    return provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="reviewed local commit or ref, resolved to a full commit SHA")
    parser.add_argument("--destination", required=True, type=Path, help="new/empty skill directory")
    parser.add_argument("--skill", default="proportional-controls", help="declared native Skill to export")
    args = parser.parse_args()
    try:
        result = export(args.ref, args.destination, args.skill)
    except (ValueError, KeyError, subprocess.CalledProcessError, OSError) as error:
        parser.exit(1, "Export failed: " + str(error) + "\n")
    print(json.dumps({"export": "PASS", "revision": result["revision"], "files": len(result["sha256"])}))


if __name__ == "__main__":
    main()
