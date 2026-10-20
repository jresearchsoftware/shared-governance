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

AUTHORIZATION_MESSAGES = {
    'SOURCE_NOT_ON_MAIN': 'This source is not on accepted first-parent main; do not publish this commit.',
    'PACKAGE_BASELINE_UNRESOLVED': 'The accepted package baseline is not verifiably on first-parent main at or before this source; correct the bound baseline before retrying.',
    'OWNER_DISPOSITION_REQUIRED': 'This package removal needs an explicit owner disposition before publication.',
    'PACKAGE_VERSION_REUSE': "Package bytes changed without a new package version; correct the version under the producer's release policy.",
    'PACKAGE_MAPPING_CHANGED': 'The immediate transition changes a package root, adapter or destination; obtain the producer-owned migration disposition before using that transition for publication.',
    'SOURCE_REPOSITORY_MISMATCH': 'The checked source repository does not match the accepted producer binding; correct the binding or source checkout.',
    'UNSUPPORTED_MERGE_ROUTE': 'This binding supports squash integration only; another merge route needs producer-specific qualification and owner disposition.',
    'OWNER_ACCEPTANCE_NOT_ESTABLISHED': 'No unique authorized owner squash merge was found; resolve the owner and PR acceptance evidence before retrying.',
    'QUALIFYING_CI_MISMATCH': 'The configured qualifying CI workflow identity does not match; correct the trusted producer binding.',
    'MATCHING_SOURCE_CI_MISSING': 'No successful push CI run for this exact source commit was found; resolve that CI result before retrying.',
    'TRIGGER_RUN_MISMATCH': 'The triggering run is not the bound successful push run for this exact source commit; do not publish from it.',
    'ACCEPTANCE_EVIDENCE_UNAVAILABLE': 'Required GitHub acceptance or CI evidence could not be read; restore read access and verify the exact source before retrying.',
    'PRODUCER_BINDING_UNSUPPORTED': "The accepted producer binding uses an unsupported schema or acceptance rule; resolve it in the producer's authority.",
    'PACKAGE_IDENTITY_MISMATCH': "The package identity or frozen version does not match its accepted binding; correct the package under its owner's release policy.",
    'DEPENDENCY_CLOSURE_UNQUALIFIED': 'An included dependency is unresolved, mutable or lacks matching native lock/slot hashes. Materialize the frozen closure with pinned VibeVM and approve its complete export inventory.',
}

AUTHORIZATION_FALLBACK = (
    "ACCEPTANCE_OR_OWNER_DISPOSITION_UNRESOLVED",
    "The publisher could not establish package, source, owner or CI eligibility. Resolve the trusted evidence or owner disposition before retrying.")

DIAGNOSTIC_MESSAGES = {
    "NO_PACKAGE_CHANGE": "No approved package payload changed; no publication was attempted.",
    "ELIGIBLE_NOT_PUBLISHED": "Eligibility checks passed, but publication has not run.",
    "STAGED_NOT_PUBLISHED": "The native release is staged locally; destination publication is not confirmed.",
    "PUBLISHED_CONFIRMED": "The exact staged tag object was read back from the destination; publication is confirmed.",
    "EXISTING_TAG_UNVERIFIED": "An existing release tag was retained. Its presence does not prove this exact source was published; compare trusted tag provenance before claiming success.",
    "COMPETING_TAG_RETAINED": "A competing release identity was retained and this exact source was not published; resolve its provenance before any retry.",
    "ATOMIC_PUSH_UNCERTAIN": "The atomic push result is uncertain. Inspect exact destination tag and main refs before retrying with the same source SHA and workflow implementation pin.",
    "RELEASE_TAG_NOT_OBSERVED": "No release tag was observed. Recover the credential, network or concurrency issue, then retry with the same source SHA and workflow implementation pin.",
    "PUBLICATION_READBACK_UNAVAILABLE": "Destination readback was unavailable; do not claim publication. Restore read access and inspect the exact tag and branch before retrying with the same pins.",
    "UNCLASSIFIED_PUBLICATION_FAILURE": "Publication failed or remains unverified. Inspect the failed step and exact destination refs before retrying with the same source SHA and workflow implementation pin.",
    "PINNED_TOOL_MISMATCH": "The pinned VibeVM binary check failed; restore the recorded tool before retrying the same source and publisher pins.",
    "STAGED_PAYLOAD_MISMATCH": "The staged package payload differs from the plan; discard this attempt and investigate the exact source and export before retrying.",
    "NATIVE_PUBLISHER_FAILED": "Credential-free native staging failed; inspect the pinned publisher and local staging inputs. No destination write was attempted.",
    "NATIVE_PUBLISHER_NO_TAG": "Native staging produced no release tag; inspect the pinned publisher output before retrying. No destination write was attempted.",
    "DISTRIBUTION_CLONE_FAILED": "The destination repository could not be cloned for credential-free staging; restore read access and retry the same pins.",
    "DISTRIBUTION_REF_READ_FAILED": "Destination refs could not be read during credential-free staging; restore read access and retry the same pins.",
    "NATIVE_STAGING_TIMEOUT": "Pinned native staging timed out; inspect the local staging environment before retrying the same pins.",
    "LOCAL_STAGING_FAILED": "Local credential-free staging failed; inspect the failed preparation step. No destination write was attempted.",
    "STAGING_VALIDATION_FAILED": "Package or staging validation failed; review the accepted source and binding before retrying.",
    "STAGING_SUBPROCESS_FAILED": "A local staging process failed; inspect the failed preparation step. No destination write was attempted.",
    "STAGING_PREPARATION_FAILED": "Credential-free preparation failed; inspect the failed preparation step. No destination write was attempted.",
    "WORKFLOW_INTERRUPTED_BEFORE_CONFIRMATION": "The workflow stopped before a final package result was confirmed. Inspect destination refs before retrying with the same source SHA and workflow implementation pin.",
    "PUBLISHER_REPORT_UNREADABLE": "The package report could not be read. Do not infer publication; inspect the failed workflow step and exact destination refs.",
}

