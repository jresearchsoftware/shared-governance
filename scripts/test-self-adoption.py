#!/usr/bin/env python3
"""Accepted-source, publication ordering and atomic local activation regressions."""
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
SPEC = importlib.util.spec_from_file_location("adoption", ROOT / "scripts/self-adopt.py")
ADOPTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADOPTION)


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="adoption-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.source = self.directory / "source"
        self.client = self.directory / "client"
        self.distribution = self.directory / "distribution"
        self.git(ROOT, "clone", "--quiet", "--shared", str(ROOT), str(self.source))
        self.git(self.source, "switch", "--quiet", "-C", "main", ADOPTION.BASELINE)
        (self.source / ".agents/self-adoption.json").write_bytes((ROOT / ".agents/self-adoption.json").read_bytes())
        with (self.source / ".gitignore").open("a") as stream:
            stream.write("\n.agents/accepted/\n")
        self.commit(self.source)
        self.distribution.mkdir()
        self.git(self.distribution, "init", "-q", "-b", "main")
        release = self.publish(ADOPTION.BASELINE)
        self.addCleanup(setattr, ADOPTION, "BASELINE_RELEASE", ADOPTION.BASELINE_RELEASE)
        ADOPTION.BASELINE_RELEASE = release
        pin = json.loads((self.source / ".agents/self-adoption.json").read_text())
        pin["release_commit"] = release
        (self.source / ".agents/self-adoption.json").write_text(json.dumps(pin))
        self.commit(self.source)
        self.git(ROOT, "clone", "--quiet", str(self.source), str(self.client))

    def git(self, root, *args):
        env = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                   GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        return subprocess.check_output(["git", "-c", "core.autocrlf=false", "-c", "core.filemode=false",
                                        "-c", "core.hooksPath=/nonexistent", "-c", "commit.gpgsign=false",
                                        "-c", "maintenance.auto=false", "-c", "gc.auto=0", *args],
                                       cwd=root, env=env, stderr=subprocess.PIPE).decode().strip()

    def commit(self, root):
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "Disposable qualification")
        return self.git(root, "rev-parse", "HEAD")

    def changed(self, version="1.3.0"):
        path = self.source / ADOPTION.PREPARATION.PACKAGE / "vibe.toml"
        path.write_text(path.read_text().replace('version = "1.2.0"', 'version = "' + version + '"'))
        with (path.parent / "README.md").open("a") as stream:
            stream.write("\nDisposable accepted update.\n")
        return self.commit(self.source)

    def publish(self, revision):
        files, receipt = ADOPTION.snapshot(self.source, revision)
        for name, data in files.items():
            target = self.distribution / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        commit = self.commit(self.distribution)
        self.git(self.distribution, "tag", "-a", "v" + receipt["version"], "-m", "Disposable publication")
        return commit

    def refresh(self, **kwargs):
        return ADOPTION.refresh(self.client, source=str(self.source), distribution=str(self.distribution), **kwargs)

    def pointer(self):
        return (self.client / ADOPTION.CACHE / "ACTIVE.json").read_bytes()

    def test_fresh_clone_bootstrap_is_reproducible_offline(self):
        result = self.refresh(offline=True)
        self.assertEqual(result["source_revision"], ADOPTION.BASELINE)
        files, _ = ADOPTION.snapshot(self.source, ADOPTION.BASELINE)
        directory = Path(result["directory"])
        self.assertEqual({p.relative_to(directory).as_posix(): p.read_bytes()
                          for p in directory.rglob("*") if p.is_file()}, files)

    def test_candidate_branch_and_dirty_package_do_not_activate(self):
        self.git(self.source, "switch", "-qc", "candidate")
        revision = self.changed()
        self.publish(revision)
        (self.client / ADOPTION.PREPARATION.PACKAGE / ADOPTION.PREPARATION.PROTOCOL).write_text("Unreviewed rule")
        self.assertEqual(self.refresh()["source_revision"], ADOPTION.BASELINE)

    def test_valid_fresh_online_selection_has_no_warning(self):
        self.assertEqual(self.refresh()["self_adoption"], "PASS")

    @unittest.skipUnless(os.name == "nt", "Windows inherited-DACL regression")
    def test_projection_retains_inherited_workspace_reader_access(self):
        import ctypes
        from ctypes import wintypes
        directory = self.refresh(offline=True)["directory"]
        security = ctypes.WinDLL("advapi32", use_last_error=True)
        security.GetFileSecurityW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID,
                                             wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
        needed = wintypes.DWORD()
        security.GetFileSecurityW(directory, 4, None, 0, ctypes.byref(needed))
        descriptor = ctypes.create_string_buffer(needed.value)
        if not security.GetFileSecurityW(directory, 4, descriptor, len(descriptor), ctypes.byref(needed)):
            raise ctypes.WinError(ctypes.get_last_error())
        control, revision = wintypes.WORD(), wintypes.DWORD()
        if not security.GetSecurityDescriptorControl(descriptor, ctypes.byref(control), ctypes.byref(revision)):
            raise ctypes.WinError(ctypes.get_last_error())
        self.assertFalse(control.value & 0x1000, "projection acquired a private DACL during materialization")

    def test_source_network_failure_retains_last_verified_guidance(self):
        self.refresh()
        before = self.pointer()
        result = ADOPTION.refresh(self.client, source=str(self.directory / "absent"),
                                  distribution=str(self.distribution))
        self.assertTrue(result["warnings"])
        self.assertEqual(before, self.pointer())

    def test_refresh_preserves_project_git_refs_index_and_instruction_files(self):
        before = (self.git(self.client, "for-each-ref"), self.git(self.client, "ls-files", "--stage"),
                  (self.client / "AGENTS.md").read_bytes(),
                  (self.client / ".agents/self-adoption.json").read_bytes())
        self.refresh()
        after = (self.git(self.client, "for-each-ref"), self.git(self.client, "ls-files", "--stage"),
                 (self.client / "AGENTS.md").read_bytes(),
                 (self.client / ".agents/self-adoption.json").read_bytes())
        self.assertEqual(before, after)

    def test_side_branch_commit_is_not_accepted_after_merge(self):
        self.git(self.source, "switch", "-qc", "candidate")
        revision = self.changed()
        self.publish(revision)
        self.git(self.source, "switch", "-q", "main")
        self.git(self.source, "merge", "--no-ff", "candidate", "-m", "Accepted merge fixture")
        self.assertEqual(self.refresh()["source_revision"], ADOPTION.BASELINE)

    def test_publication_must_follow_acceptance_then_update(self):
        revision = self.changed()
        result = self.refresh()
        self.assertEqual(result["source_revision"], ADOPTION.BASELINE)
        self.assertTrue(result["warnings"])
        self.publish(revision)
        self.assertEqual(self.refresh()["source_revision"], revision)

    def test_major_is_eligible_under_this_producers_accepted_merge_authority(self):
        revision = self.changed("2.0.0")
        self.publish(revision)
        self.assertEqual(self.refresh()["version"], "2.0.0")

    def test_retry_and_non_package_changes_do_not_rewrite_active_pointer(self):
        self.refresh()
        before = self.pointer()
        (self.source / "docs/disposable.txt").write_text("No package change")
        self.commit(self.source)
        self.refresh()
        self.assertEqual(self.pointer(), before)

    def test_registry_failure_keeps_active_bytes_and_retry_recovers(self):
        self.refresh()
        before = self.pointer()
        revision = self.changed()
        self.publish(revision)
        result = ADOPTION.refresh(self.client, source=str(self.source), distribution=str(self.directory / "absent"))
        self.assertTrue(result["warnings"])
        self.assertEqual(before, self.pointer())
        self.assertEqual(self.refresh()["source_revision"], revision)

    def test_counterfeit_published_payload_is_rejected(self):
        self.refresh()
        before = self.pointer()
        revision = self.changed()
        self.publish(revision)
        (self.distribution / ADOPTION.PREPARATION.PROTOCOL).write_text("Counterfeit instructions")
        self.commit(self.distribution)
        self.git(self.distribution, "tag", "-f", "v1.3.0")
        result = self.refresh()
        self.assertTrue(result["warnings"])
        self.assertEqual(self.pointer(), before)

    def test_frozen_tag_move_is_rejected_even_for_identical_payload(self):
        self.refresh()
        before = self.pointer()
        self.git(self.distribution, "commit", "--allow-empty", "-qm", "Moved release")
        self.git(self.distribution, "tag", "-f", "v1.2.0")
        self.assertTrue(self.refresh()["warnings"])
        self.assertEqual(self.pointer(), before)

    def test_interrupted_selector_write_keeps_previous_version(self):
        self.refresh()
        before = self.pointer()
        revision = self.changed()
        self.publish(revision)
        with patch.object(ADOPTION.os, "replace", side_effect=OSError("Interrupted fixture")):
            self.assertTrue(self.refresh()["warnings"])
        self.assertEqual(self.pointer(), before)
        self.assertEqual(self.refresh()["source_revision"], revision)

    def test_local_rollback_and_retry_use_only_verified_versions(self):
        self.refresh()
        revision = self.changed()
        self.publish(revision)
        self.refresh()
        self.assertEqual(self.refresh(rollback=True)["source_revision"], ADOPTION.BASELINE)
        self.assertEqual(self.refresh(offline=True)["source_revision"], ADOPTION.BASELINE)
        self.assertEqual(self.refresh()["source_revision"], revision)

    def test_corrupt_active_files_and_forged_candidate_pointer_are_rejected(self):
        result = self.refresh()
        protocol = Path(result["directory"]) / ADOPTION.PREPARATION.PROTOCOL
        protocol.write_text("Unreviewed active bytes")
        with self.assertRaisesRegex(ValueError, "active files differ"):
            self.refresh(offline=True)

    def test_self_consistent_candidate_pointer_does_not_prove_acceptance(self):
        self.refresh()
        self.git(self.client, "switch", "-qc", "candidate")
        path = self.client / ADOPTION.PREPARATION.PACKAGE / "vibe.toml"
        path.write_text(path.read_text().replace('version = "1.2.0"', 'version = "1.3.0"'))
        candidate = self.commit(self.client)
        files, receipt = ADOPTION.snapshot(self.client, candidate)
        cache = self.client / ADOPTION.CACHE / candidate
        for name, data in files.items():
            target = cache / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (cache.parent / "ACTIVE.json").write_text(json.dumps({"current": {**receipt, "release_commit": "a" * 40}}))
        with self.assertRaisesRegex(ValueError, "not accepted first-parent"):
            self.refresh(offline=True)

    def test_accepted_but_unpublished_forged_pointer_is_rejected(self):
        self.refresh()
        revision = self.changed()
        self.refresh()  # Observe accepted main while publication is still absent.
        files, receipt = ADOPTION.snapshot(self.source, revision)
        cache = self.client / ADOPTION.CACHE / revision
        for name, data in files.items():
            target = cache / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (cache.parent / "ACTIVE.json").write_text(json.dumps({"current": {**receipt, "release_commit": "a" * 40}}))
        with self.assertRaises(subprocess.SubprocessError):
            self.refresh(offline=True)

    def test_malformed_release_receipt_retains_verified_guidance(self):
        self.refresh()
        before = self.pointer()
        revision = self.changed()
        self.publish(revision)
        (self.distribution / "DISTRIBUTION.json").write_text("[]")
        self.commit(self.distribution)
        self.git(self.distribution, "tag", "-f", "v1.3.0")
        self.assertTrue(self.refresh()["warnings"])
        self.assertEqual(before, self.pointer())


if __name__ == "__main__":
    unittest.main(verbosity=2)
