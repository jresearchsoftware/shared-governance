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
import textwrap
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
                 "path": ".github/workflows/check.yml",
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
                "redistribution": {"status": "approved", "license": "MIT",
                                   "approval": "https://github.com/fixture/private-source/issues/1"},
                "destination": ("https://github.com/fixture/" + name + ".git" if getattr(self, "public_destinations", False)
                                else (self.directory / (name + ".git")).as_uri())})
        self.binding = {"schema": 1, "repository": "fixture/private-source", "repository_id": 123,
            "branch": "main", "ci_workflow": ".github/workflows/check.yml",
            "acceptance": "owner-squash-attestation-v1", "authorized_integrators": ["owner"],
            "packages": self.packages}
        self.save_binding()
        self.baseline = self.commit()
        for package in self.packages:
            package["baseline"] = self.baseline
            name = package["coordinate"].split("/")[1]
            root = package["root"]
            target = self.source / root
            target.mkdir(parents=True)
            (target / "vibe.toml").write_text('[package]\ngroup = "org.fixture"\nname = "' + name +
                '"\nversion = "1.0.0"\nkind = "flow"\nfrozen = true\npublish = false\nlicense = "MIT"\n')
            (target / "README.md").write_text("Approved public guidance.\n")
            (target / "LICENSE").write_text("MIT\nPublic synthetic fixture.\n")
            (target / "private.txt").write_text("PRIVATE_PACKAGE_SENTINEL")
        self.save_binding()
        self.revision = self.commit()
        self.api = Evidence(self.binding, [self.revision])

    def git(self, *args, cwd=None):
        return subprocess.check_output(["git", *map(str, args)], cwd=cwd or self.source,
                                       env=self.env, stderr=subprocess.PIPE).decode().strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Disposable source")
        return self.git("rev-parse", "HEAD")

    def save_binding(self):
        (self.source / "binding.json").write_text(json.dumps(self.binding))

    def change(self, number=0, version="1.0.1"):
        manifest = self.source / self.packages[number]["root"] / "vibe.toml"
        manifest.write_text(re.sub(r'version = "[^"]+"', 'version = "' + version + '"', manifest.read_text()))
        readme = manifest.parent / "README.md"
        readme.write_text(readme.read_text() + "Changed guidance.\n")
        return self.commit()

    def plan(self, revision=None):
        return P.plan(self.source, revision or self.revision, "main", self.binding, self.api, CODE_SHA, "binding.json")

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
                       {"path": ".github/workflows/wrong.yml"}, {"head_branch": "side"},
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


