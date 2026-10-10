#!/usr/bin/env python3
"""Check this producer's version transition or publish one accepted source commit."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("preparation", ROOT / "scripts/prepare-distribution.py")
PREPARATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARATION)
DESTINATION = "https://github.com/jrs-vibevm/org.jresearch.ai.development-governance.git"


def git(*args, cwd=None, env=None):
    return subprocess.check_output(["git", *args], cwd=cwd or ROOT, env=env,
                                   stderr=subprocess.PIPE, timeout=120).decode().strip()


def bump(version, category):
    major, minor, patch = map(int, version.split("."))
    if category == "major":
        return f"{major + 1}.0.0"
    if category == "minor":
        return f"{major}.{minor + 1}.0"
    if category == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError("package change requires Package bump: major, minor or patch in the PR")


def transition(base, revision, category=None):
    """Compare package payloads independently of the historical source directory move."""
    before, old = PREPARATION.snapshot(base)
    after, new = PREPARATION.snapshot(revision)
    before.pop(PREPARATION.RECEIPT)
    after.pop(PREPARATION.RECEIPT)
    changed = before != after
    if changed:
        if old["version"] == new["version"]:
            raise ValueError("package content changed without a new whole-package version")
        if category and bump(old["version"], category) != new["version"]:
            raise ValueError("recompute the intended bump against current accepted main: " + old["version"])
        if not category and tuple(map(int, new["version"].split("."))) <= tuple(map(int, old["version"].split("."))):
            raise ValueError("this source main release line must advance its authored version")
    return {"changed": changed, "before": old["version"], "version": new["version"],
            "source_revision": revision, "bump": category}


def accepted_transition(revision, accepted_main="origin/main"):
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("retry requires a full accepted source SHA")
    # Reachability alone would also admit side-branch PR commits after a merge.
    if revision not in git("rev-list", "--first-parent", accepted_main).splitlines():
        raise ValueError("source SHA must be an accepted first-parent commit on source main")
    parent = git("rev-parse", revision + "^1")
    return transition(parent, revision)


def tag_exists(destination, tag, env=None):
    return bool(git("ls-remote", "--refs", destination, "refs/tags/" + tag, env=env))


def publish(revision, vibe, destination=DESTINATION, accepted_main="origin/main", before_push=None):
    decision = accepted_transition(revision, accepted_main)
    if not decision["changed"]:
        return {**decision, "publication": "NO_PACKAGE_CHANGE"}
    tag = "v" + decision["version"]
    if tag_exists(destination, tag):
        return {**decision, "publication": "ALREADY_PUBLISHED", "tag": tag}
    if destination == DESTINATION and not os.environ.get("RELEASE_TOKEN"):
        raise ValueError("configure DEVELOPMENT_GOVERNANCE_PUBLISH_TOKEN for the distribution repository")
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())
    vibe = Path(vibe).resolve()
    if hashlib.sha256(vibe.read_bytes()).hexdigest() != pin["linux_x86_64_musl_binary"]["sha256"]:
        raise ValueError("publisher must use the pinned VibeVM musl binary")
    with tempfile.TemporaryDirectory(prefix="governance-release-") as temporary:
        temporary = Path(temporary)
        payload = temporary / "payload"
        PREPARATION.prepare(revision, payload)
        staging = temporary / "distribution.git"
        # Native publisher may replace tags. Stage locally, then use an ordinary
        # atomic, non-force push: a concurrent new tag or main update fails safely.
        git("clone", "--bare", "--", destination, str(staging))
        if tag_exists(staging.as_uri(), tag):
            return {**decision, "publication": "ALREADY_PUBLISHED", "tag": tag}
        env = dict(os.environ)
        env.update(VIBE_SETTINGS=str(temporary / "settings"),
                   VIBEVM_USER_CONFIG=str(temporary / "settings/config.toml"))
        result = subprocess.run([str(vibe), "--json", "registry", "publish", str(payload),
                                 "--repo-url", staging.as_uri()], env=env, cwd=payload,
                                capture_output=True, text=True, timeout=180)
        if result.returncode:
            raise ValueError("native publisher failed; retry this accepted SHA after recovery")
        if before_push:  # Disposable integration tests inject a competing writer here.
            before_push(staging, tag)
        git("push", "--atomic", "--", destination,
            "refs/heads/main:refs/heads/main", f"refs/tags/{tag}:refs/tags/{tag}", cwd=staging)
        remote = git("ls-remote", destination, "refs/tags/" + tag, "refs/tags/" + tag + "^{}")
        return {**decision, "publication": "PUBLISHED", "tag": tag, "remote_refs": remote.splitlines()}


def report(result):
    print(json.dumps(result))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as output:
            output.write("\n```json\n" + json.dumps(result, indent=2) + "\n```\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--base", help="candidate transition from current accepted main")
    action.add_argument("--publish", action="store_true", help="publish to the fixed distribution repository")
    action.add_argument("--inspect-accepted", action="store_true", help="inspect a main commit without publication")
    parser.add_argument("--accepted-main", default="origin/main")
    parser.add_argument("--vibe", type=Path)
    parser.add_argument("--pr-body-file", type=Path)
    args = parser.parse_args()
    try:
        revision = git("rev-parse", "--verify", args.source_ref + "^{commit}")
        if args.inspect_accepted:
            if args.source_ref != revision:
                raise ValueError("accepted inspection requires a full SHA")
            result = accepted_transition(revision, args.accepted_main)
            report(result)
            if os.environ.get("GITHUB_OUTPUT"):
                with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
                    output.write("changed=" + str(result["changed"]).lower() + "\n")
        elif args.publish:
            if args.source_ref != revision or args.vibe is None:
                raise ValueError("publication requires a full SHA and --vibe")
            report(publish(revision, args.vibe, accepted_main=args.accepted_main))
        else:
            base = git("rev-parse", "--verify", args.base + "^{commit}")
            category = None
            if args.pr_body_file:
                categories = re.findall(r"(?im)^Package bump:\s*(major|minor|patch)\s*$",
                                        args.pr_body_file.read_text(encoding="utf-8"))
                if len(categories) != 1:
                    if transition(base, revision)["changed"]:
                        raise ValueError("package PR requires one Package bump: major, minor or patch line")
                else:
                    category = categories[0].lower()
            report(transition(base, revision, category))
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        # Git stderr/URLs and credentials are not emitted by the release wrapper.
        report({"publication": "FAILED_OR_PENDING", "source_revision": args.source_ref,
                "reason": str(error) if isinstance(error, ValueError) else type(error).__name__,
                "recovery": "retry the same accepted source SHA; do not bump or move an existing tag"})
        parser.exit(1)


if __name__ == "__main__":
    main()
