#!/usr/bin/env python3
"""Behavioral checks for passive distribution preparation using disposable Git sources."""
import hashlib
import importlib.util
import json
import re
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
SLOT = "vibevm/vibedeps/org.jresearch.ai.development-governance/2.2.0"


class DistributionTests(unittest.TestCase):
    def current_export(self):
        DISTRIBUTION.ROOT = REPOSITORY
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY).decode().strip()
        files, _ = DISTRIBUTION.snapshot(revision)
        files.pop(DISTRIBUTION.RECEIPT)
        return files

    def test_current_changelog_is_exported_verified_and_required(self):
        files = self.current_export()
        self.assertIn(DISTRIBUTION.CHANGELOG, files)
        self.assertIn(b"2.7.0", files[DISTRIBUTION.CHANGELOG])
        self.assertIn(b"3.0.0", files[DISTRIBUTION.CHANGELOG])
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY).decode().strip()
        destination = self.directory / "current-package"
        DISTRIBUTION.prepare(revision, destination)
        DISTRIBUTION.verify(revision, destination)
        (destination / DISTRIBUTION.CHANGELOG).unlink()
        with self.assertRaisesRegex(ValueError, "file set differs"):
            DISTRIBUTION.verify(revision, destination)
        for content in (None, b"", b" \n"):
            with self.subTest(content=content):
                changed = dict(files)
                if content is None:
                    del changed[DISTRIBUTION.CHANGELOG]
                else:
                    changed[DISTRIBUTION.CHANGELOG] = content
                with self.assertRaises(ValueError):
                    DISTRIBUTION.validate_payload(changed, files["LICENSE"])
        historical, _ = DISTRIBUTION.snapshot("ec048fb39ae28cf2d747101466a603ddd062b1b0")
        historical.pop(DISTRIBUTION.RECEIPT)
        self.assertNotIn(DISTRIBUTION.CHANGELOG, historical)
        historical[DISTRIBUTION.CHANGELOG] = files[DISTRIBUTION.CHANGELOG]
        with self.assertRaises(ValueError):
            DISTRIBUTION.validate_payload(historical, files["LICENSE"])

    def test_rule_addresses_reject_collisions_missing_routes_and_wrong_targets(self):
        files = self.current_export()
        for path, suffix in (
                (DISTRIBUTION.HANDOFF, b'\n<a id="TH-006"></a>\n'),
                (DISTRIBUTION.INDEPENDENT_REVIEW, b'\n<a id="TH-006"></a>\n'),
                ("README.md", b'\n[Missing](vibevm/vibespecs/protocols/task-handoff.md#TH-999)\n'),
                ("README.md", b'\n[Wrong owner](vibevm/vibespecs/protocols/independent-review.md#TH-006)\n')):
            with self.subTest(path=path, suffix=suffix):
                changed = dict(files)
                changed[path] += suffix
                with self.assertRaises(ValueError):
                    DISTRIBUTION.validate_payload(changed, files["LICENSE"])
        changed = dict(files)
        changed[DISTRIBUTION.HANDOFF] = re.sub(rb'<a id="TH-[0-9]{3}"></a>', b"", files[DISTRIBUTION.HANDOFF])
        with self.assertRaises(ValueError):
            DISTRIBUTION.validate_payload(changed, files["LICENSE"])

    def test_legacy_heading_links_and_annotation_only_semantics_are_preserved(self):
        files = self.current_export()
        historical, _ = DISTRIBUTION.snapshot("ec048fb39ae28cf2d747101466a603ddd062b1b0")
        protocols = [name for name in files if name.startswith("vibevm/vibespecs/protocols/") and name in historical]
        for name in protocols:
            with self.subTest(protocol=name):
                headings = re.findall(rb"^#{1,6} .+$", historical[name], re.M)
                self.assertTrue(set(headings) <= set(re.findall(rb"^#{1,6} .+$", files[name], re.M)))
        # PC gained a normative rule after 3.0.0; check that accepted prefix
        # separately instead of asserting the old annotation-only transition.
        unchanged = set(protocols) - {DISTRIBUTION.HANDOFF, DISTRIBUTION.INDEPENDENT_REVIEW,
                                      DISTRIBUTION.VERSIONING, DISTRIBUTION.PROTOCOL, DISTRIBUTION.AUTHORITY}
        # Task 62 removes the ChatGPT receipt reference from the current guide;
        # retain the annotation-only historical guide comparison at accepted 3.0.0.
        annotated, _ = DISTRIBUTION.snapshot("e654d9e20a7c42c50cc05786dc83a4f7a16f84e4")
        stripped = re.sub(rb'\n<a id="[A-Z]+-[0-9]{3}"></a>\n\*\*[^\n]+\*\*\n\n', b"\n",
                          annotated[DISTRIBUTION.ONBOARDING])
        self.assertEqual(stripped, historical[DISTRIBUTION.ONBOARDING])
        unchanged.add(DISTRIBUTION.ENGINEERING_METHODS)
        for name in unchanged:
            with self.subTest(meaning=name):
                stripped = re.sub(rb'\n<a id="[A-Z]+-[0-9]{3}"></a>\n\*\*[^\n]+\*\*\n\n', b"\n", files[name])
                self.assertEqual(stripped, historical[name])

    def test_review_scope_change_preserves_accepted_rules_and_unaffected_protocols(self):
        # Historical Task 52 transition; future authorized edits do not redefine it.
        DISTRIBUTION.ROOT = REPOSITORY
        files, _ = DISTRIBUTION.snapshot("99034dd708e5d0201060986b561ada4d2cffd453")
        files.pop(DISTRIBUTION.RECEIPT)
        accepted, _ = DISTRIBUTION.snapshot("e654d9e20a7c42c50cc05786dc83a4f7a16f84e4")
        # Seven untouched protocols and all earlier PC rules keep exact bytes.
        for name in files:
            if name.startswith("vibevm/vibespecs/protocols/") and name not in {
                    DISTRIBUTION.PROTOCOL, DISTRIBUTION.INDEPENDENT_REVIEW}:
                with self.subTest(protocol=name):
                    self.assertEqual(files[name], accepted[name])
        self.assertTrue(files[DISTRIBUTION.PROTOCOL].startswith(accepted[DISTRIBUTION.PROTOCOL]))
        anchors = lambda value: set(re.findall(rb'<a id="([A-Z]+-[0-9]{3})"></a>', value))
        for name, new in ((DISTRIBUTION.PROTOCOL, {b"PC-013"}),
                          (DISTRIBUTION.INDEPENDENT_REVIEW, set())):
            self.assertEqual(anchors(files[name]), anchors(accepted[name]) | new)
        owners = [name for name, content in files.items() if b'<a id="PC-013"></a>' in content]
        self.assertEqual(owners, [DISTRIBUTION.PROTOCOL])
        DISTRIBUTION.validate_payload(files, files["LICENSE"])

    def test_joint_authority_settings_change_preserves_unaffected_contracts(self):
        # Historical Tasks 60/62 transition; later authorized TH-026 edits do not
        # redefine the accepted 5.0.0 contract this regression protects.
        DISTRIBUTION.ROOT = REPOSITORY
        files, _ = DISTRIBUTION.snapshot("414077e956aa47b18ddc436f68c3245b508baf46")
        accepted, _ = DISTRIBUTION.snapshot("61aa3444365b02a27c392d48aa9ea33e85c5d5d4")
        guide = files[DISTRIBUTION.ONBOARDING].replace(b'its content check/diff', b'its check/diff/receipt')
        guide = guide.replace(b'remain separate and conditional on application scope.', b'remain separate.')
        self.assertEqual(guide, accepted[DISTRIBUTION.ONBOARDING])
        changed = {DISTRIBUTION.AUTHORITY, DISTRIBUTION.HANDOFF, DISTRIBUTION.INDEPENDENT_REVIEW}
        for name in files:
            if name.startswith("vibevm/vibespecs/protocols/") and name not in changed:
                with self.subTest(protocol=name):
                    self.assertEqual(files[name], accepted[name])
        self.assertTrue(files[DISTRIBUTION.AUTHORITY].startswith(accepted[DISTRIBUTION.AUTHORITY]))
        anchors = lambda value: set(re.findall(rb'<a id="([A-Z]+-[0-9]{3})"></a>', value))
        for name, new in ((DISTRIBUTION.AUTHORITY, {b"RA-006"}),
                          (DISTRIBUTION.HANDOFF, {b"TH-029"}),
                          (DISTRIBUTION.INDEPENDENT_REVIEW, set())):
            self.assertEqual(anchors(files[name]), anchors(accepted[name]) | new)
        # Retain every accepted TH/IR paragraph except the three bounded applications.
        th = files[DISTRIBUTION.HANDOFF].split(b'\n<a id="TH-029"></a>')[0]
        th = th.replace(b'Apply [RA-006](requirement-authority.md#RA-006) when authoring the Task and its\n'
                        b'acceptance/completion criteria; agent-written gates cannot authorize themselves.\n\n', b'')
        th = th.replace(b'Apply [RA-006](requirement-authority.md#RA-006) before admitting continuation;\n'
                        b'reconcile apparent self-expansion through existing Decisions. ', b'')
        self.assertEqual(th, accepted[DISTRIBUTION.HANDOFF])
        ir = files[DISTRIBUTION.INDEPENDENT_REVIEW].replace(
            b'Apply [RA-006](requirement-authority.md#RA-006) to finding classification, blocker\n'
            b'decisions and recommendations, preserving initiative and explicit per-finding\n'
            b'owner dispositions without turning proposals into obligations.\n\n', b'')
        self.assertEqual(ir, accepted[DISTRIBUTION.INDEPENDENT_REVIEW])

    def test_closure_change_preserves_all_other_accepted_rules(self):
        # Preserve the accepted 5.1.0 transition; Task 74 deliberately changes
        # TH-029 later, without retroactively changing this earlier contract.
        DISTRIBUTION.ROOT = REPOSITORY
        files, _ = DISTRIBUTION.snapshot("2361868c41a916871d687aa8eea8f14573e2c82e")
        accepted, _ = DISTRIBUTION.snapshot("414077e956aa47b18ddc436f68c3245b508baf46")
        changed_rules = {DISTRIBUTION.HANDOFF: b"TH-026", DISTRIBUTION.AUTHORITY: b"RA-006"}
        for name, before in accepted.items():
            if not name.startswith("vibevm/vibespecs/protocols/"):
                continue
            with self.subTest(protocol=name):
                if name not in changed_rules:
                    self.assertEqual(files[name], before)
                    continue
                # Stable rule addresses bind the scope, independent of paragraph
                # wording. No other accepted rule may be silently rewritten.
                rule = changed_rules[name]
                def parts(value):
                    pieces = re.split(rb'(<a id="[A-Z]+-[0-9]{3}"></a>)', value)
                    return dict(zip(pieces[1::2], pieces[2::2]))
                old, new = parts(before), parts(files[name])
                self.assertEqual(set(old), set(new))
                for anchor in old:
                    if anchor == b'<a id="' + rule + b'"></a>':
                        self.assertNotEqual(old[anchor], new[anchor])
                    else:
                        self.assertEqual(old[anchor], new[anchor])

    def test_effective_instructions_change_preserves_other_accepted_protocol_rules(self):
        current = self.current_export()
        # Bind Task 74's preservation claim to its accepted release; later
        # authorized RA-006 corrections do not rewrite that historical claim.
        files, _ = DISTRIBUTION.snapshot("80a088500d3944ad9b2391a56b16b949507a0070")
        self.assertEqual(current[DISTRIBUTION.HANDOFF], files[DISTRIBUTION.HANDOFF])
        accepted, _ = DISTRIBUTION.snapshot("1121fc8966a2c7142cc0d6067eff0cf1d15e9cd9")
        for name, before in accepted.items():
            if not name.startswith("vibevm/vibespecs/protocols/"):
                continue
            with self.subTest(protocol=name):
                if name != DISTRIBUTION.HANDOFF:
                    self.assertEqual(files[name], before)
                else:
                    # Only TH-029 changes; retain TH-026 closure guidance and
                    # all existing rule addresses/paragraphs before this rule.
                    anchor = b'<a id="TH-029"></a>'
                    self.assertEqual(files[name].split(anchor)[0], before.split(anchor)[0])
                    self.assertNotEqual(files[name].split(anchor)[1], before.split(anchor)[1])
        self.assertEqual(set(name for name in files if name.startswith("vibevm/vibespecs/protocols/")),
                         set(name for name in accepted if name.startswith("vibevm/vibespecs/protocols/")))

    def test_rule_links_survive_paragraph_and_section_insertion(self):
        files = self.current_export()
        changed = dict(files)
        changed[DISTRIBUTION.HANDOFF] = files[DISTRIBUTION.HANDOFF].replace(
            b'<a id="TH-006"></a>', b'## Additional explanatory section\n\nExplanation.\n\n<a id="TH-006"></a>')
        # Rule lookup follows the explicit ID, not the generated heading slug or order.
        changed["README.md"] += b'\n[Execution cycle](vibevm/vibespecs/protocols/task-handoff.md#TH-006)\n'
        DISTRIBUTION.validate_payload(changed, files["LICENSE"])

    def test_pr_readiness_rule_keeps_prior_addresses_and_its_lifecycle_owner(self):
        files = self.current_export()
        # The prior candidate commit need not survive squash integration. Keep
        # its structural contract in-tree instead of looking up a PR-only object.
        previous = json.loads((REPOSITORY / "scripts/fixtures/task-handoff-before-th-028.json")
                              .read_text(encoding="utf-8"))
        anchors = lambda value: set(re.findall(rb'<a id="(TH-[0-9]{3})"></a>', value))
        self.assertEqual(anchors(files[DISTRIBUTION.HANDOFF]),
                         {value.encode() for value in previous["anchors"]} | {b"TH-028", b"TH-029"})
        for heading in previous["headings"]:
            self.assertIn(heading.encode(), files[DISTRIBUTION.HANDOFF])
        owners = [name for name, content in files.items() if b'<a id="TH-028"></a>' in content]
        self.assertEqual(owners, [DISTRIBUTION.HANDOFF])
        self.assertIn(b"#TH-028", files[DISTRIBUTION.CHANGELOG])
        self.assertIn(b"#TH-028", files["README.md"])
        # Product commands stay in the producer binding, outside the passive flow.
        self.assertNotIn(b"gh pr ready", files[DISTRIBUTION.HANDOFF])

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="governance-distribution-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.source = self.directory / "source"
        self.source.mkdir()
        self.package = self.source / DISTRIBUTION.PACKAGE
        # Keep historical negative fixtures truthful instead of relabelling newer assets 2.2.0.
        baseline, _ = DISTRIBUTION.snapshot("15e8191435a126e54b4d1739a73fab112e01c081")
        for name, data in baseline.items():
            if name != DISTRIBUTION.RECEIPT:
                target = self.package / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        shutil.copyfile(REPOSITORY / "LICENSE", self.source / "LICENSE")
        manifest_path = self.package / "vibe.toml"
        authored = tomllib.loads(manifest_path.read_text())["package"]["version"]
        manifest_path.write_text(manifest_path.read_text().replace('version = "' + authored + '"', 'version = "2.2.0"'))
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
            '{version = "=2.2.0", git = "file:///disposable/distribution.git", tag = "v2.2.0"}\n')
        (consumer / "vibe.lock").write_text(
            '[meta]\nschema_version = 7\n\n[[package]]\ngroup = "org.jresearch.ai"\nname = "development-governance"\n'
            'version = "2.2.0"\nsource_kind = "git"\n'
            'source_url = "file:///disposable/distribution.git"\nsource_ref = "v2.2.0"\n'
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
        expected = {name: data for name, data in expected.items() if name not in DISTRIBUTION.SOURCE_ARTIFACTS}
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

    def test_historical_22_flow_has_seven_protocols_no_native_skill_and_is_frozen(self):
        manifest = tomllib.loads((self.package / "vibe.toml").read_text())
        self.assertIs(manifest["package"]["frozen"], True)
        self.assertNotIn("skill", manifest)
        consumer, _, receipt = self.consumer_fixture("flow")
        self.assertFalse((consumer / ".agents/skills").exists())
        self.assertIn(DISTRIBUTION.PROTOCOL, receipt["sha256"])
        self.assertIn(DISTRIBUTION.VERSIONING, receipt["sha256"])
        self.assertIn(DISTRIBUTION.AUTHORITY, receipt["sha256"])
        self.assertIn(DISTRIBUTION.HANDOFF, receipt["sha256"])
        self.assertIn(DISTRIBUTION.SELF_ADOPTION, receipt["sha256"])
        self.assertIn(DISTRIBUTION.REPOSITORY_GOVERNANCE, receipt["sha256"])
        self.assertIn(DISTRIBUTION.INDEPENDENT_REVIEW, receipt["sha256"])

    def test_accepted_historical_payload_shapes_remain_exportable(self):
        # The disposable source has no accepted objects; select the real history.
        DISTRIBUTION.ROOT = REPOSITORY
        for revision, version, count in (
                ("3fa243b83a630ccd4973114e5cad12e1351d1558", "0.1.0", 1),
                ("901186bdd1aabc9b7f1094eeb2cc294f96b688f7", "1.0.0", 2),
                ("129d452ddfa6b9ac1030ccc7803994793467ab2d", "1.1.0", 3),
                ("1b97f0aadcc769c04415d8f4855098cee35b9f3a", "2.0.0", 5),
                ("c3fbc8c2d10982889bea526161f810902def4289", "2.1.0", 6),
                ("15e8191435a126e54b4d1739a73fab112e01c081", "2.2.0", 7),
                ("bff65a38f61e7fc618ef86260a291637bf3477d1", "2.3.0", 7),
                ("9bd05c89f15e6c83a3d84f68368d7a8ef50f3119", "2.4.0", 8),
                ("88a95f7604b2d81d7a3dd3f76f095beddb71bdab", "2.5.0", 9)):
            with self.subTest(version=version):
                files, receipt = DISTRIBUTION.snapshot(revision)
                self.assertEqual(receipt["version"], version)
                self.assertEqual(sum(name.startswith("vibevm/vibespecs/protocols/")
                                     for name in files), count)
                self.assertEqual(DISTRIBUTION.AUTHORITY in files, count >= 3)
                self.assertEqual(DISTRIBUTION.HANDOFF in files, count >= 4)
                self.assertEqual(DISTRIBUTION.REPOSITORY_GOVERNANCE in files, count >= 6)
                self.assertEqual(DISTRIBUTION.INDEPENDENT_REVIEW in files, count >= 7)
                self.assertEqual("tools/chatgpt/project.py" in files, version in ("2.3.0", "2.4.0", "2.5.0"))
                self.assertEqual(DISTRIBUTION.CONTRACT_MAINTENANCE in files, count >= 8)
                self.assertEqual(DISTRIBUTION.CONTEXT_LOADING in files, count >= 9)
                self.assertNotIn(DISTRIBUTION.ONBOARDING, files)

    def test_new_review_topic_cannot_reuse_accepted_six_topic_version(self):
        manifest = self.package / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('version = "2.2.0"', 'version = "2.1.0"'))
        self.rejected_source()

    def test_optional_chatgpt_assets_require_new_whole_package_version(self):
        for name in ("project.py", "base.md", "README.md"):
            target = self.package / "tools/chatgpt" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPOSITORY / DISTRIBUTION.PACKAGE / "tools/chatgpt" / name, target)
        self.rejected_source()  # Frozen 2.2.0 cannot acquire new maintenance files.
        manifest = self.package / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('version = "2.2.0"', 'version = "2.3.0"'))
        files, receipt = DISTRIBUTION.snapshot(self.commit())
        self.assertEqual(receipt["version"], "2.3.0")
        self.assertIn("tools/chatgpt/project.py", files)
        self.assertNotIn("hooks", tomllib.loads(files["vibe.toml"].decode()))

    def accepted_23_fixture(self):
        # New-topic tests start from genuine accepted 2.3 bytes, not a relabelled current package.
        DISTRIBUTION.ROOT = REPOSITORY
        try:
            files, _ = DISTRIBUTION.snapshot("bff65a38f61e7fc618ef86260a291637bf3477d1")
        finally:
            DISTRIBUTION.ROOT = self.source
        for name, data in files.items():
            if name != DISTRIBUTION.RECEIPT:
                target = self.package / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                target.chmod(0o644)
        self.revision = self.commit()
        return self.package / DISTRIBUTION.CONTRACT_MAINTENANCE

    def test_contract_maintenance_requires_new_whole_package_version(self):
        protocol = self.accepted_23_fixture()
        shutil.copyfile(REPOSITORY / DISTRIBUTION.PACKAGE / DISTRIBUTION.CONTRACT_MAINTENANCE,
                        protocol)
        protocol.chmod(0o644)
        self.rejected_source()  # Frozen accepted 2.3 cannot acquire the eighth protocol.
        manifest = self.package / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('version = "2.3.0"', 'version = "2.4.0"'))
        destination = self.directory / "contract-flow"
        receipt = DISTRIBUTION.prepare(self.commit(), destination)
        files = self.payload(destination)
        self.assertEqual(receipt["version"], "2.4.0")
        self.assertEqual(files[DISTRIBUTION.CONTRACT_MAINTENANCE], protocol.read_bytes())
        self.assertEqual(sum(name.startswith("vibevm/vibespecs/protocols/") for name in files), 8)
        self.assertEqual({name for name in files if name.startswith("tools/")},
                         {"tools/chatgpt/project.py", "tools/chatgpt/base.md", "tools/chatgpt/README.md"})
        metadata = tomllib.loads(files["vibe.toml"].decode())
        self.assertIs(metadata["package"]["frozen"], True)
        self.assertEqual(set(metadata), {"package", "boot_snippet"})

    def test_contract_maintenance_missing_empty_or_escaping_payload_is_rejected(self):
        protocol = self.accepted_23_fixture()
        shutil.copyfile(REPOSITORY / DISTRIBUTION.PACKAGE / DISTRIBUTION.CONTRACT_MAINTENANCE,
                        protocol)
        protocol.chmod(0o644)
        original = protocol.read_bytes()
        manifest = self.package / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('version = "2.3.0"', 'version = "2.4.0"'))
        DISTRIBUTION.snapshot(self.commit())
        protocol.unlink()
        self.rejected_source()
        for invalid in (b"", b" \n", b"\xff\xfe",
                        original + b"\n[Escape](../../../../README.md)\n",
                        original + b"\n[Encoded](%2e%2e/%2e%2e/%2e%2e/%2e%2e/README.md)\n"):
            with self.subTest(data=invalid[-80:]):
                protocol.write_bytes(invalid)
                protocol.chmod(0o644)
                self.rejected_source()

    def accepted_24_fixture(self):
        # Retain genuine accepted eight-topic bytes when testing the next addition.
        DISTRIBUTION.ROOT = REPOSITORY
        try:
            files, _ = DISTRIBUTION.snapshot("9bd05c89f15e6c83a3d84f68368d7a8ef50f3119")
        finally:
            DISTRIBUTION.ROOT = self.source
        for name, data in files.items():
            if name != DISTRIBUTION.RECEIPT:
                target = self.package / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                target.chmod(0o644)
        self.revision = self.commit()
        return self.package / DISTRIBUTION.CONTEXT_LOADING

    def test_current_flow_exports_complete_protocol_set(self):
        # Exercise the actual committed candidate, not a relabelled older payload.
        DISTRIBUTION.ROOT = REPOSITORY
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY).decode().strip()
        destination = self.directory / "current-context-flow"
        receipt = DISTRIBUTION.prepare(revision, destination)
        files = self.payload(destination)
        source_version = tomllib.loads((REPOSITORY / DISTRIBUTION.PACKAGE /
                                       "vibe.toml").read_text())["package"]["version"]
        self.assertEqual(receipt["version"], source_version)
        self.assertGreaterEqual(tuple(map(int, source_version.split("."))), (2, 5, 0))
        expected = 10 if tuple(map(int, source_version.split("."))) >= (5, 2, 0) else 9
        self.assertEqual(sum(name.startswith("vibevm/vibespecs/protocols/") for name in files), expected)
        self.assertEqual(files[DISTRIBUTION.CONTEXT_LOADING],
                         (REPOSITORY / DISTRIBUTION.PACKAGE / DISTRIBUTION.CONTEXT_LOADING).read_bytes())
        self.assertEqual({name for name in files if name.startswith("tools/")},
                         {"tools/chatgpt/project.py", "tools/chatgpt/base.md", "tools/chatgpt/README.md"})
        metadata = tomllib.loads(files["vibe.toml"].decode())
        self.assertIs(metadata["package"]["frozen"], True)
        self.assertEqual(set(metadata), {"package", "boot_snippet"})

    def test_small_improvement_addition_preserves_existing_protocols_and_requires_complete_export(self):
        files = self.current_export()
        accepted, _ = DISTRIBUTION.snapshot("2361868c41a916871d687aa8eea8f14573e2c82e")
        historical, _ = DISTRIBUTION.snapshot("1121fc8966a2c7142cc0d6067eff0cf1d15e9cd9")
        # Preserve the accepted SI addition's unchanged earlier rules. Current
        # TH-029 is deliberately revised by Task 74 and qualified separately.
        for name, content in accepted.items():
            if name.startswith("vibevm/vibespecs/protocols/"):
                with self.subTest(preserved=name):
                    self.assertEqual(historical[name], content)
        new_files = (DISTRIBUTION.SMALL_IMPROVEMENTS, DISTRIBUTION.SMALL_IMPROVEMENTS_GUIDE)
        for name in new_files:
            for data in (None, b"", b"\xff"):
                with self.subTest(path=name, corruption=data):
                    changed = dict(files)
                    if data is None:
                        del changed[name]
                    else:
                        changed[name] = data
                    with self.assertRaises((ValueError, UnicodeDecodeError)):
                        DISTRIBUTION.validate_payload(changed, files["LICENSE"])
        # A new file cannot be retrofitted into an already frozen version.
        accepted.pop(DISTRIBUTION.RECEIPT)
        accepted.update({name: files[name] for name in new_files})
        with self.assertRaisesRegex(ValueError, "file set differs"):
            DISTRIBUTION.validate_payload(accepted, accepted["LICENSE"])
        # Incorrect SI IDs and boot routes must fail through normal validation.
        changed = dict(files)
        changed[DISTRIBUTION.SMALL_IMPROVEMENTS] = files[DISTRIBUTION.SMALL_IMPROVEMENTS].replace(b'SI-001', b'TH-001')
        with self.assertRaises(ValueError):
            DISTRIBUTION.validate_payload(changed, files["LICENSE"])
        changed = dict(files)
        boot = "vibevm/vibespecs/boot/development-governance.md"
        changed[boot] = files[boot].replace(b'../protocols/small-improvements.md', b'../protocols/absent.md')
        with self.assertRaisesRegex(ValueError, "missing local reference"):
            DISTRIBUTION.validate_payload(changed, files["LICENSE"])

    def test_context_loading_requires_new_whole_package_version(self):
        protocol = self.accepted_24_fixture()
        shutil.copyfile(REPOSITORY / DISTRIBUTION.PACKAGE / DISTRIBUTION.CONTEXT_LOADING,
                        protocol)
        protocol.chmod(0o644)
        self.rejected_source()  # Frozen accepted 2.4 cannot acquire the ninth protocol.
        manifest = self.package / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('version = "2.4.0"', 'version = "2.5.0"'))
        destination = self.directory / "context-flow"
        receipt = DISTRIBUTION.prepare(self.commit(), destination)
        files = self.payload(destination)
        self.assertEqual(receipt["version"], "2.5.0")
        self.assertEqual(files[DISTRIBUTION.CONTEXT_LOADING], protocol.read_bytes())
        self.assertEqual(sum(name.startswith("vibevm/vibespecs/protocols/") for name in files), 9)

    def test_context_loading_missing_empty_or_escaping_payload_is_rejected(self):
        protocol = self.accepted_24_fixture()
        shutil.copyfile(REPOSITORY / DISTRIBUTION.PACKAGE / DISTRIBUTION.CONTEXT_LOADING,
                        protocol)
        protocol.chmod(0o644)
        original = protocol.read_bytes()
        manifest = self.package / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('version = "2.4.0"', 'version = "2.5.0"'))
        DISTRIBUTION.snapshot(self.commit())
        protocol.unlink()
        self.rejected_source()
        for invalid in (b"", b" \n", b"\xff\xfe",
                        original + b"\n[Escape](../../../../README.md)\n",
                        original + b"\n[Encoded](%2e%2e/%2e%2e/%2e%2e/%2e%2e/README.md)\n"):
            with self.subTest(data=invalid[-80:]):
                protocol.write_bytes(invalid)
                protocol.chmod(0o644)
                self.rejected_source()

    def test_historical_26_onboarding_export_preserves_25_protocols_and_client_tools(self):
        # This frozen 2.6 assertion must not constrain future protocol revisions.
        DISTRIBUTION.ROOT = REPOSITORY
        revision = "f67a29aeac6defef7220a169962bac611b6f8c79"
        files, receipt = DISTRIBUTION.snapshot(revision)
        accepted, _ = DISTRIBUTION.snapshot("88a95f7604b2d81d7a3dd3f76f095beddb71bdab")
        self.assertEqual(receipt["version"], "2.6.0")
        self.assertEqual({name: data for name, data in files.items()
                          if name.startswith(("vibevm/vibespecs/protocols/", "tools/"))},
                         {name: data for name, data in accepted.items()
                          if name.startswith(("vibevm/vibespecs/protocols/", "tools/"))})
        self.assertEqual({name for name in files if name.startswith("vibevm/vibespecs/guides/")},
                         {DISTRIBUTION.ONBOARDING, DISTRIBUTION.ONBOARDING_EXAMPLES})
        # The complete package works outside the producer's README/instructions.
        destination = self.directory / "onboarding-export"
        DISTRIBUTION.prepare(revision, destination)
        self.assertEqual((destination / DISTRIBUTION.ONBOARDING).read_bytes(),
                         files[DISTRIBUTION.ONBOARDING])

    def test_onboarding_requires_new_version_and_complete_contained_guides(self):
        DISTRIBUTION.ROOT = REPOSITORY
        files, _ = DISTRIBUTION.snapshot("88a95f7604b2d81d7a3dd3f76f095beddb71bdab")
        files.pop(DISTRIBUTION.RECEIPT)
        for name in (DISTRIBUTION.ONBOARDING, DISTRIBUTION.ONBOARDING_EXAMPLES):
            files[name] = (REPOSITORY / DISTRIBUTION.PACKAGE / name).read_bytes()
        with self.assertRaises(ValueError):
            DISTRIBUTION.validate_payload(files, files["LICENSE"])
        files["vibe.toml"] = files["vibe.toml"].replace(b'"2.5.0"', b'"2.6.0"')
        DISTRIBUTION.validate_payload(files, files["LICENSE"])
        for name in (DISTRIBUTION.ONBOARDING, DISTRIBUTION.ONBOARDING_EXAMPLES):
            original = files[name]
            del files[name]
            with self.assertRaises(ValueError):
                DISTRIBUTION.validate_payload(files, files["LICENSE"])
            for invalid in (b"", b" \n", b"\xff\xfe",
                            original + b"\n[Missing](missing.md)\n",
                            original + b"\n[Escape](../../../../README.md)\n",
                            original + b"\n[Encoded](%2e%2e/%2e%2e/%2e%2e/%2e%2e/README.md)\n"):
                with self.subTest(guide=name, data=invalid[-80:]):
                    files[name] = invalid
                    with self.assertRaises(ValueError):
                        DISTRIBUTION.validate_payload(files, files["LICENSE"])
            files[name] = original

    def test_current_engineering_methods_export_and_27_preservation(self):
        DISTRIBUTION.ROOT = REPOSITORY
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY).decode().strip()
        files, receipt = DISTRIBUTION.snapshot(revision)
        accepted, _ = DISTRIBUTION.snapshot("f67a29aeac6defef7220a169962bac611b6f8c79")
        self.assertGreaterEqual(tuple(map(int, receipt["version"].split("."))), (2, 7, 0))
        if receipt["version"] == "2.7.0":
            # Task 41 preserves these bytes; later versions may revise them.
            self.assertEqual({name: data for name, data in files.items()
                              if name.startswith(("vibevm/vibespecs/protocols/", "tools/"))},
                             {name: data for name, data in accepted.items()
                              if name.startswith(("vibevm/vibespecs/protocols/", "tools/"))})
            self.assertEqual(sum(name.startswith("vibevm/vibespecs/protocols/")
                                 for name in files), 9)
        expected_guides = {DISTRIBUTION.ONBOARDING, DISTRIBUTION.ONBOARDING_EXAMPLES,
                           DISTRIBUTION.ENGINEERING_METHODS}
        if tuple(map(int, receipt["version"].split("."))) >= (5, 2, 0):
            expected_guides.add(DISTRIBUTION.SMALL_IMPROVEMENTS_GUIDE)
        self.assertEqual({name for name in files if name.startswith("vibevm/vibespecs/guides/")},
                         expected_guides)
        destination = self.directory / "engineering-methods-export"
        DISTRIBUTION.prepare(revision, destination)
        self.assertEqual((destination / DISTRIBUTION.ENGINEERING_METHODS).read_bytes(),
                         files[DISTRIBUTION.ENGINEERING_METHODS])

    def test_engineering_methods_requires_new_version_and_complete_contained_guide(self):
        DISTRIBUTION.ROOT = REPOSITORY
        files, _ = DISTRIBUTION.snapshot("f67a29aeac6defef7220a169962bac611b6f8c79")
        files.pop(DISTRIBUTION.RECEIPT)
        name = DISTRIBUTION.ENGINEERING_METHODS
        original = (REPOSITORY / DISTRIBUTION.PACKAGE / name).read_bytes()
        files[name] = original
        with self.assertRaises(ValueError):
            DISTRIBUTION.validate_payload(files, files["LICENSE"])
        files["vibe.toml"] = files["vibe.toml"].replace(b'"2.6.0"', b'"2.7.0"')
        DISTRIBUTION.validate_payload(files, files["LICENSE"])
        del files[name]
        with self.assertRaises(ValueError):
            DISTRIBUTION.validate_payload(files, files["LICENSE"])
        for invalid in (b"", b" \n", b"\xff\xfe",
                        original + b"\n[Missing](missing.md)\n",
                        original + b"\n[Escape](../../../../README.md)\n",
                        original + b"\n[Encoded](%2e%2e/%2e%2e/%2e%2e/%2e%2e/README.md)\n"):
            with self.subTest(data=invalid[-80:]):
                files[name] = invalid
                with self.assertRaises(ValueError):
                    DISTRIBUTION.validate_payload(files, files["LICENSE"])

    def test_any_skill_declaration_or_dependency_is_rejected(self):
        manifest = self.package / "vibe.toml"
        original = manifest.read_text()
        for extra in ('skill = []\n', '[[skill]]\nname = "proportional-controls"\n',
                      '[requires.packages]\n"unapproved/package" = "2.2.0"\n',
                      '[tools]\ncommand = "unapproved"\n', '[hooks]\ncommand = "unapproved"\n',
                      '[mcp]\ncommand = "unapproved"\n'):
            with self.subTest(declaration=extra):
                # An empty skill array must also be a top-level declaration.
                manifest.write_text(extra + original if extra.startswith("skill =") else original + "\n" + extra)
                self.rejected_source()

    def test_protocol_must_be_nonempty_utf8(self):
        for name in (DISTRIBUTION.PROTOCOL, DISTRIBUTION.VERSIONING,
                     DISTRIBUTION.AUTHORITY, DISTRIBUTION.HANDOFF,
                     DISTRIBUTION.SELF_ADOPTION, DISTRIBUTION.REPOSITORY_GOVERNANCE,
                     DISTRIBUTION.INDEPENDENT_REVIEW):
            path = self.package / name
            original = path.read_bytes()
            for data in (b"", b" \n", b"\xff\xfe"):
                with self.subTest(protocol=name, data=data):
                    path.write_bytes(data)
                    self.rejected_source()
            path.write_bytes(original)

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

    def test_installed_handoff_and_review_cannot_be_changed_missing_or_symlinked(self):
        for name in (DISTRIBUTION.HANDOFF, DISTRIBUTION.INDEPENDENT_REVIEW):
            for corruption in ("changed", "missing", "symlink"):
                with self.subTest(protocol=name, corruption=corruption):
                    consumer, slot, _ = self.consumer_fixture(Path(name).stem + "-" + corruption)
                    protocol = slot / name
                    if corruption == "changed":
                        protocol.write_bytes(protocol.read_bytes() + b"Altered\n")
                    else:
                        protocol.unlink()
                        if corruption == "symlink":
                            protocol.symlink_to(self.package / name)
                    with self.assertRaises(ValueError):
                        DISTRIBUTION.verify_consumer(self.revision, consumer)

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
            (lock_path, original_lock.replace('source_ref = "v2.2.0"', 'source_ref = "v2.2.1"')),
            (lock_path, original_lock.replace('file:///disposable/distribution.git', 'file:///other.git')),
            (lock_path, original_lock.replace('group = "org.jresearch.ai"',
                                             'group = "org.jresearch.governance"')),
            (lock_path, original_lock.replace('name = "development-governance"',
                                             'name = "proportional-controls"')),
            (manifest_path, original_manifest.replace(COORDINATE,
                                                     "org.jresearch.governance/proportional-controls")),
            (manifest_path, original_manifest.replace('version = "=2.2.0"', 'version = "*"')),
            (manifest_path, original_manifest.replace('tag = "v2.2.0"',
                                                     'tag = "v2.2.0", rev = "' + "a" * 40 + '"')),
            (manifest_path, original_manifest.replace('tag = "v2.2.0"', 'rev = "abcdef"')),
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
                              (b'version = "2.2.0"', b'version = "invalid"'),
                              (b'version = "2.2.0"', b'version = "1.1.0"'),
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
        for name in (DISTRIBUTION.PROTOCOL, DISTRIBUTION.VERSIONING,
                     DISTRIBUTION.AUTHORITY, DISTRIBUTION.HANDOFF,
                     DISTRIBUTION.SELF_ADOPTION, DISTRIBUTION.REPOSITORY_GOVERNANCE,
                     DISTRIBUTION.INDEPENDENT_REVIEW):
            path = self.package / name
            original = path.read_bytes()
            with self.subTest(protocol=name):
                path.unlink()
                self.rejected_source()
                path.write_bytes(original)

    def test_absent_source_package_is_rejected(self):
        shutil.rmtree(self.package)
        self.rejected_source()




if __name__ == "__main__":
    unittest.main(verbosity=2)
