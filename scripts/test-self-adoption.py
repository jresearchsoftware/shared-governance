#!/usr/bin/env python3
"""Native producer mismatch and Git recovery regressions; no VibeVM/network."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare-distribution.py")
EXPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORTER)


class NativeAdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="native-adoption-test-")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / "source"
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
                        GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
        self.git(ROOT, "clone", "-q", "--no-hardlinks", str(ROOT), str(self.work))
        self.revision = self.git(self.work, "rev-parse", "HEAD")
        self.addCleanup(setattr, EXPORTER, "ROOT", EXPORTER.ROOT)
        EXPORTER.ROOT = self.work
        self.receipt = EXPORTER.verify_producer(self.revision, self.work)
        self.slot = self.work / EXPORTER.slot(self.receipt["version"])
        self.source = self.work / "vibevm/vibepacks" / EXPORTER.COORDINATE / ("v" + self.receipt["version"])

    def git(self, work, *args):
        return subprocess.check_output(["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
                                        "-c", "core.hooksPath=/nonexistent", "-c", "maintenance.auto=false",
                                        "-c", "gc.auto=0", *args], cwd=work, env=self.env, stderr=subprocess.PIPE, text=True).strip()

    def reject(self):
        with self.assertRaises((ValueError, OSError, KeyError)):
            EXPORTER.verify_producer(self.revision, self.work)

    def test_clean_checkout_is_ready_without_runtime_or_publication(self):
        import tomllib
        manifest = tomllib.loads((self.work / EXPORTER.PACKAGE / "vibe.toml").read_text())
        self.assertEqual(self.receipt["version"], manifest["package"]["version"])
        self.assertFalse((self.slot / EXPORTER.RECEIPT).exists())
        self.assertFalse((self.source / EXPORTER.RECEIPT).exists())

    def test_registry_source_mutation_and_missing_file_rejected(self):
        target = self.source / EXPORTER.HANDOFF
        original = target.read_bytes()
        target.write_text("changed source\n")
        self.reject()
        target.write_bytes(original)
        target.unlink()
        self.reject()

    def test_corrupt_slot_and_git_restore(self):
        target = self.slot / EXPORTER.HANDOFF
        target.write_text("changed installed rules\n")
        self.reject()
        self.git(self.work, "restore", "--source", self.revision, "--", target.relative_to(self.work).as_posix())
        EXPORTER.verify_producer(self.revision, self.work)

    def test_missing_slot_rejected(self):
        shutil.rmtree(self.slot)
        self.reject()

    def test_forged_slot_metadata_rejected(self):
        (self.slot / ".vibe-slot.toml").write_text('schema=1\nsource_hash="sha256:forged"\n')
        self.reject()

    def test_lock_hash_version_and_source_kind_rejected(self):
        path = self.work / "vibe.lock"
        original = path.read_text()
        for before, after in [('content_hash = "sha256:', 'content_hash = "sha256:forged'),
                              ('version = "' + self.receipt["version"] + '"', 'version = "0.0.0"'),
                              ('source_kind = "registry"', 'source_kind = "git"')]:
            with self.subTest(before=before):
                path.write_text(original.replace(before, after))
                self.reject()
        path.write_text(original)

    def test_generated_location_and_timestamp_are_not_content_authority(self):
        path = self.work / "vibe.lock"
        text = path.read_text()
        import re
        text = re.sub(r'source_url = ".*?"', 'source_url = "file:///unreachable/windows/vibevm/vibepacks/' + EXPORTER.COORDINATE + '/v' + self.receipt["version"] + '"', text)
        text = re.sub(r'generated_at = ".*?"', 'generated_at = "2000-01-01T00:00:00Z"', text)
        path.write_text(text)
        EXPORTER.verify_producer(self.revision, self.work)

    def test_missing_or_wrong_index_rejected(self):
        path = self.work / EXPORTER.BOOT_INDEX
        original = path.read_bytes()
        path.unlink()
        self.reject()
        path.write_bytes(original.replace(self.receipt["version"].encode(), b'0.0.0'))
        self.reject()

    def test_generated_member_route_and_root_overlay(self):
        root = self.work / "AGENTS.md"
        root.write_text(root.read_text() + "\nPublic local overlay preserved.\n")
        EXPORTER.verify_producer(self.revision, self.work)
        member = self.work / EXPORTER.PACKAGE / "AGENTS.md"
        member.write_text(member.read_text() + "\nUnexpected member activation.\n")
        self.reject()

    def test_manifest_range_or_link_change_rejected(self):
        path = self.work / "vibe.toml"
        original = path.read_text()
        for before, after in [('=' + self.receipt["version"], '^' + self.receipt["version"]), ('link = "dynamic"', 'link = "static-transitive"')]:
            with self.subTest(before=before):
                path.write_text(original.replace(before, after))
                self.reject()
        path.write_text(original)

    def test_uncommitted_and_committed_authored_change_cannot_hide_behind_old_url(self):
        target = self.work / EXPORTER.PACKAGE / EXPORTER.HANDOFF
        target.write_text(target.read_text() + "\nDisposable candidate change.\n")
        self.reject()
        self.git(self.work, "add", "--", target.relative_to(self.work).as_posix())
        self.git(self.work, "commit", "-qm", "Disposable same-version source change")
        self.revision = self.git(self.work, "rev-parse", "HEAD")
        self.reject()

    def test_native_export_regenerates_proposals_and_preserves_unexpected_content(self):
        before = (self.source / EXPORTER.HANDOFF).read_bytes()
        (self.source / EXPORTER.HANDOFF).write_text("Stale proposed materialization\n")
        EXPORTER.stage_producer(self.revision, self.work)
        EXPORTER.verify_producer(self.revision, self.work)
        unexpected = self.source / "unexpected.txt"
        unexpected.write_text("preserve me\n")
        with self.assertRaises(ValueError):
            EXPORTER.stage_producer(self.revision, self.work)
        self.assertEqual(before, (self.source / EXPORTER.HANDOFF).read_bytes())
        self.assertEqual("preserve me\n", unexpected.read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
