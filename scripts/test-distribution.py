#!/usr/bin/env python3
"""Behavioral checks for passive distribution preparation using disposable Git sources."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "prepare_distribution", REPOSITORY / "scripts/prepare-distribution.py")
DISTRIBUTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DISTRIBUTION)
EXPORT_SPEC = importlib.util.spec_from_file_location(
    "vendor_skill", REPOSITORY / "scripts/vendor-skill.py")
EXPORTER = importlib.util.module_from_spec(EXPORT_SPEC)
EXPORT_SPEC.loader.exec_module(EXPORTER)
COORDINATE = "org.jresearch.ai/development-governance"
SLOT = "vibevm/vibedeps/org.jresearch.ai.development-governance/0.1.0"


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
        shutil.copyfile(REPOSITORY / "vibe.toml", self.source / "vibe.toml")
        # Windows-mounted files can appear executable; fixture Git modes are explicit.
        for path in self.package.rglob("*"):
            if path.is_file():
                path.chmod(0o644)
        (self.source / "LICENSE").chmod(0o644)
        (self.source / "vibe.toml").chmod(0o644)
        self.git("init", "-q")
        self.git("config", "user.name", "Disposable distribution test")
        self.git("config", "user.email", "distribution-test@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.filemode", "true")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.directory / "no-hooks"))
        # Short-lived fixtures must not leave Git writers racing directory cleanup.
        self.git("config", "maintenance.auto", "false")
        self.git("config", "gc.auto", "0")
        self.revision = self.commit()
        self.old_root = DISTRIBUTION.ROOT
        DISTRIBUTION.ROOT = self.source
        self.addCleanup(setattr, DISTRIBUTION, "ROOT", self.old_root)
        self.old_export_root = EXPORTER.ROOT
        EXPORTER.ROOT = self.source
        self.addCleanup(setattr, EXPORTER, "ROOT", self.old_export_root)
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

    def add_synthetic_skill(self, name="synthetic-passive"):
        """Only a disposable fixture: no new governance rule enters the source."""
        relative = "vibevm/vibespecs/skills/" + name
        manifest = self.package / "vibe.toml"
        with manifest.open("a") as stream:
            stream.write('\n[[skill]]\nname = ' + json.dumps(name)
                         + '\npath = ' + json.dumps(relative)
                         + '\ninclude = ["SKILL.md", "references/*.md"]\n')
        skill = self.package / relative
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: " + name + "\ndescription: Synthetic passive test fixture.\n---\n\n"
            "Read [references/note.md](references/note.md) for fixture text.\n")
        (skill / "references/note.md").write_text("Synthetic test fixture, without a policy rule.\n")
        (skill / "references/second.md").write_text("Another direct Markdown fixture reference.\n")
        for path in skill.rglob("*"):
            if path.is_file():
                path.chmod(0o644)
        return skill

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
        slot = consumer / SLOT
        receipt, content_hash = self.installed_fixture(slot)
        (consumer / "vibe.toml").write_text(
            '[project]\nname = "disposable-consumer"\nversion = "0.0.0"\nspec_format = "mixed"\n'
            '\n[requires.packages]\n"' + COORDINATE + '" = '
            '{version = "=0.1.0", git = "file:///disposable/distribution.git", tag = "v0.1.0"}\n')
        (consumer / "vibe.lock").write_text(
            '[meta]\nschema_version = 7\n\n[[package]]\ngroup = "org.jresearch.ai"\nname = "development-governance"\n'
            'version = "0.1.0"\nsource_kind = "git"\n'
            'source_url = "file:///disposable/distribution.git"\nsource_ref = "v0.1.0"\n'
            'content_hash = ' + json.dumps(content_hash) + '\n')
        declarations = tomllib.loads((slot / "vibe.toml").read_text())["skill"]
        for declaration in declarations:
            shutil.copytree(slot / declaration["path"],
                            consumer / ".agents/skills" / declaration["name"])
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
        self.assertEqual(receipt["package"], COORDINATE)
        self.assertEqual(receipt["source_path"],
                         "vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0")
        self.assertEqual(receipt["sha256"], {
            name: hashlib.sha256(data).hexdigest() for name, data in expected.items()})
        self.assertEqual(source_before, self.payload(self.package))
        self.assertEqual(status_before, self.git("status", "--porcelain", "--untracked-files=all"))
        self.assertEqual(self.revision, self.git("rev-parse", "HEAD").decode().strip())

    def test_multiple_declared_passive_skills_are_prepared_and_all_projected(self):
        self.add_synthetic_skill()
        self.revision = self.commit()
        expected = self.payload(self.package)
        consumer, slot, receipt = self.consumer_fixture("multiple-skills")
        self.assertEqual(set(receipt["sha256"]), set(expected))
        for name in ("proportional-controls", "synthetic-passive"):
            self.assertEqual(
                self.payload(self.package / "vibevm/vibespecs/skills" / name),
                self.payload(consumer / ".agents/skills" / name))
        self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, slot, installed=True))
        self.assertEqual(receipt, DISTRIBUTION.verify_consumer(self.revision, consumer))

    def test_safe_short_and_maximum_length_skill_names_are_supported(self):
        for name in ("a", "a" * 64):
            self.add_synthetic_skill(name)
        self.revision = self.commit()
        self.consumer_fixture("skill-name-boundaries")

    def test_native_export_selects_an_additional_declared_skill_at_the_exact_commit(self):
        second = self.add_synthetic_skill()
        self.revision = self.commit()
        expected = self.payload(second)
        # The selected commit governs both declaration and bytes, despite dirty source.
        (second / "SKILL.md").write_text("Uncommitted second Skill edit\n")
        destination = self.directory / "native-second"
        receipt = EXPORTER.export(self.revision, destination, "synthetic-passive")
        self.assertEqual(receipt["revision"], self.revision)
        self.assertEqual(receipt["source_path"],
                         DISTRIBUTION.PACKAGE + "/vibevm/vibespecs/skills/synthetic-passive")
        actual = self.payload(destination)
        self.assertEqual(set(actual), set(expected) | {"LICENSE", "SOURCE.json"})
        self.assertEqual({name: actual[name] for name in expected}, expected)
        self.assertEqual(actual["LICENSE"], (self.source / "LICENSE").read_bytes())
        self.assertEqual(receipt["sha256"], {
            name: hashlib.sha256(data).hexdigest()
            for name, data in {**expected, "LICENSE": actual["LICENSE"]}.items()})
        self.assertEqual(json.loads(actual["SOURCE.json"]), receipt)

    def test_native_export_rejects_missing_or_unsafe_skill_selection(self):
        for name in ("absent-skill", "../escape", "UPPER", "", "a" * 65):
            with self.subTest(skill=name):
                destination = self.directory / "native-rejected"
                with self.assertRaises(ValueError):
                    EXPORTER.export(self.revision, destination, name)
                self.assertFalse(destination.exists())

    def test_native_export_rejects_undeclared_duplicate_or_missing_skill(self):
        manifest = self.package / "vibe.toml"
        first_only = manifest.read_text()
        second = self.add_synthetic_skill()
        declared = manifest.read_text()
        second_declaration = declared[declared.index('[[skill]]\nname = "synthetic-passive"'):]
        for name, altered in (("undeclared", first_only),
                              ("duplicate", declared + second_declaration)):
            with self.subTest(case=name):
                manifest.write_text(altered)
                destination = self.directory / ("native-" + name)
                with self.assertRaises(ValueError):
                    EXPORTER.export(self.commit(), destination, "synthetic-passive")
                self.assertFalse(destination.exists())
        manifest.write_text(declared)
        (second / "SKILL.md").unlink()
        destination = self.directory / "native-no-entrypoint"
        with self.assertRaises(ValueError):
            EXPORTER.export(self.commit(), destination, "synthetic-passive")
        self.assertFalse(destination.exists())

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
            (lock_path, original_lock.replace('group = "org.jresearch.ai"',
                                             'group = "org.jresearch.governance"')),
            (lock_path, original_lock.replace('name = "development-governance"',
                                             'name = "proportional-controls"')),
            (manifest_path, original_manifest.replace(COORDINATE,
                                                     "org.jresearch.governance/proportional-controls")),
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

    def test_historical_installed_slot_cannot_replace_the_current_coordinate(self):
        consumer, slot, _ = self.consumer_fixture("historical-slot")
        historical = consumer / "vibevm/vibedeps/org.jresearch.governance.proportional-controls/0.1.0"
        historical.parent.mkdir(parents=True)
        slot.rename(historical)
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

    def test_each_additional_native_projection_must_match_canonical_source(self):
        self.add_synthetic_skill()
        self.revision = self.commit()
        for corruption in ("changed", "missing-skill", "missing-directory", "extra", "symlink"):
            with self.subTest(corruption=corruption):
                consumer, slot, receipt = self.consumer_fixture("second-native-" + corruption)
                projected = consumer / ".agents/skills/synthetic-passive"
                skill = projected / "SKILL.md"
                if corruption == "changed":
                    skill.write_text("Altered second Skill\n")
                elif corruption == "missing-skill":
                    skill.unlink()
                elif corruption == "missing-directory":
                    shutil.rmtree(projected)
                elif corruption == "extra":
                    (projected / "references/undeclared.md").write_text("Stale reference\n")
                else:
                    skill.unlink()
                    skill.symlink_to(slot / "vibevm/vibespecs/skills/synthetic-passive/SKILL.md")
                self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, slot, installed=True))
                # The accepted first projection is still intact; the second must be checked too.
                self.assertEqual(self.payload(self.package / "vibevm/vibespecs/skills/proportional-controls"),
                                 self.payload(consumer / ".agents/skills/proportional-controls"))
                with self.assertRaises(ValueError):
                    DISTRIBUTION.verify_consumer(self.revision, consumer)

    def test_additional_native_projection_cannot_be_a_symlink_directory(self):
        self.add_synthetic_skill()
        self.revision = self.commit()
        consumer, slot, _ = self.consumer_fixture("second-native-directory-link")
        projected = consumer / ".agents/skills/synthetic-passive"
        shutil.rmtree(projected)
        projected.symlink_to(slot / "vibevm/vibespecs/skills/synthetic-passive", target_is_directory=True)
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
        for before, after in ((b'group = "org.jresearch.ai"', b'group = "org.jresearch.governance"'),
                              (b'name = "development-governance"', b'name = "proportional-controls"'),
                              (b'version = "0.1.0"', b'version = "0.1.1"'),
                              (b'license = "MIT"', b'license = "Unapproved"'),
                              (b'publish = false', b'publish = true'),
                              (b'publish = false', b'publish = 0'),
                              (b'epoch = 1', b'epoch = true')):
            with self.subTest(change=after.decode()):
                self.assertIn(before, original)
                manifest.write_bytes(original.replace(before, after))
                self.rejected_source()

    def test_skills_must_be_a_nonempty_declaration_list(self):
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        package_and_boot = original.split("[[skill]]", 1)[0]
        for altered in (package_and_boot, "skill = []\n\n" + package_and_boot,
                        original.replace("[[skill]]", "[skill]")):
            with self.subTest(manifest=altered[-100:]):
                manifest.write_text(altered)
                self.rejected_source()

    def test_existing_proportional_controls_cannot_be_replaced_by_another_passive_skill(self):
        self.add_synthetic_skill()
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        start = original.index('[[skill]]\nname = "proportional-controls"')
        end = original.index('[[skill]]\nname = "synthetic-passive"')
        manifest.write_text(original[:start] + original[end:])
        shutil.rmtree(self.package / "vibevm/vibespecs/skills/proportional-controls")
        self.rejected_source()

    def test_duplicate_skill_names_or_paths_are_rejected(self):
        second = self.add_synthetic_skill()
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        changes = (
            original.replace('name = "synthetic-passive"', 'name = "proportional-controls"'),
            original.replace('path = "vibevm/vibespecs/skills/synthetic-passive"',
                             'path = "vibevm/vibespecs/skills/proportional-controls"'),
            original + original[original.index('[[skill]]\nname = "synthetic-passive"'):],
        )
        self.assertTrue(second.is_dir())
        for altered in changes:
            with self.subTest(manifest=altered[-180:]):
                manifest.write_text(altered)
                self.rejected_source()

    def test_skill_names_must_use_the_bounded_safe_discovery_format(self):
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        for name in ("UPPER", "under_score", "a--b", "-a", "1a", "a" * 65):
            with self.subTest(name=name):
                manifest.write_text(original)
                skill = self.add_synthetic_skill(name)
                self.rejected_source()
                shutil.rmtree(skill)
        for name in ("", "../escape"):
            with self.subTest(name=name):
                manifest.write_text(original.replace('name = "proportional-controls"',
                                                     'name = ' + json.dumps(name)))
                self.rejected_source()

    def test_skill_paths_and_include_patterns_cannot_expand_the_passive_boundary(self):
        self.add_synthetic_skill()
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        changes = [
            original.replace('path = "vibevm/vibespecs/skills/synthetic-passive"',
                             'path = ' + json.dumps(path))
            for path in ("../synthetic-passive", "/tmp/synthetic-passive",
                         "vibevm/vibespecs/skills/../synthetic-passive",
                         "vibevm/vibespecs/skills/synthetic-passive/",
                         "vibevm\\vibespecs\\skills\\synthetic-passive")
        ]
        changes.extend(original.replace('include = ["SKILL.md", "references/*.md"]', include)
                       for include in ('include = ["**/*"]',
                                       'include = ["SKILL.md", "references/**/*.md"]',
                                       'include = ["SKILL.md", "references/*.md", "*.py"]',
                                       'include = ["references/*.md", "SKILL.md"]'))
        for altered in changes:
            with self.subTest(manifest=altered[-180:]):
                manifest.write_text(altered)
                self.rejected_source()

    def test_per_skill_capabilities_or_unexpected_declaration_fields_are_rejected(self):
        self.add_synthetic_skill()
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        for field in ('tools = ["unsupported"]', 'hooks = ["unsupported"]',
                      'mcp = "unsupported"', 'description = "Extra declaration field"',
                      '[skill.capabilities]\ntools = ["unsupported"]'):
            with self.subTest(field=field):
                manifest.write_text(original + "\n" + field + "\n")
                self.rejected_source()

    def test_each_declared_skill_requires_discovery_frontmatter_and_direct_reference(self):
        second = self.add_synthetic_skill()
        original = (second / "SKILL.md").read_text()
        changes = ("No discovery frontmatter\n",
                   original.replace("name: synthetic-passive", "name: different-name"),
                   original.replace("description: Synthetic passive test fixture.", "description:"),
                   original.replace("description: Synthetic passive test fixture.", "description: "),
                   original.replace("description: Synthetic passive test fixture.\n", ""))
        for altered in changes:
            with self.subTest(frontmatter=altered[:80]):
                (second / "SKILL.md").write_text(altered)
                self.rejected_source()
        (second / "SKILL.md").write_text(original)
        for reference in (second / "references").glob("*.md"):
            reference.unlink()
        self.rejected_source()

    def test_native_frontmatter_cannot_add_tools_hooks_or_multiline_discovery(self):
        second = self.add_synthetic_skill()
        discovery = second / "SKILL.md"
        original = discovery.read_text()
        changes = [original.replace("\n---\n", "\n" + field + "\n---\n", 1)
                   for field in ("allowed-tools: Read", "hooks:\n  PreToolUse: []")]
        changes.append(original.replace("description: Synthetic passive test fixture.",
                                        "description: |\n  Synthetic passive test fixture."))
        for index, altered in enumerate(changes):
            with self.subTest(frontmatter=altered[:120]):
                discovery.write_text(altered)
                revision = self.commit()
                self.rejected_source(revision)
                destination = self.directory / ("native-frontmatter-rejected-" + str(index))
                with self.assertRaises(ValueError):
                    EXPORTER.export(revision, destination, "synthetic-passive")
                self.assertFalse(destination.exists())

    def test_markdown_reference_must_contain_utf8_text(self):
        second = self.add_synthetic_skill()
        (second / "references/note.md").write_bytes(b"\xff\x00\xfeBinary fixture\n")
        self.rejected_source()

    def test_selected_skill_local_links_remain_self_contained_in_both_exports(self):
        second = self.add_synthetic_skill()
        reference = second / "references/note.md"
        valid = ("# Fixture\n\n[Entry](../SKILL.md) and [detail](second.md#fixture).\n"
                 "[Anchor](#fixture) and [citation](https://example.invalid/reference#fixture).\n")
        reference.write_text(valid)
        self.revision = self.commit()
        prepared = self.directory / "scoped-distribution"
        DISTRIBUTION.prepare(self.revision, prepared)
        native = self.directory / "scoped-native"
        EXPORTER.export(self.revision, native, "synthetic-passive")
        self.assertEqual((native / "references/note.md").read_text(), valid)
        self.assertEqual((prepared / "vibevm/vibespecs/skills/synthetic-passive/references/note.md").read_text(),
                         valid)
        for index, target in enumerate(("../../proportional-controls/SKILL.md",
                                        "../../../../../README.md",
                                        "../../../boot/development-governance.md", "missing.md",
                                        "%2e%2e/%2e%2e/proportional-controls/SKILL.md")):
            with self.subTest(target=target):
                reference.write_text(valid + "\n[Escaping or missing](" + target + ")\n")
                revision = self.commit()
                self.rejected_source(revision)
                destination = self.directory / ("native-link-rejected-" + str(index))
                with self.assertRaises(ValueError):
                    EXPORTER.export(revision, destination, "synthetic-passive")
                self.assertFalse(destination.exists())

    def test_titled_and_reference_links_cannot_escape_the_selected_skill(self):
        second = self.add_synthetic_skill()
        reference = second / "references/note.md"
        valid = ('[Own](../SKILL.md "Title")\n[Own reference][own]\n'
                 '[own]: ../SKILL.md "Title"\n')
        reference.write_text(valid)
        revision = self.commit()
        DISTRIBUTION.snapshot(revision)
        EXPORTER.export(revision, self.directory / "native-titled-valid", "synthetic-passive")
        for index, link in enumerate((
                '[Other](../../proportional-controls/SKILL.md "Title")',
                '[Other][other]\n[other]: ../../proportional-controls/SKILL.md "Title"')):
            with self.subTest(link=link):
                reference.write_text(valid + link + "\n")
                revision = self.commit()
                self.rejected_source(revision)
                destination = self.directory / ("native-titled-rejected-" + str(index))
                with self.assertRaises(ValueError):
                    EXPORTER.export(revision, destination, "synthetic-passive")
                self.assertFalse(destination.exists())

    def test_missing_additional_skill_entrypoint_is_rejected(self):
        second = self.add_synthetic_skill()
        (second / "SKILL.md").unlink()
        self.rejected_source()

    def test_undeclared_skill_and_extra_passive_payload_are_rejected(self):
        locations = ("unexpected.md", "vibevm/vibespecs/boot/extra.md",
                     "vibevm/vibespecs/skills/undeclared/SKILL.md",
                     "vibevm/vibespecs/skills/proportional-controls/references/nested/note.md",
                     "vibevm/vibespecs/skills/proportional-controls/extra.md")
        for relative in locations:
            with self.subTest(path=relative):
                extra = self.package / relative
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_text("Undeclared passive payload\n")
                self.rejected_source()
                extra.unlink()

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
