#!/usr/bin/env python3
"""Focused disposable fixtures. All distribution writes use local bare repos."""
import argparse
import io
import importlib.util
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publisher as P

VIBE = None
CODE_SHA = "a" * 40


class Evidence:
    def __init__(self, binding, revisions):
        self.binding = binding
        self.revisions = revisions
        self.alter_pr = lambda pr: pr
        self.alter_run = lambda run: run

    def get(self, path):
        if path == "":
            return {"id": 123, "full_name": "fixture/private-source"}
        if path.startswith("actions/workflows/"):
            return {"id": 456, "path": ".github/workflows/check.yml"}
        if path.startswith("pulls/"):
            revision = list(self.revisions)[int(path.split("/")[1]) - 1]
            return self.alter_pr({"merged": True, "merge_commit_sha": revision,
                "base": {"ref": "main", "repo": {"id": 123}},
                "merged_by": {"login": "owner"}, "head": {"sha": "b" * 40},
                "html_url": "https://github.com/fixture/private-source/pull/1"})
        raise AssertionError(path)

    def pages(self, path, key=None):
        if path.startswith("commits/"):
            revision = path.split("/")[1]
            return ([{"number": list(self.revisions).index(revision) + 1}]
                    if revision in self.revisions else [])
        revision = path.split("head_sha=")[1].split("&")[0]
        return [self.alter_run({"head_sha": revision, "event": "push", "head_branch": "main",
                 "status": "completed", "conclusion": "success", "workflow_id": 456,
                 "head_repository": {"id": 123}, "repository": {"id": 123},
                 "html_url": "https://github.com/fixture/private-source/actions/runs/1"})]


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="shared-publisher-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.source = self.directory / "source"
        self.source.mkdir()
        self.env = dict(os.environ, GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                        GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid",
                        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_TERMINAL_PROMPT="0")
        self.git("init", "-q", "-b", "main")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")
        self.git("config", "core.hooksPath", str(self.directory / "no-hooks"))
        (self.source / "private-notes.txt").write_text("PRIVATE_SENTINEL_DO_NOT_EXPORT")
        self.baseline = self.commit()
        self.packages = []
        for name in ("landscape-subagents", "landscape-model-guidance"):
            root = "packages/" + name
            self.packages.append({"coordinate": "org.fixture/" + name, "root": root,
                "baseline": self.baseline, "adapter": "tree-v1", "disclosure": "opaque",
                "files": ["vibe.toml", "LICENSE", "README.md"],
                "destination": (self.directory / (name + ".git")).as_uri()})
            target = self.source / root
            target.mkdir(parents=True)
            (target / "vibe.toml").write_text('[package]\ngroup = "org.fixture"\nname = "' + name +
                '"\nversion = "1.0.0"\nkind = "flow"\nfrozen = true\npublish = false\n')
            (target / "README.md").write_text("Approved public guidance.\n")
            (target / "LICENSE").write_text("MIT\nPublic synthetic fixture.\n")
            (target / "private.txt").write_text("PRIVATE_PACKAGE_SENTINEL")
        self.revision = self.commit()
        self.binding = {"schema": 1, "repository": "fixture/private-source", "repository_id": 123,
            "branch": "main", "ci_workflow": ".github/workflows/check.yml",
            "acceptance": "owner-squash-attestation-v1", "authorized_integrators": ["owner"],
            "packages": self.packages}
        self.api = Evidence(self.binding, [self.revision])

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *map(str, args)], cwd=cwd or self.source,
                                       env=self.env, stderr=subprocess.PIPE).decode().strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Disposable source")
        return self.git("rev-parse", "HEAD")

    def change(self, number=0, version="1.0.1"):
        manifest = self.source / self.packages[number]["root"] / "vibe.toml"
        manifest.write_text(re.sub(r'version = "[^"]+"', 'version = "' + version + '"', manifest.read_text()))
        readme = manifest.parent / "README.md"
        readme.write_text(readme.read_text() + "Changed guidance.\n")
        return self.commit()

    def plan(self, revision=None):
        return P.plan(self.source, revision or self.revision, "main", self.binding, self.api, CODE_SHA)

    def remote(self, number):
        destination = self.directory / (self.packages[number]["coordinate"].split("/")[1] + ".git")
        self.git("init", "-q", "--bare", "--initial-branch=main", str(destination))
        return destination


