"""Read-only static checks for the Task 32 experiment; never a model verdict."""
from pathlib import Path
import hashlib
import json
import subprocess
import tomllib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ACCEPTED = "15e8191435a126e54b4d1739a73fab112e01c081"
STEP1 = "bae27d667e953e9d4fa0da17cdc51860d13efbf4"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def verify():
    template = (HERE / "bootstrap-template.md").read_text(encoding="utf-8")
    binding = (HERE / "bindings/shared-governance.md").read_text(encoding="utf-8")
    full = (HERE / "shared-governance-instructions.md").read_text(encoding="utf-8")
    assert template.count("{{PROJECT_BINDING}}") == 1
    expected = template.replace("{{PROJECT_BINDING}}", binding.rstrip())
    assert full == "```markdown\n" + expected + "```\n", "Full text differs from static template/binding"
    assert full.count("```") == 2 and "{{" not in full
    assert len(expected) < 8000, "Experimental text must not be clipped to fit"

    record = json.loads((HERE / "evidence/preparation.json").read_text(encoding="utf-8"))
    assert record["accepted_source_main"] == ACCEPTED
    assert record["starting_candidate_head"] == STEP1
    connector = record["connector"]
    assert connector["ref"] == ACCEPTED
    accepted_bytes = git("show", ACCEPTED + ":AGENTS.md")
    assert connector["content_sha256"] == hashlib.sha256(accepted_bytes).hexdigest()
    assert connector["git_blob_sha"] == git("rev-parse", ACCEPTED + ":AGENTS.md").decode().strip()
    for entry, filename in zip(connector["comments"][:2], ("docreview-original.md", "relay-supplied.md")):
        body = (HERE.parent / "step-1/evidence" / filename).read_text(encoding="utf-8")[:-1]
        assert len(body) == entry["characters"]
        assert hashlib.sha256(body.encode()).hexdigest() == entry["body_utf8_sha256"]

    index = tomllib.loads(git("show", ACCEPTED + ":vibevm/vibespecs/boot/INDEX.md").decode())
    paths = ["docs/manual-task-handoff.md", "docs/self-adoption.md", "vibe.lock"]
    paths += [entry["path"] for entry in index["entry"]]
    slot = "vibevm/vibedeps/org.jresearch.ai.development-governance/2.2.0/vibevm/vibespecs/protocols/"
    paths += [slot + topic + ".md" for topic in (
        "proportional-controls", "requirement-authority", "package-versioning",
        "task-handoff", "self-adoption")]
    for path in paths:
        git("cat-file", "-e", ACCEPTED + ":" + path)
    tree = git("ls-tree", "--name-only", ACCEPTED, "vibevm/vibespecs/boot/STATIC.md")
    assert not tree, "Recorded absent STATIC differs from accepted tree"
    for consumer_ref, consumer_paths in (
        ("52bebbc9cafc1e82737943a6d37f00945ffadfef", [
            "AGENTS.md", "packages/codex-relay/skill/SKILL.md",
            "packages/codex-relay/skill/references/workflow.md",
            "packages/codex-relay/skill/references/compatibility.md",
            "docs/relay-guidance-ownership.md"]),
        ("6014e8e2c20faebfaa656ee1e8e6efb1dcd9d630", [
            "AGENTS.md", "docs-evolution-poc/PROJECT-RULES.md",
            "docs-evolution-poc/methodology/relay-consumer-methodology.md",
            "docs-evolution-poc/methodology/reader-documentation-gates/gate-policy.yaml",
            "docs-evolution-poc/methodology/review-finalization-contract.yaml"]),
    ):
        for path in consumer_paths:
            git("cat-file", "-e", consumer_ref + ":" + path)

    assert not git("diff", STEP1, "--", "docs/task-32/step-1"), "Step 1 history changed"
    protected = ["AGENTS.md", "packages", "vibevm", "vibe.toml", "vibe.lock", "scripts", ".github"]
    assert not git("diff", ACCEPTED, "--", *protected), "Package/native/authority scope changed"
    return {
        "scope": "local text/source facts only; no settings or model qualification",
        "static_full_text": "PASS",
        "unicode_characters_inside_fence": len(expected),
        "utf8_sha256_inside_fence": hashlib.sha256(expected.encode()).hexdigest(),
        "unchanged_inputs_reproduce_identical_output": "PASS",
        "accepted_connector_content_and_routes": "PASS",
        "frozen_consumer_route_existence_only": "PASS",
        "step_1_and_package_native_preservation": "PASS",
        "real_chatgpt_cases": "NOT RUN / UNQUALIFIED",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
