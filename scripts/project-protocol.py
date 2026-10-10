#!/usr/bin/env python3
"""Reproduce the first flow protocol from the accepted historical Skill bytes."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ACCEPTED_SKILL_REVISION = "fd609af8a1ea8ce015fda4652e5a8c444ca821c5"
PROTOCOL = "vibevm/vibespecs/protocols/proportional-controls.md"


def snapshot():
    spec = importlib.util.spec_from_file_location("vendor", ROOT / "scripts/vendor-skill.py")
    vendor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vendor)
    with tempfile.TemporaryDirectory(prefix="governance-protocol-origin-") as temporary:
        target = Path(temporary) / "skill"
        source = vendor.export(ACCEPTED_SKILL_REVISION, target)
        wrapper = (target / "SKILL.md").read_bytes().split(b"\n---\n\n", 1)[1]
        navigation = b"Read [references/protocol.md](references/protocol.md) when a proposed control\n"
        if wrapper.count(navigation) != 1 or wrapper.count(b"The skill does not require") != 1:
            raise ValueError("accepted wrapper differs from the reviewed conversion")
        wrapper = wrapper.replace(navigation, b"Apply this protocol when a proposed control\n")
        wrapper = wrapper.replace(b"The skill does not require", b"This protocol does not require")
        protocol = wrapper.rstrip() + b"\n\n" + (target / "references/protocol.md").read_bytes()
        license_bytes = (target / "LICENSE").read_bytes()
    receipt = {"schema": 1, "transformation": "skill-to-protocol-v1", "source": source,
               "sha256": {"proportional-controls.md": hashlib.sha256(protocol).hexdigest(),
                          "LICENSE": hashlib.sha256(license_bytes).hexdigest()}}
    return protocol, license_bytes, receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, required=True, help="new/empty disposable directory")
    args = parser.parse_args()
    target = args.destination
    if target.is_symlink() or (target.exists() and (not target.is_dir() or any(target.iterdir()))):
        parser.exit(1, "Destination must be absent or empty, not a symlink\n")
    protocol, license_bytes, receipt = snapshot()
    target.mkdir(parents=True, exist_ok=True)
    (target / "proportional-controls.md").write_bytes(protocol)
    (target / "LICENSE").write_bytes(license_bytes)
    (target / "SOURCE.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"projection": "PASS", "accepted_origin": ACCEPTED_SKILL_REVISION,
                      "protocol_sha256": receipt["sha256"]["proportional-controls.md"]}))


if __name__ == "__main__":
    main()
