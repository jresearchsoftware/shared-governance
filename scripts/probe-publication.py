#!/usr/bin/env python3
"""Read-only actual push-CI probe with explicit producer/candidate identities."""
import argparse
import importlib.util
import os
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--publisher", type=Path, required=True)
parser.add_argument("--candidate", required=True)
args = parser.parse_args()
spec = importlib.util.spec_from_file_location("publisher", args.publisher / "tooling/vibe-publisher/publisher.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)
binding = {"repository": "jresearchsoftware/shared-governance", "repository_id": 1408747561,
           "branch": "main", "ci_workflow": ".github/workflows/candidate.yml"}
api = publisher.GitHub(binding["repository"], os.environ.get("GH_TOKEN"))
accepted = "5a1e5de66388501235fc9ffd23d45efb34df2b85"
publisher.eligible(api, binding, accepted, [])
print("Accepted exact-source push CI: verified " + accepted)
try:
    publisher.eligible(api, binding, args.candidate, [])
except publisher.AuthorizationError as error:
    if error.code != "MATCHING_SOURCE_CI_MISSING":
        raise
    print("Candidate without source-main push CI: rejected " + args.candidate)
else:
    raise SystemExit("Candidate unexpectedly has qualifying push CI")
