"""Read-only static checks for the Task 32 experiment; never a model verdict."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import tomllib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ACCEPTED = "15e8191435a126e54b4d1739a73fab112e01c081"
STEP1 = "bae27d667e953e9d4fa0da17cdc51860d13efbf4"
STEP3_START = "981ca259fab7e533653a7efc8aef8acfad95d4e9"
SLOT = "vibevm/vibedeps/org.jresearch.ai.development-governance/2.2.0/"
ADOPTED = frozenset((
    "proportional-controls", "requirement-authority", "package-versioning",
    "task-handoff", "self-adoption"))
ACTIVE_FILES = frozenset("docs/task-32/step-2/" + path for path in (
    "bootstrap-template.md", "bindings/shared-governance.md",
    "shared-governance-instructions.md", "verify-text.py"))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def verify_composition(template, binding, full):
    assert template.count("{{PROJECT_BINDING}}") == 1, "Expected one binding placeholder"
    expected = template.replace("{{PROJECT_BINDING}}", binding.rstrip())
    assert "{{" not in expected and "}}" not in expected, "Unresolved placeholder"
    assert full == "```markdown\n" + expected + "```\n", "Full text differs from static template/binding"
    assert full.count("```") == 2, "Expected one complete Markdown fence"
    assert len(expected) < 8000, "Experimental text must not be clipped to fit"
    assert len(expected) <= 7000, "Keep at least 1000 characters of experimental headroom"
    return expected


def verify_step3_paths(changed_paths):
    unexpected = sorted(path for path in changed_paths
                        if path not in ACTIVE_FILES and not path.startswith("docs/task-32/step-3/"))
    assert not unexpected, "Outside Step 3 scope: " + ", ".join(unexpected)


def changed_paths():
    # Include committed changes, both workspace/index views and ordinary untracked files.
    paths = set()
    for args in (
        ("diff", "--name-only", "--no-renames", "-z", STEP3_START),
        ("diff", "--cached", "--name-only", "--no-renames", "-z", STEP3_START),
        ("ls-files", "--others", "--exclude-standard", "-z"),
    ):
        paths.update(path for path in git(*args).decode().split("\0") if path)
    return paths


def negative_probes():
    # In-memory malformed inputs, not simulated ChatGPT behavior or workspace mutations.
    template = "# Fixture\n\n{{PROJECT_BINDING}}\n"
    binding = "Fixture binding\n"
    full = "```markdown\n" + template.replace("{{PROJECT_BINDING}}", binding.rstrip()) + "```\n"
    probes = {
        "composition_mismatch": lambda: verify_composition(template, binding, full + "changed\n"),
        "unresolved_placeholder": lambda: verify_composition(
            template, "{{UNRESOLVED}}\n",
            "```markdown\n" + template.replace("{{PROJECT_BINDING}}", "{{UNRESOLVED}}") + "```\n"),
        "oversize": lambda: verify_composition("{{PROJECT_BINDING}}\n", "x" * 8000,
                                               "```markdown\n" + "x" * 8000 + "\n```\n"),
        "headroom": lambda: verify_composition("{{PROJECT_BINDING}}\n", "x" * 7000,
                                               "```markdown\n" + "x" * 7000 + "\n```\n"),
        "step_1_history": lambda: verify_step3_paths({"docs/task-32/step-1/README.md"}),
        "step_2_history": lambda: verify_step3_paths({"docs/task-32/step-2/evidence/preparation.json"}),
        "protected_new_path": lambda: verify_step3_paths({"packages/untracked-fixture.md"}),
    }
    for name, probe in probes.items():
        try:
            probe()
        except AssertionError:
            continue
        raise AssertionError("Negative probe did not reject: " + name)
    return {name: "REJECTED AS EXPECTED" for name in probes}


def verify():
    template = (HERE / "bootstrap-template.md").read_text(encoding="utf-8")
    binding = (HERE / "bindings/shared-governance.md").read_text(encoding="utf-8")
    full = (HERE / "shared-governance-instructions.md").read_text(encoding="utf-8")
    expected = verify_composition(template, binding, full)

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
    slot = SLOT + "vibevm/vibespecs/protocols/"
    paths += [slot + topic + ".md" for topic in sorted(ADOPTED)]
    for path in paths:
        git("cat-file", "-e", ACCEPTED + ":" + path)
    tree = git("ls-tree", "--name-only", ACCEPTED, "vibevm/vibespecs/boot/STATIC.md")
    assert not tree, "Recorded absent STATIC differs from accepted tree"
    # Check concrete binding identities/routes; this cannot infer model compliance.
    bound_shas = set(re.findall(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", binding))
    assert bound_shas == {ACCEPTED}, "Binding must retain the accepted source SHA"
    code_spans = set(re.findall(r"`([^`]+)`", binding))
    assert {"docs/manual-task-handoff.md", "docs/self-adoption.md", "task-handoff.md",
            "vibevm/vibespecs/boot/INDEX.md", "vibevm/vibespecs/boot/STATIC.md",
            "vibe.lock", SLOT} <= code_spans, "Binding lacks accepted local/native routes"
    agents_url = "https://github.com/jresearchsoftware/shared-governance/blob/" + ACCEPTED + "/AGENTS.md"
    assert agents_url in binding, "Accepted AGENTS link differs from binding"
    decision_url = "https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6177571849"
    assert decision_url in binding, "Active binding lacks the controlling Step 3 Decision"
    adoption = re.search(r"Conditional adopted topics:\s*([^\.\n]+)", binding)
    assert adoption, "Binding lacks its conditional topic declaration"
    assert set(re.findall(r"[a-z]+(?:-[a-z]+)+", adoption.group(1))) == ADOPTED, "Topic adoption changed"
    excluded = re.search(r"Neither\s+([a-z-]+)\s+nor\s+([a-z-]+)\s+is adopted", binding)
    assert excluded and set(excluded.groups()) == {"github-repository-governance", "independent-review"}, "Unadopted topic boundary missing"
    lock = tomllib.loads(git("show", ACCEPTED + ":vibe.lock").decode())
    package = lock["package"]
    assert len(package) == 1 and (package[0]["group"], package[0]["name"], package[0]["version"]) == (
        "org.jresearch.ai", "development-governance", "2.2.0"), "Binding slot differs from accepted lock"
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
    verify_step3_paths(changed_paths())
    history = set(git("ls-tree", "-r", "--name-only", STEP3_START,
                      "docs/task-32/step-2").decode().splitlines()) - ACTIVE_FILES
    assert not git("diff", STEP3_START, "--", *sorted(history)), "Step 2 historical files changed"
    protected = ["AGENTS.md", "packages", "vibevm", "vibe.toml", "vibe.lock", "scripts", ".github"]
    assert not git("diff", ACCEPTED, "--", *protected), "Package/native/authority scope changed"
    return {
        "scope": "local text/source facts only; no settings or model qualification",
        "static_full_text": "PASS",
        "unicode_characters_inside_fence": len(expected),
        "characters_below_8000_limit": 8000 - len(expected),
        "utf8_sha256_inside_fence": hashlib.sha256(expected.encode()).hexdigest(),
        "unchanged_inputs_reproduce_identical_output": "PASS",
        "accepted_connector_content_and_routes": "PASS",
        "active_binding_identity_routes_and_topic_boundary": "PASS",
        "frozen_consumer_route_existence_only": "PASS",
        "step_1_step_2_history_and_package_native_preservation": "PASS",
        "step_3_tracked_staged_and_untracked_scope": "PASS",
        "negative_static_probes": negative_probes(),
        "model_behavior": "NOT QUALIFIED; owner-reported trials recorded separately in Step 3",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