FAILURE_REASON_CODES = {
    "Atomic publication failed or transport result is ambiguous; retry the same source SHA and workflow implementation pin.": "ATOMIC_PUSH_UNCERTAIN",
    "No release tag observed; retry the same source SHA and workflow implementation pin.": "RELEASE_TAG_NOT_OBSERVED",
    "Publication readback unavailable; inspect and retry the same source SHA and workflow implementation pin.": "PUBLICATION_READBACK_UNAVAILABLE",
}

WARNING_CODES = {
    "Existing identity retained; this does not prove this retry source was published.": "EXISTING_TAG_UNVERIFIED",
    "Existing identity retained; compare its original provenance if recovery differs.": "EXISTING_TAG_UNVERIFIED",
    "Existing identity retained; the retry source has not been proven published.": "EXISTING_TAG_UNVERIFIED",
    "A competing identity exists and was retained; this source was not published.": "COMPETING_TAG_RETAINED",
}

STAGING_ERROR_CODES = {
    "publisher must use the pinned VibeVM musl binary": "PINNED_TOOL_MISMATCH",
    "planned and staged payload differ": "STAGED_PAYLOAD_MISMATCH",
    "native staging failed; recover and retry the same source SHA": "NATIVE_PUBLISHER_FAILED",
    "native staging produced no release tag": "NATIVE_PUBLISHER_NO_TAG",
    "Git operation failed: clone": "DISTRIBUTION_CLONE_FAILED",
    "Git operation failed: ls-remote": "DISTRIBUTION_REF_READ_FAILED",
}

SUMMARY_PHASES = (
    ("inputs", "INPUT_VALIDATION_FAILED", "Immutable workflow inputs or publisher identity did not validate; correct the caller pins before retrying."),
    ("publisher_checkout", "PUBLISHER_CHECKOUT_FAILED", "The pinned reusable workflow code could not be checked out; no package result or destination write was produced."),
    ("producer_checkout", "PRODUCER_CHECKOUT_FAILED", "The exact producer source could not be checked out; no package result or destination write was produced."),
    ("source_identity", "SOURCE_IDENTITY_VERIFICATION_FAILED", "The checked-out publisher or producer SHA did not match its bound identity; correct the exact pins before retrying."),
    ("plan", "SOURCE_ACCEPTANCE_OR_CI_CHECK_FAILED", "The publisher did not produce a package report during planning. Resolve the source, binding, owner acceptance or exact CI evidence before retrying."),
    ("tool", "PINNED_TOOL_PREPARATION_FAILED", "The pinned VibeVM tool could not be prepared; no destination write was attempted. Recover the download or digest issue before retrying."),
    ("stage", "CREDENTIAL_FREE_STAGING_FAILED", "Credential-free staging did not produce a package report; no final publication result is available. Recover the failed staging step before retrying."),
    ("finalize", "PUBLICATION_RESULT_UNCONFIRMED", "Finalization did not produce a package report. Read the exact destination tag and main refs before claiming publication or retrying."),
)


class AuthorizationError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


