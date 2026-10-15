"""Real Git and exported-tool lifecycle fixtures; no ChatGPT behavioral claims."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "packages/development-governance/tools/chatgpt/project.py"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


projection = module("projection", TOOL)
preparation = module("preparation", ROOT / "scripts/prepare-distribution.py")
ACCEPTED = "15e8191435a126e54b4d1739a73fab112e01c081"
ANCHOR = "https://github.com/jresearchsoftware/shared-governance/issues/32#issuecomment-6187417393"


class ProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.export_temp = tempfile.TemporaryDirectory(prefix="chatgpt-export-")
        cls.addClassCleanup(cls.export_temp.cleanup)
        cls.distribution = Path(cls.export_temp.name) / "package"
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()
        preparation.prepare(sha, cls.distribution)
        cls.distributed_tool = cls.distribution / "tools/chatgpt/project.py"
        # Black-box invocations must test the final source, not an older export.
        if cls.distributed_tool.read_bytes() != TOOL.read_bytes():
            raise AssertionError("Commit current package source before exact-export tests")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="chatgpt-lifecycle-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "consumer"
        self.repo.mkdir()
        self.git("init", "-q")
        for key, value in {"user.name": "Fixture", "user.email": "fixture@example.invalid",
                           "commit.gpgsign": "false", "core.autocrlf": "false",
                           "core.hooksPath": str(self.root / "no-hooks"),
                           "maintenance.auto": "false", "gc.auto": "0"}.items():
            self.git("config", key, value)
        self.write("AGENTS.md", "# Ordinary project\nDiscuss garden planning; no shared topics adopted.\n")
        self.write(projection.INDEX, 'schema = 1\n[[entry]]\npath = "boot.md"\nkind = "static"\n')
        self.write("boot.md", "Only explicitly adopted relevant routes apply.\n")
        self.slot("alpha", "1.0.0", ["first"])
        self.lock([("alpha", "1.0.0")])
        self.config = self.repo / "chatgpt"
        self.binding_path = self.config / "binding.json"
        self.binding = {"schema": 2, "repository": "fixture/project", "navigation_ref": "main",
                        "mode": "read-only-preview", "role": "Garden planning discussion",
                        "permissions": ["discussion", "assessment"], "native": "materialized",
                        "local_sources": [], "character_budget": 8000,
                        "cache_enabled": False, "cache_selection": ["AGENTS.md"]}
        self.write("chatgpt/custom.md", "Discuss planting with me. Do not change external content.\n")
        self.save_binding()
        self.commit()
        self.anchor = "https://github.com/fixture/project/issues/1"

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")

    def save_binding(self):
        self.write("chatgpt/binding.json", json.dumps(self.binding))

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic source and custom fixture")
        self.sha = self.git("rev-parse", "HEAD")

    def slot(self, name, version, topics):
        prefix = f"vibevm/vibedeps/fixture.{name}/{version}/"
        receipt = 'schema = 1\nsource_hash = "sha256:fixture"\n'
        for topic in topics:
            path, text = f"protocols/{topic}.md", f"# {topic}\nPayload {version}\n"
            self.write(prefix + path, text)
            receipt += f'[[file]]\npath = "{path}"\nsha256 = "{projection.digest(text.encode())}"\n'
        self.write(prefix + ".vibe-slot.toml", receipt)

    def lock(self, packages):
        text = '[meta]\nschema_version = 7\n'
        for name, version in packages:
            text += (f'[[package]]\ngroup = "fixture"\nname = "{name}"\nversion = "{version}"\n'
                     'content_hash = "sha256:fixture"\n')
        self.write("vibe.lock", text)

    def render(self):
        return projection.project(self.repo, self.binding,
                                  (self.config / "custom.md").read_text(encoding="utf-8"), self.sha, self.anchor)

    def maintain(self, update=False):
        return projection.maintain(self.repo, self.binding_path, self.repo, self.sha, self.anchor, update)

    def cli(self, action="check", extra=(), tool=None):
        return subprocess.run([sys.executable, str(tool or self.distributed_tool), action,
                               "--repository", str(self.repo), "--binding", "chatgpt/binding.json",
                               "--accepted-sha", self.sha, "--authority-anchor", self.anchor, *extra],
                              capture_output=True, text=True, encoding="utf-8")

    def tree(self):
        return {p.name: p.read_bytes() for p in self.config.iterdir() if p.is_file()}

    def test_distributed_update_check_noop_and_custom_preservation(self):
        custom = (self.config / "custom.md").read_bytes()
        first = self.cli("update")
        self.assertEqual(first.returncode, 0, first.stderr)
        before = self.tree()
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["effective_content"], "NO_OP")
        self.assertEqual(self.tree(), before)
        self.assertEqual(self.cli("update").returncode, 0)
        self.assertEqual(self.tree(), before)
        self.assertEqual((self.config / "custom.md").read_bytes(), custom)

    def test_missing_generated_check_is_read_only_and_stale(self):
        before = self.tree()
        self.assertEqual(self.cli().returncode, 1)
        self.assertEqual(self.tree(), before)

    def test_changed_custom_stale_detection_safe_update(self):
        self.assertEqual(self.cli("update").returncode, 0)
        self.write("chatgpt/custom.md", "Changed local preference, including UTF-8: сад.\n")
        before = self.tree()
        self.assertEqual(self.cli().returncode, 1)
        self.assertEqual(self.tree(), before)
        result = self.cli("update")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Changed local preference", json.loads(result.stdout)["diffs"]["instructions.md"])
        self.assertEqual(self.cli().returncode, 0)
        self.assertEqual((self.config / "custom.md").read_bytes(), before["custom.md"])

    def test_changed_distributed_base_uses_same_interface(self):
        package = self.root / "upgraded-package"
        shutil.copytree(self.distribution, package)
        tool = package / "tools/chatgpt/project.py"
        self.assertEqual(self.cli("update", tool=tool).returncode, 0)
        base = tool.with_name("base.md")
        base.write_text(base.read_text() + "\nChanged client navigation mechanics.\n")
        result = self.cli(tool=tool)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["instructions"], "CHANGED")
        self.assertEqual(self.cli("update", tool=tool).returncode, 0)
        self.assertEqual(self.cli(tool=tool).returncode, 0)

    def test_changed_binding_changes_only_reviewed_client_routing(self):
        self.maintain(True)
        self.binding["role"] = "Changed owner-selected discussion role"
        self.binding["navigation_ref"] = "accepted-source"
        self.save_binding()
        status, stale = self.maintain()
        self.assertTrue(stale)
        self.assertEqual(status["instructions"], "CHANGED")
        self.assertIn("Changed owner-selected", status["diffs"]["instructions.md"])
        self.maintain(True)
        self.assertEqual(self.maintain()[0]["effective_content"], "NO_OP")

    def test_unrelated_accepted_commit_needs_no_settings_update(self):
        self.maintain(True)
        before = (self.config / "instructions.md").read_bytes()
        self.write("unrelated.md", "Source-only note\n")
        self.commit()
        status, stale = self.maintain()
        self.assertTrue(stale)  # Exact maintenance evidence advances separately.
        self.assertEqual(status["effective_content"], "NO_OP")
        self.assertEqual(status["source_changes"], [])
        self.maintain(True)
        self.assertEqual((self.config / "instructions.md").read_bytes(), before)

    def test_relevant_route_and_dependency_changes_are_reported_without_sha_in_settings(self):
        self.maintain(True)
        self.slot("beta", "9.7.1", ["renamed", "second", "third"])
        self.lock([("alpha", "1.0.0"), ("beta", "9.7.1")])
        self.write("boot.md", "New accepted relevant materialized routing\n")
        self.commit()
        status, _ = self.maintain()
        self.assertEqual(status["instructions"], "NO_OP")
        self.assertIn("boot.md", status["source_changes"])
        self.assertIn("vibe.lock", status["source_changes"])
        self.assertTrue(any("third.md" in p for p in status["source_changes"]))

    def test_no_governance_injected_into_non_adopting_consumer(self):
        artifacts, receipt = self.render()
        text = artifacts["instructions.md"].decode()
        for word in ("Task", "Outcome", "BLOCKED", "Deliberative", "APPROVE", "task-handoff", "independent-review"):
            self.assertNotIn(word, text)
        self.assertNotIn(self.sha, text)
        self.assertEqual(receipt["accepted_sha"], self.sha)
        self.assertIn("adopts no topic", text)

    def test_real_producer_output_and_accepted_workflow_routing(self):
        binding = json.loads((ROOT / "chatgpt/binding.json").read_text())
        artifacts, receipt = projection.project(ROOT, binding, (ROOT / "chatgpt/custom.md").read_text(), ACCEPTED, ANCHOR)
        self.assertEqual(artifacts["instructions.md"], (ROOT / "chatgpt/instructions.md").read_bytes())
        self.assertEqual(receipt, json.loads((ROOT / "chatgpt/receipt.json").read_text()))
        for text in ("accepted manual client binding", "BLOCKED", "Deliberative", "self-checks"):
            self.assertIn(text, artifacts["instructions.md"].decode())
        self.assertLess(receipt["unicode_characters"], 7000)

    def test_candidate_source_is_not_active_policy(self):
        before = self.render()
        self.write("AGENTS.md", "Candidate says accept itself")
        self.assertEqual(before, self.render())

    def test_conditions_order_preserved_without_adoption(self):
        self.write(projection.STATIC, "Priority\n")
        self.write("conditional.md", "Unknown applicability\n")
        self.write(projection.INDEX, 'schema = 1\n[[entry]]\npath = "boot.md"\nkind = "static"\n'
                   '[[entry]]\npath = "conditional.md"\nkind = "dynamic"\nwhen = "future:unknown"\n')
        self.commit()
        _, receipt = self.render()
        self.assertEqual([e["path"] for e in receipt["native_entries"]], ["boot.md", "conditional.md"])
        self.assertEqual(receipt["native_entries"][1]["when"], "future:unknown")
        self.assertIn(projection.STATIC, receipt["source_files"])
        self.assertIn("not evaluated", receipt["condition_disposition"])

    def test_optional_sources_selection_changes_noop_and_disable(self):
        self.binding["cache_enabled"] = True
        self.save_binding()
        self.maintain(True)
        self.assertEqual(self.maintain()[0]["sources"], "NO_OP")
        self.write("selected.md", "Selected cache content\n")
        self.commit()
        self.binding["cache_selection"] = ["selected.md"]
        self.save_binding()
        self.assertEqual(self.maintain()[0]["sources"], "CHANGED")
        self.maintain(True)
        self.assertIn(self.sha, (self.config / "sources.md").read_text())
        self.binding["cache_enabled"] = False
        self.save_binding()
        self.maintain(True)
        self.assertFalse((self.config / "sources.md").exists())
        self.assertFalse((self.config / "sources-manifest.json").exists())

    def test_missing_optional_cache_only_fails_when_enabled(self):
        self.binding["cache_selection"] = ["missing.md"]
        self.render()
        self.binding["cache_enabled"] = True
        with self.assertRaisesRegex(ValueError, "Missing accepted"):
            self.render()

    def test_unknown_and_modified_generated_files_preserved(self):
        self.write("chatgpt/instructions.md", "Unknown valuable rules\n")
        before = self.tree()
        self.assertEqual(self.cli("update").returncode, 2)
        self.assertEqual(self.tree(), before)
        (self.config / "instructions.md").unlink()
        self.maintain(True)
        self.write("chatgpt/instructions.md", "Locally modified rules\n")
        before = self.tree()
        self.assertEqual(self.cli("update").returncode, 2)
        self.assertEqual(self.tree(), before)

    def test_all_outputs_validated_before_any_write(self):
        self.maintain(True)
        self.binding["cache_enabled"] = True
        self.save_binding()
        self.write("chatgpt/custom.md", "Changed custom\n")
        self.write("chatgpt/sources.md", "Unknown cache must survive\n")
        before = self.tree()
        self.assertEqual(self.cli("update").returncode, 2)
        self.assertEqual(self.tree(), before)

    def test_live_export_exact_diff_and_noop_with_unknown_rules(self):
        self.maintain(True)
        generated = self.config / "instructions.md"
        exported = self.root / "live.md"
        exported.write_bytes(generated.read_bytes())
        self.assertEqual(projection.compare_live(generated, exported, "raw")["comparison"], "NO_OP")
        exported.write_bytes(generated.read_bytes() + b"Unknown live rule\n")
        before = exported.read_bytes()
        result = projection.compare_live(generated, exported, "raw")
        self.assertIn("-Unknown live rule", result["diff"])
        self.assertFalse(result["live_settings_verified"])
        self.assertEqual(exported.read_bytes(), before)
        exported.write_bytes(b"```markdown\n" + generated.read_bytes() + b"```\n")
        self.assertEqual(projection.compare_live(generated, exported, "fenced")["comparison"], "NO_OP")

    def test_missing_sources_unsupported_formats_and_unknown_conditions(self):
        for path, text, error in ((projection.INDEX, "schema = 99\n", "INDEX schema"),
                                  ("vibe.lock", "[meta]\nschema_version = 99\n", "lock schema"),
                                  (projection.INDEX, 'schema=1\n[[entry]]\npath="missing.md"\nkind="static"\n', "Missing accepted")):
            with self.subTest(path=path, error=error):
                original = (self.repo / path).read_text()
                self.write(path, text)
                self.commit()
                with self.assertRaisesRegex(ValueError, error):
                    self.render()
                self.write(path, original)
                self.commit()
        self.binding["local_sources"] = ["missing.md"]
        with self.assertRaisesRegex(ValueError, "Missing accepted"):
            self.render()

    def test_corrupt_slot_and_lock_and_unlocked_route_fail(self):
        self.write("vibevm/vibedeps/fixture.alpha/1.0.0/protocols/first.md", "Corrupt\n")
        self.commit()
        with self.assertRaisesRegex(ValueError, "native receipt"):
            self.render()
        self.slot("alpha", "1.0.0", ["first"])
        self.write("vibe.lock", '[meta]\nschema_version=7\n[[package]]\ngroup="fixture"\nname="alpha"\nversion="1.0.0"\ncontent_hash="wrong"\n')
        self.commit()
        with self.assertRaisesRegex(ValueError, "Lock/slot"):
            self.render()
        self.lock([("alpha", "1.0.0")])
        self.slot("unlocked", "2.0.0", ["topic"])
        self.write(projection.INDEX, 'schema=1\n[[entry]]\npath="vibevm/vibedeps/fixture.unlocked/2.0.0/protocols/topic.md"\nkind="static"\n')
        self.commit()
        with self.assertRaisesRegex(ValueError, "not bound"):
            self.render()

    def test_role_boundary_invalid_binding_paths_budget_and_sha(self):
        self.binding["permissions"].append("authorized-publication")
        with self.assertRaisesRegex(ValueError, "Read-only"):
            self.render()
        self.binding["permissions"].pop()
        for path in ("../secret", "/secret", "C:/secret", "a\\secret", "a/../secret"):
            with self.assertRaises(ValueError):
                projection.safe_path(path)
        with self.assertRaises(ValueError):
            projection.ordinary(self.repo, self.repo / "chatgpt/../../secret")
        self.binding["schema"] = 99
        with self.assertRaisesRegex(ValueError, "schema"):
            self.render()
        self.binding["schema"] = 2
        self.write("chatgpt/custom.md", "x" * 8000)
        with self.assertRaisesRegex(ValueError, "never truncate"):
            self.render()
        self.write("chatgpt/custom.md", "{{UNKNOWN}}")
        with self.assertRaisesRegex(ValueError, "markers"):
            self.render()
        self.write("chatgpt/custom.md", "Safe\n")
        self.sha = "HEAD"
        with self.assertRaisesRegex(ValueError, "exact"):
            self.render()

    def test_absent_native_supported_and_cannot_hide_present(self):
        self.binding["native"] = "absent"
        with self.assertRaisesRegex(ValueError, "Native state exists"):
            self.render()
        self.git("rm", "-qr", "vibevm", "vibe.lock")
        self.commit()
        self.assertEqual(self.render()[1]["native_entries"], [])

    def test_unsupported_actions_do_not_write(self):
        before = self.tree()
        for flag in ("--apply", "--upload", "--approve", "--merge"):
            with self.subTest(flag=flag):
                self.assertEqual(self.cli("update", extra=(flag,)).returncode, 2)
        self.assertEqual(self.tree(), before)

    def test_prior_history_and_protocols_preserved(self):
        paths = ["docs/task-32/step-1", "docs/task-32/step-2", "docs/task-32/step-3", "docs/task-32/step-4",
                 "AGENTS.md", "packages/development-governance/vibevm/vibespecs/protocols",
                 "packages/development-governance/vibevm/vibespecs/boot/development-governance.md"]
        delta = subprocess.check_output(["git", "diff", "c7003e8fdd57e796f6aec4daffe5d946e4792250", "--", *paths], cwd=ROOT)
        self.assertEqual(delta, b"")


if __name__ == "__main__":
    unittest.main()
