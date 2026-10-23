#!/usr/bin/env python3
"""Offline integrity check for the reviewed Task 57 native consumer graph."""
import hashlib
import json
from pathlib import Path
import tomllib

RELAY = "flow:org.jresearch.ai/codex-relay"
SHARED = "flow:org.jresearch.ai/development-governance"
PINS = {
    RELAY: ("3.0.0", "325c96371783e2d628bfa9903b3244468c688fe6",
            "sha256:451ee21dbfd63abd7918f0aee979220fb57cb8a8dffde20009a25f11bf9071e7"),
    SHARED: ("5.0.0", "30a23f467c30c41fec918204cbbf2ecfffd7bef5",
             "sha256:e686314f26c82f32f55958a242481d792e9fcd0d755a6eebf933431f3e0875d9"),
}
SLOT = "vibevm/vibedeps/org.jresearch.ai.codex-relay/3.0.0"


def require(condition, message):
    if not condition:
        raise ValueError("native Relay: " + message)


def read_files(directory):
    require(directory.is_dir() and not directory.is_symlink(), "missing ordinary directory " + str(directory))
    files = {}
    for path in directory.rglob("*"):
        require(not path.is_symlink(), "symlink " + str(path))
        if path.is_file():
            files[path.relative_to(directory).as_posix()] = path.read_bytes()
    return files


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}


def check(root, authored, vibe_hash):
    root = Path(root)
    manifest = tomllib.loads((root / "vibe.toml").read_text(encoding="utf-8"))
    requirements = manifest["requires"]["packages"]
    require(set(requirements) == set(PINS), "unexpected root graph")
    lock = tomllib.loads((root / "vibe.lock").read_text(encoding="utf-8"))
    require(lock["meta"]["schema_version"] == 7 and
            lock["meta"]["root_dependencies"] == sorted(PINS), "lock root identity")
    entries = lock["package"]
    require(len(entries) == 2, "expected two unique locked packages")
    payloads = {}
    for coordinate, (version, revision, content_hash) in PINS.items():
        group, name = coordinate.removeprefix("flow:").split("/")
        url = "https://github.com/jrs-vibevm/" + group + "." + name + ".git"
        require(requirements[coordinate] == dict(version="=" + version, link="dynamic",
                git=url, rev=revision, auth="none"), "immutable source requirement " + name)
        selected = [e for e in entries if e.get("group") == group and e.get("name") == name]
        require(len(selected) == 1, "ambiguous lock " + name)
        require(all(selected[0].get(k) == v for k, v in dict(kind="flow", version=version,
                source_kind="git", source_url=url, source_ref=revision,
                content_hash=content_hash).items()), "locked public source " + name)
        directory = root / "vibevm/vibedeps" / (group + "." + name) / version
        files = read_files(directory)
        marker = tomllib.loads(files.pop(".vibe-slot.toml").decode())
        require(vibe_hash(files) == content_hash, "public package bytes " + name)
        require(marker == dict(schema=1, source_hash=content_hash, spec_format="mixed",
                file=[dict(path=k, sha256=v) for k, v in hashes(files).items()]), "slot receipt " + name)
        distribution = json.loads(files["DISTRIBUTION.json"])
        payload = {k: v for k, v in files.items() if k != "DISTRIBUTION.json"}
        require(distribution["sha256"] == hashes(payload), "distribution inventory " + name)
        require(distribution["payload_sha256"] == hashlib.sha256(json.dumps(hashes(payload),
                sort_keys=True, separators=(",", ":")).encode()).hexdigest(), "distribution digest " + name)
        payloads[name] = payload
    shared = payloads["development-governance"]
    require(shared == authored, "public Shared payload differs from authored governance")
    relay = payloads["codex-relay"]
    skill = {k.removeprefix("skill/"): v for k, v in relay.items() if k.startswith("skill/")}
    require(read_files(root / ".agents/skills/codex-relay") == skill, "projected Skill bytes")
    provenance = json.loads(skill["PROVENANCE.json"])
    require(provenance["version"] == "3.0.0" and provenance["protocol_source"] == "consumer-vibe-lock"
            and provenance["delivery_form"] == "vpm" and provenance["shared_requirement"] == ">=2.5.0",
            "native Skill provenance")
    require(provenance["files"] == hashes({k: v for k, v in skill.items() if k != "PROVENANCE.json"}),
            "Skill provenance inventory")
    receipt = tomllib.loads((root / ".agents/skills/.codex-relay.vibe-skill-receipt.toml").read_text())
    require(receipt == dict(schema=1, skill="codex-relay",
            file=[dict(path=k, sha256=v) for k, v in hashes(skill).items()]), "native projection receipt")
    require(not (root / ".codex/skills/codex-relay").exists(), "competing legacy Skill")
    return {"version": "3.0.0", "shared_version": "5.0.0", "files": len(skill)}
