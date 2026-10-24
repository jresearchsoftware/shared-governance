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
import tomllib
import textwrap
import unittest
import urllib.error
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publisher as P

VIBE = None
CODE_SHA = "a" * 40


class DestinationEvidence:
    token = "synthetic-publication-marker"

    def __init__(self, exists=False):
        self.exists = exists
        self.calls = []
        self.repository = "jrs-vibevm/org.fixture.example"
        self.metadata = {"full_name": self.repository, "private": False,
                         "visibility": "public", "owner": {"login": "jrs-vibevm"}}
        self.get_status = None
        self.identity = {"id": 123, "login": "fixture-publisher", "type": "User"}
        self.headers = {}  # Fine-grained PATs do not report classic scopes.
        self.create_status = 201
        self.on_create = lambda: None

    def request(self, method, path, data=None):
        self.calls.append((method, path, data))
        if method == "POST":
            if self.create_status in (0, 201, 422, 503):
                self.on_create()
                self.exists = True
            return self.create_status, self.metadata, {}
        if path == "user":
            return 200, self.identity, self.headers
        return (self.get_status if self.get_status is not None else (200 if self.exists else 404)), self.metadata, {}


class ProvisioningTests(unittest.TestCase):
    def setUp(self):
        self.api = DestinationEvidence()

    def test_exact_namespace_only(self):
        self.assertEqual(P.provisioned_repository("https://github.com/" + self.api.repository + ".git"), self.api.repository)
        for url in ("https://github.com/other/name.git", "https://user@github.com/jrs-vibevm/name.git",
                    "https://github.com/jrs-vibevm/../name.git", "https://github.com/jrs-vibevm/name.git?x=1",
                    "https://github.com/jrs-vibevm/..git", "file:///tmp/name.git"):
            self.assertIsNone(P.provisioned_repository(url))

    def test_absent_public_destination_is_created_once_and_read_back(self):
        P.ensure_destination(self.api.repository, self.api)
        self.assertEqual([c for c in self.api.calls if c[0] == "POST"], [
            ("POST", "orgs/jrs-vibevm/repos", {"name": "org.fixture.example", "private": False, "auto_init": False})])
        self.assertEqual(self.api.calls[-1][:2], ("GET", "repos/" + self.api.repository))
        self.api.calls.clear()
        P.ensure_destination(self.api.repository, self.api)
        self.assertEqual(len(self.api.calls), 1)  # Retry: no metadata/setup mutation.

    def test_existing_repository_needs_no_create_or_owner_visibility_proof(self):
        self.api.exists = True
        self.api.identity = {}
        P.ensure_destination(self.api.repository, self.api)
        self.assertEqual(len(self.api.calls), 1)

    def test_forbidden_transient_and_redirect_do_not_create(self):
        for status in (0, 301, 403, 429, 500, 503):
            with self.subTest(status=status):
                self.api = DestinationEvidence()
                # Zero means transport failure; override request for that case.
                self.api.get_status = status
                with patch.object(self.api, "request", return_value=(status, {}, {})):
                    with self.assertRaises(ValueError):
                        P.ensure_destination(self.api.repository, self.api)

    def test_hidden_private_or_wrong_identity_never_mutated(self):
        for change in ({"private": True}, {"visibility": "private"}, {"full_name": "other/repo"}):
            self.api = DestinationEvidence(exists=True)
            self.api.metadata.update(change)
            with self.assertRaises(ValueError):
                P.ensure_destination(self.api.repository, self.api)
            self.assertFalse(any(c[0] == "POST" for c in self.api.calls))
        for identity, headers in (({}, {}), ({"id": 123, "login": "fixture"}, {}),
                                   ({"id": 0, "login": "fixture", "type": "User"}, {}),
                                   ({"id": 123, "login": "", "type": "User"}, {}),
                                   (self.api.identity, {"X-GitHub-SSO": "required"})):
            self.api = DestinationEvidence()
            self.api.identity, self.api.headers = identity, headers
            with self.assertRaises(ValueError):
                P.ensure_destination(self.api.repository, self.api)
            self.assertFalse(any(c[0] == "POST" for c in self.api.calls))

    def test_create_race_and_ambiguous_transport_reconcile_without_reposting(self):
        for status in (422, 0, 503):
            self.api = DestinationEvidence()
            self.api.create_status = status
            P.ensure_destination(self.api.repository, self.api)
            self.assertEqual(sum(c[0] == "POST" for c in self.api.calls), 1)

    def test_fine_grained_authentication_errors_and_inconclusive_refresh_cannot_create(self):
        for failure in (0, 301, 401, 403, 404, 429, 503):
            for phase in ("authentication", "refresh"):
                if phase == "refresh" and failure == 404:
                    continue  # Expected absence under the owner-confirmed visibility premise.
                with self.subTest(status=failure, phase=phase):
                    api = DestinationEvidence()
                    original = api.request
                    reads = 0
                    def request(method, path, data=None):
                        nonlocal reads
                        if path.startswith("repos/"):
                            reads += 1
                        if (phase == "authentication" and path == "user"
                                or phase == "refresh" and reads == 2):
                            api.calls.append((method, path, data))
                            return failure, {}, {}
                        return original(method, path, data)
                    with patch.object(api, "request", side_effect=request), self.assertRaises(ValueError):
                        P.ensure_destination(api.repository, api)
                    self.assertFalse(any(c[0] == "POST" for c in api.calls))

    def test_authenticated_fine_grained_credential_without_create_permission_cannot_push(self):
        self.api.create_status = 403
        row = {"status": "STAGED", "destination": "https://github.com/" + self.api.repository + ".git",
               "tag": "v1.0.0", "staging": "unused"}
        with patch.object(P, "remote_refs", side_effect=ValueError("Git unavailable")), \
                patch.object(P, "git", side_effect=AssertionError("no push")):
            result = P.finalize(row, destination_api=self.api)
        self.assertEqual(result["failure_code"], "DESTINATION_PROVISIONING_PENDING")
        self.assertFalse(self.api.exists)

    def test_private_name_race_does_not_create_or_publish(self):
        self.api.create_status = 422
        self.api.on_create = lambda: self.api.metadata.update(private=True, visibility="private")
        with self.assertRaises(ValueError):
            P.ensure_destination(self.api.repository, self.api)
        self.assertEqual(sum(c[0] == "POST" for c in self.api.calls), 1)

    def test_failed_create_and_failed_readback_stay_pending(self):
        for status in (403, 422, 0, 503):
            self.api = DestinationEvidence()
            self.api.create_status = status
            self.api.on_create = lambda: setattr(self.api, "get_status", 404)
            with self.assertRaises(ValueError):
                P.ensure_destination(self.api.repository, self.api)
        self.api = DestinationEvidence()
        self.api.on_create = lambda: self.api.metadata.update(private=True)
        with self.assertRaises(ValueError):
            P.ensure_destination(self.api.repository, self.api)

    def test_nonstaged_noops_never_access_destination_or_credentials(self):
        for status in ("NO_PACKAGE_CHANGE", "ALREADY_PUBLISHED", "AUTHORIZATION_PENDING", "READY", "FAILED_OR_PENDING"):
            row = {"status": status}
            with patch.object(P, "ensure_destination", side_effect=AssertionError("no provisioning")):
                self.assertEqual(P.finalize(row), row)
            if status != "READY":
                with patch.object(P, "DestinationAPI", side_effect=AssertionError("no API in no-op staging")):
                    self.assertEqual(P.stage(None, None, row, None, None), row)

    def test_sso_masked_404_and_unavailable_post_readback_do_not_push(self):
        with patch.object(self.api, "request", return_value=(404, {}, {"X-GitHub-SSO": "required"})) as request:
            with self.assertRaises(ValueError):
                P.ensure_destination(self.api.repository, self.api)
            self.assertEqual(request.call_count, 1)
        self.api.on_create = lambda: setattr(self.api, "get_status", 503)
        with self.assertRaises(ValueError):
            P.ensure_destination(self.api.repository, self.api)
        self.assertEqual(sum(c[0] == "POST" for c in self.api.calls), 1)

    def test_provision_failure_prevents_push_and_has_redacted_diagnostic(self):
        row = {"status": "STAGED", "destination": "https://github.com/" + self.api.repository + ".git",
               "tag": "v1.0.0", "staging": "unused"}
        with patch.object(P, "ensure_destination", side_effect=ValueError("PRIVATE_SENTINEL")), \
                patch.object(P, "remote_refs", side_effect=ValueError("Git unavailable")), \
                patch.object(P, "git", side_effect=AssertionError("no push")):
            result = P.finalize(row, destination_api=self.api)
        self.assertEqual(result["status"], "FAILED_OR_PENDING")
        self.assertEqual(P.operator_diagnostic(result)[0], "DESTINATION_PROVISIONING_PENDING")
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(result))

    def test_git_failure_and_ambiguous_rest_never_stage_or_push(self):
        destination = "https://github.com/" + self.api.repository + ".git"
        for status in (0, 301, 403, 429, 503):
            with self.subTest(status=status), \
                    patch.object(P, "remote_refs", side_effect=ValueError("Git unavailable")), \
                    patch.object(P, "git", side_effect=AssertionError("no push")), \
                    patch.object(P, "DestinationAPI", return_value=self.api), \
                    patch.object(self.api, "request", return_value=(status, {}, {})) as request:
                row = {"status": "READY", "version": "1.0.0", "destination": destination}
                with self.assertRaises(ValueError):
                    P.stage(None, {"destination": destination}, row, None, None)
                row.update(status="STAGED", tag="v1.0.0", staging="unused")
                self.assertEqual(P.finalize(row, destination_api=self.api)["status"], "FAILED_OR_PENDING")
                self.assertTrue(all(call.args[0] == "GET" for call in request.call_args_list))
                self.assertFalse(any(c[0] == "POST" for c in self.api.calls))

    def test_api_status_and_transport_are_redacted_and_redirects_disabled(self):
        api = P.DestinationAPI("PRIVATE_TOKEN_SENTINEL")
        opener = unittest.mock.Mock()
        opener.open.side_effect = urllib.error.HTTPError("https://api.github.com/hidden", 403, "private", {}, None)
        with patch.object(P.urllib.request, "build_opener", return_value=opener) as build:
            self.assertEqual(api.request("GET", "repos/hidden/repo"), (403, {}, {}))
            handler = build.call_args.args[0]()
            self.assertIsNone(handler.redirect_request(None, None, 301, "", {}, "https://example.invalid"))
            request = opener.open.call_args.args[0]
            self.assertEqual(request.get_header("Authorization"), "Bearer PRIVATE_TOKEN_SENTINEL")
        opener.open.side_effect = OSError("PRIVATE_TOKEN_SENTINEL")
        with patch.object(P.urllib.request, "build_opener", return_value=opener):
            self.assertEqual(api.request("POST", "orgs/jrs-vibevm/repos", {}), (0, {}, {}))


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
        return P.plan(self.source, revision or self.revision, "main", self.binding, self.api, "binding.json")

    def remote(self, number):
        destination = self.directory / (self.packages[number]["coordinate"].split("/")[1] + ".git")
        self.git("init", "-q", "--bare", "--initial-branch=main", str(destination))
        return destination


