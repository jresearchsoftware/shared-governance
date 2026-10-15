#!/usr/bin/env python3
"""Task-local static route evidence from an ordinary native-installed consumer."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import tomllib


ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--consumer", required=True, type=Path)
    parser.add_argument("--source-ref", required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("distribution", ROOT / "scripts/prepare-distribution.py")
    distribution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(distribution)
    receipt = distribution.verify_consumer(args.source_ref, args.consumer)
    slot = args.consumer / distribution.slot(receipt["version"])
    index = tomllib.loads((args.consumer / distribution.BOOT_INDEX).read_text())
    boot = slot / "vibevm/vibespecs/boot/development-governance.md"
    assert index["entry"] == [{"path": boot.relative_to(args.consumer).as_posix(), "kind": "static"}]
    assert not (args.consumer / "vibevm/vibespecs/boot/STATIC.md").exists()
    initial_reads = [args.consumer / entry["path"] for entry in index["entry"]]
    guide = slot / distribution.ONBOARDING
    examples = slot / distribution.ONBOARDING_EXAMPLES
    assert guide not in initial_reads and examples not in initial_reads
    text = boot.read_text()
    match = re.search(r"\[onboarding procedure\]\(([^)]+)\)", text)
    assert match and (boot.parent / match[1]).resolve() == guide.resolve()
    assert "Skip that detail in ordinary sessions and on package install/update alone." in text
    assert "explicitly requests project onboarding" in text
    assert not (args.consumer / "docs/onboarding.md").exists()
    assert not (args.consumer / "packages/development-governance").exists()
    # All procedure/example Markdown links were checked against the complete export
    # by verify_consumer. Open the actual installed files and selected detail here.
    guide_text, examples_text = guide.read_text(), examples.read_text()
    assert guide_text and examples_text
    assert (slot / "tools/chatgpt/README.md").is_file()
    assert len(list((slot / "vibevm/vibespecs/protocols").glob("*.md"))) == 9
    overlay = re.sub(r"<vibevm>.*?</vibevm>", "", (args.consumer / "AGENTS.md").read_text(), flags=re.S).strip()
    assert overlay == "Human-owned fixture instructions."
    print(json.dumps({
        "qualification": "PASS", "source_revision": receipt["source_revision"],
        "version": receipt["version"], "payload_sha256": receipt["payload_sha256"],
        "consumer": str(args.consumer), "initial_index_entries": index["entry"],
        "conditional_boot_excerpt": text[text.index("When a person explicitly"):].strip(),
        "explicit_onboarding_route": ["AGENTS.md", distribution.BOOT_INDEX,
                                      boot.relative_to(args.consumer).as_posix(),
                                      guide.relative_to(args.consumer).as_posix()],
        "ordinary_session": "INDEX reads only compact boot; guide/examples are conditional links, not eager entries",
        "producer_readme_or_local_instructions_required": False,
        "installed_protocols": 9, "human_overlay": overlay,
        "scope": "real native-installed files and static reading contract; no live agent/model execution or adoption/settings action"
    }, indent=2))


if __name__ == "__main__":
    main()