AUTHORIZATION_MESSAGES.update({
    "INITIAL_PUBLICATION_UNRESOLVED": "Initial publication requires the exact accepted onboarding commit, frozen source/version/digest and explicit owner baseline disposition; retry those same pins.",
    "HISTORICAL_BINDING_UNRESOLVED": "Historical export or acceptance policy is unavailable or incompatible; obtain explicit owner disposition of the affected baseline before publication.",
    "POLICY_PIN_MISMATCH": "The source-time binding differs from the independently accepted policy pin; reconcile the exact producer pins before publication.",
    "PUBLIC_EXPORT_INCOMPLETE": "Approved public package files or license are missing or invalid; prepare a new version before source acceptance.",
    "REDISTRIBUTION_UNRESOLVED": "License metadata does not match an explicit redistribution approval; resolve rights and notices with the owner before accepting package source.",
})


def operator_diagnostic(result, status=None):
    """Return a safe allowlisted category and message; never echo report details."""
    status = status or result.get("status", "")
    if status == "NO_PACKAGE_CHANGE":
        return "NO_PACKAGE_CHANGE", DIAGNOSTIC_MESSAGES["NO_PACKAGE_CHANGE"]
    if status == "READY":
        return "ELIGIBLE_NOT_PUBLISHED", DIAGNOSTIC_MESSAGES["ELIGIBLE_NOT_PUBLISHED"]
    if status == "CANDIDATE_VALID":
        return "CANDIDATE_VALID", "Source-time package checks passed; independent acceptance and publication remain pending."
    if status == "STAGED":
        return "STAGED_NOT_PUBLISHED", DIAGNOSTIC_MESSAGES["STAGED_NOT_PUBLISHED"]
    if status == "PUBLISHED":
        return "PUBLISHED_CONFIRMED", DIAGNOSTIC_MESSAGES["PUBLISHED_CONFIRMED"]
    if status == "AUTHORIZATION_PENDING":
        code = result.get("reason_code")
        return (code, AUTHORIZATION_MESSAGES[code]) if code in AUTHORIZATION_MESSAGES else AUTHORIZATION_FALLBACK
    if status == "ALREADY_PUBLISHED":
        code = WARNING_CODES.get(result.get("warning"), "EXISTING_TAG_UNVERIFIED")
        return code, DIAGNOSTIC_MESSAGES[code]
    if status == "FAILED_OR_PENDING":
        code = result.get("failure_code") or FAILURE_REASON_CODES.get(result.get("reason"))
        if code not in DIAGNOSTIC_MESSAGES:
            code = "STAGING_PREPARATION_FAILED" if "failure_code" in result else "UNCLASSIFIED_PUBLICATION_FAILURE"
        return code, DIAGNOSTIC_MESSAGES[code]
    return "OPERATOR_REVIEW_REQUIRED", "The publisher returned an unrecognized state. Inspect trusted evidence; do not infer publication."


def staging_failure_code(error):
    if isinstance(error, subprocess.TimeoutExpired):
        return "NATIVE_STAGING_TIMEOUT"
    code = STAGING_ERROR_CODES.get(str(error))
    if code:
        return code
    if isinstance(error, OSError):
        return "LOCAL_STAGING_FAILED"
    if isinstance(error, subprocess.SubprocessError):
        return "STAGING_SUBPROCESS_FAILED"
    if isinstance(error, ValueError):
        return "STAGING_VALIDATION_FAILED"
    return "STAGING_PREPARATION_FAILED"


def failed_workflow_phase(outcomes):
    for phase, code, message in SUMMARY_PHASES:
        if outcomes.get(phase) in ("failure", "cancelled"):
            return code, message
    return None


def missing_report_diagnostic(outcomes):
    failed_phase = failed_workflow_phase(outcomes)
    if failed_phase:
        return failed_phase
    return "PUBLISHER_REPORT_MISSING", "No package report was produced. Inspect the first failed workflow step; do not infer publication."


