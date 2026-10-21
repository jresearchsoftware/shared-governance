#!/usr/bin/env python3
"""Producer readiness around the accepted shared planner; never stage or publish."""
import argparse
import importlib.util
import json
import os
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BINDING = "vibe-publisher.json"
COORDINATE = "org.jresearch.ai/development-governance"


def check(publisher, source, revision, base=None, api=None, main="origin/main"):
    """Use the executing workflow's transition and producer rights acknowledgement."""
    binding = publisher.binding_at(source, revision, BINDING)
    api = api or publisher.GitHub(binding["repository"], os.environ.get("GH_TOKEN"))
    result = publisher.plan(source, revision, main, binding, api, BINDING,
                            candidate_base=base, selected=COORDINATE)
    changed = False
    for item in result["packages"]:
        if item["status"] == "NO_PACKAGE_CHANGE":
            continue
        if item["status"] not in ("READY", "CANDIDATE_VALID"):
            raise ValueError(item.get("reason_code", "PUBLICATION_PENDING"))
        package = publisher.package_binding(binding, COORDINATE)
        rights = package.get("redistribution", {})
        # shared-governance-v1 already checks the real MIT payload/metadata,
        # exact export inventory, standalone links and dependency-free contract.
        # Its early return precedes tree-v1's affirmative acknowledgement check.
        if not (rights.get("status") == "approved" and rights.get("license") == "MIT"
                and rights.get("approval", "").startswith("https://")):
            raise ValueError("REDISTRIBUTION_UNRESOLVED")
        changed = True
    if base is None and changed:
        publisher.verify_trigger(api, binding, revision)
    return result, changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publisher", type=Path, required=True)
    parser.add_argument("--publisher-sha", required=True)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--base")
    args = parser.parse_args()
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.publisher).decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", args.publisher_sha) or actual != args.publisher_sha:
        raise SystemExit("Executing workflow publisher checkout mismatch")
    spec = importlib.util.spec_from_file_location("accepted_publisher", args.publisher / "tooling/vibe-publisher/publisher.py")
    publisher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(publisher)
    try:
        result, changed = check(publisher, args.source, args.source_sha, args.base)
    except (ValueError, KeyError, OSError, subprocess.SubprocessError):
        raise SystemExit("Producer readiness failed; inspect exact source binding, MIT rights and push CI.") from None
    print(json.dumps({"source_sha": args.source_sha, "publisher_sha": actual, "changed": changed,
                      "status": [item["status"] for item in result["packages"]]}))
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as output:
            output.write("changed=" + str(changed).lower() + "\n")


if __name__ == "__main__":
    main()