class PackageOnboardingTests(Fixture):
    def bind_only_a(self):
        self.binding["packages"] = self.packages[:1]
        self.save_binding()
        return self.change(1, "1.0.1")

    def test_existing_unbound_b_added_to_a_binding_is_noop(self):
        self.bind_only_a()
        self.binding["packages"] = self.packages
        self.save_binding()
        onboarding = self.commit()
        with patch.object(self.api, "pages", wraps=self.api.pages) as pages, \
                patch.object(P, "remote_refs", side_effect=AssertionError("no destination for onboarding")):
            report = self.plan(onboarding)
        self.assertEqual([r["status"] for r in report["packages"]], ["NO_PACKAGE_CHANGE"] * 2)
        pages.assert_not_called()
        # Unchanged old B also needs no retrospective rights/readiness approval.
        self.packages[1]["redistribution"] = {}
        self.save_binding()
        without_rights = self.commit()
        self.assertEqual(self.plan(without_rights)["packages"][1]["status"], "NO_PACKAGE_CHANGE")

    def test_new_binding_does_not_hide_a_same_version_rewrite_of_b(self):
        self.bind_only_a()
        self.binding["packages"] = self.packages
        self.save_binding()
        rewritten = self.change(1, "1.0.1")
        self.assertEqual(self.plan(rewritten)["packages"][1]["reason_code"], "PACKAGE_VERSION_REUSE")

    def test_new_binding_and_new_version_of_existing_b_is_ready(self):
        self.bind_only_a()
        self.binding["packages"] = self.packages
        self.save_binding()
        versioned = self.change(1, "1.0.2")
        rows = self.plan(versioned)["packages"]
        self.assertEqual([r["status"] for r in rows], ["NO_PACKAGE_CHANGE", "READY"])
        self.assertEqual(rows[1]["acceptance"][0]["source_sha"], versioned)

    def test_genuinely_new_b_can_publish_when_first_added_to_a_binding(self):
        self.binding["packages"] = self.packages[:1]
        self.save_binding()
        root = self.packages[1]["root"]
        self.git("rm", "-r", root)
        self.commit()
        self.git("restore", "--source", self.revision, "--", root)
        self.binding["packages"] = self.packages
        self.save_binding()
        introduced = self.change(1, "1.0.1")
        rows = self.plan(introduced)["packages"]
        self.assertEqual([r["status"] for r in rows], ["NO_PACKAGE_CHANGE", "READY"])
        self.assertEqual(rows[1]["version"], "1.0.1")