def append_actions_summary(report_path, summary_path, job_status, outcomes):
    """Append only safe status and diagnostic text to the durable Actions summary."""
    report_path, summary_path = Path(report_path), Path(summary_path)
    rows = []
    pending_authorization = False
    failed = False
    if not report_path.exists():
        code, message = missing_report_diagnostic(outcomes)
        rows.append(f"Publisher result unavailable: **FAILED_OR_PENDING** — `{code}`: {message}")
        failed = True
    else:
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            packages = report["packages"]
        except (OSError, ValueError, KeyError, TypeError):
            rows.append("Publisher result unavailable: **FAILED_OR_PENDING** — `PUBLISHER_REPORT_UNREADABLE`: "
                        + DIAGNOSTIC_MESSAGES["PUBLISHER_REPORT_UNREADABLE"])
            failed = True
            packages = []
        for package in packages:
            status = package.get("status", "")
            if status in ("READY", "STAGED") and job_status != "success":
                status = "FAILED_OR_PENDING"
                phase_failure = failed_workflow_phase(outcomes)
                if phase_failure:
                    code, message = phase_failure
                else:
                    code = "WORKFLOW_INTERRUPTED_BEFORE_CONFIRMATION"
                    message = DIAGNOSTIC_MESSAGES[code]
            else:
                code, message = operator_diagnostic(package)
            rows.append(f"{package.get('package', 'Package')}: **{status}** — `{code}`: {message}")
            pending_authorization |= status == "AUTHORIZATION_PENDING"
            failed |= status == "FAILED_OR_PENDING"

    if pending_authorization:
        rows.append("Resolve the listed owner acceptance or disposition evidence before retrying; these packages are not currently eligible for publication.")
    if failed:
        rows.append("After recovering a retryable failure, inspect exact destination refs and retry only with the same source SHA and workflow implementation pin. Existing tags are retained.")
    with summary_path.open("a", encoding="utf-8") as summary:
        summary.write("## Shared publisher result\n\n")
        summary.write("\n\n".join(rows) + "\n")


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


def binding_at(root, source_sha, path, allow_local=False):
    exact(root, source_sha)
    binding = json.loads(git(root, "show", source_sha + ":" + safe_path(path)))
    if binding.get("schema") != 1:
        raise AuthorizationError("PRODUCER_BINDING_UNSUPPORTED", "unsupported producer binding / acceptance rule")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", binding["repository"]):
        raise ValueError("invalid source repository")
    if not isinstance(binding["repository_id"], int):
        raise ValueError("source repository identity is required")
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


def package_binding(binding, coordinate):
    matches = [p for p in binding["packages"] if p["coordinate"] == coordinate]
    if len(matches) != 1:
        raise AuthorizationError("HISTORICAL_BINDING_UNRESOLVED", "historical package binding requires owner disposition")
    return matches[0]


