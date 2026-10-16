#!/usr/bin/env python3
"""Read-only primary-evidence probe; no staging, push or publication credential."""
import json
import os
from pathlib import Path
import publisher as P

binding = json.loads((Path(__file__).parent / "examples/shared-governance.json").read_text())
source = binding["packages"][0]["baseline"]
api = P.GitHub(binding["repository"], os.environ.get("GH_TOKEN"))
parents = P.git(P.ROOT, "show", "-s", "--format=%P", source).decode().split()
print(json.dumps(P.eligible(api, binding, source, parents), sort_keys=True))
# This candidate is deliberately not a merged-main acceptance attestation.
candidate = P.git(P.ROOT, "rev-parse", "HEAD").decode().strip()
parents = P.git(P.ROOT, "show", "-s", "--format=%P", candidate).decode().split()
try:
    P.eligible(api, binding, candidate, parents)
except ValueError:
    print("Unaccepted candidate: rejected")
else:
    raise SystemExit("Candidate unexpectedly eligible")
