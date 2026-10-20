#!/usr/bin/env python3
"""Task 53 producer parity, exact-source Git histories and local native release."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PIN = "5a1e5de66388501235fc9ffd23d45efb34df2b85"
VIBE = None


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P = load("shared", ROOT / "tooling/vibe-publisher/publisher.py")
C = load("producer", ROOT / "scripts/check-publication.py")
E = load("exporter", ROOT / "scripts/prepare-distribution.py")


class Evidence:
    def __init__(self, source):
        self.source = source
        self.bad = False
        self.calls = []

    def pages(self, path, key):
        self.calls.append(path)
        return [{"head_sha": "0" * 40 if self.bad else self.source,
                 "event": "push", "head_branch": "main", "status": "completed",
                 "conclusion": "success", "path": ".github/workflows/candidate.yml",
                 "workflow_id": 123, "head_repository": {"id": 1408747561},
                 "repository": {"id": 1408747561}, "html_url": "https://example.invalid/ci"}]

    def get(self, path):
        raise AssertionError("No PR, owner or integrator lookup: " + path)


class ProducerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="task53-producer-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.source = self.directory / "source"
        self.source.mkdir()
        self.env = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0")
        self.git("init", "-q", "-b", "main")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.hooksPath", str(self.directory / "no-hooks"))
        # Actual accepted package, not a synthetic subset or a relabelled old release.
        self.package = self.source / "packages/development-governance"
        self.package.mkdir(parents=True)
        files, _ = E.snapshot(PIN)
        for name, data in files.items():
            if name == E.RECEIPT:
                continue
            target = self.package / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        shutil.copyfile(ROOT / "LICENSE", self.source / "LICENSE")
        (self.source / "vibe.toml").write_text('[workspace]\nmembers=["packages/development-governance"]\n')
        self.before_binding = self.commit()
        self.binding = json.loads((ROOT / C.BINDING).read_text())
        self.save_binding()
        self.baseline = self.commit()

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *map(str, args)], cwd=cwd or self.source,
                                       env=self.env, stderr=subprocess.PIPE).decode().strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Disposable producer source")
        return self.git("rev-parse", "HEAD")

    def save_binding(self):
        (self.source / C.BINDING).write_text(json.dumps(self.binding))

    def change(self, bump=True):
        readme = self.package / "README.md"
        readme.write_bytes(readme.read_bytes() + b"\nDisposable fixture change.\n")
        if bump:
            manifest = self.package / "vibe.toml"
            manifest.write_bytes(manifest.read_bytes().replace(b'3.0.0', b'3.0.1'))
        return self.commit()

    def check(self, revision, base=None):
        api = Evidence(revision)
        with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "workflow_dispatch"}):
            result = C.check(P, self.source, revision, base, api, "main")
        return result, api

    def test_binding_onboarding_and_later_tooling_are_noops_before_rights_or_api(self):
        for revision in (self.baseline,):
            (report, changed), api = self.check(revision)
            self.assertFalse(changed)
            self.assertEqual(report["packages"][0]["status"], "NO_PACKAGE_CHANGE")
            self.assertEqual(api.calls, [])
        self.binding["packages"][0].pop("redistribution")
        self.save_binding()
        (self.source / "research.txt").write_text("outside payload")
        with patch.object(P, "remote_refs", side_effect=AssertionError("no destination")):
            (report, changed), api = self.check(self.commit())
        self.assertFalse(changed)
        self.assertEqual(api.calls, [])

    def test_changed_source_uses_its_committed_binding_and_exact_ci(self):
        revision = self.change()
        # Worktree/main policy cannot replace retry's embedded binding.
        self.binding["packages"][0]["redistribution"] = {}
        self.save_binding()
        (report, changed), api = self.check(revision)
        self.assertTrue(changed)
        self.assertEqual(report["source_sha"], revision)
        self.assertEqual(len(api.calls), 1)
        api.bad = True
        with self.assertRaisesRegex(ValueError, "MATCHING_SOURCE_CI_MISSING"):
            C.check(P, self.source, revision, api=api, main="main")
        wrong = dict(self.binding)
        with self.assertRaisesRegex(ValueError, "binding must come"):
            P.plan(self.source, revision, "main", wrong, api, C.BINDING)

    def test_missing_and_mismatched_rights_reject_changed_source(self):
        for rights in ({}, {"status": "pending"},
                       {"status": "approved", "license": "MIT"},
                       {"status": "approved", "license": "Apache-2.0", "approval": "https://example.invalid"}):
            self.binding["packages"][0]["redistribution"] = rights
            self.save_binding()
            revision = self.change() if not hasattr(self, "changed") else self.commit()
            self.changed = True
            # Compare each candidate against the unchanged accepted baseline.
            self.git("update-ref", "refs/heads/accepted", self.baseline)
            with self.assertRaisesRegex(ValueError, "REDISTRIBUTION_UNRESOLVED"):
                C.check(P, self.source, revision, base=self.baseline, main="accepted")

    def test_same_version_change_and_non_first_parent_source_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "PACKAGE_VERSION_REUSE"):
            self.check(self.change(bump=False))
        self.git("checkout", "-qb", "side", self.baseline)
        side = self.change()
        self.git("checkout", "main")
        with self.assertRaisesRegex(ValueError, "first-parent"):
            self.check(side)

    def test_exact_bytes_receipt_and_dependency_free_export_are_preserved(self):
        revision = self.change()
        package = self.binding["packages"][0]
        actual = P.snapshot(self.source, revision, package)
        with patch.object(E, "ROOT", self.source):
            expected = E.snapshot(revision)
        self.assertEqual(actual, expected)
        manifest = self.package / "vibe.toml"
        manifest.write_bytes(manifest.read_bytes() + b'\n[requires]\n"org.fixture/unapproved"="=1.0.0"\n')
        bad = self.commit()
        with self.assertRaisesRegex(ValueError, "capability or dependency"):
            P.snapshot(self.source, bad, package)

    def test_missing_license_is_rejected(self):
        self.change()
        (self.package / "LICENSE").unlink()
        with self.assertRaises(ValueError):
            self.check(self.commit())

    def route(self, route):
        if route != "direct":
            self.git("checkout", "-qb", "feature")
        original = self.change()
        if route != "direct":
            self.git("checkout", "main")
            if route == "squash":
                self.git("merge", "--squash", "feature")
                revision = self.commit()
            elif route == "merge":
                self.git("merge", "--no-ff", "feature", "-m", "Ordinary fixture merge")
                revision = self.git("rev-parse", "HEAD")
            else:
                (self.source / "tooling.txt").write_text("rebase target")
                self.commit()
                self.git("checkout", "feature")
                self.git("rebase", "main")
                self.git("checkout", "main")
                self.git("merge", "--ff-only", "feature")
                revision = self.git("rev-parse", "HEAD")
        else:
            revision = original
        (report, changed), _ = self.check(revision)
        self.assertTrue(changed)
        self.assertEqual(report["packages"][0]["status"], "READY")

    def test_direct_main(self):
        self.route("direct")

    def test_squash(self):
        self.route("squash")

    def test_ordinary_merge(self):
        self.route("merge")

    def test_rebase(self):
        self.route("rebase")

    def test_native_exact_export_same_source_retry_and_immutable_collision(self):
        if VIBE is None:
            self.skipTest("optional pinned native Linux publisher")
        revision = self.change()
        (report, _), _ = self.check(revision)
        destination = self.directory / "distribution.git"
        self.git("init", "-q", "--bare", "--initial-branch=main", destination)
        # Redirect only this disposable native fixture to a local bare repository.
        package = dict(self.binding["packages"][0], destination=destination.as_uri())
        decision = dict(report["packages"][0], destination=destination.as_uri())
        staged = P.stage(self.source, package, decision, VIBE, self.directory / "stage")
        self.assertEqual(staged["status"], "STAGED")
        def failed_push(*args):
            raise ValueError("simulated transport failure")
        self.assertEqual(P.finalize(staged, failed_push)["status"], "FAILED_OR_PENDING")
        self.assertEqual(P.finalize(staged)["status"], "PUBLISHED")
        tag = self.git("rev-parse", "v3.0.1", cwd=destination)
        expected, _ = P.snapshot(self.source, revision, package)
        for name, data in expected.items():
            observed = subprocess.check_output(["git", "show", "v3.0.1:" + name], cwd=destination)
            self.assertEqual(observed, data, name)
        repeated = P.stage(self.source, package, decision, None, self.directory / "unused")
        self.assertEqual(repeated["status"], "ALREADY_PUBLISHED")
        self.assertFalse((self.directory / "unused").exists())
        # Another same-version staged identity cannot displace an existing tag.
        self.assertEqual(P.finalize(dict(staged, expected_tag="0" * 40))["status"], "ALREADY_PUBLISHED")
        self.assertEqual(self.git("rev-parse", "v3.0.1", cwd=destination), tag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vibe", type=Path)
    args, remaining = parser.parse_known_args()
    if args.vibe:
        VIBE = args.vibe.resolve()
    unittest.main(argv=[__file__, *remaining], verbosity=2)