def revision_binding(root, revision, path):
    """Git owns the policy chronology; today's pin cannot rewrite old rules."""
    try:
        return binding_at(root, revision, path, allow_local=True)
    except (ValueError, KeyError, TypeError) as error:
        raise AuthorizationError("HISTORICAL_BINDING_UNRESOLVED", "historical producer binding is unavailable") from error


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
            request = urllib.request.Request("https://api.github.com/repos/" + self.repository + ("/" + path if path else ""),
                                             headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    self.cache[path] = json.load(response)
            except Exception:
                raise AuthorizationError("ACCEPTANCE_EVIDENCE_UNAVAILABLE", "GitHub evidence unavailable") from None
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


def valid_ci(run, binding, revision, workflow_id=None):
    return (run["head_sha"] == revision and run["event"] == "push"
            and run["head_branch"] == binding["branch"] and run["status"] == "completed"
            and run["conclusion"] == "success"
            and run.get("path") == binding["ci_workflow"]
            and (workflow_id is None or run["workflow_id"] == workflow_id)
            and run["head_repository"]["id"] == binding["repository_id"]
            and run["repository"]["id"] == binding["repository_id"])


def verify_trigger(api, binding, source_sha):
    if os.environ.get("GITHUB_EVENT_NAME") != "workflow_run":
        return
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    run = api.get("actions/runs/" + str(int(event["workflow_run"]["id"])))
    if not valid_ci(run, binding, source_sha):
        raise AuthorizationError("TRIGGER_RUN_MISMATCH", "automatic trigger is not the bound successful exact-source push run")


def owner_integration(api, binding, revision, parents):
    """Owner integration attests review; it does not prove independent review identity."""
    repository = api.get("")
    if (repository["id"], repository["full_name"]) != (binding["repository_id"], binding["repository"]):
        raise AuthorizationError("SOURCE_REPOSITORY_MISMATCH", "source repository identity differs")
    if len(parents) != 1:
        raise AuthorizationError("UNSUPPORTED_MERGE_ROUTE", "initial integration supports squash commits only")
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
        raise AuthorizationError("OWNER_ACCEPTANCE_NOT_ESTABLISHED", "no unambiguous authorized owner squash integration")
    pr = matches[0]
    return {"pr": pr["html_url"], "reviewed_head": pr["head"]["sha"],
            "integrator": pr["merged_by"]["login"], "source_sha": revision,
            "attestation": binding["acceptance"]}


def eligible(api, binding, revision, parents):
    # The producer owns review and integration mechanics. Only exact push CI
    # is publication evidence here; no PR, integrator or identity API lookup.
    # Run records retain the workflow path used at this source revision, even
    # after a workflow is renamed/deleted. Never resolve yesterday via today's
    # workflow-name endpoint.
    runs = api.pages(f"actions/runs?head_sha={revision}&event=push", "workflow_runs")
    runs = [run for run in runs if valid_ci(run, binding, revision)]
    if not runs:
        raise AuthorizationError("MATCHING_SOURCE_CI_MISSING", "no successful matching source-main push CI")
    return {"source_sha": revision, "ci_run": runs[0]["html_url"],
            "ci_workflow": binding["ci_workflow"], "ci_workflow_id": runs[0]["workflow_id"]}


def included_dependencies(blobs, manifest):
    """Qualify native lock/installed slots actually shipped by the allowlist.

    Resolution and hashes belong to VibeVM. This reads its committed evidence;
    it neither resolves ranges nor downloads/materializes additional content.
    """
    prefix = "vibevm/vibedeps/"
    slots = {}
    for name in blobs:
        if name.startswith(prefix):
            parts = name[len(prefix):].split("/")
            if len(parts) < 3:
                raise AuthorizationError("DEPENDENCY_CLOSURE_UNQUALIFIED", "included dependency has no native versioned slot")
            slots.setdefault((parts[0], parts[1]), {})["/".join(parts[2:])] = blobs[name]
    if slots:
        if "vibe.lock" not in blobs:
            raise AuthorizationError("DEPENDENCY_CLOSURE_UNQUALIFIED", "include the native vibe.lock for the exported dependency slots")
        lock = tomllib.loads(blobs["vibe.lock"].decode())
        if lock.get("meta", {}).get("schema_version") != 7:
            raise AuthorizationError("DEPENDENCY_CLOSURE_UNQUALIFIED", "materialize dependencies with pinned VibeVM schema-7 lock metadata")
        entries = lock.get("package", [])
    else:
        entries = []
    included = set()
    manifests = [manifest]
    for (identity, version), files in slots.items():
        if "vibe.toml" not in files:
            raise AuthorizationError("DEPENDENCY_CLOSURE_UNQUALIFIED", "included dependency slot is missing its native manifest")
        resolved = tomllib.loads(files["vibe.toml"].decode())
        metadata = resolved.get("package", {})
        group, name = metadata.get("group", ""), metadata.get("name", "")
        matches = [e for e in entries if (e.get("group"), e.get("name"), e.get("version")) == (group, name, version)]
        if (identity != group + "." + name or metadata.get("version") != version
                or not VERSION.fullmatch(version) or metadata.get("frozen") is not True
                or len(matches) != 1 or matches[0].get("kind") != metadata.get("kind")
                or not matches[0].get("source_url")
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", matches[0].get("content_hash", ""))):
            raise AuthorizationError("DEPENDENCY_CLOSURE_UNQUALIFIED", "included dependency needs frozen identity and native resolved source/content hash: " + identity)
        marker = tomllib.loads(files.get(".vibe-slot.toml", b"").decode())
        recorded = marker.get("file", [])
        hashes = {f: hashlib.sha256(data).hexdigest() for f, data in files.items() if f != ".vibe-slot.toml"}
        if (marker.get("schema") != 1 or marker.get("source_hash") != matches[0]["content_hash"]
                or len(recorded) != len(hashes)
                or {f["path"]: f["sha256"] for f in recorded} != hashes):
            raise AuthorizationError("DEPENDENCY_CLOSURE_UNQUALIFIED", "included slot differs from native materialization hashes/inventory: " + identity)
        included.add(group + "/" + name)
        manifests.append(resolved)
    # Check required edges for unresolved/excluded runtime members, including
    # transitives. Optional and dev declarations outside the shipped slots are
    # not the release closure. Included dev/optional slots were checked above.
    for resolved in manifests:
        for coordinate, requirement in resolved.get("requires", {}).get("packages", {}).items():
            if isinstance(requirement, dict) and requirement.get("optional") is True:
                continue
            coordinate = coordinate.removeprefix("flow:").removeprefix("skill:")
            if coordinate not in included:
                raise AuthorizationError("DEPENDENCY_CLOSURE_UNQUALIFIED", "materialize and approve the required dependency slot: " + coordinate)
    return sorted(included)


def snapshot(root, revision, package, require_ready=True):
    """Export only Git blobs, never worktree files, caches, or live observations."""
    if package["adapter"] == "shared-governance-v1":
        spec = importlib.util.spec_from_file_location("governance_export", ROOT / "scripts/prepare-distribution.py")
        exporter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exporter)
        exporter.ROOT = Path(root)
        files, receipt = exporter.snapshot(revision)
        if receipt["package"] != package["coordinate"]:
            raise ValueError("governance adapter coordinate differs from binding")
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
    if (require_ready and set(blobs) != set(package["files"])) or RECEIPT in blobs:
        raise AuthorizationError("PUBLIC_EXPORT_INCOMPLETE", "approved public export files missing or reserved receipt supplied")
    manifest = tomllib.loads(blobs["vibe.toml"].decode())
    metadata = manifest["package"]
    if (metadata["group"] + "/" + metadata["name"] != package["coordinate"]
            or not VERSION.fullmatch(metadata["version"]) or metadata.get("frozen") is not True):
        raise AuthorizationError("PACKAGE_IDENTITY_MISMATCH", "canonical frozen package identity differs")
    if require_ready:
        included_dependencies(blobs, manifest)
    if require_ready and not blobs["LICENSE"].strip():
        raise AuthorizationError("PUBLIC_EXPORT_INCOMPLETE", "public package license is empty")
    rights = package.get("redistribution", {})
    if require_ready and not (rights.get("status") == "approved" and rights.get("approval", "").startswith("https://")
            and rights.get("license") and rights["license"] == metadata.get("license")):
        raise AuthorizationError("REDISTRIBUTION_UNRESOLVED", "package license metadata or redistribution approval is unresolved")
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(blobs.items())}
    digest = hashlib.sha256(json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    receipt = {"schema": 1, "package": package["coordinate"], "version": metadata["version"],
               "disclosure": package["disclosure"],
               "payload_sha256": digest, "sha256": hashes}
    if package["disclosure"] == "public-source":
        receipt.update(source_revision=revision, source_path=package["root"])
    blobs[RECEIPT] = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
    return blobs, receipt


def payload(snapshot_value):
    if snapshot_value is None:
        return None
    receipt = snapshot_value[1]
    # Source SHA changes alone are not releases; deliberate disclosure changes
    # are versioned export content. The governance adapter keeps its own schema.
    return receipt["payload_sha256"], receipt.get("disclosure")


def initial_plan(root, initiation_sha, main, binding, api, binding_path, candidate_base=None):
    """Explicit first publication; current readiness never impersonates historic CI."""
    exact(root, initiation_sha)
    chain = git(root, "rev-list", "--first-parent", main).decode().splitlines()
    if candidate_base is not None:
        if not chain or candidate_base != chain[0]:
            raise ValueError("candidate base must be the current accepted source main")
        chain = [initiation_sha] + chain
    results = []
    for package in binding["packages"]:
        result = {"package": package["coordinate"], "source_sha": initiation_sha,
                  "initiation_sha": initiation_sha,
                  "destination": package["destination"], "operation": "initial-publication"}
        try:
            if initiation_sha not in chain:
                raise AuthorizationError("SOURCE_NOT_ON_MAIN", "initiation is not on first-parent main")
            if revision_binding(root, initiation_sha, binding_path) != binding:
                raise AuthorizationError("POLICY_PIN_MISMATCH", "initial publication requires the exact accepted binding")
            initial = package.get("initial_publication", {})
            frozen_sha = initial.get("source_sha", "")
            if (package["adapter"] != "tree-v1" or not SHA.fullmatch(frozen_sha)
                    or not VERSION.fullmatch(initial.get("version", ""))
                    or not re.fullmatch(r"[0-9a-f]{64}", initial.get("payload_sha256", ""))
                    or not package.get("baseline_disposition", "").startswith("https://")):
                raise AuthorizationError("INITIAL_PUBLICATION_UNRESOLVED", "explicit frozen source, version, digest and owner disposition are required")
            if frozen_sha not in chain or chain.index(frozen_sha) <= chain.index(initiation_sha):
                raise AuthorizationError("PACKAGE_BASELINE_UNRESOLVED", "frozen source must precede initiation on first-parent main")
            parents = git(root, "show", "-s", "--format=%P", initiation_sha).decode().split()
            authority = binding
            # Only the accepted integration introducing this record is an initiation.
            # An unchanged declaration on a later factual commit cannot initiate.
            if git(root, "ls-tree", parents[0], "--", binding_path):
                before = revision_binding(root, parents[0], binding_path)
                prior = package_binding(before, package["coordinate"])
                if prior.get("initial_publication") == initial:
                    raise AuthorizationError("INITIAL_PUBLICATION_UNRESOLVED", "retry the original initiation, not a later commit")
                if any(before[k] != binding[k] for k in ("repository", "repository_id", "branch", "acceptance")):
                    raise AuthorizationError("HISTORICAL_BINDING_UNRESOLVED", "source identity policy changes require owner disposition")
                authority = dict(binding, authorized_integrators=before["authorized_integrators"])
            readiness = ({**owner_integration(api, authority, initiation_sha, parents),
                          **eligible(api, authority, initiation_sha, parents)} if candidate_base is None else None)
            source_parents = git(root, "show", "-s", "--format=%P", frozen_sha).decode().split()
            source_acceptance = (owner_integration(api, binding, frozen_sha, source_parents)
                                 if candidate_base is None else None)
            frozen = snapshot(root, frozen_sha, package)
            current = snapshot(root, initiation_sha, package)
            if (frozen is None or current is None or frozen[1]["version"] != initial["version"]
                    or frozen[1]["payload_sha256"] != initial["payload_sha256"]
                    or payload(frozen) != payload(current)):
                raise AuthorizationError("PACKAGE_VERSION_REUSE", "initial publication must retain the attested frozen payload")
            # The explicitly approved inventory is used to compare source-only
            # history, never asserted to be a historical publisher policy.
            # Check the first accepted identity, not just today's remote tag.
            history = list(reversed(chain[chain.index(initiation_sha):]))
            first = None
            for revision in history:
                if (chain.index(revision) >= chain.index(frozen_sha)
                        and git(root, "ls-tree", revision, "--", binding_path)):
                    raise AuthorizationError("HISTORICAL_BINDING_UNRESOLVED", "initial publication does not override an existing historical publisher policy")
                value = snapshot(root, revision, package, require_ready=False)
                if value is not None and value[1]["version"] == initial["version"]:
                    first = first or revision
                    if payload(value) != payload(frozen):
                        raise AuthorizationError("PACKAGE_VERSION_REUSE", "accepted frozen identity changed in source history")
            if first != frozen_sha:
                raise AuthorizationError("PACKAGE_VERSION_REUSE", "attestation must name the first source-main integration of this version")
            result.update(status="CANDIDATE_VALID" if candidate_base is not None else "READY",
                          source_sha=frozen_sha, version=initial["version"],
                          payload_sha256=initial["payload_sha256"],
                          baseline_disposition=package["baseline_disposition"],
                          source_acceptance=source_acceptance, readiness_acceptance=readiness)
        except (ValueError, KeyError, TypeError) as error:
            result.update(status="AUTHORIZATION_PENDING", reason=str(error),
                          reason_code=error.code if isinstance(error, AuthorizationError) else "INITIAL_PUBLICATION_UNRESOLVED")
        results.append(result)
    return {"source_sha": initiation_sha,
            "operation": "initial-publication", "packages": results}


def plan(root, source_sha, main, binding, api, binding_path, candidate_base=None):
    """Compare one source transition; never reconstruct historical eligibility."""
    exact(root, source_sha)
    chain = git(root, "rev-list", "--first-parent", main).decode().splitlines()
    if candidate_base is None and source_sha not in chain:
        raise AuthorizationError("SOURCE_NOT_ON_MAIN", "source is not on first-parent source main")
    if candidate_base is not None:
        exact(root, candidate_base)
        if not chain or candidate_base != chain[0]:
            raise ValueError("candidate base must be the current accepted source main")
    # The source commit is the only configuration identity, including on retry.
    if binding_at(root, source_sha, binding_path, allow_local=True) != binding:
        raise ValueError("binding must come from the exact source commit")
    parents = git(root, "show", "-s", "--format=%P", source_sha).decode().split()
    previous_sha = candidate_base or (parents[0] if parents else None)
    previous_binding = None
    if previous_sha and git(root, "ls-tree", previous_sha, "--", binding_path):
        previous_binding = binding_at(root, previous_sha, binding_path, allow_local=True)
    results = []
    for package in binding["packages"]:
        result = {"package": package["coordinate"], "source_sha": source_sha,
                  "destination": package["destination"]}
        try:
            current = snapshot(root, source_sha, package, require_ready=False)
            # When an immediate previous binding exists use its own export
            # inventory. Initial late onboarding compares the unchanged source
            # under the newly selected inventory without demanding older policy.
            prior_package = package
            if previous_binding is not None:
                prior_package = next((p for p in previous_binding["packages"]
                                      if p["coordinate"] == package["coordinate"]), None)
                if prior_package is not None and any(prior_package[k] != package[k]
                                                     for k in ("root", "adapter", "destination")):
                    raise AuthorizationError("PACKAGE_MAPPING_CHANGED", "immediate package mapping changed")
            previous = (snapshot(root, previous_sha, prior_package, require_ready=False)
                        if previous_sha and prior_package is not None else None)
            inventory_changed = (previous_binding is not None and prior_package is not None
                                 and set(prior_package.get("files", [])) != set(package.get("files", [])))
            if payload(current) == payload(previous) and not inventory_changed:
                result["status"] = "NO_PACKAGE_CHANGE"
            else:
                if current is None:
                    raise AuthorizationError("OWNER_DISPOSITION_REQUIRED", "package removal requires owner disposition")
                if previous and previous[1]["version"] == current[1]["version"]:
                    raise AuthorizationError("PACKAGE_VERSION_REUSE", "package payload changed without a new version")
                snapshot(root, source_sha, package)
                acceptance = [] if candidate_base is not None else [eligible(api, binding, source_sha, parents)]
                result.update(status="CANDIDATE_VALID" if candidate_base is not None else "READY",
                              version=current[1]["version"], payload_sha256=current[1]["payload_sha256"],
                              acceptance=acceptance)
        except (ValueError, KeyError, TypeError) as error:
            result.update(status="AUTHORIZATION_PENDING", reason=str(error),
                          reason_code=error.code if isinstance(error, AuthorizationError)
                          else "ACCEPTANCE_OR_OWNER_DISPOSITION_UNRESOLVED")
        results.append(result)
    return {"source_sha": source_sha, "packages": results}


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
        result.update(status="ALREADY_PUBLISHED", remote_refs=remote_refs(package["destination"], tag),
                      warning="Existing identity retained; the retry source has not been proven published.")
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
        result.update(status="FAILED_OR_PENDING", reason="Atomic publication failed or transport result is ambiguous; retry the same source SHA and workflow implementation pin.")
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
                          reason="No release tag observed; retry the same source SHA and workflow implementation pin.")
    except ValueError:
        result.update(status="FAILED_OR_PENDING", reason="Publication readback unavailable; inspect and retry the same source SHA and workflow implementation pin.")
    return result