class PlanningTests(Fixture):
    def test_two_independent_initial_versions(self):
        report = self.plan()
        self.assertEqual([row["version"] for row in report["packages"]], ["1.0.0", "1.0.0"])
        self.assertEqual([row["status"] for row in report["packages"]], ["READY", "READY"])
        self.assertEqual(report["packages"][0]["acceptance"][0]["reviewed_head"], "b" * 40)

    def test_a_only_change_leaves_b_noop(self):
        changed = self.change()
        self.api.revisions.append(changed)
        self.assertEqual([row["status"] for row in self.plan(changed)["packages"]],
                         ["READY", "NO_PACKAGE_CHANGE"])

    def test_exact_accepted_baseline_can_be_retried(self):
        for package in self.packages:
            package["baseline"] = self.revision
        self.assertEqual([row["status"] for row in self.plan()["packages"]], ["READY", "READY"])

    def test_factual_direct_main_noop_without_api(self):
        (self.source / "research.txt").write_text("Ordinary direct-main research")
        revision = self.commit()
        with patch.object(self.api, "get", side_effect=AssertionError("no authority check needed")):
            self.assertEqual([row["status"] for row in self.plan(revision)["packages"]],
                             ["NO_PACKAGE_CHANGE", "NO_PACKAGE_CHANGE"])

    def test_receipt_source_sha_alone_is_noop(self):
        package = self.packages[0]
        package["disclosure"] = "public-source"
        before = P.snapshot(self.source, self.revision, package)
        (self.source / "research.txt").write_text("Source only")
        revision = self.commit()
        after = P.snapshot(self.source, revision, package)
        self.assertNotEqual(before[0][P.RECEIPT], after[0][P.RECEIPT])
        self.assertEqual(P.payload(before), P.payload(after))

    def test_direct_main_versioned_change_is_pending(self):
        changed = self.change()
        self.assertEqual(self.plan(changed)["packages"][0]["status"], "AUTHORIZATION_PENDING")

    def test_later_owner_merge_cannot_launder_ineligible_payload(self):
        rejected = self.change()
        accepted = self.change(version="1.0.2")
        self.api.revisions.append(accepted)
        self.assertEqual(self.plan(accepted)["packages"][0]["status"], "AUTHORIZATION_PENDING")
        self.assertNotIn(rejected, self.api.revisions)
        # An explicitly owner-reconciled binding can name this reviewed baseline.
        self.packages[0]["baseline"] = rejected
        self.assertEqual(self.plan(accepted)["packages"][0]["status"], "READY")

    def test_reused_version_is_rejected(self):
        readme = self.source / self.packages[0]["root"] / "README.md"
        readme.write_text("Changed without bump")
        changed = self.commit()
        self.api.revisions.append(changed)
        self.assertIn("without a new version", self.plan(changed)["packages"][0]["reason"])

    def test_unmerged_wrong_integrator_repository_and_sha_are_pending(self):
        for change in (lambda pr: dict(pr, merged=False),
                       lambda pr: dict(pr, merged_by={"login": "stranger"}),
                       lambda pr: dict(pr, merge_commit_sha="c" * 40),
                       lambda pr: dict(pr, base={"ref": "main", "repo": {"id": 999}}),
                       lambda pr: dict(pr, head={"sha": self.revision})):
            with self.subTest(change=change):
                self.api.alter_pr = change
                self.assertEqual(self.plan()["packages"][0]["status"], "AUTHORIZATION_PENDING")

    def test_ci_identity_failures_are_pending(self):
        for values in ({"event": "pull_request"}, {"head_sha": "c" * 40},
                       {"workflow_id": 999}, {"head_branch": "side"},
                       {"conclusion": "failure"}, {"repository": {"id": 999}},
                       {"head_repository": {"id": 999}}):
            with self.subTest(values=values):
                self.api.alter_run = lambda run: dict(run, **values)
                self.assertEqual(self.plan()["packages"][0]["status"], "AUTHORIZATION_PENDING")

    def test_side_branch_and_mutable_source_rejected(self):
        with self.assertRaises(ValueError):
            self.plan("main")
        self.git("switch", "-qc", "side")
        (self.source / "side.txt").write_text("side")
        side = self.commit()
        self.git("switch", "-q", "main")
        with self.assertRaisesRegex(ValueError, "first-parent"):
            self.plan(side)

    def test_private_source_export_only_discloses_approved_bytes(self):
        files, receipt = P.snapshot(self.source, self.revision, self.packages[0])
        self.assertEqual(set(files), {"vibe.toml", "LICENSE", "README.md", P.RECEIPT})
        data = b"".join(files.values())
        for forbidden in (b"PRIVATE", self.revision.encode(), b"packages/", b"private-source"):
            self.assertNotIn(forbidden, data)
        self.assertNotIn("source_revision", receipt)

    def test_frozen_dependencies_and_license_are_adapter_boundaries(self):
        manifest = self.source / self.packages[0]["root"] / "vibe.toml"
        manifest.write_text(manifest.read_text() + '\n[requires.packages]\n"org.fixture/dep" = "=1.0.0"\n')
        with self.assertRaisesRegex(ValueError, "closure"):
            P.snapshot(self.source, self.commit(), self.packages[0])
        self.packages[1]["files"].remove("LICENSE")
        (self.source / "binding.json").write_text(json.dumps(self.binding))
        policy = self.commit()
        with self.assertRaisesRegex(ValueError, "license"):
            P.binding_at(self.source, policy, "binding.json", allow_local=True)

    def test_pinned_binding_ignores_worktree_and_rejects_credentials(self):
        for package in self.packages:
            package["destination"] = "https://github.com/fixture/" + package["coordinate"].split("/")[1] + ".git"
        path = self.source / "binding.json"
        path.write_text(json.dumps(self.binding))
        policy = self.commit()
        path.write_text("candidate bytes")
        self.assertEqual(P.binding_at(self.source, policy, "binding.json"), self.binding)
        self.packages[0]["destination"] = "https://credential@github.com/fixture/repo.git"
        path.write_text(json.dumps(self.binding))
        with self.assertRaisesRegex(ValueError, "credential-free"):
            P.binding_at(self.source, self.commit(), "binding.json")

    def test_complete_api_pagination(self):
        api = P.GitHub("fixture/private-source")
        with patch.object(api, "get", side_effect=[list(range(100)), ["last"]]) as get:
            self.assertEqual(len(api.pages("commits/sha/pulls")), 101)
        self.assertIn("page=2", get.call_args.args[0])

    def test_repository_api_endpoint_has_no_trailing_slash(self):
        with patch.object(P.urllib.request, "urlopen", return_value=io.BytesIO(b'{"id":123}')) as open_url:
            self.assertEqual(P.GitHub("fixture/source").get("")["id"], 123)
        self.assertEqual(open_url.call_args.args[0].full_url, "https://api.github.com/repos/fixture/source")

    def test_native_environment_has_no_tokens_or_askpass(self):
        with patch.dict(os.environ, GH_TOKEN="api-sentinel", PUBLISH_TOKEN="publish-sentinel",
                        GIT_ASKPASS="credential-helper"):
            env = P.native_environment(self.directory)
        self.assertNotIn("GH_TOKEN", env)
        self.assertNotIn("PUBLISH_TOKEN", env)
        self.assertNotIn("GIT_ASKPASS", env)

    def test_automatic_trigger_is_read_back_by_run_id(self):
        event = self.directory / "event.json"
        event.write_text(json.dumps({"workflow_run": {"id": 987}}))
        good_run = self.api.pages("actions/workflows/456/runs?head_sha=" + self.revision)[0]
        api = P.GitHub("fixture/private-source")
        with patch.dict(os.environ, GITHUB_EVENT_NAME="workflow_run", GITHUB_EVENT_PATH=str(event)), \
                patch.object(api, "get", side_effect=[good_run, {"id": 456, "path": self.binding["ci_workflow"]}]) as get:
            P.verify_trigger(api, self.binding, self.revision)
        self.assertEqual(get.call_args_list[0].args[0], "actions/runs/987")
        with patch.dict(os.environ, GITHUB_EVENT_NAME="workflow_run", GITHUB_EVENT_PATH=str(event)), \
                patch.object(api, "get", side_effect=[dict(good_run, head_sha="c" * 40),
                    {"id": 456, "path": self.binding["ci_workflow"]}]):
            with self.assertRaisesRegex(ValueError, "automatic trigger"):
                P.verify_trigger(api, self.binding, self.revision)

    def test_governance_compatibility_uses_existing_export_and_receipt(self):
        spec = importlib.util.spec_from_file_location("existing", P.ROOT / "scripts/prepare-distribution.py")
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        accepted = "ec048fb39ae28cf2d747101466a603ddd062b1b0"
        expected = old.snapshot(accepted)
        actual = P.snapshot(P.ROOT, accepted, {"adapter": "shared-governance-v1",
                                             "coordinate": "org.jresearch.ai/development-governance"})
        self.assertEqual(actual, expected)
        with self.assertRaisesRegex(ValueError, "coordinate"):
            P.snapshot(P.ROOT, accepted, {"adapter": "shared-governance-v1", "coordinate": "org.fixture/wrong"})