class PackageSelectionTests(Fixture):
    public_destinations = True

    def invoke(self, operation, revision, selected, extra=()):
        report = self.directory / (operation + "-selected.json")
        command = ["publisher.py", operation, "--source", str(self.source),
                   "--source-sha", revision, "--main", "main", "--binding", "binding.json",
                   "--package", selected, "--report", str(report), *extra]
        with patch.object(sys, "argv", command), patch("sys.stdout", new=io.StringIO()):
            code = P.main()
        return code, json.loads(report.read_text())

    def test_selected_noop_b_skips_changed_a_in_plan_check_and_stage(self):
        self.git("branch", "accepted", self.revision)
        changed = self.change(0)
        a, b = [p["coordinate"] for p in self.packages]
        snapshot = P.snapshot
        def selected_snapshot(root, revision, package, require_ready=True):
            self.assertNotEqual(package["coordinate"], a, "selected B must not inspect sibling A")
            self.assertFalse(require_ready, "no release readiness for unchanged B")
            return snapshot(root, revision, package, require_ready=require_ready)
        with patch.object(P, "snapshot", side_effect=selected_snapshot), \
                patch.object(P.GitHub, "get", side_effect=AssertionError("no API for selected no-op")), \
                patch.object(P.GitHub, "pages", side_effect=AssertionError("no CI for selected no-op")), \
                patch.object(P, "verify_trigger", side_effect=AssertionError("no trigger for selected no-op")), \
                patch.object(P, "remote_refs", side_effect=AssertionError("no destination for selected no-op")), \
                patch.object(P, "included_dependencies", side_effect=AssertionError("no native readiness")):
            for operation in ("plan", "check", "stage"):
                with self.subTest(operation=operation):
                    extra = (["--base", self.revision, "--main", "accepted"] if operation == "check"
                             else ["--directory", str(self.directory / "unused-stage"),
                                   "--vibe", str(self.directory / "absent-vibe")] if operation == "stage" else [])
                    code, report = self.invoke(operation, changed, b, extra)
                    self.assertEqual(code, 0)
                    self.assertEqual([(p["package"], p["status"]) for p in report["packages"]], [(b, "NO_PACKAGE_CHANGE")])
        self.assertFalse((self.directory / "unused-stage").exists())

    def test_selected_changed_a_requires_current_ci_and_trigger(self):
        changed = self.change(0)
        a = self.packages[0]["coordinate"]
        event = self.directory / "event.json"
        event.write_text(json.dumps({"workflow_run": {"id": 987}}))
        run = self.api.pages("actions/runs?head_sha=" + changed)[0]
        with patch.dict(os.environ, GITHUB_EVENT_NAME="workflow_run", GITHUB_EVENT_PATH=str(event)), \
                patch.object(P, "GitHub", return_value=self.api), \
                patch.object(self.api, "pages", wraps=self.api.pages) as pages, \
                patch.object(self.api, "get", return_value=run) as get:
            code, report = self.invoke("plan", changed, a)
            self.assertEqual(code, 0)
            self.assertEqual([(p["package"], p["status"]) for p in report["packages"]], [(a, "READY")])
            self.assertIn("head_sha=" + changed, pages.call_args.args[0])
            get.assert_called_once_with("actions/runs/987")
            get.reset_mock()
            self.api.alter_run = lambda run: dict(run, head_sha=self.revision)
            code, report = self.invoke("plan", changed, a)
            self.assertEqual(code, 1)
            self.assertEqual(report["packages"][0]["reason_code"], "MATCHING_SOURCE_CI_MISSING")
            get.assert_not_called()
            self.api.alter_run = lambda run: run
            get.return_value = dict(run, head_sha=self.revision)
            with self.assertRaisesRegex(P.AuthorizationError, "automatic trigger"):
                self.invoke("plan", changed, a)

    def test_unknown_selection_fails_before_package_evidence(self):
        with patch.object(P.GitHub, "pages", side_effect=AssertionError("no sibling CI")), \
                patch.object(P, "snapshot", side_effect=AssertionError("no sibling export")):
            with self.assertRaisesRegex(ValueError, "selected package is absent"):
                self.invoke("plan", self.revision, "org.fixture/absent")