def stage_all(root, binding, report, vibe, directory, selected):
    results = []
    for package, decision in zip(binding["packages"], report["packages"]):
        if selected and package["coordinate"] != selected:
            continue
        try:
            result = stage(root, package, decision, vibe, Path(directory) / package["coordinate"].replace("/", "."))
        except (ValueError, OSError, subprocess.SubprocessError) as error:
            result = {**decision, "status": "FAILED_OR_PENDING",
                      "reason": "Credential-free preparation did not complete; no destination write was attempted.",
                      "failure_code": staging_failure_code(error)}
        results.append(result)
    if selected and not results:
        raise ValueError("selected package is absent from the accepted binding")
    return {**report, "packages": results}


def write_report(report, path):
    Path(path).write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    # Artifacts are deliberately not uploaded: private source identity can be sensitive.
    for result in report["packages"]:
        code, message = operator_diagnostic(result)
        print(f"{result['package']}: {result['status']} — {code}: {message}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("check", "plan", "stage", "finalize", "summary"))
    parser.add_argument("--base", help="Exact accepted main for source-time candidate checks")
    parser.add_argument("--initial-publication", action="store_true",
                        help="Explicitly initiate the frozen version attested in the accepted onboarding binding")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--source-sha")
    parser.add_argument("--main", default="origin/main")
    parser.add_argument("--binding")
    parser.add_argument("--package", help="One destination per named-secret workflow call")
    parser.add_argument("--vibe", type=Path)
    parser.add_argument("--directory", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    args = parser.parse_args()
    if args.operation == "summary":
        if not args.summary:
            raise ValueError("summary output path is required")
        outcomes = {phase: os.environ.get(phase.upper() + "_OUTCOME", "unknown")
                    for phase, _, _ in SUMMARY_PHASES}
        append_actions_summary(args.report, args.summary,
                               os.environ.get("PUBLICATION_JOB_STATUS", "unknown"), outcomes)
        return 0
    if args.operation == "finalize":
        report = json.loads(args.report.read_text())
        if len(report["packages"]) != 1:
            raise ValueError("finalize requires one destination per named credential")
        report["packages"] = [finalize(report["packages"][0])]
    else:
        binding = binding_at(args.source, args.source_sha, args.binding)
        api = GitHub(binding["repository"], os.environ.get("GH_TOKEN"))
        if args.operation == "check" and not args.base:
            raise ValueError("candidate check requires an exact accepted base")
        planner = initial_plan if args.initial_publication else plan
        report = planner(args.source, args.source_sha, args.main, binding, api,
                         args.binding, args.base if args.operation == "check" else None)
        # No-op onboarding must not query even the triggering CI run.
        if args.operation != "check" and any(p["status"] == "READY" for p in report["packages"]):
            verify_trigger(api, binding, args.source_sha)
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
