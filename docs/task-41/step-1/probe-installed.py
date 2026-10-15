#!/usr/bin/env python3
"""Task-local evidence: optional methods route in an actual installed consumer."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import tomllib


ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer", type=Path, required=True)
    parser.add_argument("--source-ref", required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("distribution", ROOT / "scripts/prepare-distribution.py")
    distribution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(distribution)
    receipt = distribution.verify_consumer(args.source_ref, args.consumer)
    slot = args.consumer / distribution.slot(receipt["version"])
    index = tomllib.loads((args.consumer / distribution.BOOT_INDEX).read_text())
    boot = slot / "vibevm/vibespecs/boot/development-governance.md"
    guide = slot / distribution.ENGINEERING_METHODS
    assert index["entry"] == [{"path": boot.relative_to(args.consumer).as_posix(), "kind": "static"}]
    assert not (args.consumer / "vibevm/vibespecs/boot/STATIC.md").exists()
    text = boot.read_text()
    link = re.search(r"\[optional FPF guide\]\(([^)]+)\)", text)
    assert link and (boot.parent / link[1]).resolve() == guide.resolve()
    assert guide.read_text() and guide not in [args.consumer / e["path"] for e in index["entry"]]
    protocols = list((slot / "vibevm/vibespecs/protocols").glob("*.md"))
    assert len(protocols) == 9
    manifest = tomllib.loads((slot / "vibe.toml").read_text())
    assert set(manifest) == {"package", "boot_snippet"}
    assert not any((args.consumer / path).exists() for path in (
        "docs/authoring.md", "packages/development-governance", "README.md"))
    overlay = re.sub(r"<vibevm>.*?</vibevm>", "", (args.consumer / "AGENTS.md").read_text(), flags=re.S).strip()
    assert overlay == "Human-owned fixture instructions."
    print(json.dumps({
        "qualification": "PASS", "source_revision": receipt["source_revision"],
        "version": receipt["version"], "payload_sha256": receipt["payload_sha256"],
        "initial_index_entries": index["entry"],
        "discovery_route": ["AGENTS.md", distribution.BOOT_INDEX,
                            boot.relative_to(args.consumer).as_posix(),
                            guide.relative_to(args.consumer).as_posix()],
        "boot_discovery_excerpt": text[text.index("When external engineering"):].strip(),
        "installed_protocols": len(protocols), "manifest_tables": sorted(manifest),
        "human_overlay": overlay,
        "producer_docs_required": False, "fpf_mcp_calls_or_configuration": 0,
        "ordinary_task_or_review": "Static route leaves guide optional; no eager guide INDEX entry",
        "no_mcp": "Native install, export/integrity checks and file route work without an FPF client/server",
        "scope": "Installed files and static reading contract; no model obedience, live review behavior or consumer adoption claim"
    }, indent=2))


if __name__ == "__main__":
    main()
