#!/usr/bin/env python3
"""Source-only VibeVM publisher. Producer authority is supplied by a pinned binding.

No producer is integrated by installing this file. See docs/shared-publisher.md.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tomllib
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
SHA = re.compile(r"[0-9a-f]{40}")
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
RECEIPT = "DISTRIBUTION.json"


def git(root, *args):
    result = subprocess.run(["git", *map(str, args)], cwd=root, capture_output=True)
    if result.returncode:
        # Git stderr can contain credential-helper diagnostics or private URLs.
        raise ValueError("Git operation failed: " + args[0])
    return result.stdout


def exact(root, revision):
    if not SHA.fullmatch(revision):
        raise ValueError("a full source commit SHA is required")
    if git(root, "rev-parse", "--verify", revision + "^{commit}").decode().strip() != revision:
        raise ValueError("commit identity differs")
    return revision


def safe_path(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value or ":" in value:
        raise ValueError("expected a repository-relative path")
    if any(part == ".git" for part in path.parts):
        raise ValueError("Git metadata cannot be exported")
    return value


def binding_at(policy_root, policy_sha, path, allow_local=False):
    exact(policy_root, policy_sha)
    binding = json.loads(git(policy_root, "show", policy_sha + ":" + safe_path(path)))
    if binding.get("schema") != 1 or binding.get("acceptance") != "owner-squash-attestation-v1":
        raise ValueError("unsupported producer binding / acceptance rule")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", binding["repository"]):
        raise ValueError("invalid source repository")
    if not isinstance(binding["repository_id"], int) or not binding["authorized_integrators"]:
        raise ValueError("source repository identity and owner integrators are required")
    if not re.fullmatch(r"[\w.-]+", binding["branch"]):
        raise ValueError("unsupported source branch")
    if not binding["ci_workflow"].startswith(".github/workflows/"):
        raise ValueError("qualifying push workflow is required")
    coordinates, destinations = set(), set()
    if not binding["packages"]:
        raise ValueError("package bindings are required")
    for package in binding["packages"]:
        if package["coordinate"] in coordinates or package["destination"] in destinations:
            raise ValueError("each coordinate needs its own distribution repository")
        coordinates.add(package["coordinate"])
        destinations.add(package["destination"])
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", package["coordinate"]):
            raise ValueError("invalid package coordinate")
        safe_path(package["root"])
        if not SHA.fullmatch(package["baseline"]):
            raise ValueError("an explicitly accepted package baseline SHA is required")
        if package["adapter"] not in ("tree-v1", "shared-governance-v1"):
            raise ValueError("unsupported export adapter")
        if package["adapter"] == "tree-v1":
            for path in package["files"]:
                safe_path(path)
            if not {"vibe.toml", "LICENSE"}.issubset(package["files"]):
                raise ValueError("explicit manifest and public license are required")
            if package["disclosure"] not in ("public-source", "opaque"):
                raise ValueError("explicit provenance disclosure is required")
        if not re.fullmatch(r"https://github\.com/[\w.-]+/[\w.-]+\.git", package["destination"]):
            if not allow_local or not package["destination"].startswith("file://"):
                raise ValueError("destination must be a credential-free GitHub HTTPS repository")
    return binding


class GitHub:
    """Read GitHub API evidence, following all result pages; never execute API text."""
    def __init__(self, repository, token=None):
        self.repository = repository
        self.token = token
        self.cache = {}

    def get(self, path):
        if path not in self.cache:
            headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
            if self.token:
                headers["Authorization"] = "Bearer " + self.token
            request = urllib.request.Request("https://api.github.com/repos/" + self.repository + "/" + path,
                                             headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    self.cache[path] = json.load(response)
            except Exception:
                raise ValueError("GitHub evidence unavailable") from None
        return self.cache[path]

    def pages(self, path, key=None):
        result, page = [], 1
        while True:
            data = self.get(path + ("&" if "?" in path else "?") + f"per_page=100&page={page}")
            rows = data[key] if key else data
            result.extend(rows)
            if len(rows) < 100:
                return result
            page += 1


def valid_ci(run, binding, revision, workflow_id):
    return (run["head_sha"] == revision and run["event"] == "push"
            and run["head_branch"] == binding["branch"] and run["status"] == "completed"
            and run["conclusion"] == "success" and run["workflow_id"] == workflow_id
            and run["head_repository"]["id"] == binding["repository_id"]
            and run["repository"]["id"] == binding["repository_id"])


def verify_trigger(api, binding, source_sha):
    if os.environ.get("GITHUB_EVENT_NAME") != "workflow_run":
        return
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    run = api.get("actions/runs/" + str(int(event["workflow_run"]["id"])))
    workflow = api.get("actions/workflows/" + binding["ci_workflow"].rsplit("/", 1)[1])
    if workflow["path"] != binding["ci_workflow"] or not valid_ci(run, binding, source_sha, workflow["id"]):
        raise ValueError("automatic trigger is not the bound successful exact-source push run")


def eligible(api, binding, revision, parents):
    """Owner integration attests review; it does not prove independent review identity."""
    repository = api.get("")
    if (repository["id"], repository["full_name"]) != (binding["repository_id"], binding["repository"]):
        raise ValueError("source repository identity differs")
    if len(parents) != 1:
        raise ValueError("initial integration supports squash commits only")
    pulls = api.pages(f"commits/{revision}/pulls")
    matches = []
    for associated in pulls:
        pr = api.get("pulls/" + str(associated["number"]))
        if (pr.get("merged") and pr.get("merge_commit_sha") == revision
                and pr["base"]["ref"] == binding["branch"]
                and pr["base"]["repo"]["id"] == binding["repository_id"]
                and pr["merged_by"]["login"] in binding["authorized_integrators"]
                and pr["head"]["sha"] != revision):
            matches.append(pr)
    if len(matches) != 1:
        raise ValueError("no unambiguous authorized owner squash integration")
    workflow = api.get("actions/workflows/" + binding["ci_workflow"].rsplit("/", 1)[1])
    if workflow["path"] != binding["ci_workflow"]:
        raise ValueError("qualifying CI workflow identity differs")
    runs = api.pages(f"actions/workflows/{workflow['id']}/runs?head_sha={revision}&event=push", "workflow_runs")
    runs = [run for run in runs if valid_ci(run, binding, revision, workflow["id"])]
    if not runs:
        raise ValueError("no successful matching source-main push CI")
    pr = matches[0]
    return {"pr": pr["html_url"], "reviewed_head": pr["head"]["sha"],
            "integrator": pr["merged_by"]["login"], "ci_run": runs[0]["html_url"],
            "source_sha": revision, "attestation": binding["acceptance"]}


def snapshot(root, revision, package):
    """Export only Git blobs, never worktree files, caches, or live observations."""
    if package["adapter"] == "shared-governance-v1":
        spec = importlib.util.spec_from_file_location("governance_export", ROOT / "scripts/prepare-distribution.py")
        exporter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exporter)
        exporter.ROOT = Path(root)
        files, receipt = exporter.snapshot(revision)
        return files, receipt
    entries = git(root, "ls-tree", "-rz", revision, "--", package["root"]).split(b"\0")
    blobs = {}
    for entry in filter(None, entries):
        metadata, path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        relative = str(PurePosixPath(path.decode()).relative_to(package["root"]))
        if relative not in package["files"]:
            continue
        if mode != "100644" or kind != "blob":
            raise ValueError("export requires ordinary Git blobs")
        blobs[relative] = git(root, "cat-file", "blob", oid)
    if not blobs:
        return None
    if set(blobs) != set(package["files"]) or RECEIPT in blobs:
        raise ValueError("approved public export files missing or reserved receipt supplied")
    manifest = tomllib.loads(blobs["vibe.toml"].decode())
    metadata = manifest["package"]
    if (metadata["group"] + "/" + metadata["name"] != package["coordinate"]
            or not VERSION.fullmatch(metadata["version"]) or metadata.get("frozen") is not True):
        raise ValueError("canonical frozen package identity differs")
    if manifest.get("requires") or manifest.get("dev-requires"):
        # The adapter contract must be extended with actual lock/slot closure
        # evidence before admitting dependencies. Do not implement a resolver.
        raise ValueError("tree-v1 supports an empty dependency closure only")
    if not blobs["LICENSE"].strip():
        raise ValueError("public package license is empty")
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(blobs.items())}
    digest = hashlib.sha256(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    receipt = {"schema": 1, "package": package["coordinate"], "version": metadata["version"],
               "payload_sha256": digest, "sha256": hashes}
    if package["disclosure"] == "public-source":
        receipt.update(source_revision=revision, source_path=package["root"])
    blobs[RECEIPT] = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
    return blobs, receipt


def payload(snapshot_value):
    return None if snapshot_value is None else snapshot_value[1]["payload_sha256"]


def plan(root, source_sha, main, binding, api, publisher_sha):
    exact(root, source_sha)
    if not SHA.fullmatch(publisher_sha):
        raise ValueError("a full called-workflow publisher SHA is required")
    chain = git(root, "rev-list", "--first-parent", main).decode().splitlines()
    if source_sha not in chain:
        raise ValueError("source is not on first-parent source main")
    evidence_cache, snapshots = {}, {}
    def export(revision, package):
        key = revision, package["coordinate"]
        if key not in snapshots:
            snapshots[key] = snapshot(root, revision, package)
        return snapshots[key]
    results = []
    for package in binding["packages"]:
        result = {"package": package["coordinate"], "source_sha": source_sha,
                  "publisher_sha": publisher_sha, "destination": package["destination"]}
        try:
            parents = git(root, "show", "-s", "--format=%P", source_sha).decode().split()
            current = export(source_sha, package)
            previous = export(parents[0], package) if parents else None
            if payload(current) == payload(previous):
                result["status"] = "NO_PACKAGE_CHANGE"
            else:
                baseline = package["baseline"]
                if baseline not in chain or chain.index(baseline) <= chain.index(source_sha):
                    raise ValueError("accepted package baseline must precede source on first-parent main")
                history = list(reversed(chain[chain.index(source_sha):chain.index(baseline)]))
                prior = export(baseline, package)
                accepted = []
                for revision in history:
                    next_value = export(revision, package)
                    if payload(prior) != payload(next_value):
                        if next_value is None:
                            raise ValueError("package removal requires owner disposition")
                        if prior and prior[1]["version"] == next_value[1]["version"]:
                            raise ValueError("package payload changed without a new version")
                        if revision not in evidence_cache:
                            revision_parents = git(root, "show", "-s", "--format=%P", revision).decode().split()
                            evidence_cache[revision] = eligible(api, binding, revision, revision_parents)
                        accepted.append(evidence_cache[revision])
                    prior = next_value
                result.update(status="READY", version=current[1]["version"],
                              payload_sha256=current[1]["payload_sha256"], acceptance=accepted)
        except (ValueError, KeyError, TypeError) as error:
            result.update(status="AUTHORIZATION_PENDING", reason=str(error))
        results.append(result)
    return {"source_sha": source_sha, "publisher_sha": publisher_sha, "packages": results}


def remote_refs(destination, tag):
    return git(None, "ls-remote", "--", destination, "refs/heads/main", "refs/tags/" + tag,
               "refs/tags/" + tag + "^{}").decode().splitlines()


def tag_oid(refs, tag):
    return next((line.split()[0] for line in refs if line.split()[1] == "refs/tags/" + tag), None)


def native_environment(temporary):
    # Producer adapters and native publishers never inherit publication/API tokens.
    env = {key: value for key, value in os.environ.items()
           if key in ("PATH", "HOME", "SYSTEMROOT", "TMP", "TEMP", "LANG", "LC_ALL",
                      "GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL")}
    env.update(VIBE_SETTINGS=str(temporary / "settings"),
               VIBEVM_USER_CONFIG=str(temporary / "settings/config.toml"), GIT_TERMINAL_PROMPT="0",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return env


def stage(root, package, decision, vibe, directory):
    """Credential-free preparation. directory is disposable, never a release ledger."""
    if decision["status"] != "READY":
        return dict(decision)
    result = dict(decision)
    tag = "v" + result["version"]
    result["tag"] = tag
    refs = remote_refs(package["destination"], tag)
    if tag_oid(refs, tag):
        result.update(status="ALREADY_PUBLISHED", remote_refs=refs,
                      warning="Existing identity retained; this does not prove this retry source was published.")
        return result
    pin = json.loads((ROOT / "toolchain/vibevm.json").read_text())["linux_x86_64_musl_binary"]
    vibe = Path(vibe).resolve()
    if hashlib.sha256(vibe.read_bytes()).hexdigest() != pin["sha256"]:
        raise ValueError("publisher must use the pinned VibeVM musl binary")
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    files, receipt = snapshot(root, decision["source_sha"], package)
    if receipt["payload_sha256"] != decision["payload_sha256"]:
        raise ValueError("planned and staged payload differ")
    payload_root, staging = directory / "payload", directory / "distribution.git"
    payload_root.mkdir()
    for relative, data in files.items():
        target = payload_root / safe_path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    git(None, "clone", "--bare", "--", package["destination"], str(staging))
    if tag_oid(remote_refs(staging.as_uri(), tag), tag):
        result.update(status="ALREADY_PUBLISHED", remote_refs=remote_refs(package["destination"], tag))
        return result
    command = [str(vibe), "--json", "registry", "publish", str(payload_root), "--repo-url", staging.as_uri()]
    completed = subprocess.run(command, cwd=payload_root, env=native_environment(directory),
                               capture_output=True, timeout=180)
    if completed.returncode:
        raise ValueError("native staging failed; recover and retry the same source SHA")
    staged_refs = remote_refs(staging.as_uri(), tag)
    if not tag_oid(staged_refs, tag):
        raise ValueError("native staging produced no release tag")
    result.update(status="STAGED", staging=str(staging), expected_tag=tag_oid(staged_refs, tag))
    return result


def finalize(staged, push=None):
    """Only this operation may receive a narrowly scoped destination credential."""
    if staged["status"] != "STAGED":
        return staged
    result = {key: value for key, value in staged.items() if key != "staging"}
    destination, tag = staged["destination"], staged["tag"]
    try:
        refs = remote_refs(destination, tag)
        if tag_oid(refs, tag):
            result.update(status="ALREADY_PUBLISHED", remote_refs=refs,
                          warning="Existing identity retained; compare its original provenance if recovery differs.")
            return result
        operation = push or git
        operation(Path(staged["staging"]), "push", "--atomic", "--", destination,
                  "refs/heads/main:refs/heads/main", f"refs/tags/{tag}:refs/tags/{tag}")
    except (ValueError, subprocess.SubprocessError):
        result.update(status="FAILED_OR_PENDING", reason="Atomic publication failed or transport result is ambiguous; retry the same source and publisher SHA.")
    try:
        refs = remote_refs(destination, tag)
        observed = tag_oid(refs, tag)
        if observed == staged["expected_tag"]:
            result.update(status="PUBLISHED", remote_refs=refs)
        elif observed:
            result.update(status="ALREADY_PUBLISHED", remote_refs=refs,
                          warning="A competing identity exists and was retained; this source was not published.")
        else:
            result.update(status="FAILED_OR_PENDING", remote_refs=refs,
                          reason="No release tag observed; retry the same source and publisher SHA.")
    except ValueError:
        result.update(status="FAILED_OR_PENDING", reason="Publication readback unavailable; inspect and retry the same source and publisher SHA.")
    return result


def stage_all(root, binding, report, vibe, directory, selected):
    results = []
    for package, decision in zip(binding["packages"], report["packages"]):
        if selected and package["coordinate"] != selected:
            continue
        try:
            result = stage(root, package, decision, vibe, Path(directory) / package["coordinate"].replace("/", "."))
        except (ValueError, OSError, subprocess.SubprocessError):
            result = {**decision, "status": "FAILED_OR_PENDING",
                      "reason": "Preparation failed; retry the same source and publisher SHA after recovery."}
        results.append(result)
    if selected and not results:
        raise ValueError("selected package is absent from the accepted binding")
    return {**report, "packages": results}


def write_report(report, path):
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    # Artifacts are deliberately not uploaded: private source identity can be sensitive.
    for result in report["packages"]:
        print(result["package"] + ": " + result["status"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("plan", "stage", "finalize"))
    parser.add_argument("--source", type=Path)
    parser.add_argument("--source-sha")
    parser.add_argument("--main", default="origin/main")
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--policy-sha")
    parser.add_argument("--binding")
    parser.add_argument("--publisher-sha")
    parser.add_argument("--package", help="One destination per named-secret workflow call")
    parser.add_argument("--vibe", type=Path)
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.operation == "finalize":
        report = json.loads(args.report.read_text())
        if len(report["packages"]) != 1:
            raise ValueError("finalize requires one destination per named credential")
        report["packages"] = [finalize(report["packages"][0])]
    else:
        exact(ROOT, args.publisher_sha)
        if git(ROOT, "rev-parse", "HEAD").decode().strip() != args.publisher_sha:
            raise ValueError("CLI code checkout differs from publisher pin")
        binding = binding_at(args.policy, args.policy_sha, args.binding)
        api = GitHub(binding["repository"], os.environ.get("GH_TOKEN"))
        verify_trigger(api, binding, args.source_sha)
        report = plan(args.source, args.source_sha, args.main, binding, api, args.publisher_sha)
        if args.operation == "stage":
            report = stage_all(args.source, binding, report, args.vibe, args.directory, args.package)
        elif args.package:
            report["packages"] = [row for row in report["packages"] if row["package"] == args.package]
            if not report["packages"]:
                raise ValueError("selected package is absent from the accepted binding")
    write_report(report, args.report)
    return int(any(item["status"] in ("AUTHORIZATION_PENDING", "FAILED_OR_PENDING") for item in report["packages"]))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, subprocess.SubprocessError):
        raise SystemExit("Publisher failed or pending. Preserve exact source/publisher pins and inspect trusted evidence.") from None