class TemporalTests(Fixture):
    def incomplete_initial_package(self):
        (self.source / self.packages[0]["root"] / "LICENSE").unlink()
        self.git("add", ".")
        self.git("commit", "--amend", "--no-edit", "-q")
        self.revision = self.git("rev-parse", "HEAD")
        self.api = Evidence(self.binding, [self.revision])

    def test_incomplete_historical_package_factual_noop_and_source_time_readiness(self):
        self.incomplete_initial_package()
        (self.source / "research.txt").write_text("Ordinary factual direct-main update")
        factual = self.commit()
        with patch.object(self.api, "get", side_effect=AssertionError("no acceptance API for no-op")), \
                patch.object(self.api, "pages", side_effect=AssertionError("no acceptance API for no-op")):
            decisions = self.plan(factual)["packages"]
            self.assertEqual([p["status"] for p in decisions],
                             ["NO_PACKAGE_CHANGE", "NO_PACKAGE_CHANGE"])
        with patch.object(P, "remote_refs", side_effect=AssertionError("no distribution access for no-op")):
            self.assertEqual(P.stage(self.source, self.packages[0], decisions[0],
                                     self.directory / "absent-vibe", self.directory / "unused"), decisions[0])
        # Production requested no release; an applicable source-time preparation
        # check must still reject the same unchanged incomplete payload.
        self.git("switch", "-qc", "candidate")
        (self.source / "research.txt").write_text("Candidate factual update")
        proposed = self.commit()
        self.assertEqual(self.candidate(proposed, factual)["reason_code"], "PUBLIC_EXPORT_INCOMPLETE")

    def test_changed_incomplete_release_never_uses_the_noop_exemption(self):
        self.incomplete_initial_package()
        # Initial incomplete source is a new export, not a no-op.
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "PUBLIC_EXPORT_INCOMPLETE")
        self.git("switch", "-qc", "candidate")
        proposed = self.change()
        self.assertEqual(self.candidate(proposed)["reason_code"], "PUBLIC_EXPORT_INCOMPLETE")
        self.git("switch", "-q", "main")
        self.git("merge", "--squash", "candidate")
        accepted = self.commit()
        self.api.revisions.append(accepted)
        self.assertEqual(self.plan(accepted)["packages"][0]["reason_code"], "PUBLIC_EXPORT_INCOMPLETE")

    def test_candidate_valid_is_bounded_and_production_retains_inherited_acceptance_gate(self):
        inherited = self.change()
        self.git("switch", "-qc", "candidate")
        proposed = self.change(version="1.0.2")
        with patch.object(self.api, "pages", side_effect=AssertionError("offline source check")):
            candidate = self.candidate(proposed, inherited)
        self.assertEqual(candidate["status"], "CANDIDATE_VALID")
        self.assertEqual(candidate["acceptance"], [])
        self.git("switch", "-q", "main")
        self.git("merge", "--squash", "candidate")
        accepted = self.commit()
        self.api.revisions.append(accepted)
        self.assertEqual(self.plan(accepted)["packages"][0]["reason_code"], "OWNER_ACCEPTANCE_NOT_ESTABLISHED")
        # A separately accepted explicit disposition can move this audit baseline;
        # candidate validity itself did not supply acceptance authority.
        self.packages[0]["baseline"] = inherited
        self.packages[0]["baseline_disposition"] = "https://github.com/fixture/private-source/issues/2"
        self.assertEqual(self.plan(accepted)["packages"][0]["status"], "READY")

    def candidate(self, revision, base=None):
        with patch.object(self.api, "get", side_effect=AssertionError("source checks do not grant acceptance")):
            return P.plan(self.source, revision, base or self.revision, self.binding, self.api, CODE_SHA,
                          "binding.json", base or self.revision)["packages"][0]

    def reset_fixture(self):
        self.git("reset", "--hard", self.revision)
        self.binding = json.loads((self.source / "binding.json").read_text())
        self.packages = self.binding["packages"]
        self.api = Evidence(self.binding, [self.revision])

    def test_revision_appropriate_add_delete_rename_and_binding_only_inventory(self):
        for operation in ("add", "delete", "rename", "binding-only"):
            for version in ("1.0.0", "1.0.1"):
                with self.subTest(operation=operation, version=version):
                    self.reset_fixture()
                    package = self.packages[0]
                    root = self.source / package["root"]
                    if operation == "add":
                        (root / "guide.md").write_text("Approved new public guide")
                        package["files"].append("guide.md")
                    else:
                        package["files"].remove("README.md")
                        if operation == "delete":
                            (root / "README.md").unlink()
                        elif operation == "rename":
                            (root / "README.md").rename(root / "guide.md")
                            package["files"].append("guide.md")
                    manifest = root / "vibe.toml"
                    manifest.write_text(manifest.read_text().replace('"1.0.0"', '"' + version + '"'))
                    self.save_binding()
                    changed = self.commit()
                    self.api.revisions.append(changed)
                    result = self.plan(changed)["packages"][0]
                    self.assertEqual(result["status"], "READY" if version == "1.0.1" else "AUTHORIZATION_PENDING")
                    candidate = self.candidate(changed)
                    self.assertEqual(candidate["status"], "CANDIDATE_VALID" if version == "1.0.1" else "AUTHORIZATION_PENDING")
                    files = P.snapshot(self.source, changed, package)[0]
                    self.assertNotIn("private.txt", files)
                    self.assertNotIn(b"PRIVATE_SENTINEL", b"".join(files.values()))

    def test_unapproved_and_missing_public_files_never_export(self):
        package = self.packages[0]
        (self.source / package["root"] / "unapproved.md").write_text("PRIVATE_SENTINEL")
        changed = self.commit()
        self.assertEqual(self.plan(changed)["packages"][0]["status"], "NO_PACKAGE_CHANGE")
        package["files"].append("missing.md")
        self.save_binding()
        self.assertEqual(self.candidate(self.commit())["status"], "AUTHORIZATION_PENDING")

    def test_disclosure_change_requires_new_version_but_source_sha_alone_does_not(self):
        self.packages[0]["disclosure"] = "public-source"
        self.save_binding()
        changed = self.commit()
        self.assertEqual(self.candidate(changed)["reason_code"], "PACKAGE_VERSION_REUSE")
        changed = self.change()
        self.assertEqual(self.candidate(changed)["status"], "CANDIDATE_VALID")

    def test_owner_addition_does_not_reauthorize_historical_package_bytes(self):
        rejected = self.change()
        self.binding["authorized_integrators"].append("new-owner")
        self.save_binding()
        rotation = self.commit()
        changed = self.change(version="1.0.2")
        self.api.revisions.extend([rejected, rotation, changed])
        self.api.alter_pr = lambda pr: dict(pr, merged_by={"login": "new-owner" if pr["merge_commit_sha"] == rejected else "owner"})
        self.assertEqual(self.plan(changed)["packages"][0]["status"], "AUTHORIZATION_PENDING")
        # Explicit owner disposition of the accumulated delta is a distinct pin,
        # not a side effect of adding an integrator.
        self.packages[0]["baseline"] = rejected
        self.packages[0]["baseline_disposition"] = "https://github.com/fixture/private-source/issues/2"
        self.assertEqual(self.plan(changed)["packages"][0]["status"], "READY")

    def test_historical_workflow_and_owner_survive_rotation_and_deletion(self):
        self.binding["ci_workflow"] = ".github/workflows/replacement.yml"
        self.binding["authorized_integrators"] = ["new-owner"]
        self.save_binding()
        rotation = self.commit()
        changed = self.change()
        self.api.revisions.extend([rotation, changed])
        self.api.alter_pr = lambda pr: dict(pr, merged_by={"login": "new-owner" if pr["merge_commit_sha"] == changed else "owner"})
        self.api.alter_run = lambda run: dict(run, path=(".github/workflows/check.yml" if run["head_sha"] == self.revision
                                                        else self.binding["ci_workflow"]))
        original = self.api.get
        def get(path):
            self.assertFalse(path.startswith("actions/workflows/"), "deleted historical workflows need no current lookup")
            return original(path)
        with patch.object(self.api, "get", side_effect=get):
            result = self.plan(changed)["packages"][0]
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["acceptance"][0]["ci_workflow"], ".github/workflows/check.yml")
        self.assertIn(rotation, [e["source_sha"] for e in result["acceptance"]])

    def test_new_integrator_cannot_self_authorize_policy_rotation(self):
        self.binding["authorized_integrators"] = ["new-owner"]
        self.save_binding()
        changed = self.change()
        self.api.revisions.append(changed)
        self.api.alter_pr = lambda pr: dict(pr, merged_by={"login": "new-owner" if pr["merge_commit_sha"] == changed else "owner"})
        self.assertEqual(self.plan(changed)["packages"][0]["status"], "AUTHORIZATION_PENDING")

    def test_premerge_license_readiness_and_unresolved_rights(self):
        for defect in ("missing", "empty", "metadata", "rights"):
            with self.subTest(defect=defect):
                self.reset_fixture()
                root = self.source / self.packages[0]["root"]
                if defect == "missing":
                    (root / "LICENSE").unlink()
                elif defect == "empty":
                    (root / "LICENSE").write_text("  \n")
                elif defect == "metadata":
                    path = root / "vibe.toml"
                    path.write_text(path.read_text().replace('license = "MIT"', 'license = "UNRESOLVED"'))
                else:
                    self.packages[0]["redistribution"]["status"] = "unresolved"
                    self.save_binding()
                changed = self.change()
                self.assertEqual(self.candidate(changed)["status"], "AUTHORIZATION_PENDING")

    def test_unpublished_accepted_identity_cannot_be_completed_in_place(self):
        root = self.source / self.packages[0]["root"]
        (root / "LICENSE").unlink()
        incomplete_main = self.commit()
        self.assertEqual(self.git("tag"), "")
        self.git("switch", "-qc", "candidate")
        (root / "LICENSE").write_text("MIT\nPublic synthetic fixture.\n")
        repair = self.commit()
        self.assertEqual(self.candidate(repair, incomplete_main)["status"], "AUTHORIZATION_PENDING")
        repair = self.change(version="1.0.1")
        self.assertEqual(self.candidate(repair, incomplete_main)["status"], "CANDIDATE_VALID")

    def test_candidate_branch_can_refine_new_version_before_acceptance(self):
        self.git("switch", "-qc", "candidate")
        self.change()
        revised = self.change(version="1.0.1")
        self.assertEqual(self.candidate(revised)["status"], "CANDIDATE_VALID")

    def test_forward_license_repair_checks_candidate_and_accepted_production_history(self):
        root = self.source / self.packages[0]["root"]
        (root / "LICENSE").unlink()
        self.git("add", ".")
        self.git("commit", "--amend", "--no-edit", "-q")
        self.revision = self.git("rev-parse", "HEAD")
        self.api = Evidence(self.binding, [self.revision])
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "PUBLIC_EXPORT_INCOMPLETE")
        self.git("switch", "-qc", "candidate")
        (root / "LICENSE").write_text("MIT\nPublic synthetic fixture.\n")
        repair = self.change()
        self.assertEqual(self.candidate(repair)["status"], "CANDIDATE_VALID")
        self.git("switch", "-q", "main")
        self.git("merge", "--squash", "candidate")
        accepted = self.commit()
        self.api.revisions.append(accepted)
        result = self.plan(accepted)["packages"][0]
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["version"], "1.0.1")
        self.assertEqual([e["source_sha"] for e in result["acceptance"]], [self.revision, accepted])
        self.assertEqual(self.git("tag"), "")
        # Historical incompleteness is comparable, not an eligibility waiver.
        self.api.revisions.remove(self.revision)
        self.assertEqual(self.plan(accepted)["packages"][0]["reason_code"], "OWNER_ACCEPTANCE_NOT_ESTABLISHED")

    def test_baseline_disposition_preserves_older_frozen_versions_in_candidate_and_plan(self):
        for version in ("1.0.0", "3.0.0"):
            with self.subTest(version=version):
                self.reset_fixture()
                newer = self.change(version="2.0.0")
                self.packages[0]["baseline"] = newer
                self.packages[0]["baseline_disposition"] = "https://github.com/fixture/private-source/issues/2"
                self.save_binding()
                disposed = self.commit()
                # Earlier eligibility is disposed, not replayed; older identity
                # still exists in Git without a remote tag or new registry.
                self.api = Evidence(self.binding, [disposed])
                self.git("switch", "-qc", "candidate")
                proposed = self.change(version=version)
                candidate = self.candidate(proposed, disposed)
                expected = "AUTHORIZATION_PENDING" if version == "1.0.0" else "CANDIDATE_VALID"
                self.git("switch", "-q", "main")
                self.git("merge", "--squash", "candidate")
                accepted = self.commit()
                self.api.revisions.append(accepted)
                production = self.plan(accepted)["packages"][0]
                self.git("branch", "-D", "candidate")
                self.assertEqual(candidate["status"], expected)
                self.assertEqual(production["status"], "AUTHORIZATION_PENDING" if version == "1.0.0" else "READY")
                if version == "1.0.0":
                    self.assertEqual(candidate["reason_code"], "PACKAGE_VERSION_REUSE")
                    self.assertEqual(production["reason_code"], "PACKAGE_VERSION_REUSE")
                else:
                    self.assertNotIn(self.revision, [e["source_sha"] for e in production["acceptance"]])
                self.assertEqual(self.git("tag"), "")

    def test_source_check_rejects_a_stale_main_baseline(self):
        changed = self.change()
        with self.assertRaisesRegex(ValueError, "current accepted"):
            P.plan(self.source, changed, "main", self.binding, self.api, CODE_SHA,
                   "binding.json", self.revision)

    def test_baseline_cannot_hide_unsupported_historical_package_root_change(self):
        original = self.packages[0]["root"]
        self.packages[0]["root"] = "packages/relocated-subagents"
        self.git("mv", original, self.packages[0]["root"])
        self.save_binding()
        moved = self.change(version="2.0.0")
        self.packages[0]["baseline"] = moved
        self.packages[0]["baseline_disposition"] = "https://github.com/fixture/private-source/issues/2"
        self.save_binding()
        disposed = self.commit()
        changed = self.change(version="3.0.0")
        self.api = Evidence(self.binding, [disposed, changed])
        candidate = self.candidate(changed, disposed)
        production = self.plan(changed)["packages"][0]
        self.assertEqual((candidate["status"], production["status"]),
                         ("AUTHORIZATION_PENDING", "AUTHORIZATION_PENDING"))
        self.assertEqual(candidate["reason_code"], "HISTORICAL_BINDING_UNRESOLVED")
        self.assertEqual(production["reason_code"], "HISTORICAL_BINDING_UNRESOLVED")

    def test_missing_policy_history_cannot_fall_back_to_current_policy(self):
        result = P.plan(self.source, self.revision, "main", self.binding, self.api, CODE_SHA)
        self.assertEqual(result["packages"][0]["reason_code"], "HISTORICAL_BINDING_UNRESOLVED")
        self.git("rm", "binding.json")
        missing = self.commit()
        self.save_binding()
        changed = self.change()
        self.api.revisions.extend([missing, changed])
        self.assertEqual(self.plan(changed)["packages"][0]["reason_code"], "HISTORICAL_BINDING_UNRESOLVED")


