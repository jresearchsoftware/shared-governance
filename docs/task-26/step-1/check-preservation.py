#!/usr/bin/env python3
"""Optional Task 26 evidence capture, not a standing release gate."""
import json
from pathlib import Path
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[3]
BASE = "80318d00ec14ee3bc49a1b94cbc24e859371f80f"
PACKAGE = "packages/development-governance"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    candidate = git("rev-parse", "HEAD").decode().strip()
    unchanged = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONTRIBUTING.md",
                 "LICENSE", "docs/releases.md", "toolchain", ".github",
                 "scripts/prepare-distribution.py", "scripts/package-release.py",
                 "vibevm/vibepacks/org.jresearch.ai/development-governance/v0.1.0",
                 "vibevm/vibepacks/org.jresearch.ai/development-governance/v1.3.0"]
    prior_docs = git("ls-tree", "--name-only", BASE + ":docs").decode().splitlines()
    unchanged.extend("docs/" + name for name in prior_docs if name.startswith("task-"))
    for name in unchanged:
        if git("diff", "--name-only", BASE, candidate, "--", name).strip():
            raise ValueError("protected baseline changed: " + name)
    protocols = ["proportional-controls", "requirement-authority", "package-versioning", "self-adoption"]
    for topic in protocols:
        path = PACKAGE + "/vibevm/vibespecs/protocols/" + topic + ".md"
        accepted = git("show", BASE + ":" + path)
        slot = "vibevm/vibedeps/org.jresearch.ai.development-governance/1.3.0/vibevm/vibespecs/protocols/" + topic + ".md"
        if accepted != git("show", BASE + ":" + slot):
            raise ValueError("accepted authored/slot baseline differs: " + topic)
        if accepted != git("show", candidate + ":" + path):
            raise ValueError("unrelated protocol changed: " + topic)
    versions = [tomllib.loads(git("show", revision + ":" + PACKAGE + "/vibe.toml").decode())["package"]["version"]
                for revision in (BASE, candidate)]
    print(json.dumps({"preservation": "PASS", "accepted_source_main": BASE,
                      "candidate": candidate, "versions": versions,
                      "unchanged_paths": unchanged, "unchanged_protocols": protocols,
                      "slot_lifecycle": "native install replaces current 1.3.0 slot with 2.0.0; frozen sources retained",
                      "authority": "candidate rules remain proposals; independent review pending"}, indent=2))


if __name__ == "__main__":
    main()
