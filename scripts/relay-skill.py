#!/usr/bin/env python3
"""Offline integrity check for pinned Relay and producer-owned Shared adoption."""
import hashlib
import json
from pathlib import Path
import tomllib

RELAY = "flow:org.jresearch.ai/codex-relay"
SHARED = "flow:org.jresearch.ai/development-governance"
RELAY_VERSION = "10.0.0"
RELAY_PIN = (RELAY_VERSION, "5cc8d97d6c88eb77c15d640c1e022974036d5037",
             "sha256:feb84ec2551c558e15230f20e5ed471335139c0201a854b4a5d16f6fc6346bdf")
RELAY_SOURCE = "c2fed9a7edb1b9f9d6694b746f4be943669cb270"
RELAY_DISTRIBUTION_HASH = "3451635330cd96379e5009314e5f39f46840138e8a24d4a0c1799de611549c5b"
SHARED_REQUIREMENT = ">=12.1.0"
SLOT = f"vibevm/vibedeps/org.jresearch.ai.codex-relay/{RELAY_VERSION}"
LANDSCAPE = {
    "flow:org.jresearch.ai/landscape-model-guidance": (
        "1.1.0", "a810317f87fb4378be19edb04506444553f60148",
        "sha256:f7245df4142fe6d9651f1050edc493dfe0b7078e0075211e7190440ff04cbd5d"),
    "flow:org.jresearch.ai/landscape-subagents": (
        "1.1.0", "b3e9da5a10af2b258699e7d1667dc925d247ae8d",
        "sha256:4ea4a61964e63d2fc91a6aa2ae486e6edc8231823266f6feefb83de6b615f1ae"),
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
    shared_version = tomllib.loads(authored["vibe.toml"].decode())["package"]["version"]
    pins = {RELAY: RELAY_PIN, SHARED: (shared_version, None, vibe_hash(authored)), **LANDSCAPE}
    require(set(requirements) == set(pins), "unexpected root graph")
    require(requirements[SHARED] == dict(version="=" + shared_version, link="dynamic"),
            "exact producer Shared root")
    root_dependencies = sorted(key + "@=" + version for key, (version, _, _) in pins.items())
    lock = tomllib.loads((root / "vibe.lock").read_text(encoding="utf-8"))
    require(lock["meta"]["schema_version"] == 7 and
            sorted(lock["meta"]["root_dependencies"]) == root_dependencies, "lock root identity")
    entries = lock["package"]
    require(len(entries) == len(pins), "expected unique locked packages without extra closure")
    payloads = {}
    for coordinate, (version, revision, content_hash) in pins.items():
        group, name = coordinate.removeprefix("flow:").split("/")
        producer_source = coordinate == SHARED
        if not producer_source:
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
                    and not {"source_ref", "resolved_commit"} & selected[0].keys(),
                    "local producer source identity")
        else:
            expected = dict(kind="flow", version=version, source_kind="git", source_url=url,
                            source_ref=revision, resolved_commit=revision, content_hash=content_hash)
        require(all(selected[0].get(k) == v for k, v in expected.items()), "locked source " + name)
        if coordinate == RELAY:
            require(selected[0].get("dependencies") == [SHARED.removeprefix("flow:") + "@=" + shared_version],
                    "Relay dependency must bind to the root-selected Shared slot")
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
            require(distribution["package"] == group + "/" + name and distribution["version"] == version,
                    "distribution identity " + name)
            if coordinate == RELAY:
                require(distribution["source_revision"] == RELAY_SOURCE
                        and distribution["payload_sha256"] == RELAY_DISTRIBUTION_HASH,
                        "pinned Relay distribution identity")
            if coordinate in LANDSCAPE:
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
    relay_manifest = tomllib.loads(relay["vibe.toml"].decode())
    require(relay_manifest["requires"]["packages"] == {SHARED.removeprefix("flow:"): SHARED_REQUIREMENT},
            "Relay's declared Shared requirement")
    skill = {k.removeprefix("skill/"): v for k, v in relay.items() if k.startswith("skill/")}
    require(read_files(root / ".agents/skills/codex-relay") == skill, "projected Skill bytes")
    provenance = json.loads(skill["PROVENANCE.json"])
    require(provenance["version"] == RELAY_VERSION and provenance["protocol_source"] == "consumer-vibe-lock"
            and provenance["delivery_form"] == "vpm" and provenance["shared_requirement"] == SHARED_REQUIREMENT,
            "native Skill provenance")
    protocols = [line.removeprefix("- `").removesuffix("`")
                 for line in skill["references/shared-protocols.md"].decode().splitlines()
                 if line.startswith("- `vibevm/vibespecs/protocols/")]
    require(len(protocols) == len(set(protocols)) == 10 and all(path in shared for path in protocols),
            "Relay protocols must all resolve in the root-selected Shared slot")
    require(provenance["files"] == hashes({k: v for k, v in skill.items() if k != "PROVENANCE.json"}),
            "Skill provenance inventory")
    receipt = tomllib.loads((root / ".agents/skills/.codex-relay.vibe-skill-receipt.toml").read_text())
    require(receipt == dict(schema=1, skill="codex-relay",
            file=[dict(path=k, sha256=v) for k, v in hashes(skill).items()]), "native projection receipt")
    require(not (root / ".codex/skills/codex-relay").exists(), "competing legacy Skill")
    return {"version": RELAY_VERSION, "shared_version": shared_version, "files": len(skill)}
