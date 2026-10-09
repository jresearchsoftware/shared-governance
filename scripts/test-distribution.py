#!/usr/bin/env python3
"""Behavioral checks for passive distribution preparation using disposable Git sources."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "prepare_distribution", REPOSITORY / "scripts/prepare-distribution.py")
DISTRIBUTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISTRIBUTION)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="governance-distribution-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.source = self.directory / "source"
        self.source.mkdir()
        self.package = self.source / DISTRIBUTION.PACKAGE
        shutil.copytree(REPOSITORY / DISTRIBUTION.PACKAGE, self.package)
        shutil.copyfile(REPOSITORY / "LICENSE", self.source / "LICENSE")
        # Windows-mounted files can appear executable; fixture Git modes are explicit.
        for path in self.package.rglob("*"):
            if path.is_file():
                path.chmod(0o644)
        (self.source / "LICENSE").chmod(0o644)
        self.git("init", "-q")
        self.git("config", "user.name", "Disposable distribution test")
        self.git("config", "user.email", "distribution-test@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.filemode", "true")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.directory / "no-hooks"))
        self.revision = self.commit()
        self.old_root = DISTRIBUTION.ROOT
        DISTRIBUTION.ROOT = self.source
        self.addCleanup(setattr, DISTRIBUTION, "ROOT", self.old_root)
        DISTRIBUTION.snapshot(self.revision)  # Negative tests start with a valid source.

    def git(self, *args):
        return subprocess.check_output(
            ["git", *args], cwd=self.source, stderr=subprocess.PIPE)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Disposable source fixture")
        return self.git("rev-parse", "HEAD").decode().strip()

    def payload(self, directory):
        return {path.relative_to(directory).as_posix(): path.read_bytes()
                for path in directory.rglob("*") if path.is_file()}

    def rejected_source(self, revision=None):
        destination = self.directory / "rejected"
        with self.assertRaises((ValueError, subprocess.CalledProcessError)):
            DISTRIBUTION.prepare(revision or self.commit(), destination)
        self.assertFalse(destination.exists())

    def installed_fixture(self, directory):
        receipt = DISTRIBUTION.prepare(self.revision, directory)
        files = self.payload(directory)
        content_hash = DISTRIBUTION.vibe_hash(files)
        marker = ['schema = 1', 'spec_format = "mixed"',
                  'source_hash = ' + json.dumps(content_hash)]
        for name, data in sorted(files.items()):
            marker.extend(['', '[[file]]', 'path = ' + json.dumps(name),
                           'sha256 = ' + json.dumps(hashlib.sha256(data).hexdigest())])
        (directory / ".vibe-slot.toml").write_text("\n".join(marker) + "\n")
        return receipt, content_hash

    def consumer_fixture(self, name):
        consumer = self.directory / name
        slot = consumer / "vibevm/vibedeps/org.jresearch.governance.proportional-controls/0.1.0"
        receipt, content_hash = self.installed_fixture(slot)
        (consumer / "vibe.toml").write_text(
            '[project]\nname = "disposable-consumer"\nversion = "0.0.0"\nspec_format = "mixed"\n'
            '\n[requires.packages]\n"org.jresearch.governance/proportional-controls" = '
            '{version = "=0.1.0", git = "file:///disposable/distribution.git", tag = "v0.1.0"}\n')
        (consumer / "vibe.lock").write_text(
            '[meta]\nschema_version = 7\n\n[[package]]\ngroup = "org.jresearch.governance"\nname = "proportional-controls"\n'
            'version = "0.1.0"\nsource_kind = "git"\n'
            'source_url = "file:///disposable/distribution.git"\nsource_ref = "v0.1.0"\n'
            'content_hash = ' + json.dumps(content_hash) + '\n')
        shutil.copytree(slot / "vibevm/vibespecs/skills/proportional-controls",
                        consumer / ".agents/skills/proportional-controls")
        self.assertEqual(receipt, DISTRIBUTION.verify_consumer(self.revision, consumer))
        return consumer, slot, receipt

    def test_exact_commit_is_deterministic_and_source_is_unchanged(self):
        expected = self.payload(self.package)
        # Preparation must read the selected commit even when the checkout is dirty.
        (self.package / "README.md").write_text("Uncommitted source edit\n")
        source_before = self.payload(self.package)
        status_before = self.git("status", "--porcelain", "--untracked-files=all")
        first = self.directory / "first"
        second = self.directory / "second"
        receipt = DISTRIBUTION.prepare(self.revision, first)
        self.assertEqual(receipt, DISTRIBUTION.prepare(self.revision, second))
        self.assertEqual(self.payload(first), self.payload(second))
        self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, first))
        prepared = self.payload(first)
        self.assertEqual(set(prepared), set(expected) | {DISTRIBUTION.RECEIPT})
        self.assertEqual({name: prepared[name] for name in expected}, expected)
        self.assertEqual(receipt["source_revision"], self.revision)
        self.assertEqual(receipt["sha256"], {
            name: hashlib.sha256(data).hexdigest() for name, data in expected.items()})
        self.assertEqual(source_before, self.payload(self.package))
        self.assertEqual(status_before, self.git("status", "--porcelain", "--untracked-files=all"))
        self.assertEqual(self.revision, self.git("rev-parse", "HEAD").decode().strip())

    def test_only_full_source_commit_identity_is_accepted(self):
        for reference in ("HEAD", "main", self.revision[:12], self.revision.upper(),
                          self.revision + "0", "../source"):
            with self.subTest(reference=reference):
                self.rejected_source(reference)

    def test_occupied_destinations_are_preserved(self):
        directory = self.directory / "occupied"
        directory.mkdir()
        (directory / "keep.txt").write_bytes(b"Retain existing destination\n")
        existing_file = self.directory / "file"
        existing_file.write_bytes(b"Retain existing file\n")
        for target in (directory, existing_file):
            with self.subTest(target=target.name), self.assertRaises(ValueError):
                DISTRIBUTION.prepare(self.revision, target)
        self.assertEqual((directory / "keep.txt").read_bytes(), b"Retain existing destination\n")
        self.assertEqual(existing_file.read_bytes(), b"Retain existing file\n")

    def test_existing_empty_destination_is_supported(self):
        destination = self.directory / "empty"
        destination.mkdir()
        receipt = DISTRIBUTION.prepare(self.revision, destination)
        self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, destination))

    def test_destination_inside_checkout_is_rejected_before_creation(self):
        destination = self.source / "new" / "distribution"
        with self.assertRaises(ValueError):
            DISTRIBUTION.prepare(self.revision, destination)
        self.assertFalse((self.source / "new").exists())

    def test_symlink_destination_is_rejected(self):
        target = self.directory / "target"
        target.mkdir()
        destination = self.directory / "linked"
        destination.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError):
            DISTRIBUTION.prepare(self.revision, destination)
        self.assertEqual(list(target.iterdir()), [])

    def test_verification_rejects_corruption_missing_extra_and_symlink_files(self):
        for corruption in ("changed", "missing", "extra", "symlink", "receipt"):
            with self.subTest(corruption=corruption):
                destination = self.directory / corruption
                DISTRIBUTION.prepare(self.revision, destination)
                readme = destination / "README.md"
                if corruption == "changed":
                    readme.write_bytes(readme.read_bytes() + b"Altered\n")
                elif corruption == "missing":
                    readme.unlink()
                elif corruption == "extra":
                    (destination / "unexpected.md").write_text("Unexpected payload\n")
                elif corruption == "symlink":
                    readme.unlink()
                    readme.symlink_to(self.package / "README.md")
                else:
                    (destination / DISTRIBUTION.RECEIPT).write_text("{}\n")
                with self.assertRaises(ValueError):
                    DISTRIBUTION.verify(self.revision, destination)

    def test_verification_rejects_symlink_directory(self):
        destination = self.directory / "ordinary"
        DISTRIBUTION.prepare(self.revision, destination)
        alias = self.directory / "alias"
        alias.symlink_to(destination, target_is_directory=True)
        with self.assertRaises(ValueError):
            DISTRIBUTION.verify(self.revision, alias)

    def test_self_consistent_counterfeit_receipt_cannot_authorize_changed_content(self):
        destination = self.directory / "counterfeit"
        DISTRIBUTION.prepare(self.revision, destination)
        readme = destination / "README.md"
        readme.write_text("Counterfeit editable semantic source\n")
        receipt_path = destination / DISTRIBUTION.RECEIPT
        receipt = json.loads(receipt_path.read_bytes())
        receipt["sha256"]["README.md"] = hashlib.sha256(readme.read_bytes()).hexdigest()
        receipt["payload_sha256"] = hashlib.sha256(json.dumps(
            receipt["sha256"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
        with self.assertRaises(ValueError):
            DISTRIBUTION.verify(self.revision, destination)

    def test_pinned_tree_hash_has_stable_path_order_and_byte_boundaries(self):
        files = {"z.md": b"Last\n", "a.md": b"Root\n",
                 "a/b.md": b"Nested\n", "LICENSE": b"MIT\n"}
        # Independent fixed vector for recipe0's component ordering and NUL boundaries.
        self.assertEqual(DISTRIBUTION.vibe_hash(files),
                         "sha256:41ba7247fd957c0bd7bba6464f417c0ded04510da769f6f9fba3794600c61881")
        self.assertNotEqual(DISTRIBUTION.vibe_hash(files),
                            DISTRIBUTION.vibe_hash({**files, "a.md": b"Root"}))

    def test_installed_slot_metadata_must_match_canonical_content(self):
        directory = self.directory / "installed"
        receipt, content_hash = self.installed_fixture(directory)
        self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, directory, installed=True))
        with self.assertRaises(ValueError):
            DISTRIBUTION.verify(self.revision, directory)
        marker = directory / ".vibe-slot.toml"
        original = marker.read_text()
        readme_hash = hashlib.sha256((directory / "README.md").read_bytes()).hexdigest()
        for altered in (original.replace(content_hash, "sha256:" + "0" * 64),
                        original.replace(readme_hash, "0" * 64),
                        original.replace('spec_format = "mixed"', 'spec_format = "simple"')):
            with self.subTest(marker=altered[:80]):
                self.assertNotEqual(original, altered)
                marker.write_text(altered)
                with self.assertRaises(ValueError):
                    DISTRIBUTION.verify(self.revision, directory, installed=True)

    def test_consumer_lock_and_requirement_must_bind_the_installed_slot(self):
        consumer, slot, receipt = self.consumer_fixture("consumer-lock")
        lock_path = consumer / "vibe.lock"
        manifest_path = consumer / "vibe.toml"
        original_lock = lock_path.read_text()
        original_manifest = manifest_path.read_text()
        _, content_hash = self.installed_fixture(self.directory / "same-package")
        mutations = [
            (lock_path, original_lock.replace('schema_version = 7', 'schema_version = 999')),
            (lock_path, original_lock.replace('[meta]\nschema_version = 7\n\n', '')),
            (lock_path, original_lock.replace(content_hash, "sha256:" + "0" * 64)),
            (lock_path, original_lock.replace('source_ref = "v0.1.0"', 'source_ref = "v0.1.1"')),
            (lock_path, original_lock.replace('file:///disposable/distribution.git', 'file:///other.git')),
            (manifest_path, original_manifest.replace('version = "=0.1.0"', 'version = "*"')),
            (manifest_path, original_manifest.replace('tag = "v0.1.0"',
                                                     'tag = "v0.1.0", rev = "' + "a" * 40 + '"')),
            (manifest_path, original_manifest.replace('tag = "v0.1.0"', 'rev = "abcdef"')),
        ]
        for path, altered in mutations:
            with self.subTest(file=path.name, content=altered[-100:]):
                lock_path.write_text(original_lock)
                manifest_path.write_text(original_manifest)
                path.write_text(altered)
                # Package/slot remain valid: consumer declaration/lock are the rejected layer.
                self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, slot, installed=True))
                with self.assertRaises(ValueError):
                    DISTRIBUTION.verify_consumer(self.revision, consumer)

    def test_consumer_native_projection_cannot_remain_stale_or_drift(self):
        for corruption in ("stale", "missing", "extra", "symlink"):
            with self.subTest(corruption=corruption):
                consumer, slot, receipt = self.consumer_fixture("native-" + corruption)
                projected = consumer / ".agents/skills/proportional-controls"
                skill = projected / "SKILL.md"
                if corruption == "stale":
                    skill.write_text("Previously materialized skill\n")
                elif corruption == "missing":
                    skill.unlink()
                elif corruption == "extra":
                    (projected / "old-reference.md").write_text("Old native policy\n")
                else:
                    skill.unlink()
                    skill.symlink_to(slot / "vibevm/vibespecs/skills/proportional-controls/SKILL.md")
                self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, slot, installed=True))
                with self.assertRaises(ValueError):
                    DISTRIBUTION.verify_consumer(self.revision, consumer)

    def test_executable_source_file_is_rejected(self):
        (self.package / "README.md").chmod(0o755)
        self.rejected_source()

    def test_symlink_source_file_is_rejected(self):
        readme = self.package / "README.md"
        readme.unlink()
        readme.symlink_to("LICENSE")
        self.rejected_source()

    def test_source_runtime_file_is_rejected(self):
        (self.package / "run.py").write_text("print('Unsupported runtime')\n")
        self.rejected_source()

    def test_capability_declaration_is_rejected(self):
        manifest = self.package / "vibe.toml"
        manifest.write_bytes(manifest.read_bytes() + b'\n[capabilities]\ntools = ["unsupported"]\n')
        self.rejected_source()

    def test_changed_version_license_or_publication_boundary_is_rejected(self):
        manifest = self.package / "vibe.toml"
        original = manifest.read_bytes()
        for before, after in ((b'version = "0.1.0"', b'version = "0.1.1"'),
                              (b'license = "MIT"', b'license = "Unapproved"'),
                              (b'publish = false', b'publish = true'),
                              (b'publish = false', b'publish = 0'),
                              (b'epoch = 1', b'epoch = true')):
            with self.subTest(change=after.decode()):
                self.assertIn(before, original)
                manifest.write_bytes(original.replace(before, after))
                self.rejected_source()

    def test_license_notice_drift_is_rejected(self):
        (self.package / "LICENSE").write_text("Different license notice\n")
        self.rejected_source()

    def test_incomplete_source_package_is_rejected(self):
        (self.package / "vibevm/vibespecs/skills/proportional-controls/references/protocol.md").unlink()
        self.rejected_source()

    def test_absent_source_package_is_rejected(self):
        shutil.rmtree(self.package)
        self.rejected_source()


if __name__ == "__main__":
    unittest.main(verbosity=2)