class PublicationTests(Fixture):
    def test_existing_tag_skips_before_binary_or_native_invocation(self):
        remote = self.remote(0)
        self.git("push", str(remote), "HEAD:refs/heads/main", "HEAD:refs/tags/v1.0.0")
        decision = self.plan()["packages"][0]
        result = P.stage(self.source, self.packages[0], decision, Path("absent"), self.directory / "stage")
        self.assertEqual(result["status"], "ALREADY_PUBLISHED")

    def test_failed_package_does_not_erase_other_statuses(self):
        decisions = self.plan()
        with patch.object(P, "stage", side_effect=[{**decisions["packages"][0], "status": "ALREADY_PUBLISHED"}, ValueError("failure")]):
            report = P.stage_all(self.source, self.binding, decisions, None, self.directory, None)
        self.assertEqual([row["status"] for row in report["packages"]],
                         ["ALREADY_PUBLISHED", "FAILED_OR_PENDING"])


@unittest.skipUnless(VIBE, "pass --vibe for pinned Linux native staging")
class NativeTests(Fixture):
    def setUp(self):
        super().setUp()
        self.env_patch = patch.dict(os.environ, self.env)
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        for index in range(2):
            self.remote(index)

    def stage(self, index=0, suffix="stage"):
        report = self.plan()
        return P.stage(self.source, self.packages[index], report["packages"][index], VIBE,
                       self.directory / (suffix + str(index)))

    def test_native_two_packages_partial_failure_and_same_source_retry(self):
        a, b = self.stage(0), self.stage(1)
        self.assertEqual(P.finalize(a)["status"], "PUBLISHED")
        def fail(*args):
            raise ValueError("injected absent-tag failure")
        self.assertEqual(P.finalize(b, push=fail)["status"], "FAILED_OR_PENDING")
        self.assertEqual(self.stage(0, "retry")["status"], "ALREADY_PUBLISHED")
        self.assertEqual(P.finalize(self.stage(1, "retry"))["status"], "PUBLISHED")

    def test_a_only_publication_preserves_b_and_private_export(self):
        for index in range(2):
            self.assertEqual(P.finalize(self.stage(index))["status"], "PUBLISHED")
        b_destination = self.packages[1]["destination"]
        b_before = P.remote_refs(b_destination, "v1.0.0")
        changed = self.change()
        self.api.revisions.append(changed)
        self.revision = changed
        a = self.stage(0, "updated")
        self.assertEqual(P.finalize(a)["status"], "PUBLISHED")
        b = self.stage(1, "updated")
        self.assertEqual(b["status"], "NO_PACKAGE_CHANGE")
        self.assertEqual(P.remote_refs(b_destination, "v1.0.0"), b_before)
        receipt = self.git("show", "v1.0.1:DISTRIBUTION.json", cwd=Path(a["staging"]))
        self.assertNotIn(changed, receipt)
        self.assertNotIn("source_revision", receipt)
        paths = self.git("ls-tree", "-r", "--name-only", "v1.0.1", cwd=Path(a["staging"]))
        self.assertNotIn("private", paths)

    def test_native_staging_failure_and_retry(self):
        run = P.subprocess.run
        def fail_native(command, **kwargs):
            if command[0] == str(VIBE):
                return subprocess.CompletedProcess(command, 1)
            return run(command, **kwargs)
        with patch.object(P.subprocess, "run", side_effect=fail_native):
            with self.assertRaisesRegex(ValueError, "native staging failed"):
                self.stage()
        self.assertIsNone(P.tag_oid(P.remote_refs(self.packages[0]["destination"], "v1.0.0"), "v1.0.0"))
        self.assertEqual(P.finalize(self.stage(0, "retry"))["status"], "PUBLISHED")

    def test_ambiguous_transport_is_reconciled_by_exact_tag_readback(self):
        staged = self.stage()
        def ambiguous(*args):
            P.git(*args)
            raise ValueError("lost successful response")
        self.assertEqual(P.finalize(staged, push=ambiguous)["status"], "PUBLISHED")

    def test_concurrent_same_tag_preserves_remote_refs(self):
        staged = self.stage()
        destination = self.packages[0]["destination"]
        def race(*args):
            self.git("push", destination, "HEAD:refs/heads/main", "HEAD:refs/tags/v1.0.0")
            P.git(*args)
        result = P.finalize(staged, push=race)
        self.assertEqual(result["status"], "ALREADY_PUBLISHED")
        self.assertEqual(P.tag_oid(P.remote_refs(destination, "v1.0.0"), "v1.0.0"), self.revision)
        self.assertEqual(self.git("ls-remote", destination, "refs/heads/main").split()[0], self.revision)

    def test_concurrent_different_version_main_rejects_entire_push(self):
        staged = self.stage()
        destination = self.packages[0]["destination"]
        def race(*args):
            self.git("push", destination, "HEAD:refs/heads/main", "HEAD:refs/tags/v9.0.0")
            P.git(*args)
        result = P.finalize(staged, push=race)
        self.assertEqual(result["status"], "FAILED_OR_PENDING")
        self.assertIsNone(P.tag_oid(P.remote_refs(destination, "v1.0.0"), "v1.0.0"))
        self.assertEqual(P.tag_oid(P.remote_refs(destination, "v9.0.0"), "v9.0.0"), self.revision)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vibe", type=Path)
    args, remaining = parser.parse_known_args()
    if args.vibe:
        VIBE = args.vibe.resolve()
        NativeTests.__unittest_skip__ = False
    unittest.main(argv=[sys.argv[0], *remaining])
