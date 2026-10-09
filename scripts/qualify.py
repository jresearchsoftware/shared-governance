#!/usr/bin/env python3
"""Check the bounded bootstrap candidate without VibeVM or network access."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MARKERS = re.compile(rb"github_pat_[A-Za-z0-9_]{30,}|gh[pousr]_[A-Za-z0-9_]{20,}|"
                     rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
                     rb"AKIA[0-9A-Z]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{40,}")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(export_ref=None):
    tracked = [Path(name) for name in subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0") if name]
    require(tracked, "no tracked candidate files; stage intended additions")
    links = 0
    for relative in tracked:
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), str(relative) + ": non-regular file")
        data = path.read_bytes()
        require(not MARKERS.search(data), str(relative) + ": credential marker")
        text = data.decode("utf-8")
        if path.suffix == ".json":
            json.loads(text)
        if path.suffix == ".toml":
            tomllib.loads(text)
        if path.suffix != ".md":
            continue
        prose = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)
        for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", prose):
            url = urlsplit(target.strip("<>"))
            if url.scheme or url.netloc:
                continue
            links += 1
            resolved = (path.parent / unquote(url.path)).resolve() if url.path else path
            require(resolved.is_relative_to(ROOT) and resolved.exists(), str(relative) + ": broken local link")
    workspace = tomllib.loads((ROOT / "vibe.toml").read_text(encoding="utf-8"))
    require(set(workspace) == {"workspace"}, "root must remain an authoring-only workspace")
    members = workspace["workspace"]["members"]
    require(len(members) == 1, "authoring has one bounded governance package")
    member = ROOT / members[0]
    require(member.resolve().is_relative_to(ROOT), "member must remain inside the source")
    spec = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare-distribution.py")
    preparation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(preparation)
    require(members == [preparation.PACKAGE], "authoring member differs from the current package coordinate")
    payload = {}
    for path in member.rglob("*"):
        require(not path.is_symlink(), "package must contain ordinary passive text only")
        if path.is_file():
            payload[path.relative_to(member).as_posix()] = path.read_bytes()
    skills = preparation.validate_payload(payload, (ROOT / "LICENSE").read_bytes())
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text(encoding="utf-8"))
    require(pin["version"] == "1.0.7" and pin["source_revision"] == "b6659978453f50e6d1d4d99626d70b980a2c5847", "qualified VibeVM pin changed")
    if export_ref:
        spec = importlib.util.spec_from_file_location("vendor", ROOT / "scripts/vendor-skill.py")
        vendor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vendor)
        with tempfile.TemporaryDirectory(prefix="shared-governance-native-") as temporary:
            for skill in skills:
                skill_path = member / skill["path"]
                target = Path(temporary) / skill["name"]
                provenance = vendor.export(export_ref, target, skill["name"])
                expected = {path.relative_to(skill_path).as_posix() for path in skill_path.rglob("*") if path.is_file()}
                actual = {path.relative_to(target).as_posix() for path in target.rglob("*") if path.is_file()}
                require(actual == expected | {"LICENSE", "SOURCE.json"}, "native export file set differs from candidate")
                for relative, digest in provenance["sha256"].items():
                    require(hashlib.sha256((target / relative).read_bytes()).hexdigest() == digest, "native export digest mismatch")
                for path in skill_path.rglob("*"):
                    if path.is_file():
                        require((target / path.relative_to(skill_path)).read_bytes() == path.read_bytes(), "native export differs from candidate bytes")
    return {"qualification": "PASS", "tracked_files": len(tracked), "local_links": links,
            "secret_scan": "bounded markers PASS", "native_export": "PASS" if export_ref else "not requested"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-ref", help="also compare exact-commit native export with candidate bytes")
    args = parser.parse_args()
    try:
        result = check(args.export_ref)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, "Qualification failed: " + str(error) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
