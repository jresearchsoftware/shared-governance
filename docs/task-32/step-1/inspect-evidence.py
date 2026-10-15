"""Bounded Task 32 research measurements; no client/projection implementation."""
from pathlib import Path
import difflib
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ACCEPTED = "15e8191435a126e54b4d1739a73fab112e01c081"
RELAY = "52bebbc9cafc1e82737943a6d37f00945ffadfef"
DOC = "6014e8e2c20faebfaa656ee1e8e6efb1dcd9d630"
VIBE = "b6659978453f50e6d1d4d99626d70b980a2c5847"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=HERE)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inspect():
    timeline = json.loads((HERE / "evidence/task-chronology.json").read_text(encoding="utf-8"))
    comments = timeline["comments"]
    assert len(comments) == 3
    snapshots = [("docreview-original.md", 9740, "## Merge and closure"),
                 ("relay-supplied.md", 7884, "## Boundaries and profile")]
    measured = []
    for record, (filename, expected, ending) in zip(comments, snapshots):
        body = record["body"]
        assert len(body) == expected and ending in body
        assert (HERE / "evidence" / filename).read_text(encoding="utf-8") == body + "\n"
        sections = []
        for i, line in enumerate(body.splitlines(), 1):
            if line.startswith("## "):
                sections.append({"line": i, "section": line[3:]})
        clipped = body[:8000]
        measured.append({"comment": record["url"], "unicode_characters": len(body),
                         "utf8_sha256": sha(body.encode()), "headroom_to_8000": 8000 - len(body),
                         "clipped_characters": len(body) - len(clipped),
                         "clipped_last_180": clipped[-180:], "removed_suffix": body[8000:],
                         "sections": sections})
    a, b = (record["body"] for record in comments[:2])
    ratio = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    connector = json.loads((HERE / "evidence/connector-source.json").read_text(encoding="utf-8"))
    source = git("show", ACCEPTED + ":AGENTS.md")
    assert connector["content"].encode() == source
    assert connector["sha"] == git("rev-parse", ACCEPTED + ":AGENTS.md").decode().strip()
    reads = {
        ACCEPTED: [
            ("AGENTS.md", "full"),
            ("vibevm/vibespecs/boot/INDEX.md", "full; STATIC.md absent"),
            ("vibevm/vibespecs/boot/00-authoring.md", "full"),
            ("vibevm/vibedeps/org.jresearch.ai.development-governance/2.2.0/vibevm/vibespecs/boot/development-governance.md", "full"),
            ("vibevm/vibedeps/org.jresearch.ai.development-governance/2.2.0/vibevm/vibespecs/protocols/task-handoff.md", "full"),
            ("vibevm/vibedeps/org.jresearch.ai.development-governance/2.2.0/vibevm/vibespecs/protocols/proportional-controls.md", "full"),
            ("vibevm/vibedeps/org.jresearch.ai.development-governance/2.2.0/vibevm/vibespecs/protocols/requirement-authority.md", "full"),
            ("packages/development-governance/vibevm/vibespecs/protocols/independent-review.md", "full as research source; not newly adopted"),
            ("docs/manual-task-handoff.md", "full"),
            ("docs/authoring.md", "full"),
            ("docs/self-adoption.md", "full"),
            ("CONTRIBUTING.md", "full"),
            ("vibe.lock", "full"),
            ("vibe.toml", "full"),
            ("toolchain/vibevm.json", "full"),
        ],
        RELAY: [
            ("AGENTS.md", "full"),
            ("packages/codex-relay/skill/SKILL.md", "full"),
            ("packages/codex-relay/skill/references/workflow.md", "full"),
            ("packages/codex-relay/skill/references/compatibility.md", "full"),
            ("docs/relay-guidance-ownership.md", "full"),
            ("vibe.lock", "full"),
            ("vibevm/vibespecs/boot/INDEX.md", "full"),
            ("guidance/artifacts/vpm/vibe.toml", "full"),
        ],
        DOC: [
            ("AGENTS.md", "full"),
            ("docs-evolution-poc/methodology/relay-consumer-methodology.md", "full"),
            ("docs-evolution-poc/PROJECT-RULES.md", "bounded slices: 1-95, 598-681, 682-692, 725-735, 780-822, 1062-1082; headings scanned"),
            ("docs-evolution-poc/methodology/reader-documentation-gates/gate-policy.yaml", "full"),
            ("docs-evolution-poc/methodology/review-finalization-contract.yaml", "full"),
        ],
        VIBE: [
            ("crates/vibe-agent-projection/src/agents.rs", "1-190: complete Agent enum; scope/What definitions"),
            ("crates/vibe-core/src/manifest/package/when.rs", "full: enum, parser and test source; tests not executed"),
            ("crates/vibe-workspace/src/boot.rs", "bounded when/boot-entry/ordering sections"),
            ("crates/vibe-workspace/src/boot/hybrid.rs", "bounded conditional/static-zone sections"),
        ],
    }
    identities = []
    for revision, files in reads.items():
        for path, scope in files:
            data = git("show", revision + ":" + path)
            identities.append({"revision": revision, "path": path, "inspection": scope,
                               "bytes": len(data), "blob": git("rev-parse", revision + ":" + path).decode().strip(),
                               "sha256": sha(data)})
    comparisons = []
    for accepted, live, paths in [
        (RELAY, "ed2ec60e8096bd2a7477e9eac9e9f9d2603c0f20",
         ["AGENTS.md", "packages/codex-relay/skill", "vibe.lock", "vibevm/vibespecs/boot/INDEX.md"]),
        (DOC, "fd6b0c4eda5c6b5390cbdcdb8a26820f0e5d45c2",
         ["AGENTS.md", "docs-evolution-poc/PROJECT-RULES.md", "docs-evolution-poc/methodology/relay-consumer-methodology.md"]),
    ]:
        differences = git("diff", "--name-only", accepted, live, "--", *paths).decode()
        assert not differences
        comparisons.append({"accepted": accepted, "observed_remote_main": live,
                            "paths": paths, "changed_paths": []})
    return {"scope": "deterministic text/source observations only, not semantic equivalence or model compliance",
            "sources": measured, "character_sequence_similarity": ratio,
            "similarity_limit": "textual diagnostic only; not a percentage of shared obligations",
            "connector_exact_source_match": True, "inspected_git_sources": identities,
            "currentness_comparisons": comparisons}

if __name__ == "__main__":
    result = inspect()
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(output, encoding="utf-8")
        print(json.dumps({"source_completeness": "PASS", "connector_match": "PASS",
                          "currentness": "PASS", "character_sequence_similarity": result["character_sequence_similarity"],
                          "source_files": len(result["inspected_git_sources"])}, indent=2))
    else:
        print(output, end="")
