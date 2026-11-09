#!/usr/bin/env python3
"""Offline integrity check for pinned Relay and producer-owned Shared adoption."""
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
LANDSCAPE = {
    "flow:org.jresearch.ai/landscape-model-guidance": (
        "1.0.3", "48432f00802f5aad106f3e1a9264e17c1edc354c",
        "sha256:a64d829c0e50ac228d9bc39608db7e081e87c13d69e9cfeafc46720ec022f7f6"),
    "flow:org.jresearch.ai/landscape-subagents": (
        "1.0.2", "042e92884278d748502157945301dbc3f3c8318c",
        "sha256:58a76e39b4861f8205726930d89d4f16c320704cb21b146ce4c47c3d2b959e56"),
}


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
    # Retain qualification of historical producer checkouts without Landscape.
    pins = dict(PINS)
    if set(requirements) & set(LANDSCAPE):
        pins.update(LANDSCAPE)
    require(set(requirements) == set(pins), "unexpected root graph")
    shared_version = tomllib.loads(authored["vibe.toml"].decode())["package"]["version"]
    local_shared = requirements[SHARED] == dict(version="=" + shared_version, link="dynamic")
    root_dependencies = sorted(SHARED + "@=" + shared_version if local_shared and key == SHARED
                               else key for key in pins)
    lock = tomllib.loads((root / "vibe.lock").read_text(encoding="utf-8"))
    require(lock["meta"]["schema_version"] == 7 and
            sorted(lock["meta"]["root_dependencies"]) == root_dependencies, "lock root identity")
    entries = lock["package"]
    require(len(entries) == len(pins), "expected unique locked packages without extra closure")
    payloads = {}
    for coordinate, (version, revision, content_hash) in pins.items():
        group, name = coordinate.removeprefix("flow:").split("/")
        producer_source = coordinate == SHARED and local_shared
        if producer_source:
            version, content_hash = shared_version, vibe_hash(authored)
        else:
            url = "https://github.com/jrs-vibevm/" + group + "." + name + ".git"
            require(requirements[coordinate] == dict(version="=" + version, link="dynamic",
                    git=url, rev=revision, auth="none"), "immutable source requirement " + name)
        selected = [e for e in entries if e.get("group") == group and e.get("name") == name]
        require(len(selected) == 1, "ambiguous lock " + name)
        if producer_source:
            expected = dict(kind="flow", version=version, source_kind="registry", content_hash=content_hash)
            source_url = selected[0].get("source_url", "")
            require(source_url.startswith("file://") and source_url.endswith(
                    "/vibevm/vibepacks/org.jresearch.ai/development-governance/v" + version)
                    and "source_ref" not in selected[0], "local producer source identity")
        else:
            expected = dict(kind="flow", version=version, source_kind="git", source_url=url,
                            source_ref=revision, content_hash=content_hash)
        require(all(selected[0].get(k) == v for k, v in expected.items()), "locked source " + name)
        directory = root / "vibevm/vibedeps" / (group + "." + name) / version
        files = read_files(directory)
        marker = tomllib.loads(files.pop(".vibe-slot.toml").decode())
        require(vibe_hash(files) == content_hash, "package bytes " + name)
        require(marker == dict(schema=1, source_hash=content_hash, spec_format="mixed",
                file=[dict(path=k, sha256=v) for k, v in hashes(files).items()]), "slot receipt " + name)
        if producer_source:
            # Local projection is bound to the exact authored Git export by the caller.
            # It has no release-only distribution receipt or invented public revision.
            require(files == authored, "local Shared payload differs from authored governance")
            payloads[name] = files
        else:
            distribution = json.loads(files["DISTRIBUTION.json"])
            payload = {k: v for k, v in files.items() if k != "DISTRIBUTION.json"}
            require(distribution["sha256"] == hashes(payload), "distribution inventory " + name)
            require(distribution["payload_sha256"] == hashlib.sha256(json.dumps(hashes(payload),
                    sort_keys=True, separators=(",", ":")).encode()).hexdigest(), "distribution digest " + name)
            if coordinate in LANDSCAPE:
                require(distribution["package"] == group + "/" + name and distribution["version"] == version,
                        "distribution identity " + name)
                package = tomllib.loads(files["vibe.toml"].decode())
                require(set(package) == {"package", "boot_snippet"} and
                        package["package"]["frozen"] is True and
                        package["package"]["version"] == version and
                        package["package"]["group"] == group and package["package"]["name"] == name,
                        "passive frozen identity " + name)
            payloads[name] = payload
    shared = payloads["development-governance"]
    require(shared == authored, "Shared payload differs from authored governance")
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
    return {"version": "3.0.0", "shared_version": shared_version, "files": len(skill)}