class SourceCliTests(Fixture):
    public_destinations = True

    def test_source_time_cli_validates_a_candidate_without_api_or_distribution(self):
        self.git("switch", "-qc", "candidate")
        changed = self.change()
        code_sha = P.git(P.ROOT, "rev-parse", "HEAD").decode().strip()
        report = self.directory / "candidate.json"
        result = subprocess.run([sys.executable, str(Path(P.__file__)), "check",
            "--source", str(self.source), "--source-sha", changed, "--main", "main",
            "--base", self.revision, "--policy", str(self.source), "--policy-sha", changed,
            "--binding", "binding.json", "--publisher-sha", code_sha, "--report", str(report)],
            env=dict(self.env, GH_TOKEN="", GITHUB_EVENT_NAME="pull_request"), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([p["status"] for p in json.loads(report.read_text())["packages"]],
                         ["CANDIDATE_VALID", "NO_PACKAGE_CHANGE"])
        self.assertIn("independent acceptance and publication remain pending", result.stdout)


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


class DiagnosticsTests(unittest.TestCase):
    @unittest.skipIf(sys.platform == "win32", "workflow shell qualification runs on supported Linux")
    def test_real_no_checkout_shell_fallback_after_input_failure(self):
        workflow = (P.ROOT / ".github/workflows/vibe-publisher.yml").read_text()
        validation = textwrap.dedent(workflow.split("        run: |\n", 1)[1].split("      - name:", 1)[0])
        summary = textwrap.dedent(workflow.split("      - name: Visible per-package result", 1)[1].split("        run: |\n", 1)[1])
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "summary.md"
            env = dict(os.environ, SOURCE_SHA="invalid-private-sentinel", PUBLISHER_SHA="a" * 40,
                       PUBLISHER_REPOSITORY="fixture/publisher", MODE="plan",
                       GITHUB_STEP_SUMMARY=str(output))
            self.assertNotEqual(subprocess.run(["bash", "-e", "-c", validation], cwd=temporary, env=env,
                                               capture_output=True).returncode, 0)
            for inputs, checkout, expected in (("failure", "skipped", "INPUT_VALIDATION_FAILED"),
                                               ("cancelled", "skipped", "INPUT_VALIDATION_FAILED"),
                                               ("success", "failure", "PUBLISHER_CHECKOUT_FAILED")):
                env.update(INPUTS_OUTCOME=inputs, PUBLISHER_CHECKOUT_OUTCOME=checkout)
                output.write_text("")
                subprocess.run(["bash", "-e", "-c", summary], cwd=temporary, env=env, check=True)
                text = output.read_text()
                self.assertIn(expected, text)
                self.assertNotIn("invalid-private-sentinel", text)
                if inputs != "success":
                    self.assertNotIn("PUBLISHER_CHECKOUT_FAILED", text)

    def test_report_and_actions_summary_show_safe_reasons_and_warnings(self):
        report = {"packages": [
            {"package": "org.fixture/pending", "status": "AUTHORIZATION_PENDING",
             "reason": "no unambiguous authorized owner squash integration",
             "reason_code": "OWNER_ACCEPTANCE_NOT_ESTABLISHED"},
            {"package": "org.fixture/readback", "status": "FAILED_OR_PENDING",
             "reason": "Publication readback unavailable; inspect and retry the same source and publisher SHA."},
            {"package": "org.fixture/competing", "status": "ALREADY_PUBLISHED",
             "warning": "A competing identity exists and was retained; this source was not published."},
            {"package": "org.fixture/unknown", "status": "FAILED_OR_PENDING",
             "reason": "private/path https://user:secret@example.invalid/repo"},
        ]}
        with tempfile.TemporaryDirectory() as temporary:
            report_path = Path(temporary) / "publication.json"
            summary_path = Path(temporary) / "summary.md"
            with patch("builtins.print") as output:
                P.write_report(report, report_path)
            log_text = "\n".join(call.args[0] for call in output.call_args_list)
            self.assertIn("OWNER_ACCEPTANCE_NOT_ESTABLISHED", log_text)
            self.assertIn("PUBLICATION_READBACK_UNAVAILABLE", log_text)
            self.assertIn("COMPETING_TAG_RETAINED", log_text)
            self.assertIn("UNCLASSIFIED_PUBLICATION_FAILURE", log_text)
            self.assertNotIn("secret@example.invalid", log_text)
            self.assertNotIn("private/path", log_text)

            P.append_actions_summary(report_path, summary_path, "failure", {"plan": "success"})
            summary = summary_path.read_text(encoding="utf-8")
            self.assertIn("OWNER_ACCEPTANCE_NOT_ESTABLISHED", summary)
            self.assertIn("PUBLICATION_READBACK_UNAVAILABLE", summary)
            self.assertIn("COMPETING_TAG_RETAINED", summary)
            self.assertIn("Resolve the listed owner acceptance or disposition", summary)
            self.assertNotIn("secret@example.invalid", summary)
            self.assertNotIn("private/path", summary)

    def test_staging_failure_reports_a_safe_failure_category(self):
        coordinate = "org.fixture/failure"
        binding = {"packages": [{"coordinate": coordinate, "destination": "unused"}]}
        report = {"source_sha": "a" * 40, "publisher_sha": "b" * 40,
                  "packages": [{"package": coordinate, "status": "READY"}]}
        with patch.object(P, "stage", side_effect=ValueError("native staging failed; recover and retry the same source SHA")):
            staged = P.stage_all(Path("."), binding, report, None, Path("."), None)
        result = staged["packages"][0]
        self.assertEqual(result["failure_code"], "NATIVE_PUBLISHER_FAILED")
        self.assertEqual(P.operator_diagnostic(result)[0], "NATIVE_PUBLISHER_FAILED")
        self.assertNotIn("native staging failed", result["reason"])

    def test_missing_report_summary_identifies_the_failed_phase_safely(self):
        with tempfile.TemporaryDirectory() as temporary:
            summary_path = Path(temporary) / "summary.md"
            P.append_actions_summary(Path(temporary) / "missing.json", summary_path,
                                     "failure", {"plan": "failure"})
            summary = summary_path.read_text(encoding="utf-8")
        self.assertIn("SOURCE_ACCEPTANCE_OR_CI_CHECK_FAILED", summary)
        self.assertIn("Resolve the source, binding, owner acceptance or exact CI evidence", summary)
        self.assertNotIn("private/path", summary)

    def test_actions_summary_names_failed_phase_when_eligibility_report_exists(self):
        with tempfile.TemporaryDirectory() as temporary:
            report_path = Path(temporary) / "publication.json"
            summary_path = Path(temporary) / "summary.md"
            report_path.write_text(json.dumps({"packages": [
                {"package": "org.fixture/ready", "status": "READY"}
            ]}), encoding="utf-8")
            P.append_actions_summary(report_path, summary_path, "failure", {"tool": "failure"})
            summary = summary_path.read_text(encoding="utf-8")
        self.assertIn("**FAILED_OR_PENDING**", summary)
        self.assertIn("PINNED_TOOL_PREPARATION_FAILED", summary)
        self.assertIn("no destination write was attempted", summary)


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



class InitialPublicationTests(Fixture):
    def setUp(self):
        super().setUp()
        # Independent source history: no publisher binding or CI existed at 1.0.x.
        self.git("checkout", "--orphan", "source-only")
        self.git("rm", "--cached", "-r", ".")
        (self.source / "binding.json").unlink()
        for package in self.packages:
            root = self.source / package["root"]
            (root / "LICENSE").unlink()
            manifest = root / "vibe.toml"
            manifest.write_text(manifest.read_text().replace('license = "MIT"\n', ''))
        self.old = self.commit()
        for package in self.packages:
            root = self.source / package["root"]
            (root / "LICENSE").write_text("MIT\nSynthetic contributors\n")
            manifest = root / "vibe.toml"
            manifest.write_text(manifest.read_text().replace('1.0.0', '1.0.1') + 'license = "MIT"\n')
        self.frozen = self.commit()
        for package in self.packages:
            package.update(baseline=self.frozen,
                baseline_disposition="https://github.com/fixture/private-source/issues/1#issuecomment-1",
                initial_publication={"source_sha": self.frozen, "version": "1.0.1",
                    "payload_sha256": P.snapshot(self.source, self.frozen, package)[1]["payload_sha256"]})
        self.save_binding()
        self.initiation = self.commit()
        self.api = Evidence(self.binding, [self.frozen, self.initiation])
        pages = self.api.pages
        self.api.pages = lambda path, key=None: ([] if path.startswith("actions/runs?head_sha=" + self.frozen)
                                                  else pages(path, key))
        self.main = "source-only"

    def initial(self, revision=None):
        return P.initial_plan(self.source, revision or self.initiation, self.main,
                              self.binding, self.api, CODE_SHA, "binding.json")

    def amend_binding(self):
        self.git("reset", "--soft", self.frozen)
        self.save_binding()
        self.initiation = self.commit()
        self.api.revisions[-1] = self.initiation

    def test_current_baseline_disposition_alone_does_not_publish(self):
        for revision in (self.frozen, self.initiation):
            report = P.plan(self.source, revision, self.main, self.binding, self.api, CODE_SHA, "binding.json")
            self.assertEqual([(p["status"], p["reason_code"]) for p in report["packages"]],
                [("AUTHORIZATION_PENDING", "HISTORICAL_BINDING_UNRESOLVED")] * 2)
        (self.source / "research.txt").write_text("Unrelated direct-main evidence")
        revision = self.commit()
        report = P.plan(self.source, revision, self.main, self.binding, self.api, CODE_SHA, "binding.json")
        self.assertEqual([p["status"] for p in report["packages"]], ["NO_PACKAGE_CHANGE"] * 2)

    def test_first_publication_separates_source_acceptance_and_current_ci(self):
        report = self.initial()
        self.assertEqual([p["status"] for p in report["packages"]], ["READY"] * 2)
        for row in report["packages"]:
            self.assertEqual(row["source_sha"], self.frozen)
            self.assertEqual(row["readiness_acceptance"]["source_sha"], self.initiation)
            self.assertNotIn("ci_run", row["source_acceptance"])
            self.assertEqual(row["version"], "1.0.1")
        self.assertEqual(self.initial(), report)

    def test_source_owner_acceptance_is_required_independently_of_onboarding(self):
        def forge_old(pr):
            return dict(pr, merged=False) if pr["merge_commit_sha"] == self.frozen else pr
        self.api.alter_pr = forge_old
        self.assertEqual(self.initial()["packages"][0]["reason_code"], "OWNER_ACCEPTANCE_NOT_ESTABLISHED")

    def test_initial_candidate_check_is_offline_and_cannot_authorize_staging(self):
        self.git("branch", "accepted", self.frozen)
        with patch.object(self.api, "get", side_effect=AssertionError("candidate checks are offline")):
            report = P.initial_plan(self.source, self.initiation, "accepted", self.binding,
                                    self.api, CODE_SHA, "binding.json", self.frozen)
        self.assertEqual([p["status"] for p in report["packages"]], ["CANDIDATE_VALID"] * 2)
        self.assertEqual(P.stage(self.source, self.packages[0], report["packages"][0], None, None),
                         report["packages"][0])
        with self.assertRaisesRegex(ValueError, "current accepted source main"):
            P.initial_plan(self.source, self.initiation, "accepted", self.binding,
                           self.api, CODE_SHA, "binding.json", self.old)

    def test_initial_candidate_cli_requires_the_same_source_and_policy_pin(self):
        for i, package in enumerate(self.packages):
            package["destination"] = "https://github.com/fixture/distribution-" + str(i) + ".git"
        self.amend_binding()
        self.git("branch", "accepted", self.frozen)
        code_sha = P.git(P.ROOT, "rev-parse", "HEAD").decode().strip()
        report = self.directory / "candidate.json"
        command = [sys.executable, str(Path(P.__file__)), "check", "--initial-publication",
            "--source", str(self.source), "--source-sha", self.initiation, "--main", "accepted",
            "--base", self.frozen, "--policy", str(self.source), "--policy-sha", self.initiation,
            "--binding", "binding.json", "--publisher-sha", code_sha, "--report", str(report)]
        result = subprocess.run(command, env=dict(self.env, GH_TOKEN="", GITHUB_EVENT_NAME="pull_request"),
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([p["status"] for p in json.loads(report.read_text())["packages"]],
                         ["CANDIDATE_VALID"] * 2)
        command[command.index("--policy-sha") + 1] = self.frozen
        result = subprocess.run(command, env=self.env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def test_missing_failed_or_wrong_current_ci_stops(self):
        for field, value in (("conclusion", "failure"), ("head_sha", self.frozen),
                             ("event", "pull_request"), ("path", ".github/workflows/other.yml")):
            with self.subTest(field=field):
                self.api.alter_run = lambda run: dict(run, **{field: value})
                self.assertEqual(self.initial()["packages"][0]["reason_code"], "MATCHING_SOURCE_CI_MISSING")

    def test_forged_owner_or_unmerged_or_wrong_source_is_rejected(self):
        for update in ({"merged_by": {"login": "intruder"}}, {"merged": False},
                       {"merge_commit_sha": "c" * 40}, {"base": {"ref": "main", "repo": {"id": 999}}}):
            with self.subTest(update=update):
                self.api.alter_pr = lambda pr: dict(pr, **update)
                self.assertEqual(self.initial()["packages"][0]["reason_code"], "OWNER_ACCEPTANCE_NOT_ESTABLISHED")

    def test_missing_or_wrong_attestation_stops(self):
        package = self.packages[0]
        for field, value in (("payload_sha256", "0" * 64), ("version", "1.0.0"),
                             ("source_sha", "a" * 40)):
            with self.subTest(field=field):
                original = package["initial_publication"][field]
                package["initial_publication"][field] = value
                self.amend_binding()
                self.assertEqual(self.initial()["packages"][0]["status"], "AUTHORIZATION_PENDING")
                package["initial_publication"][field] = original
        package.pop("baseline_disposition")
        self.amend_binding()
        self.assertEqual(self.initial()["packages"][0]["reason_code"], "INITIAL_PUBLICATION_UNRESOLVED")

    def test_current_readiness_cannot_complete_or_change_old_version(self):
        root = self.source / self.packages[0]["root"]
        (root / "README.md").write_text("Changed accepted 1.0.1")
        revision = self.commit()
        self.api.revisions.append(revision)
        # Rebuild the original initiation with these changed bytes.
        self.amend_binding()
        self.assertEqual(self.initial()["packages"][0]["reason_code"], "PACKAGE_VERSION_REUSE")

    def test_license_rights_allowlist_and_disclosure_are_enforced(self):
        package = self.packages[0]
        for field, value in (("redistribution", {}), ("files", package["files"] + ["missing.md"]),
                             ("disclosure", "public-source")):
            with self.subTest(field=field):
                original = package[field]
                package[field] = value
                self.amend_binding()
                row = self.initial()["packages"][0]
                if field == "disclosure":
                    self.assertEqual(row["status"], "READY")
                    receipt = P.snapshot(self.source, self.frozen, package)[1]
                    self.assertEqual(receipt["source_revision"], self.frozen)
                else:
                    self.assertEqual(row["status"], "AUTHORIZATION_PENDING")
                package[field] = original
        files, receipt = P.snapshot(self.source, self.frozen, package)
        self.assertNotIn("source_revision", receipt)
        self.assertFalse(any("private" in name for name in files))

    def test_irrelevant_commit_cannot_reinitiate_and_ordinary_path_stays_noop(self):
        (self.source / "research.txt").write_text("Unrelated direct-main update")
        later = self.commit()
        self.api.revisions.append(later)
        self.assertEqual(self.initial(later)["packages"][0]["reason_code"], "INITIAL_PUBLICATION_UNRESOLVED")
        self.assertEqual(self.initial()["packages"][0]["status"], "READY")
        ordinary = P.plan(self.source, later, self.main, self.binding, self.api, CODE_SHA, "binding.json")
        self.assertEqual([p["status"] for p in ordinary["packages"]], ["NO_PACKAGE_CHANGE"] * 2)

    def test_frozen_version_first_integration_and_intervening_reuse(self):
        root = self.source / self.packages[0]["root"]
        # New accepted commit tries to replace an already frozen identity.
        (root / "README.md").write_text("same version, different frozen bytes")
        self.git("reset", "--soft", self.frozen)
        changed_frozen = self.commit()
        package = self.packages[0]
        package["initial_publication"].update(source_sha=changed_frozen,
            payload_sha256=P.snapshot(self.source, changed_frozen, package)[1]["payload_sha256"])
        self.save_binding()
        self.initiation = self.commit()
        self.api.revisions = [self.frozen, changed_frozen, self.initiation]
        self.assertEqual(self.initial()["packages"][0]["reason_code"], "PACKAGE_VERSION_REUSE")

    def test_existing_historical_policy_is_not_overridden(self):
        # A real old policy requires ordinary source-time interpretation.
        self.git("reset", "--soft", self.old)
        self.save_binding()
        bound_frozen = self.commit()
        self.packages[0]["initial_publication"]["source_sha"] = bound_frozen
        self.save_binding()
        self.initiation = self.commit()
        self.api.revisions = [bound_frozen, self.initiation]
        self.assertEqual(self.initial()["packages"][0]["reason_code"], "HISTORICAL_BINDING_UNRESOLVED")

    @unittest.skipUnless(VIBE, "pass --vibe for pinned Linux native staging")
    def test_native_first_publication_partial_success_retry_and_exact_bytes(self):
        with patch.dict(os.environ, self.env):
            for i in range(2):
                self.remote(i)
            report = self.initial()
            staged = P.stage_all(self.source, self.binding, report, VIBE, self.directory / "stage", None)
            a, b = staged["packages"]
            self.assertEqual(P.finalize(a)["status"], "PUBLISHED")
            def fail(*args):
                raise ValueError("Injected transport failure")
            self.assertEqual(P.finalize(b, push=fail)["status"], "FAILED_OR_PENDING")
            retry = P.stage_all(self.source, self.binding, self.initial(), VIBE, self.directory / "retry", None)
            self.assertEqual(retry["packages"][0]["status"], "ALREADY_PUBLISHED")
            self.assertEqual(P.finalize(retry["packages"][1])["status"], "PUBLISHED")
            for i, row in enumerate(staged["packages"]):
                paths = self.git("ls-tree", "-r", "--name-only", "v1.0.1", cwd=Path(row["staging"]))
                self.assertNotIn("private", paths)
                self.assertNotIn("v1.0.0", self.git("tag", cwd=Path(row["staging"])))
                files, _ = P.snapshot(self.source, self.frozen, self.packages[i])
                for name, data in files.items():
                    self.assertEqual(P.git(Path(row["staging"]), "show", "v1.0.1:" + name), data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vibe", type=Path)
    args, remaining = parser.parse_known_args()
    if args.vibe:
        VIBE = args.vibe.resolve()
        NativeTests.__unittest_skip__ = False
        native_initial = InitialPublicationTests.test_native_first_publication_partial_success_retry_and_exact_bytes
        InitialPublicationTests.test_native_first_publication_partial_success_retry_and_exact_bytes = native_initial.__wrapped__
    unittest.main(argv=[sys.argv[0], *remaining])
