#!/usr/bin/env python3
"""Bounded public Relay incident replay; distribution mutations stay local.

No token is read. Source Git objects and public push-CI run records are actual
Relay evidence. Local distribution refs are explicitly substituted fixtures.
"""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

import publisher as P

SOURCE = "10d2614372cbf578dfb552d3d62fdb8f640f7501"
FROZEN = "0aff32a6873262185f60364463f4e97ef330de89"
BINDING = "vibe-publisher.json"
ACCEPTED_PUBLISHER = "1110f10b996c2f81fa842e6339ab6d7c13111cd7"


class PublicEvidence(P.GitHub):
    def __init__(self):
        super().__init__("jresearchsoftware/codex-relay", token=None)

    def records(self):
        # Retain only fields consumed by exact-CI qualification and source URLs.
        fields = ("id", "html_url", "head_sha", "event", "head_branch", "status",
                  "conclusion", "path", "workflow_id")
        result = {}
        for path, data in self.cache.items():
            if path.startswith("actions/runs?"):
                result[path] = [dict({k: run.get(k) for k in fields},
                                    repository={"id": run["repository"]["id"]},
                                    head_repository={"id": run["head_repository"]["id"]})
                                for run in data["workflow_runs"]]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-repo", required=True, type=Path,
                        help="disposable public Relay Git clone with first-parent history")
    parser.add_argument("--vibe", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.source_repo.resolve()
    # Git remains anonymous, including native VibeVM subprocesses.
    os.environ.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null",
                      GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="/bin/false")
    api = PublicEvidence()
    binding = P.binding_at(root, SOURCE, BINDING)
    package = binding["packages"][0]
    parent = P.git(root, "rev-parse", SOURCE + "^").decode().strip()
    assert parent == FROZEN
    current_snapshot = P.snapshot(root, SOURCE, package)
    frozen_snapshot = P.snapshot(root, FROZEN, package)
    assert P.payload(current_snapshot) == P.payload(frozen_snapshot)
    assert current_snapshot[1]["version"] == "5.0.0"
    with tempfile.TemporaryDirectory(prefix="accepted-publisher-") as baseline_dir:
        baseline_path = Path(baseline_dir) / "publisher.py"
        baseline_path.write_bytes(P.git(P.ROOT, "show", ACCEPTED_PUBLISHER
                                        + ":tooling/vibe-publisher/publisher.py"))
        spec = importlib.util.spec_from_file_location("accepted_publisher", baseline_path)
        baseline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(baseline)
        baseline_plan = baseline.plan(root, SOURCE, SOURCE, binding, api, BINDING)
        assert baseline_plan["packages"][0]["status"] == "NO_PACKAGE_CHANGE", baseline_plan
    # Capture historical failure separately; it must never supply current CI.
    failed_report = P.plan(root, FROZEN, SOURCE,
                           P.binding_at(root, FROZEN, BINDING), api, BINDING)
    assert failed_report["packages"][0]["status"] == "AUTHORIZATION_PENDING", failed_report
    assert failed_report["packages"][0]["reason_code"] == "MATCHING_SOURCE_CI_MISSING", failed_report
    report = P.plan(root, SOURCE, SOURCE, binding, api, BINDING)
    decision = report["packages"][0]
    assert report["source_sha"] == SOURCE
    assert decision["status"] == "READY", decision
    assert decision["source_sha"] == FROZEN, decision
    assert decision["trigger_sha"] == SOURCE, decision
    assert decision["payload_sha256"] == frozen_snapshot[1]["payload_sha256"]
    # A denied exact current CI lookup must not fall back to an older run.
    class NoCurrentCI:
        def pages(self, path, key=None):
            return [] if SOURCE in path else api.pages(path, key)
    missing = P.plan(root, SOURCE, SOURCE, binding, NoCurrentCI(), BINDING)
    assert missing["packages"][0]["status"] == "AUTHORIZATION_PENDING", missing
    assert missing["packages"][0]["reason_code"] == "MATCHING_SOURCE_CI_MISSING", missing

    destination = package["destination"]
    # This is the sole public destination operation and is read-only.
    observed_remote = P.remote_refs(destination, "v5.0.0")
    original_git = P.git
    with tempfile.TemporaryDirectory(prefix="relay-recovery-") as temporary:
        temporary = Path(temporary)
        local = temporary / "destination.git"
        original_git(None, "init", "--bare", "--initial-branch=main", local)
        local_url = local.as_uri()
        writes = []
        def local_git(cwd, *arguments):
            mapped = tuple(local_url if str(a) == destination else a for a in arguments)
            if arguments and arguments[0] == "push":
                assert local_url in mapped and destination not in mapped
                writes.append("local atomic distribution push")
            return original_git(cwd, *mapped)
        # Source/binding stays exact; only Git transport addresses are mapped.
        with patch.object(P, "git", side_effect=local_git):
            staged = P.stage(root, package, decision, args.vibe, temporary / "stage")
            assert staged["status"] == "STAGED", staged
            result = P.finalize(staged)
            assert result["status"] == "PUBLISHED", result
            repeated = P.finalize(staged)
            assert repeated["status"] == "ALREADY_PUBLISHED", repeated
            retry = P.stage(root, package, decision, args.vibe, temporary / "retry")
            assert retry["status"] == "ALREADY_PUBLISHED", retry
            assert len(writes) == 1
            receipt = json.loads(original_git(local, "show", "v5.0.0:DISTRIBUTION.json"))
            assert receipt["source_revision"] == FROZEN
            assert receipt["payload_sha256"] == decision["payload_sha256"]
        output = {
            "observed_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_repository": binding["repository"], "binding_path": BINDING,
            "accepted_publisher_sha": ACCEPTED_PUBLISHER,
            "accepted_publisher_plan": baseline_plan,
            "trigger_source_sha": SOURCE, "first_frozen_source_sha": FROZEN,
            "public_destination_refs": observed_remote,
            "public_v5_tag_observed": bool(P.tag_oid(observed_remote, "v5.0.0")),
            "public_ci_evidence": api.records(),
            "failed_version_source_plan": failed_report,
            "current_source_plan": report,
            "missing_current_ci_plan": missing,
            "local_distribution": {
                "stage": staged["status"], "finalize": result["status"],
                "repeat_finalize": repeated["status"], "repeat_stage": retry["status"],
                "push_count": len(writes), "receipt": receipt,
            },
            "limits": ["No public destination write or consumer migration occurred.",
                       "Distribution began empty locally; it does not reproduce public destination history.",
                       "Native staging and exact-tag readback are real local operations.",
                       "GitHub Actions reusable-workflow dispatch and credential delivery were not exercised."],
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print("Relay public-source recovery and local distribution replay passed")


if __name__ == "__main__":
    main()
