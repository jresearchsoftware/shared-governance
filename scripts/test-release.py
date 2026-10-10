#!/usr/bin/env python3
"""Focused release regressions; optional real pinned-publisher integration fixtures."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release", ROOT / "scripts/package-release.py")
RELEASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELEASE)
VIBE = None


class ReleaseFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="release-test-")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.source = self.directory / "source"
        self.source.mkdir()
        self.env = dict(os.environ)
        self.env.update(GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        self.git("init", "-q", "-b", "main")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.filemode", "false")
        self.git("config", "core.hooksPath", str(self.directory / "no-hooks"))
        self.git("config", "maintenance.auto", "false")
        self.git("config", "gc.auto", "0")
        preparation = RELEASE.PREPARATION
        historical = preparation.HISTORICAL_PACKAGE
        shutil.copytree(ROOT / historical, self.source / historical)
        shutil.copyfile(ROOT / "LICENSE", self.source / "LICENSE")
        (self.source / "vibe.toml").write_text('[workspace]\nmembers = ["' + historical + '"]\n')
        self.base = self.commit()
        shutil.copytree(ROOT / preparation.PACKAGE, self.source / preparation.PACKAGE)
        (self.source / "vibe.toml").write_text('[workspace]\nmembers = ["' + preparation.PACKAGE + '"]\n')
        shutil.copytree(ROOT / "toolchain", self.source / "toolchain")
        self.revision = self.commit()
        self.addCleanup(setattr, preparation, "ROOT", preparation.ROOT)
        self.addCleanup(setattr, RELEASE, "ROOT", RELEASE.ROOT)
        preparation.ROOT = self.source
        RELEASE.ROOT = self.source

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *args], cwd=cwd or self.source,
                                       env=self.env, stderr=subprocess.PIPE).decode().strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Disposable source")
        return self.git("rev-parse", "HEAD")


class ReleaseTests(ReleaseFixture):
    def test_stable_path_and_major_transition_from_frozen_history(self):
        result = RELEASE.transition(self.base, self.revision, "major")
        self.assertTrue(result["changed"])
        self.assertEqual((result["before"], result["version"]), ("0.1.0", "1.0.0"))
        for revision, source_path in ((self.base, RELEASE.PREPARATION.HISTORICAL_PACKAGE),
                                      (self.revision, RELEASE.PREPARATION.PACKAGE)):
            self.assertEqual(RELEASE.PREPARATION.snapshot(revision)[1]["source_path"], source_path)

    def test_source_only_change_skips_release(self):
        (self.source / "notes.md").write_text("Research outside the package.\n")
        revision = self.commit()
        self.assertFalse(RELEASE.transition(self.revision, revision)["changed"])
        with patch.object(RELEASE, "tag_exists", side_effect=AssertionError("no remote probe")):
            self.assertEqual(RELEASE.publish(revision, Path("absent"), accepted_main="main")["publication"],
                             "NO_PACKAGE_CHANGE")

    def test_same_version_content_change_is_rejected(self):
        readme = self.source / RELEASE.PREPARATION.PACKAGE / "README.md"
        readme.write_text(readme.read_text() + "\nChanged contract.\n")
        with self.assertRaisesRegex(ValueError, "without a new"):
            RELEASE.transition(self.revision, self.commit(), "patch")

    def test_stale_parallel_bump_is_recomputed(self):
        self.assertEqual(RELEASE.bump("1.95.0", "major"), "2.0.0")
        self.assertEqual(RELEASE.bump("2.0.0", "minor"), "2.1.0")
        self.assertEqual(RELEASE.bump("2.0.0", "patch"), "2.0.1")
        with self.assertRaisesRegex(ValueError, "recompute"):
            RELEASE.transition(self.base, self.revision, "patch")

    def test_unaccepted_and_side_branch_heads_are_rejected(self):
        (self.source / "side.md").write_text("Side branch.\n")
        side = self.commit()
        with self.assertRaisesRegex(ValueError, "first-parent"):
            RELEASE.accepted_transition(side, self.revision)
        with self.assertRaises(ValueError):
            RELEASE.accepted_transition("main", "main")

    def test_existing_tag_never_invokes_native_publisher(self):
        with patch.object(RELEASE, "tag_exists", return_value=True), patch.object(
                RELEASE.subprocess, "run", side_effect=AssertionError("publisher called")):
            result = RELEASE.publish(self.revision, Path("absent"), accepted_main="main")
        self.assertEqual(result["publication"], "ALREADY_PUBLISHED")

    def test_missing_production_credential_is_visible_and_retryable(self):
        with patch.object(RELEASE, "tag_exists", return_value=False), patch.dict(os.environ, {"RELEASE_TOKEN": ""}):
            with self.assertRaisesRegex(ValueError, "PUBLISH_TOKEN"):
                RELEASE.publish(self.revision, Path("absent"), accepted_main="main")

    def test_invalid_pinned_binary_cannot_publish(self):
        binary = self.directory / "vibe"
        binary.write_bytes(b"unqualified")
        with patch.object(RELEASE, "tag_exists", return_value=False):
            with self.assertRaisesRegex(ValueError, "pinned"):
                RELEASE.publish(self.revision, binary, "file:///fixture", "main")


@unittest.skipUnless(VIBE, "pass --vibe for one-time native publisher integration")
class NativeReleaseTests(ReleaseFixture):
    def remote(self):
        remote = self.directory / "distribution.git"
        self.git("init", "--bare", "-b", "main", str(remote))
        return remote

    def publish(self, remote, callback=None):
        with patch.dict(os.environ, self.env):
            return RELEASE.publish(self.revision, VIBE, remote.as_uri(), "main", callback)

    def test_real_publish_repeat_and_same_sha_retry(self):
        remote = self.remote()
        result = self.publish(remote)
        self.assertEqual(result["publication"], "PUBLISHED")
        refs = self.git("for-each-ref", cwd=remote)
        self.assertEqual(self.publish(remote)["publication"], "ALREADY_PUBLISHED")
        self.assertEqual(self.git("for-each-ref", cwd=remote), refs)
        cold = self.directory / "cold"
        cold.mkdir()
        (cold / "vibe.toml").write_text(
            '[project]\nname="cold"\nversion="0.0.0"\nspec_format="mixed"\n'
            '[requires.packages]\n"org.jresearch.ai/development-governance" = '
            '{version="=1.0.0",git="' + remote.as_uri() + '",tag="v1.0.0",auth="none"}\n')
        (cold / "AGENTS.md").write_text("Existing local version policy stays authoritative.\n")
        env = {**self.env, "VIBE_SETTINGS": str(self.directory / "settings"),
               "VIBEVM_USER_CONFIG": str(self.directory / "settings/config.toml")}
        subprocess.run([str(VIBE), "--json", "install", "--path", str(cold),
                        "--no-default-registry", "--assume-yes"], env=env, check=True, capture_output=True)
        RELEASE.PREPARATION.verify_consumer(self.revision, cold)
        self.assertIn("Existing local version policy", (cold / "AGENTS.md").read_text())
        boot = cold / RELEASE.PREPARATION.slot("1.0.0") / "vibevm/vibespecs/boot/development-governance.md"
        self.assertIn("does not activate", boot.read_text())
        # Newly adopting consumer selects a human-owned route, with no flags/service.
        with (cold / "AGENTS.md").open("a") as output:
            output.write("\nAdopt package-versioning for our package lifecycle decisions.\n")
        subprocess.run([str(VIBE), "--json", "install", "--path", str(cold),
                        "--no-default-registry", "--assume-yes"], env=env, check=True, capture_output=True)
        self.assertIn("Adopt package-versioning", (cold / "AGENTS.md").read_text())

    def test_concurrent_tag_cannot_be_replaced_or_change_main(self):
        remote = self.remote()
        def competitor(staging, tag):
            # Publish the frozen historical version as a distinct competing tree.
            payload = self.directory / "historical-payload"
            RELEASE.PREPARATION.prepare(self.base, payload)
            env = {**self.env, "VIBE_SETTINGS": str(self.directory / "race-settings"),
                   "VIBEVM_USER_CONFIG": str(self.directory / "race-settings/config.toml")}
            subprocess.run([str(VIBE), "registry", "publish", str(payload), "--repo-url", remote.as_uri()],
                           env=env, check=True, capture_output=True)
            self.git("tag", tag, "main", cwd=remote)
            self.retained = self.git("for-each-ref", cwd=remote)
        with self.assertRaises(subprocess.CalledProcessError):
            self.publish(remote, competitor)
        self.assertEqual(self.git("for-each-ref", cwd=remote), self.retained)
        self.assertEqual(self.publish(remote)["publication"], "ALREADY_PUBLISHED")
        self.assertEqual(self.git("for-each-ref", cwd=remote), self.retained)

    def test_failure_with_absent_tag_can_retry_same_accepted_sha(self):
        remote = self.remote()
        def fail(staging, tag):
            raise ValueError("disposable transport failure")
        with self.assertRaises(ValueError):
            self.publish(remote, fail)
        self.assertFalse(self.git("for-each-ref", cwd=remote))
        self.assertEqual(self.publish(remote)["publication"], "PUBLISHED")

    def test_new_lower_version_is_valid_after_higher_tag(self):
        remote = self.remote()
        payload = self.directory / "higher"
        RELEASE.PREPARATION.prepare(self.revision, payload)
        manifest = payload / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('version = "1.0.0"', 'version = "2.0.0"'))
        env = {**self.env, "VIBE_SETTINGS": str(self.directory / "higher-settings"),
               "VIBEVM_USER_CONFIG": str(self.directory / "higher-settings/config.toml")}
        subprocess.run([str(VIBE), "registry", "publish", str(payload), "--repo-url", remote.as_uri()],
                       env=env, check=True, capture_output=True)
        higher = self.git("rev-parse", "v2.0.0", cwd=remote)
        self.assertEqual(self.publish(remote)["publication"], "PUBLISHED")
        self.assertEqual(self.git("rev-parse", "v2.0.0", cwd=remote), higher)


@unittest.skipUnless(VIBE, "pass --vibe for one-time resolver integration")
class NativeDependencyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="dependency-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.registry = self.root / "registry"
        self.consumer = self.root / "consumer"
        self.consumer.mkdir()
        self.env = {**os.environ, "VIBE_SETTINGS": str(self.root / "settings"),
                    "VIBEVM_USER_CONFIG": str(self.root / "settings/config.toml")}

    def package(self, name, version, dependencies=None, frozen=True):
        target = self.registry / "org.fixture" / name / ("v" + version)
        target.mkdir(parents=True)
        text = (f'[package]\ngroup="org.fixture"\nname="{name}"\nversion="{version}"\n'
                'kind="flow"\nformat="simple"\nepoch=1\npublish=false\n'
                f'frozen={str(frozen).lower()}\nlicense="MIT"\n')
        if dependencies:
            text += '\n[requires.packages]\n' + ''.join(
                f'"org.fixture/{key}" = "{value}"\n' for key, value in dependencies.items())
        (target / "vibe.toml").write_text(text)

    def project(self, requirements):
        (self.consumer / "vibe.toml").write_text(
            '[project]\nname="fixture"\nversion="0.0.0"\nspec_format="mixed"\n'
            '[requires.packages]\n' + ''.join(
                f'"org.fixture/{key}"="{value}"\n' for key, value in requirements.items()))

    def run_vibe(self, command="install", success=True):
        args = [str(VIBE), "--offline", "--json", command, "--path", str(self.consumer),
                "--registry", str(self.registry), "--no-default-registry", "--assume-yes"]
        if command == "update":
            args.append("--all")
        result = subprocess.run(args, env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def closure(self):
        packages = tomllib.loads((self.consumer / "vibe.lock").read_text())["package"]
        for entry in packages:
            slot = self.consumer / "vibevm/vibedeps" / (entry["group"] + "." + entry["name"]) / entry["version"]
            manifest = tomllib.loads((slot / "vibe.toml").read_text())["package"]
            if not manifest["frozen"] or not entry.get("content_hash"):
                raise ValueError("included transitive snapshot or absent tool hash")
        return {entry["name"]: entry["version"] for entry in packages}

    def test_frozen_transitive_diamond_conflict_and_deliberate_lock_update(self):
        self.package("shared", "1.0.0")
        self.package("shared", "2.0.0")
        self.package("left", "1.0.0", {"shared": "~1.0.0"})
        self.package("right", "1.0.0", {"shared": "=2.0.0"})
        self.project({"left": "=1.0.0", "right": "=1.0.0"})
        self.run_vibe(success=False)
        self.project({"left": "=1.0.0"})
        self.run_vibe()
        self.assertEqual(self.closure(), {"left": "1.0.0", "shared": "1.0.0"})
        before = (self.consumer / "vibe.lock").read_bytes()
        self.package("shared", "1.0.1")
        # Publishing available versions does not edit the consumer's lock.
        self.assertEqual((self.consumer / "vibe.lock").read_bytes(), before)
        self.run_vibe("update")
        self.assertEqual(self.closure()["shared"], "1.0.1")

    def test_included_snapshot_is_detected_but_unused_optional_fixture_is_not_in_closure(self):
        self.package("snapshot", "1.0.0", frozen=False)
        self.package("left", "1.0.0", {"snapshot": "=1.0.0"})
        self.package("unused", "1.0.0", frozen=False)
        self.project({"left": "=1.0.0"})
        self.run_vibe()
        with self.assertRaisesRegex(ValueError, "snapshot"):
            self.closure()
        names = {e["name"] for e in tomllib.loads((self.consumer / "vibe.lock").read_text())["package"]}
        self.assertNotIn("unused", names)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", type=Path)
    args, rest = parser.parse_known_args()
    if args.vibe:
        VIBE = args.vibe.resolve()
        NativeReleaseTests.__unittest_skip__ = False
        NativeDependencyTests.__unittest_skip__ = False
    unittest.main(argv=[__file__, *rest], verbosity=2)