class PlanningTests(Fixture):
    def test_integration_methods_use_only_current_push_ci(self):
        self.binding.pop("acceptance")
        self.binding.pop("authorized_integrators")
        for package in self.packages:
            package.pop("baseline")
        self.save_binding()
        self.commit()
        with patch.object(self.api, "get", side_effect=AssertionError("no PR/integrator API")):
            for route, version in (("direct", "1.0.1"), ("squash", "1.0.2"),
                                   ("merge", "1.0.3"), ("rebase", "1.0.4")):
                with self.subTest(route=route):
                    if route == "direct":
                        accepted = self.change(version=version)
                    else:
                        self.git("switch", "-qc", "candidate-" + route)
                        self.change(version=version)
                        if route == "rebase":
                            self.git("switch", "main")
                            (self.source / "fact.txt").write_text(route)
                            self.commit()
                            self.git("switch", "candidate-" + route)
                            self.git("rebase", "main")
                        self.git("switch", "main")
                        if route == "squash":
                            self.git("merge", "--squash", "candidate-" + route)
                            accepted = self.commit()
                        else:
                            self.git("merge", "--no-ff" if route == "merge" else "--ff-only",
                                     "-m", "Accepted fixture", "candidate-" + route)
                            accepted = self.git("rev-parse", "HEAD")
                    self.assertEqual(self.plan(accepted)["packages"][0]["status"], "READY")

    def test_invalid_version_and_unapproved_redistribution_fail(self):
        for version in ("01.0.1", "v1.0.1", "1.0", "1.0.1+private"):
            with self.subTest(version=version):
                self.git("reset", "--hard", self.revision)
                revision = self.change(version=version)
                self.assertEqual(self.plan(revision)["packages"][0]["reason_code"], "PACKAGE_IDENTITY_MISMATCH")
        self.git("reset", "--hard", self.revision)
        for rights in ({}, {"status": "pending"},
                       {"status": "approved", "license": "MIT"},
                       {"status": "approved", "license": "Apache-2.0", "approval": "https://example.com/decision"}):
            self.git("reset", "--hard", self.revision)
            self.packages[0]["redistribution"] = rights
            self.save_binding()
            revision = self.change(version="1.0.2")
            self.assertEqual(self.plan(revision)["packages"][0]["reason_code"], "REDISTRIBUTION_UNRESOLVED")

    def test_two_independent_initial_versions(self):
        report = self.plan()
        self.assertEqual([row["version"] for row in report["packages"]], ["1.0.0", "1.0.0"])
        self.assertEqual([row["status"] for row in report["packages"]], ["READY", "READY"])
        self.assertEqual(report["packages"][0]["acceptance"][0]["source_sha"], self.revision)

    def test_a_only_change_leaves_b_noop(self):
        changed = self.change()
        self.api.revisions.append(changed)
        self.assertEqual([row["status"] for row in self.plan(changed)["packages"]],
                         ["READY", "NO_PACKAGE_CHANGE"])


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



    def test_reused_version_is_rejected(self):
        readme = self.source / self.packages[0]["root"] / "README.md"
        readme.write_text("Changed without bump")
        changed = self.commit()
        self.api.revisions.append(changed)
        self.assertIn("without a new version", self.plan(changed)["packages"][0]["reason"])


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
        with self.assertRaisesRegex(ValueError, "dependency slot"):
            P.snapshot(self.source, self.commit(), self.packages[0])
        self.packages[1]["files"].remove("LICENSE")
        (self.source / "binding.json").write_text(json.dumps(self.binding))
        policy = self.commit()
        with self.assertRaisesRegex(ValueError, "license"):
            P.binding_at(self.source, policy, "binding.json", allow_local=True)

    def test_thin_dependency_failure_guides_source_evidence_in_operator_outputs(self):
        manifest = self.source / self.packages[0]["root"] / "vibe.toml"
        manifest.write_text(manifest.read_text() + '\n[requires.packages]\n"org.fixture/dep" = "=1.0.0"\n')
        self.revision = self.change()
        report = self.plan()
        row = report["packages"][0]
        self.assertEqual(row["status"], "AUTHORIZATION_PENDING")
        code, message = P.operator_diagnostic(row)
        self.assertEqual(code, "DEPENDENCY_CLOSURE_UNQUALIFIED")

        report_path = self.directory / "publication.json"
        summary_path = self.directory / "summary.md"
        with patch("builtins.print") as output:
            P.write_report(report, report_path)
        log_text = "\n".join(call.args[0] for call in output.call_args_list)
        P.append_actions_summary(report_path, summary_path, "success", {"plan": "success"})
        summary = summary_path.read_text(encoding="utf-8")
        for text in (message, log_text, summary):
            with self.subTest(output=text):
                self.assertIn("frozen native closure with pinned VibeVM", text)
                self.assertIn("vibe.lock", text)
                self.assertIn("complete materialized dependency slots", text)
                self.assertIn("selected package source root at the exact source SHA", text)
                self.assertIn("producer-approved files", text)
                self.assertIn("Thin packages need not export dependency slots", text)
                self.assertIn("deliberately vendored slots require complete shipped inventories", text)
                self.assertNotIn("approve its complete export inventory", text)
        self.assertIn(code, log_text)
        self.assertIn(code, summary)
        self.assertIn("**AUTHORIZATION_PENDING**", summary)

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

    def test_incomplete_historical_package_factual_and_candidate_noops(self):
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
        # Candidate non-package changes also request no release; unchanged older
        # incomplete content must not acquire a retrospective readiness gate.
        self.git("switch", "-qc", "candidate")
        (self.source / "research.txt").write_text("Candidate factual update")
        proposed = self.commit()
        self.assertEqual(self.candidate(proposed, factual)["status"], "NO_PACKAGE_CHANGE")

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


    def candidate(self, revision, base=None):
        with patch.object(self.api, "get", side_effect=AssertionError("source checks do not grant acceptance")):
            return P.plan(self.source, revision, base or self.revision, self.binding, self.api,
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
        self.assertEqual([e["source_sha"] for e in result["acceptance"]], [accepted])
        self.assertEqual(self.git("tag"), "")
        # Historical incompleteness is comparable; only current push CI is needed.
        self.api.revisions.remove(self.revision)
        self.assertEqual(self.plan(accepted)["packages"][0]["status"], "READY")


    def test_source_check_rejects_a_stale_main_baseline(self):
        changed = self.change()
        with self.assertRaisesRegex(ValueError, "current accepted"):
            P.plan(self.source, changed, "main", self.binding, self.api,
                   "binding.json", self.revision)




class SourceCliTests(Fixture):
    public_destinations = True

    def test_ordinary_noop_cli_needs_no_other_sha_or_ci_event_access(self):
        (self.source / "notes.txt").write_text("Non-package source evidence")
        revision = self.commit()
        report = self.directory / "noop.json"
        command = [sys.executable, str(Path(P.__file__)), "plan",
                   "--source", str(self.source), "--source-sha", revision,
                   "--main", "main", "--binding", "binding.json", "--report", str(report)]
        result = subprocess.run(command, capture_output=True, text=True,
            env=dict(self.env, GH_TOKEN="", GITHUB_EVENT_NAME="workflow_run",
                     GITHUB_EVENT_PATH=str(self.directory / "absent-event.json")))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([p["status"] for p in json.loads(report.read_text())["packages"]],
                         ["NO_PACKAGE_CHANGE"] * 2)
        self.assertEqual(json.loads(report.read_text())["publisher"]["sha"],
                         P.git(P.ROOT, "rev-parse", "HEAD").decode().strip())

    def test_finalize_rejects_report_from_different_implementation_before_destination_access(self):
        report = self.directory / "mismatched.json"
        for identity in (None, {"repository": "jresearchsoftware/shared-governance", "sha": "0" * 40}):
            report.write_text(json.dumps({"publisher": identity, "packages": [{"status": "STAGED"}]}))
            result = subprocess.run([sys.executable, str(Path(P.__file__)), "finalize", "--report", str(report)],
                                    env=self.env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(report.read_text())["packages"][0]["status"], "STAGED")
        report.write_text(json.dumps({"publisher": {"repository": "jresearchsoftware/shared-governance",
                                                   "sha": P.git(P.ROOT, "rev-parse", "HEAD").decode().strip()},
                                      "packages": [{"package": "org.fixture/noop", "status": "NO_PACKAGE_CHANGE"}]}))
        result = subprocess.run([sys.executable, str(Path(P.__file__)), "finalize", "--report", str(report)],
                                env=self.env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_source_time_cli_validates_a_candidate_without_api_or_distribution(self):
        self.git("switch", "-qc", "candidate")
        changed = self.change()
        report = self.directory / "candidate.json"
        result = subprocess.run([sys.executable, str(Path(P.__file__)), "check",
            "--source", str(self.source), "--source-sha", changed, "--main", "main",
            "--base", self.revision,
            "--binding", "binding.json", "--report", str(report)],
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
             "reason": "Publication readback unavailable; inspect and retry the same source SHA and workflow implementation pin."},
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
            self.assertIn("Resolve the listed source, CI, readiness or explicit initial-publication", summary)
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

    def test_existing_git_destination_stages_and_finalizes_without_rest(self):
        local = self.directory / "existing-distribution.git"
        self.git("init", "-q", "--bare", "--initial-branch=main", str(local))
        api = DestinationEvidence(exists=True)
        destination = "https://github.com/" + api.repository + ".git"
        self.packages[0]["destination"] = destination
        self.save_binding()
        self.commit()
        original_git = P.git

        def mapped_git(root, *args):
            return original_git(root, *(local.as_uri() if arg == destination else arg for arg in args))

        for index, status in enumerate((403, 429, 503, 0)):
            with self.subTest(rest_status=status):
                api.get_status = status
                api.calls.clear()
                self.revision = self.change(0, version="1.0." + str(index + 1))
                with patch.object(P, "git", side_effect=mapped_git), \
                        patch.object(P, "DestinationAPI", return_value=api):
                    staged = self.stage(suffix="existing-" + str(index))
                    self.assertEqual(staged["status"], "STAGED")
                    published = P.finalize(staged, destination_api=api)
                    self.assertEqual(published["status"], "PUBLISHED")
                    self.assertEqual(P.finalize(staged, destination_api=api)["status"], "ALREADY_PUBLISHED")
                    # The stage retry must also skip the retained tag before native work.
                    self.assertEqual(self.stage(suffix="retained-" + str(index))["status"], "ALREADY_PUBLISHED")
                self.assertEqual(api.calls, [])
                self.assertEqual(self.git("rev-parse", "refs/tags/" + staged["tag"], cwd=local), staged["expected_tag"])

    def test_native_absent_destination_stages_before_create_and_atomic_first_push(self):
        api = DestinationEvidence()
        destination = "https://github.com/" + api.repository + ".git"
        local = self.directory / "new-distribution.git"
        self.packages[0]["destination"] = destination
        self.save_binding()
        self.commit()  # Accepted mapping precedes this package transition.
        self.revision = self.change(0)
        row = self.plan()["packages"][0]
        original_refs, original_git = P.remote_refs, P.git

        def mapped_refs(url, tag):
            return original_refs(local.as_uri() if url == destination else url, tag)

        def push(root, *args):
            self.assertEqual(args[:3], ("push", "--atomic", "--"))
            self.assertEqual(args[3], destination)
            return original_git(root, *args[:3], local.as_uri(), *args[4:])

        with patch.object(P, "destination_exists", return_value=False), \
                patch.object(P, "remote_refs", side_effect=mapped_refs):
            staged = P.stage(self.source, self.packages[0], row, VIBE, self.directory / "absent-stage")
        self.assertEqual(staged["status"], "STAGED")
        self.assertFalse(local.exists())
        self.assertEqual(api.calls, [])
        api.on_create = lambda: self.git("init", "-q", "--bare", "--initial-branch=main", str(local))
        def fail_push(*args):
            raise ValueError("injected transport failure before push")

        with patch.object(P, "remote_refs", side_effect=mapped_refs):
            self.assertEqual(P.finalize(staged, push=fail_push, destination_api=api)["status"], "FAILED_OR_PENDING")
            self.assertTrue(local.exists())
            published = P.finalize(staged, push=push, destination_api=api)
        self.assertEqual(published["status"], "PUBLISHED")
        self.assertEqual(sum(c[0] == "POST" for c in api.calls), 1)
        self.assertEqual(self.git("rev-parse", "refs/tags/v1.0.1", cwd=local), staged["expected_tag"])
        api.calls.clear()
        with patch.object(P, "remote_refs", side_effect=mapped_refs):
            self.assertEqual(P.finalize(staged, push=push, destination_api=api)["status"], "ALREADY_PUBLISHED")
        self.assertEqual(api.calls, [])

    def test_native_failure_on_absent_destination_cannot_create(self):
        api = DestinationEvidence()
        self.packages[0]["destination"] = "https://github.com/" + api.repository + ".git"
        self.save_binding()
        self.commit()
        self.revision = self.change(0)
        row = self.plan()["packages"][0]
        original_run = P.subprocess.run

        def fail_native(command, *args, **kwargs):
            if command[0] == str(VIBE):
                self.assertNotIn("PUBLISH_TOKEN", kwargs["env"])
                return subprocess.CompletedProcess(command, 1)
            return original_run(command, *args, **kwargs)

        original_refs = P.remote_refs
        def missing_destination(url, tag):
            if url == self.packages[0]["destination"]:
                raise ValueError("Git unavailable")
            return original_refs(url, tag)

        with patch.object(P, "destination_exists", return_value=False), \
                patch.object(P, "remote_refs", side_effect=missing_destination), \
                patch.object(P.subprocess, "run", side_effect=fail_native), \
                patch.object(P, "ensure_destination", side_effect=AssertionError("no provisioning in stage")):
            with self.assertRaisesRegex(ValueError, "native staging failed"):
                P.stage(self.source, self.packages[0], row, VIBE, self.directory / "failed-absent-stage")
        self.assertEqual(api.calls, [])

    def test_native_selected_b_stages_its_own_payload_and_destination(self):
        self.revision = self.change(1)
        b = self.packages[1]["coordinate"]
        report = P.plan(self.source, self.revision, "main", self.binding, self.api,
                        "binding.json", selected=b)
        self.assertEqual([r["package"] for r in report["packages"]], [b])
        staged = P.stage_all(self.source, self.binding, report, VIBE,
                             self.directory / "selected-b", b)["packages"][0]
        self.assertEqual(staged["destination"], self.packages[1]["destination"])
        self.assertEqual(P.finalize(staged)["status"], "PUBLISHED")
        files = P.snapshot(self.source, self.revision, self.packages[1])[0]
        for path, data in files.items():
            self.assertEqual(P.git(Path(staged["staging"]), "show", "v1.0.1:" + path), data)
        self.assertEqual(P.remote_refs(self.packages[0]["destination"], "v1.0.1"), [])

    def native_dependencies(self, mutable=False, vendored=True):
        registry, consumer = self.directory / "registry", self.directory / "consumer"
        consumer.mkdir()
        for name in ("direct", "transitive"):
            target = registry / "org.fixture" / name / "v1.0.0"
            target.mkdir(parents=True)
            text = ('[package]\ngroup="org.fixture"\nname="' + name + '"\nversion="1.0.0"\n'
                    'kind="flow"\nformat="simple"\nepoch=1\nlicense="MIT"\npublish=false\n'
                    'frozen=' + ("false" if mutable and name == "transitive" else "true") + '\n')
            if name == "direct":
                text += '\n[requires.packages]\n"org.fixture/transitive"="=1.0.0"\n'
            (target / "vibe.toml").write_text(text)
        (consumer / "vibe.toml").write_text('[project]\nname="deps"\nversion="0.0.0"\nspec_format="mixed"\n'
            '[requires.packages]\n"org.fixture/direct"="=1.0.0"\n')
        result = subprocess.run([str(VIBE), "--offline", "--json", "install", "--path", str(consumer),
            "--registry", str(registry), "--assume-yes", "--no-default-registry"],
            env=P.native_environment(self.directory), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        package = self.packages[0]
        target = self.source / package["root"]
        for path in consumer.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(consumer).as_posix()
            if relative != "vibe.lock" and not relative.startswith("vibevm/vibedeps/"):
                continue
            output = target / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(path.read_bytes())
            if vendored:
                package["files"].append(relative)
        manifest = target / "vibe.toml"
        manifest.write_text(manifest.read_text() + '\n[requires.packages]\n"org.fixture/direct"="=1.0.0"\n')
        self.save_binding()
        self.revision = self.change()

    def test_native_thin_release_cold_install_and_update(self):
        self.native_release_consumer(vendored=False)

    def test_native_vendored_release_cold_install_and_update(self):
        self.native_release_consumer(vendored=True)

    def native_release_consumer(self, vendored):
        self.native_dependencies(vendored=vendored)
        staged = self.stage()
        self.assertEqual(P.finalize(staged)["status"], "PUBLISHED")
        paths = self.git("ls-tree", "-r", "--name-only", "v1.0.1", cwd=Path(staged["staging"]))
        if vendored:
            self.assertIn("vibevm/vibedeps/org.fixture.direct/1.0.0/vibe.toml", paths.splitlines())
        else:
            self.assertEqual(set(paths.splitlines()), {"vibe.toml", "README.md", "LICENSE", "DISTRIBUTION.json"})
        consumer = self.directory / "cold"
        consumer.mkdir()
        remotes = self.directory / "dependency-remotes"
        remotes.mkdir()
        for name in ("direct", "transitive"):
            remote = remotes / ("org.fixture." + name + ".git")
            self.git("init", "-q", "--bare", "--initial-branch=main", str(remote))
            result = subprocess.run([str(VIBE), "--json", "registry", "publish",
                str(self.directory / "registry/org.fixture" / name / "v1.0.0"),
                "--repo-url", remote.as_uri()], env=P.native_environment(self.directory / "deps-publish"),
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        coordinate = self.packages[0]["coordinate"]
        manifest = consumer / "vibe.toml"
        manifest.write_text('[project]\nname="cold"\nversion="0.0.0"\nspec_format="mixed"\n'
            '[requires.packages]\n"' + coordinate + '"={git="' + self.packages[0]["destination"] +
            '", tag="v1.0.1", version="=1.0.1"}\n'
            '[[registry]]\nname="fixture"\nurl="' + str(remotes) + '"\n')
        env = P.native_environment(self.directory / "cold-settings")
        for operation in ("install", "install", "update"):
            if operation == "update":
                self.revision = self.change(version="1.0.2")
                updated = self.stage(suffix="thin-update")
                self.assertEqual(P.finalize(updated)["status"], "PUBLISHED")
                manifest.write_text(manifest.read_text().replace("1.0.1", "1.0.2"))
            command = [str(VIBE), "--json", operation, "--path", str(consumer)]
            if operation == "install":
                command += ["--no-default-registry", "--no-prefer-local", "--assume-yes"]
            result = subprocess.run(command, cwd=consumer, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, operation + ": " + result.stdout + result.stderr)
            lock = tomllib.loads((consumer / "vibe.lock").read_text())
            self.assertEqual({e["name"] for e in lock["package"]},
                             {coordinate.split("/")[1], "direct", "transitive"})
            self.assertEqual(next(e["version"] for e in lock["package"] if e["name"] == coordinate.split("/")[1]),
                             "1.0.2" if operation == "update" else "1.0.1")
            evidence = {p.relative_to(consumer).as_posix(): p.read_bytes()
                        for p in consumer.rglob("*") if p.is_file()}
            P.included_dependencies({}, tomllib.loads(manifest.read_text()), evidence)
            for name in ("direct", "transitive"):
                installed = consumer / "vibevm/vibedeps" / ("org.fixture." + name) / "1.0.0/vibe.toml"
                self.assertEqual(installed.read_bytes(),
                    (self.directory / "registry/org.fixture" / name / "v1.0.0/vibe.toml").read_bytes())

    def test_native_thin_missing_or_tampered_source_evidence_rejected(self):
        self.native_dependencies(vendored=False)
        root = self.source / self.packages[0]["root"]
        slot = root / "vibevm/vibedeps/org.fixture.transitive/1.0.0/vibe.toml"
        original = slot.read_bytes()
        slot.write_bytes(original + b"\n# drift\n")
        # Uncommitted worktree drift cannot alter exact-source qualification.
        self.assertEqual(self.plan()["packages"][0]["status"], "READY")
        self.revision = self.change(version="1.0.2")
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")
        slot.unlink()
        self.revision = self.change(version="1.0.3")
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")

    def test_native_partial_vendoring_cannot_borrow_unexported_slot_bytes(self):
        self.native_dependencies()
        self.packages[0]["files"].remove("vibevm/vibedeps/org.fixture.direct/1.0.0/.vibe-slot.toml")
        self.save_binding()
        self.revision = self.change(version="1.0.2")
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")

    def test_native_thin_mutable_closure_rejected(self):
        self.native_dependencies(mutable=True, vendored=False)
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")

    def test_native_unused_source_slots_do_not_enter_thin_closure(self):
        self.native_dependencies(mutable=True, vendored=False)
        manifest = self.source / self.packages[0]["root"] / "vibe.toml"
        manifest.write_text(manifest.read_text().replace("[requires.packages]", "[dev-requires.packages]"))
        self.revision = self.change(version="1.0.2")
        self.assertEqual(self.plan()["packages"][0]["status"], "READY")

    def test_native_thin_stale_exact_lock_rejected(self):
        self.native_dependencies(vendored=False)
        manifest = self.source / self.packages[0]["root"] / "vibe.toml"
        manifest.write_text(manifest.read_text().replace('"org.fixture/direct"="=1.0.0"',
                                                           '"org.fixture/direct"="=2.0.0"'))
        self.revision = self.change(version="1.0.2")
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")

    def test_native_direct_transitive_dependency_release(self):
        self.native_dependencies()
        staged = self.stage()
        self.assertEqual(staged["status"], "STAGED")
        self.assertEqual(P.finalize(staged)["status"], "PUBLISHED")
        paths = self.git("ls-tree", "-r", "--name-only", "v1.0.1", cwd=Path(staged["staging"]))
        self.assertIn("org.fixture.direct/1.0.0/vibe.toml", paths)
        self.assertIn("org.fixture.transitive/1.0.0/vibe.toml", paths)
        files = P.snapshot(self.source, self.revision, self.packages[0])[0]
        for path, data in files.items():
            self.assertEqual(P.git(Path(staged["staging"]), "show", "v1.0.1:" + path), data)

    def test_native_included_mutable_or_unresolved_closure_rejected(self):
        self.native_dependencies(mutable=True)
        row = self.plan()["packages"][0]
        self.assertEqual(row["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")
        # Missing source transitive slot fails even with valid direct metadata.
        self.packages[0]["files"] = [f for f in self.packages[0]["files"]
                                     if "org.fixture.transitive/" not in f]
        self.save_binding()
        (self.source / self.packages[0]["root"] /
         "vibevm/vibedeps/org.fixture.transitive/1.0.0/vibe.toml").unlink()
        self.revision = self.change(version="1.0.2")
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")

    def test_native_included_hash_and_inventory_evidence_is_required(self):
        self.native_dependencies()
        root = self.source / self.packages[0]["root"]
        marker = root / "vibevm/vibedeps/org.fixture.direct/1.0.0/.vibe-slot.toml"
        marker.write_text(marker.read_text().replace('source_hash = "sha256:', 'source_hash = "sha256:0'))
        self.revision = self.change(version="1.0.2")
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")

    def test_included_dependency_is_checked_even_when_labelled_development_only(self):
        self.native_dependencies(mutable=True)
        path = self.source / self.packages[0]["root"] / "vibe.toml"
        path.write_text(path.read_text().replace("[requires.packages]", "[dev-requires.packages]"))
        self.revision = self.change(version="1.0.2")
        self.assertEqual(self.plan()["packages"][0]["reason_code"], "DEPENDENCY_CLOSURE_UNQUALIFIED")

    def test_nonincluded_dev_optional_planning_and_native_schema_limit(self):
        manifest = self.source / self.packages[0]["root"] / "vibe.toml"
        manifest.write_text(manifest.read_text() + '\n[dev-requires.packages]\n"org.fixture/dev"="*"\n'
            '[requires.packages]\n"org.fixture/optional"={version="*", optional=true}\n')
        self.revision = self.change()
        self.assertEqual(self.plan()["packages"][0]["status"], "READY")
        # VibeVM 1.0.7 itself cannot parse dev-requires/optional=true. Do not
        # rewrite frozen manifests to hide this upstream schema limitation.
        with self.assertRaisesRegex(ValueError, "native staging failed"):
            self.stage()

    def test_native_excluded_optional_suggestion_publishes(self):
        manifest = self.source / self.packages[0]["root"] / "vibe.toml"
        manifest.write_text(manifest.read_text() + '\n[suggests]\npackages=["flow:org.fixture/unused@*"]\n')
        self.revision = self.change()
        self.assertEqual(P.finalize(self.stage())["status"], "PUBLISHED")

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
                              self.binding, self.api, "binding.json")

    def test_initial_selected_b_retains_its_acceptance_without_inspecting_a(self):
        a, b = [p["coordinate"] for p in self.packages]
        snapshot = P.snapshot
        def selected_snapshot(root, revision, package, require_ready=True):
            self.assertNotEqual(package["coordinate"], a, "initial selected B must not inspect A")
            return snapshot(root, revision, package, require_ready=require_ready)
        with patch.object(P, "snapshot", side_effect=selected_snapshot):
            report = P.initial_plan(self.source, self.initiation, self.main, self.binding,
                                    self.api, "binding.json", selected=b)
        self.assertEqual([(r["package"], r["status"]) for r in report["packages"]], [(b, "READY")])
        row = report["packages"][0]
        self.assertEqual(row["source_acceptance"]["source_sha"], self.frozen)
        self.assertEqual(row["readiness_acceptance"]["source_sha"], self.initiation)

    def test_late_onboarding_then_generic_102_103_without_historical_evidence(self):
        # The ordinary producer supplies neither baseline nor PR/integrator
        # attestations. The explicit Task 49 route is tested separately.
        for key in ("acceptance", "authorized_integrators"):
            self.binding.pop(key)
        for package in self.packages:
            for key in ("baseline", "baseline_disposition", "initial_publication"):
                package.pop(key)
            package["redistribution"] = {}
        self.save_binding()
        onboarding = self.commit()
        def ordinary(revision):
            return P.plan(self.source, revision, self.main, self.binding, self.api, "binding.json")
        with patch.object(self.api, "get", side_effect=AssertionError("no PR/identity lookup")), \
                patch.object(self.api, "pages", side_effect=AssertionError("no CI for no-op")), \
                patch.object(P, "remote_refs", side_effect=AssertionError("no destination for no-op")):
            self.assertEqual([r["status"] for r in ordinary(onboarding)["packages"]], ["NO_PACKAGE_CHANGE"] * 2)
            (self.source / "notes.txt").write_text("non-package commit")
            factual = self.commit()
            self.assertEqual([r["status"] for r in ordinary(factual)["packages"]], ["NO_PACKAGE_CHANGE"] * 2)
        for package in self.packages:
            package["redistribution"] = {"status": "approved", "license": "MIT",
                                       "approval": "https://github.com/fixture/private-source/issues/1"}
        self.save_binding()
        self.commit()
        with patch.object(self.api, "get", side_effect=AssertionError("no PR/identity lookup")):
            for version in ("1.0.2", "1.0.3"):
                changed = self.change(version=version)
                calls = []
                pages = self.api.pages
                def current_ci(path, key=None):
                    calls.append(path)
                    self.assertIn("head_sha=" + changed, path)
                    return pages(path, key)
                with patch.object(self.api, "pages", side_effect=current_ci):
                    rows = ordinary(changed)["packages"]
                self.assertEqual([r["status"] for r in rows], ["READY", "NO_PACKAGE_CHANGE"])
                self.assertEqual(len(calls), 1)
                self.assertEqual(rows[0]["source_sha"], changed)
                self.assertEqual(rows[0]["version"], version)
            # Moving main and worktree policy cannot change the selected run.
            selected = changed
            self.binding["ci_workflow"] = ".github/workflows/later.yml"
            self.save_binding()
            self.change(version="1.0.4")
            frozen_binding = P.binding_at(self.source, selected, "binding.json", allow_local=True)
            self.assertEqual(P.plan(self.source, selected, self.main, frozen_binding,
                                   self.api, "binding.json")["packages"][0]["version"], "1.0.3")

    @unittest.skipUnless(VIBE, "pass --vibe for pinned Linux native staging")
    def test_late_onboarding_future_versions_native_publish_and_retry(self):
        with patch.dict(os.environ, self.env):
            self.remote(0)
            for version in ("1.0.2", "1.0.3"):
                changed = self.change(version=version)
                report = P.plan(self.source, changed, self.main, self.binding, self.api, "binding.json")
                row = report["packages"][0]
                self.assertEqual(row["status"], "READY")
                staged = P.stage(self.source, self.packages[0], row, VIBE, self.directory / version)
                self.assertEqual(P.finalize(staged)["status"], "PUBLISHED")
                self.assertEqual(P.stage(self.source, self.packages[0], row, None, None)["status"], "ALREADY_PUBLISHED")
            tags = self.git("tag", cwd=Path(self.packages[0]["destination"].removeprefix("file://")))
            self.assertEqual(tags.splitlines(), ["v1.0.2", "v1.0.3"])

    def amend_binding(self):
        self.git("reset", "--soft", self.frozen)
        self.save_binding()
        self.initiation = self.commit()
        self.api.revisions[-1] = self.initiation

    def test_current_baseline_disposition_alone_does_not_publish(self):
        report = P.plan(self.source, self.initiation, self.main, self.binding, self.api, "binding.json")
        self.assertEqual([p["status"] for p in report["packages"]], ["NO_PACKAGE_CHANGE"] * 2)
        (self.source / "research.txt").write_text("Unrelated direct-main evidence")
        revision = self.commit()
        report = P.plan(self.source, revision, self.main, self.binding, self.api, "binding.json")
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

    def test_initial_acceptance_contract_remains_isolated_and_required(self):
        self.binding["acceptance"] = "unsupported"
        self.amend_binding()
        self.assertEqual(self.initial()["packages"][0]["reason_code"], "PRODUCER_BINDING_UNSUPPORTED")
        self.binding["acceptance"] = "owner-squash-attestation-v1"
        self.binding.pop("authorized_integrators")
        self.amend_binding()
        self.assertEqual(self.initial()["packages"][0]["reason_code"], "PRODUCER_BINDING_UNSUPPORTED")

    def test_initial_candidate_check_is_offline_and_cannot_authorize_staging(self):
        self.git("branch", "accepted", self.frozen)
        with patch.object(self.api, "get", side_effect=AssertionError("candidate checks are offline")):
            report = P.initial_plan(self.source, self.initiation, "accepted", self.binding,
                                    self.api, "binding.json", self.frozen)
        self.assertEqual([p["status"] for p in report["packages"]], ["CANDIDATE_VALID"] * 2)
        self.assertEqual(P.stage(self.source, self.packages[0], report["packages"][0], None, None),
                         report["packages"][0])
        with self.assertRaisesRegex(ValueError, "current accepted source main"):
            P.initial_plan(self.source, self.initiation, "accepted", self.binding,
                           self.api, "binding.json", self.old)

    def test_initial_candidate_cli_uses_only_the_source_binding(self):
        for i, package in enumerate(self.packages):
            package["destination"] = "https://github.com/fixture/distribution-" + str(i) + ".git"
        self.amend_binding()
        self.git("branch", "accepted", self.frozen)
        report = self.directory / "candidate.json"
        command = [sys.executable, str(Path(P.__file__)), "check", "--initial-publication",
            "--source", str(self.source), "--source-sha", self.initiation, "--main", "accepted",
            "--base", self.frozen,
            "--binding", "binding.json", "--report", str(report)]
        result = subprocess.run(command, env=dict(self.env, GH_TOKEN="", GITHUB_EVENT_NAME="pull_request"),
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([p["status"] for p in json.loads(report.read_text())["packages"]],
                         ["CANDIDATE_VALID"] * 2)
        command[command.index("--source-sha") + 1] = self.frozen
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
        ordinary = P.plan(self.source, later, self.main, self.binding, self.api, "binding.json")
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
        for name in dir(InitialPublicationTests):
            if name.startswith("test_native_") or name == "test_late_onboarding_future_versions_native_publish_and_retry":
                method = getattr(InitialPublicationTests, name)
                setattr(InitialPublicationTests, name, method.__wrapped__)
    unittest.main(argv=[sys.argv[0], *remaining])
