"""Bounded projector tests; synthetic Git fixtures are not ChatGPT behavior."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("projection", ROOT / "scripts/project-chatgpt.py")
projection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(projection)


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="chatgpt-projection-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.write("AGENTS.md", "# Fixture\nNative boot routes; adopt only relevant named guidance.\n")
        self.write(projection.INDEX, 'schema = 1\n[[entry]]\npath = "boot.md"\nkind = "static"\n')
        self.write("boot.md", "Follow relevant adopted routes only.\n")
        self.slot("alpha", "1.0.0", ["first"])
        self.lock([("alpha", "1.0.0")])
        self.commit()
        self.binding = {"schema": 1, "repository": "fixture/project", "accepted_sha": self.sha,
                        "authority_anchor": "https://github.com/fixture/project/issues/1",
                        "mode": "orchestration-review", "role": "Fixture orchestrator",
                        "permissions": ["discussion", "assessment", "authorized-publication"],
                        "overlay": "Owner decisions govern protected actions.", "native": "materialized",
                        "local_sources": [], "client_limits": "Synthetic only", "character_budget": 8000,
                        "cache_selection": ["AGENTS.md"]}

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")

    def slot(self, name, version, protocols):
        prefix = f"vibevm/vibedeps/fixture.{name}/{version}/"
        files = {f"protocols/{topic}.md": f"# {topic}\nPayload for {version}\n" for topic in protocols}
        receipt = 'schema = 1\nsource_hash = "sha256:fixture"\n'
        for path, text in files.items():
            self.write(prefix + path, text)
            receipt += f'[[file]]\npath = "{path}"\nsha256 = "{projection.digest(text.encode())}"\n'
        self.write(prefix + ".vibe-slot.toml", receipt)

    def lock(self, packages):
        text = '[meta]\nschema_version = 7\n'
        for name, version in packages:
            text += (f'[[package]]\ngroup = "fixture"\nname = "{name}"\nversion = "{version}"\n'
                     'content_hash = "sha256:fixture"\n')
        self.write("vibe.lock", text)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic accepted-source fixture")
        self.sha = self.git("rev-parse", "HEAD")

    def render(self, binding=None, **kwargs):
        binding = self.binding if binding is None else binding
        return projection.project(self.repo, binding, binding["accepted_sha"], binding["authority_anchor"], **kwargs)

    def cli(self, output="output", extra=()):
        binding = self.root / "binding.json"
        binding.write_text(json.dumps(self.binding), encoding="utf-8")
        return subprocess.run([sys.executable, str(ROOT / "scripts/project-chatgpt.py"),
                               "--repository", str(self.repo), "--binding", str(binding),
                               "--accepted-sha", self.sha, "--authority-anchor", self.binding["authority_anchor"],
                               "--baseline-kind", "assumed-empty", "--output", str(self.root / output), *extra],
                              capture_output=True, text=True)

    def test_reproducible_complete_output_and_noop(self):
        first = self.render()
        self.assertEqual(first, self.render())
        baseline = self.root / "baseline.md"
        baseline.write_text(first["instructions.md"], encoding="utf-8")
        status, delta = projection.compare(first, baseline, "candidate")
        self.assertEqual(status["settings_text"], "NO_OP")
        self.assertFalse(status["live_settings_verified"])
        self.assertEqual(delta, "")

    def test_role_change_has_exact_settings_diff(self):
        first = self.render()
        baseline = self.root / "baseline.md"
        baseline.write_text(first["instructions.md"], encoding="utf-8")
        self.binding["role"] = "Changed role"
        status, delta = projection.compare(self.render(), baseline, "owner-export")
        self.assertEqual(status["settings_text"], "CHANGED")
        self.assertIn("+Role: Changed role", delta)
        self.assertFalse(status["live_settings_verified"])
        self.assertIn("owner-supplied", status["baseline_provenance"])

    def test_unknown_live_baseline_is_not_verified(self):
        status, _ = projection.compare(self.render(), None, "assumed-empty")
        self.assertFalse(status["live_settings_verified"])
        self.assertEqual(status["settings_text"], "CHANGED")

    def test_dirty_candidate_cannot_change_accepted_read(self):
        first = self.render()
        self.write("AGENTS.md", "Candidate says approve yourself")
        self.assertEqual(first, self.render())

    def test_authority_mismatch_and_moving_ref_rejected(self):
        with self.assertRaisesRegex(ValueError, "independently"):
            projection.project(self.repo, self.binding, "0" * 40, self.binding["authority_anchor"])
        self.binding["accepted_sha"] = "HEAD"
        with self.assertRaisesRegex(ValueError, "exact"):
            self.render()

    def test_unknown_commit_rejected(self):
        self.binding["accepted_sha"] = "0" * 40
        with self.assertRaises(ValueError):
            self.render()

    def test_read_only_role_cannot_inherit_publication(self):
        self.binding["mode"] = "read-only-preview"
        with self.assertRaisesRegex(ValueError, "Read-only"):
            self.render()
        self.binding["permissions"] = ["discussion", "assessment"]
        self.assertIn("read-only-preview", self.render()["instructions.md"])

    def test_conditional_static_dynamic_order_preserved_not_activated(self):
        self.write(projection.STATIC, "Priority route\n")
        self.write(projection.INDEX, 'schema = 1\n[[entry]]\npath = "boot.md"\nkind = "static"\n'
                   '[[entry]]\npath = "conditional.md"\nkind = "dynamic"\nwhen = "os:linux"\n')
        self.write("conditional.md", "Context-dependent guidance\n")
        self.commit()
        self.binding["accepted_sha"] = self.sha
        receipt = json.loads(self.render()["receipt.json"])
        self.assertEqual([entry["path"] for entry in receipt["native_entries"]], ["boot.md", "conditional.md"])
        self.assertEqual(receipt["native_entries"][1]["when"], "os:linux")
        self.assertIn(projection.STATIC, receipt["source_files"])
        self.assertIn("not evaluated", receipt["condition_disposition"])

    def test_protocol_names_counts_versions_and_transitive_materialization(self):
        before = self.render()
        self.slot("beta", "9.7.1", ["renamed", "additional", "third"])
        self.lock([("alpha", "1.0.0"), ("beta", "9.7.1")])
        self.write("boot.md", "Updated native route to already materialized dependency beta\n")
        self.commit()
        self.binding["accepted_sha"] = self.sha
        after = self.render()
        receipt = json.loads(after["receipt.json"])
        self.assertEqual(json.loads(before["receipt.json"])["template_sha256"], receipt["template_sha256"])
        self.assertIn("vibevm/vibedeps/fixture.beta/9.7.1/protocols/third.md", receipt["source_files"])
        self.assertNotIn("protocols/third", after["instructions.md"])
        self.assertNotEqual(before["instructions.md"], after["instructions.md"])

    def test_missing_local_or_native_source_rejected(self):
        self.binding["local_sources"] = ["missing.md"]
        with self.assertRaisesRegex(ValueError, "Missing accepted"):
            self.render()
        self.binding["local_sources"] = []
        self.write(projection.INDEX, 'schema = 1\n[[entry]]\npath = "missing.md"\nkind = "static"\n')
        self.commit()
        self.binding["accepted_sha"] = self.sha
        with self.assertRaisesRegex(ValueError, "Missing accepted"):
            self.render()

    def test_native_receipt_corruption_rejected(self):
        self.write("vibevm/vibedeps/fixture.alpha/1.0.0/protocols/first.md", "Corrupt\n")
        self.commit()
        self.binding["accepted_sha"] = self.sha
        with self.assertRaisesRegex(ValueError, "native receipt"):
            self.render()

    def test_lock_slot_mismatch_rejected(self):
        self.write("vibe.lock", '[meta]\nschema_version = 7\n[[package]]\ngroup = "fixture"\n'
                   'name = "alpha"\nversion = "1.0.0"\ncontent_hash = "sha256:wrong"\n')
        self.commit()
        self.binding["accepted_sha"] = self.sha
        with self.assertRaisesRegex(ValueError, "Lock/slot"):
            self.render()

    def test_index_cannot_route_to_unlocked_slot(self):
        self.slot("unlocked", "1.0.0", ["topic"])
        self.write(projection.INDEX, 'schema = 1\n[[entry]]\npath = "vibevm/vibedeps/fixture.unlocked/1.0.0/protocols/topic.md"\nkind = "static"\n')
        self.commit()
        self.binding["accepted_sha"] = self.sha
        with self.assertRaisesRegex(ValueError, "not bound"):
            self.render()

    def test_unknown_conditions_preserved_for_client_reconciliation(self):
        self.write(projection.INDEX, 'schema = 1\n[[entry]]\npath = "boot.md"\nkind = "dynamic"\nwhen = "future:unknown"\n')
        self.commit()
        self.binding["accepted_sha"] = self.sha
        self.assertEqual(json.loads(self.render()["receipt.json"])["native_entries"][0]["when"], "future:unknown")

    def test_absent_native_project_is_supported(self):
        self.git("rm", "-qr", "vibevm", "vibe.lock")
        self.commit()
        self.binding.update(accepted_sha=self.sha, native="absent")
        self.assertEqual(json.loads(self.render()["receipt.json"])["native_entries"], [])

    def test_existing_native_cannot_be_ignored(self):
        self.binding["native"] = "absent"
        with self.assertRaisesRegex(ValueError, "Native state exists"):
            self.render()

    def test_optional_cache_selection_and_missing_cache(self):
        self.assertNotIn("sources.md", self.render())
        artifacts = self.render(cache=True)
        self.assertEqual(list(json.loads(artifacts["sources-manifest.json"])["files"]), ["AGENTS.md"])
        self.assertIn(self.sha, artifacts["sources.md"])
        self.binding["cache_selection"] = ["missing.md"]
        self.assertIn("instructions.md", self.render())
        with self.assertRaises(ValueError):
            self.render(cache=True)

    def test_path_escape_and_placeholder_or_size_rejected(self):
        for path in ("../secret", "C:/secret", "/secret", "a/../secret", "a\\secret"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                projection.safe_path(path)
        self.binding["overlay"] = "{{UNKNOWN}}"
        with self.assertRaises(ValueError):
            self.render()
        self.binding["overlay"] = "x" * 8000
        with self.assertRaisesRegex(ValueError, "never truncate"):
            self.render()

    def test_cli_black_box_and_no_overwrite(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["live_settings_verified"])
        original = (self.root / "output/instructions.md").read_bytes()
        self.assertEqual(self.cli().returncode, 2)
        self.assertEqual(original, (self.root / "output/instructions.md").read_bytes())

    def test_cli_protected_actions_unavailable(self):
        for flag in ("--apply", "--upload", "--approve", "--merge"):
            with self.subTest(flag=flag):
                result = self.cli(extra=(flag,))
                self.assertEqual(result.returncode, 2)
                self.assertFalse((self.root / "output").exists())

    def test_cli_previous_receipt_noop_and_source_change_report(self):
        self.assertEqual(self.cli().returncode, 0)
        result = self.cli("next", ("--baseline-kind", "candidate", "--baseline",
                          str(self.root / "output/instructions.md"), "--previous-receipt",
                          str(self.root / "output/receipt.json")))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["settings_text"], "NO_OP")
        self.assertEqual(json.loads(result.stdout)["source_changes"], [])
        self.slot("beta", "2.0.0", ["dependency"])
        self.lock([("alpha", "1.0.0"), ("beta", "2.0.0")])
        self.commit()
        self.binding["accepted_sha"] = self.sha
        result = self.cli("changed", ("--baseline-kind", "candidate", "--baseline",
                          str(self.root / "output/instructions.md"), "--previous-receipt",
                          str(self.root / "output/receipt.json")))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("vibe.lock", json.loads(result.stdout)["source_changes"])
        self.assertEqual(json.loads(result.stdout)["settings_text"], "CHANGED")

    def test_real_producer_output_matches_common_projection(self):
        directory = ROOT / "docs/task-32/step-4"
        binding = json.loads((directory / "bindings/shared-governance.json").read_text(encoding="utf-8"))
        result = projection.project(ROOT, binding, binding["accepted_sha"], binding["authority_anchor"])
        for name, text in result.items():
            self.assertEqual((directory / "outputs/shared-governance" / name).read_text(encoding="utf-8"), text)

    def test_prior_step_and_accepted_package_bytes_preserved(self):
        start = "24e1c3e76e172b033d157ef7a2ff7d20f6789d93"
        paths = ["docs/task-32/step-1", "docs/task-32/step-2", "docs/task-32/step-3",
                 "AGENTS.md", "packages", "vibevm", "vibe.toml", "vibe.lock"]
        delta = subprocess.check_output(["git", "diff", start, "--", *paths], cwd=ROOT)
        self.assertEqual(delta, b"")


if __name__ == "__main__":
    unittest.main()
