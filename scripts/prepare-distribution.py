#!/usr/bin/env python3
"""Prepare or verify one passive package from a full local source commit; never publish."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
import tomllib
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0"
REPOSITORY = "https://github.com/jresearchsoftware/shared-governance"
COORDINATE = "org.jresearch.ai/development-governance"
SLOT = "vibevm/vibedeps/org.jresearch.ai.development-governance/0.1.0"
RECEIPT = "DISTRIBUTION.json"


def vibe_hash(files):
    """Pinned VibeVM 1.0.7 legacy tree recipe, for this bounded UTF-8 file set."""
    digest = hashlib.sha256()
    for name in sorted(files, key=lambda name: Path(name).parts):
        digest.update(name.encode() + b"\0" + files[name] + b"\0")
    return "sha256:" + digest.hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def validate_skill_links(files, prefix):
    """A selected native Skill must keep local references within its own export."""
    for name, data in files.items():
        if not name.startswith(prefix + "/"):
            continue
        prose = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", data.decode(), flags=re.M | re.S)
        targets = re.findall(r"\[[^\]\n]*\]\(\s*(<[^>\n]*>|[^)\s]+)", prose)
        targets += re.findall(r"^ {0,3}\[[^\]\n]+\]:\s*(<[^>\n]*>|[^\s]+)", prose, flags=re.M)
        for target in targets:
            url = urlsplit(target.strip("<>"))
            if url.scheme or url.netloc:
                continue
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path))) if url.path else name
            if not resolved.startswith(prefix + "/") or resolved not in files:
                raise ValueError("native Skill has an escaping or missing local reference: " + name)


def validate_payload(files, license_bytes):
    """Allow only declared passive Skills and their bounded reference files."""
    for data in files.values():
        data.decode("utf-8")
    if "vibe.toml" not in files or "LICENSE" not in files:
        raise ValueError("source commit has no complete package")
    manifest = tomllib.loads(files["vibe.toml"].decode())
    package = manifest.get("package", {})
    if not isinstance(package, dict):
        raise ValueError("source package metadata must be a table")
    expected = {"group": "org.jresearch.ai", "name": "development-governance",
                "version": "0.1.0", "kind": "flow", "format": "simple", "epoch": 1,
                "publish": False, "license": "MIT"}
    if any(type(package.get(key)) is not type(value) or package.get(key) != value
           for key, value in expected.items()):
        raise ValueError("source package identity/passivity/publication boundary differs")
    if set(manifest) != {"package", "boot_snippet", "skill"}:
        raise ValueError("unexpected package capability or dependency")
    if set(package) - (set(expected) | {"description"}):
        raise ValueError("unexpected package metadata")
    boot = {"source": "vibevm/vibespecs/boot/development-governance.md",
            "category": "flow", "link": "dynamic"}
    skills = manifest["skill"]
    if manifest["boot_snippet"] != boot or not isinstance(skills, list) or not skills:
        raise ValueError("package boot/skill declarations differ")
    names = set()
    allowed = {"vibe.toml", "LICENSE", "README.md", boot["source"]}
    for skill in skills:
        name = skill.get("name") if isinstance(skill, dict) else None
        if (not isinstance(name, str) or len(name) > 64
                or not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", name) or name in names):
            raise ValueError("native Skill names must be safe and unique")
        names.add(name)
        path = "vibevm/vibespecs/skills/" + name
        if skill != {"name": name, "path": path, "include": ["SKILL.md", "references/*.md"]}:
            raise ValueError("native Skill declaration must select only its passive instructions/references")
        discovery = path + "/SKILL.md"
        text = files.get(discovery, b"").decode()
        if not re.match(r"---\nname: " + re.escape(name) + r"\ndescription: [^\n]*\S[^\n]*\n---\n", text):
            raise ValueError("native Skill discovery frontmatter is missing or mismatched: " + name)
        references = {item for item in files
                      if re.fullmatch(re.escape(path) + r"/references/[^/\\]+\.md", item)}
        if not references:
            raise ValueError("native Skill requires passive reference text: " + name)
        allowed.update({discovery, *references})
        validate_skill_links(files, path)
    if "proportional-controls" not in names:
        raise ValueError("the accepted proportional-controls Skill must be retained")
    if set(files) != allowed:
        raise ValueError("source package file set differs from declared passive payload")
    if files["LICENSE"] != license_bytes:
        raise ValueError("source/package license notices differ")
    return skills


def snapshot(revision):
    # Full commits make preparation stable even when source branches/tags move.
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("--source-ref must be a full 40-character source commit SHA")
    resolved = git("rev-parse", "--verify", revision + "^{commit}").decode().strip()
    if resolved != revision:
        raise ValueError("source commit identity differs")
    files = {}
    for entry in git("ls-tree", "-rz", revision, "--", PACKAGE).split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        relative = Path(name.decode()).relative_to(PACKAGE).as_posix()
        if mode != "100644" or kind != "blob":
            raise ValueError("package contains a non-ordinary file: " + relative)
        files[relative] = git("cat-file", "blob", oid)
    validate_payload(files, git("show", revision + ":LICENSE"))
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
    # Hash the sorted path/hash map, binding both file names and file bytes.
    content = hashlib.sha256(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    receipt = {"schema": 1, "source_repository": REPOSITORY, "source_revision": revision,
               "source_path": PACKAGE, "package": COORDINATE, "version": "0.1.0",
               "payload_sha256": content, "sha256": hashes}
    files[RECEIPT] = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
    return files, receipt


def prepare(revision, destination):
    files, receipt = snapshot(revision)  # Validate before creating any output.
    destination = Path(destination)
    if destination.is_symlink() or destination.resolve().is_relative_to(ROOT):
        raise ValueError("distribution destination must be outside the authoring checkout, not a symlink")
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError("destination must be absent or empty; distribution is not overwritten")
    destination.mkdir(parents=True, exist_ok=True)
    for relative, data in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return receipt


def verify(revision, directory, installed=False):
    # Rebuild expectations from canonical Git, never trust a co-located receipt alone.
    files, receipt = snapshot(revision)
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("distribution must be an ordinary directory")
    actual = set()
    for path in directory.rglob("*"):
        relative = path.relative_to(directory).as_posix()
        if relative == ".git" or relative.startswith(".git/"):
            continue
        if path.is_symlink():
            raise ValueError("distribution contains a symlink: " + relative)
        if path.is_file():
            actual.add(relative)
        elif not path.is_dir():
            raise ValueError("distribution contains a non-ordinary file: " + relative)
    if installed:
        actual.discard(".vibe-slot.toml")
        marker = tomllib.loads((directory / ".vibe-slot.toml").read_text())
        entries = [{"path": name, "sha256": hashlib.sha256(data).hexdigest()}
                   for name, data in sorted(files.items())]
        if (set(marker) != {"schema", "source_hash", "spec_format", "file"}
                or marker["schema"] != 1 or marker["spec_format"] != "mixed"
                or marker["source_hash"] != vibe_hash(files) or marker["file"] != entries):
            raise ValueError("installed slot metadata differs from canonical source identity")
    if actual != set(files):
        raise ValueError("distribution file set differs; missing=" + repr(sorted(set(files) - actual))
                         + "; extra=" + repr(sorted(actual - set(files))))
    for relative, expected in files.items():
        if (directory / relative).read_bytes() != expected:
            raise ValueError("distribution bytes differ: " + relative)
    return receipt


def verify_consumer(revision, directory):
    directory = Path(directory)
    files, receipt = snapshot(revision)
    slot = directory / SLOT
    verify(revision, slot, installed=True)
    manifest = tomllib.loads((directory / "vibe.toml").read_text())
    requires = manifest.get("requires", {})
    packages = requires.get("packages", {}) if isinstance(requires, dict) else None
    requirement = packages.get(COORDINATE) if isinstance(packages, dict) else None
    if (not isinstance(requirement, dict) or requirement.get("version") != "=0.1.0"
            or not isinstance(requirement.get("git"), str) or not requirement["git"]
            or bool(requirement.get("tag")) == bool(requirement.get("rev"))
            or requirement.get("branch")):
        raise ValueError("consumer must declare exact-version Git tag/rev requirement")
    if (requirement.get("rev") and (not isinstance(requirement["rev"], str)
                                   or not re.fullmatch(r"[0-9a-f]{40}", requirement["rev"]))):
        raise ValueError("consumer Git revision must be a full commit SHA")
    lock = tomllib.loads((directory / "vibe.lock").read_text())
    meta = lock.get("meta")
    if not isinstance(meta, dict) or type(meta.get("schema_version")) is not int or meta["schema_version"] != 7:
        raise ValueError("consumer lock must use pinned VibeVM schema 7")
    locked = lock.get("package", [])
    if not isinstance(locked, list) or any(not isinstance(entry, dict) for entry in locked):
        raise ValueError("consumer lock packages must be tables")
    packages = [entry for entry in locked if
                entry.get("group") == "org.jresearch.ai" and entry.get("name") == "development-governance"]
    if len(packages) != 1:
        raise ValueError("consumer lock has no unique package identity")
    entry = packages[0]
    if any(entry.get(key) != value for key, value in {
            "version": "0.1.0", "source_kind": "git", "source_url": requirement["git"],
            "source_ref": requirement.get("rev") or requirement["tag"], "content_hash": vibe_hash(files)}.items()):
        raise ValueError("consumer lock differs from canonical content/source declaration")
    for skill in tomllib.loads(files["vibe.toml"].decode())["skill"]:
        projected = directory / ".agents/skills" / skill["name"]
        prefix = skill["path"] + "/"
        expected = {name.removeprefix(prefix): data for name, data in files.items() if name.startswith(prefix)}
        if not projected.is_dir() or projected.is_symlink():
            raise ValueError("consumer native skill projection is missing: " + skill["name"])
        paths = list(projected.rglob("*"))
        if any(path.is_symlink() or (not path.is_file() and not path.is_dir()) for path in paths):
            raise ValueError("consumer native skill projection contains non-ordinary files")
        actual = {path.relative_to(projected).as_posix(): path.read_bytes() for path in paths if path.is_file()}
        if actual != expected:
            raise ValueError("consumer native skill projection differs from canonical source: " + skill["name"])
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", required=True, help="full source commit; acceptance is verified by its owner")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--destination", type=Path, help="new/empty directory outside this authoring checkout")
    action.add_argument("--verify", type=Path, metavar="DIRECTORY", help="compare prepared bytes with canonical source")
    action.add_argument("--verify-installed", type=Path, metavar="DIRECTORY", help="also validate VibeVM's generated slot receipt")
    action.add_argument("--verify-consumer", type=Path, metavar="DIRECTORY", help="validate manifest, lock, installed bytes and native projection")
    args = parser.parse_args()
    try:
        if args.destination is not None:
            receipt = prepare(args.source_ref, args.destination)
        elif args.verify_consumer:
            receipt = verify_consumer(args.source_ref, args.verify_consumer)
        else:
            receipt = verify(args.source_ref, args.verify or args.verify_installed, bool(args.verify_installed))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, "Distribution validation failed: " + str(error) + "\n")
    print(json.dumps({"distribution": "PASS", "action": "prepare" if args.destination else "verify",
                      "source_revision": receipt["source_revision"],
                      "payload_sha256": receipt["payload_sha256"], "files": len(receipt["sha256"]),
                      "publication": "this command never publishes; acceptance/remote authority are external"}))


if __name__ == "__main__":
    main()
