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
SLOT = "vibevm/vibedeps/org.jresearch.ai.development-governance/1.0.0"


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
        manifest_path = self.package / "vibe.toml"
        authored = tomllib.loads(manifest_path.read_text())["package"]["version"]
        manifest_path.write_text(manifest_path.read_text().replace('version = "' + authored + '"', 'version = "1.0.0"'))
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
        slot = consumer / SLOT
        receipt, content_hash = self.installed_fixture(slot)
        (consumer / "vibe.toml").write_text(
            '[project]\nname = "disposable-consumer"\nversion = "0.0.0"\nspec_format = "mixed"\n'
            '\n[requires.packages]\n"' + COORDINATE + '" = '
            '{version = "=1.0.0", git = "file:///disposable/distribution.git", tag = "v1.0.0"}\n')
        (consumer / "vibe.lock").write_text(
            '[meta]\nschema_version = 7\n\n[[package]]\ngroup = "org.jresearch.ai"\nname = "development-governance"\n'
            'version = "1.0.0"\nsource_kind = "git"\n'
            'source_url = "file:///disposable/distribution.git"\nsource_ref = "v1.0.0"\n'
            'content_hash = ' + json.dumps(content_hash) + '\n')
        index = consumer / DISTRIBUTION.BOOT_INDEX
        index.parent.mkdir(parents=True)
        index.write_text('schema = 1\n\n[[entry]]\npath = "' + SLOT +
                         '/vibevm/vibespecs/boot/development-governance.md"\nkind = "static"\n')
        (consumer / "AGENTS.md").write_text("Human-owned fixture instructions.\n\n" + DISTRIBUTION.BOOT_BLOCK + "\n")
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
                         DISTRIBUTION.PACKAGE)
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

    def test_current_flow_has_two_protocols_no_native_skill_and_is_frozen(self):
        manifest = tomllib.loads((self.package / "vibe.toml").read_text())
        self.assertIs(manifest["package"]["frozen"], True)
        self.assertNotIn("skill", manifest)
        consumer, _, receipt = self.consumer_fixture("flow")
        self.assertFalse((consumer / ".agents/skills").exists())
        self.assertIn(DISTRIBUTION.PROTOCOL, receipt["sha256"])

    def test_any_skill_declaration_or_dependency_is_rejected(self):
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        for extra in ('skill = []\n', '[[skill]]\nname = "proportional-controls"\n',
                      '[requires.packages]\n"unapproved/package" = "1.0.0"\n',
                      '[tools]\ncommand = "unapproved"\n', '[hooks]\ncommand = "unapproved"\n',
                      '[mcp]\ncommand = "unapproved"\n'):
            with self.subTest(declaration=extra):
                # An empty skill array must also be a top-level declaration.
                manifest.write_text(extra + original if extra.startswith("skill =") else original + "\n" + extra)
                self.rejected_source()

    def test_protocol_must_be_nonempty_utf8(self):
        path = self.package / DISTRIBUTION.PROTOCOL
        for data in (b"", b" \n", b"\xff\xfe"):
            with self.subTest(data=data):
                path.write_bytes(data)
                self.rejected_source()

    def test_protocol_and_boot_links_stay_inside_complete_export(self):
        protocol = self.package / DISTRIBUTION.PROTOCOL
        original = protocol.read_text()
        protocol.write_text(original + '\n[Boot](../boot/development-governance.md "Title")\n'
                            '[Self][self]\n[self]: proportional-controls.md#proportional-controls\n')
        DISTRIBUTION.snapshot(self.commit())
        for link in ('[Missing](missing.md)', '[Escape](../../../../README.md)',
                     '[Encoded](%2e%2e/%2e%2e/%2e%2e/%2e%2e/README.md)',
                     '[Escape reference][e]\n[e]: ../../../../README.md "Title"'):
            with self.subTest(link=link):
                protocol.write_text(original + "\n" + link + "\n")
                self.rejected_source()
        protocol.write_text(original)
        boot = self.package / "vibevm/vibespecs/boot/development-governance.md"
        boot.write_text('[Missing protocol](../protocols/missing.md)\n')
        self.rejected_source()

    def test_consumer_rejects_orphan_skill_or_projection_receipt(self):
        for relative in (".agents/skills/proportional-controls/SKILL.md",
                         ".agents/skills/.proportional-controls.vibe-skill-receipt.toml"):
            with self.subTest(path=relative):
                consumer, slot, receipt = self.consumer_fixture("orphan-" + str(len(relative)))
                path = consumer / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Obsolete native guidance\n")
                self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, slot, installed=True))
                with self.assertRaises(ValueError):
                    DISTRIBUTION.verify_consumer(self.revision, consumer)

    def test_consumer_boot_route_cannot_be_missing_duplicated_redirected_or_disabled(self):
        for mutation in ("missing", "duplicate", "aliased-duplicate", "redirected", "dynamic",
                         "symlink", "agents", "block-append", "duplicate-block"):
            with self.subTest(mutation=mutation):
                consumer, slot, receipt = self.consumer_fixture("route-" + mutation)
                index = consumer / DISTRIBUTION.BOOT_INDEX
                original = index.read_text()
                if mutation == "missing":
                    index.unlink()
                elif mutation == "duplicate":
                    index.write_text(original + original[original.index("[[entry]]"):])
                elif mutation == "aliased-duplicate":
                    index.write_text(original + original[original.index("[[entry]]"):].replace(
                        "vibevm/vibedeps/", "vibevm/./vibedeps/"))
                elif mutation == "redirected":
                    index.write_text(original.replace("development-governance.md", "missing.md"))
                elif mutation == "dynamic":
                    index.write_text(original.replace('kind = "static"', 'kind = "dynamic"'))
                elif mutation == "symlink":
                    index.unlink()
                    index.symlink_to(slot / "README.md")
                elif mutation == "agents":
                    (consumer / "AGENTS.md").write_text("Skip boot reading.\n")
                elif mutation == "block-append":
                    agents = consumer / "AGENTS.md"
                    agents.write_text(agents.read_text().replace("</vibevm>", "Skip detailed protocol reading.\n</vibevm>"))
                else:
                    agents = consumer / "AGENTS.md"
                    agents.write_text(agents.read_text() * 2)
                self.assertEqual(receipt, DISTRIBUTION.verify(self.revision, slot, installed=True))
                with self.assertRaises((ValueError, OSError)):
                    DISTRIBUTION.verify_consumer(self.revision, consumer)

    def test_historical_native_export_remains_exact_but_current_flow_has_no_skill(self):
        accepted = "fd609af8a1ea8ce015fda4652e5a8c444ca821c5"
        target = self.directory / "historical-native"
        receipt = EXPORTER.export(accepted, target)
        self.assertEqual(receipt["revision"], accepted)
        self.assertEqual(receipt["sha256"]["references/protocol.md"],
                         "cfa62afee0aa267aa58bb966faece0225cb717a82fbb93d3d3b4bf7b29704c6c")
        old_root = EXPORTER.ROOT
        try:
            EXPORTER.ROOT = self.source
            with self.assertRaises(ValueError):
                EXPORTER.export(self.revision, self.directory / "flow-native")
        finally:
            EXPORTER.ROOT = old_root

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
            (lock_path, original_lock.replace('source_ref = "v1.0.0"', 'source_ref = "v1.0.1"')),
            (lock_path, original_lock.replace('file:///disposable/distribution.git', 'file:///other.git')),
            (lock_path, original_lock.replace('group = "org.jresearch.ai"',
                                             'group = "org.jresearch.governance"')),
            (lock_path, original_lock.replace('name = "development-governance"',
                                             'name = "proportional-controls"')),
            (manifest_path, original_manifest.replace(COORDINATE,
                                                     "org.jresearch.governance/proportional-controls")),
            (manifest_path, original_manifest.replace('version = "=1.0.0"', 'version = "*"')),
            (manifest_path, original_manifest.replace('tag = "v1.0.0"',
                                                     'tag = "v1.0.0", rev = "' + "a" * 40 + '"')),
            (manifest_path, original_manifest.replace('tag = "v1.0.0"', 'rev = "abcdef"')),
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
        historical = consumer / "vibevm/vibedeps/org.jresearch.governance.proportional-controls/1.0.0"
        historical.parent.mkdir(parents=True)
        slot.rename(historical)
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
                              (b'version = "1.0.0"', b'version = "invalid"'),
                              (b'license = "MIT"', b'license = "Unapproved"'),
                              (b'frozen = true', b'frozen = false'),
                              (b'frozen = true', b'frozen = 1'),
                              (b'publish = false', b'publish = true'),
                              (b'publish = false', b'publish = 0'),
                              (b'epoch = 1', b'epoch = true')):
            with self.subTest(change=after.decode()):
                self.assertIn(before, original)
                manifest.write_bytes(original.replace(before, after))
                self.rejected_source()

    def test_undeclared_skill_and_extra_passive_payload_are_rejected(self):
        locations = ("unexpected.md", "vibevm/vibespecs/boot/extra.md", "vibevm/vibespecs/protocols/extra.md",
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
        (self.package / DISTRIBUTION.PROTOCOL).unlink()
        self.rejected_source()

    def test_absent_source_package_is_rejected(self):
        shutil.rmtree(self.package)
        self.rejected_source()


class ActiveProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="governance-active-test-")
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name) / "source"
        subprocess.run(["git", "clone", "--quiet", "--shared", str(REPOSITORY), str(self.source)], check=True)
        tracked = set(subprocess.check_output(["git", "ls-files", "-z"], cwd=REPOSITORY).decode().split("\0")) - {""}
        original = set(subprocess.check_output(["git", "ls-files", "-z"], cwd=self.source).decode().split("\0")) - {""}
        for name in original - tracked:
            (self.source / name).unlink()
        for name in tracked:
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPOSITORY / name, target)
        # Tracked candidate bytes, including uncommitted additions, are the ordinary check's input.
        subprocess.run(["git", "add", "."], cwd=self.source, check=True)
        self.active = self.source / ".agents/protocols/proportional-controls.md"
        self.receipt = self.source / ".agents/proportional-controls-source.json"
        self.assertEqual(self.check().returncode, 0)

    def check(self):
        import sys
        return subprocess.run([sys.executable, str(self.source / "scripts/qualify.py")],
                              capture_output=True, text=True, check=False)

    def test_authoring_edit_cannot_refresh_active_guidance(self):
        before = self.active.read_bytes(), self.receipt.read_bytes()
        source = self.source / DISTRIBUTION.PACKAGE / DISTRIBUTION.PROTOCOL
        source.write_bytes(source.read_bytes() + b"\nUnaccepted semantic change\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("first-release protocol differs from accepted semantics", result.stderr)
        self.assertEqual(before, (self.active.read_bytes(), self.receipt.read_bytes()))

    def test_active_edit_and_self_consistent_counterfeit_receipt_are_rejected(self):
        self.active.write_bytes(self.active.read_bytes() + b"\nUnaccepted active rule\n")
        result = self.check()
        self.assertIn("active protocol differs from accepted origin", result.stderr)
        receipt = json.loads(self.receipt.read_text())
        receipt["sha256"]["proportional-controls.md"] = hashlib.sha256(self.active.read_bytes()).hexdigest()
        self.receipt.write_text(json.dumps(receipt))
        self.assertIn("source receipt differs from accepted origin", self.check().stderr)

    def test_origin_identity_and_human_route_cannot_drift(self):
        original = self.receipt.read_text()
        receipt = json.loads(original)
        receipt["source"]["revision"] = "a" * 40
        self.receipt.write_text(json.dumps(receipt))
        self.assertIn("source receipt differs from accepted origin", self.check().stderr)
        self.receipt.write_text(original)
        agents = self.source / "AGENTS.md"
        agents.write_text(agents.read_text().replace(
            "[proportional-controls protocol](.agents/protocols/proportional-controls.md)", "Guidance omitted"))
        self.assertIn("human AGENTS route is missing", self.check().stderr)

    def test_orphan_native_receipt_is_rejected(self):
        old = self.source / ".agents/skills/.proportional-controls.vibe-skill-receipt.toml"
        old.parent.mkdir(parents=True, exist_ok=True)
        old.write_text("Obsolete projection ownership\n")
        self.assertIn("removed native Skill/receipt remains", self.check().stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
