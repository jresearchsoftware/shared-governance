"""Offline projection of one template and owner-reviewed data; no settings API/resolver."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/chatgpt-bootstrap.md"
INDEX = "vibevm/vibespecs/boot/INDEX.md"
STATIC = "vibevm/vibespecs/boot/STATIC.md"
PERMISSIONS = {"discussion", "assessment", "orchestration", "authorized-publication",
               "authorized-integration", "authorized-continuation"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(value):
    require(isinstance(value, str) and value and "\\" not in value
            and not value.startswith("-") and ":" not in value
            and not PurePosixPath(value).is_absolute()
            and all(part not in ("", ".", "..") for part in value.split("/")),
            "Expected repository-relative source path")
    return value


class Snapshot:
    def __init__(self, repository, revision):
        require(re.fullmatch(r"[0-9a-f]{40}", revision), "Use an exact 40-character SHA")
        self.repository, self.revision = repository, revision
        require(self.git("rev-parse", revision + "^{commit}").decode().strip() == revision,
                "Revision must name that exact commit")
        self.files = {}
        for row in self.git("ls-tree", "-rz", revision).split(b"\0"):
            if row:
                metadata, name = row.split(b"\t", 1)
                mode, kind, oid = metadata.decode().split()
                self.files[name.decode()] = (mode, kind, oid)

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.repository), *args],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        require(result.returncode == 0, "Required Git object/operation unavailable: " + args[0])
        return result.stdout

    def read(self, path):
        safe_path(path)
        require(path in self.files, "Missing accepted source: " + path)
        mode, kind, oid = self.files[path]
        require(mode in ("100644", "100755") and kind == "blob",
                "Source must be an ordinary committed file: " + path)
        return self.git("cat-file", "blob", oid)


def native_inventory(source):
    """Consume generated INDEX and native slot receipts, never resolve dependencies."""
    require(INDEX in source.files and "vibe.lock" in source.files,
            "Native binding needs accepted INDEX and lock")
    index = tomllib.loads(source.read(INDEX).decode())
    require(index.get("schema") == 1, "Unsupported native INDEX schema")
    entries = index.get("entry", [])
    require(isinstance(entries, list), "Invalid INDEX entries")
    for entry in entries:
        require(entry.get("kind") in ("static", "dynamic"), "Unsupported INDEX kind")
        source.read(entry["path"])
        require("when" not in entry or isinstance(entry["when"], str), "Invalid condition")
    lock = tomllib.loads(source.read("vibe.lock").decode())
    # Verify the materializer's own receipts, not package ranges or dependency edges.
    slots = []
    require(lock.get("meta", {}).get("schema_version") == 7, "Unsupported native lock schema")
    for package in lock.get("package", []):
        slot = ("vibevm/vibedeps/" + package["group"] + "." + package["name"]
                + "/" + package["version"] + "/")
        slots.append(slot)
        receipt = tomllib.loads(source.read(slot + ".vibe-slot.toml").decode())
        require(receipt.get("schema") == 1, "Unsupported native slot receipt")
        require(receipt["source_hash"] == package["content_hash"], "Lock/slot identity mismatch")
        for item in receipt.get("file", []):
            require(digest(source.read(slot + safe_path(item["path"]))) == item["sha256"],
                    "Materialized file differs from native receipt")
    for entry in entries:
        if entry["path"].startswith("vibevm/vibedeps/"):
            require(any(entry["path"].startswith(slot) for slot in slots),
                    "INDEX route is not bound by the native lock")
    paths = {INDEX, "vibe.lock"}
    paths.update(entry["path"] for entry in entries)
    paths.update(path for path in source.files if path.startswith("vibevm/vibedeps/"))
    if STATIC in source.files:
        paths.add(STATIC)
    return paths, entries


def validate_binding(binding, accepted_sha, authority_anchor):
    require(binding.get("schema") == 1, "Unsupported binding schema")
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", binding["repository"]),
            "Invalid repository identity")
    require(binding["accepted_sha"] == accepted_sha and binding["authority_anchor"] == authority_anchor,
            "Binding differs from independently supplied authority")
    require(authority_anchor.startswith("https://github.com/" + binding["repository"] + "/"),
            "Authority anchor must belong to the bound project")
    require(binding["mode"] in ("orchestration-review", "read-only-preview"), "Unknown client mode")
    permissions = binding["permissions"]
    require(isinstance(permissions, list) and set(permissions) <= PERMISSIONS, "Unknown capability")
    require(binding["mode"] != "read-only-preview" or set(permissions) <= {"discussion", "assessment"},
            "Read-only preview cannot enable mutations")
    require(binding["native"] in ("materialized", "absent"), "Unknown native route mode")
    require(isinstance(binding["character_budget"], int) and 0 < binding["character_budget"] <= 8000,
            "Invalid owner-bound character budget")
    for field in ("role", "overlay", "client_limits"):
        require(isinstance(binding[field], str) and binding[field].strip(), "Missing binding field: " + field)
    for field in ("local_sources", "cache_selection"):
        require(isinstance(binding[field], list), "Expected path list: " + field)
        for path in binding[field]:
            safe_path(path)


def project(repository, binding, accepted_sha, authority_anchor, template=None, cache=False):
    validate_binding(binding, accepted_sha, authority_anchor)
    source = Snapshot(repository, accepted_sha)
    source.read("AGENTS.md")
    entries, paths = [], {"AGENTS.md"}
    if binding["native"] == "materialized":
        native, entries = native_inventory(source)
        paths.update(native)
    else:
        require(INDEX not in source.files and "vibe.lock" not in source.files,
                "Native state exists; cannot declare it absent")
    paths.update(binding["local_sources"])
    if cache:
        paths.update(binding["cache_selection"])
    inputs = {path: digest(source.read(path)) for path in sorted(paths)}
    base_url = f'https://github.com/{binding["repository"]}/blob/{accepted_sha}/'
    routes = "; ".join(f'[{path}]({base_url}{path})' for path in binding["local_sources"]) or "AGENTS discovery"
    block = (f'Repository: `{binding["repository"]}`. Client mode: {binding["mode"]}.\n'
             f'Role: {binding["role"]}\n\n'
             f'Accepted revision: `{accepted_sha}`; [independent authority anchor]({authority_anchor}). '
             f'[Start at accepted AGENTS]({base_url}AGENTS.md). A new effort establishes its own accepted '
             'binding; reconcile changed acceptance before using a new revision.\n\n'
             f'Capabilities, subject to current authority: {", ".join(binding["permissions"])}. '
             f'{binding["overlay"]}\n\nLocal/product/specialist entry points: {routes}.\n'
             f'Client limitations: {binding["client_limits"]}')
    template = TEMPLATE.read_text(encoding="utf-8") if template is None else template
    require(template.count("{{BINDING}}") == 1, "Expected one template binding")
    text = template.replace("{{BINDING}}", block)
    require("{{" not in text and "}}" not in text and "```" not in text, "Unresolved/unsafe template content")
    require(len(text) < binding["character_budget"], "Full Instructions exceed budget; never truncate")
    receipt = {"schema": 1, "repository": binding["repository"], "accepted_sha": accepted_sha,
               "authority_anchor": authority_anchor, "acceptance_verification": "external owner/review evidence required",
               "binding_sha256": digest(json.dumps(binding, sort_keys=True).encode()),
               "template_sha256": digest(template.encode()), "instructions_sha256": digest(text.encode()),
               "unicode_characters": len(text), "source_files": inputs, "native_entries": entries,
               "condition_disposition": "preserved, not evaluated or adopted by projector"}
    artifacts = {"instructions.md": "```markdown\n" + text + "```\n",
                 "receipt.json": json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"}
    if cache:
        require(binding["cache_selection"], "Cache export needs an explicit reviewed selection")
        manifest = {"schema": 1, "kind": "optional-source-cache", "repository": binding["repository"],
                    "accepted_sha": accepted_sha, "authority_anchor": authority_anchor,
                    "files": {path: inputs[path] for path in binding["cache_selection"]},
                    "limitations": "snapshot only; upload/addressability/freshness/activation unverified"}
        artifacts["sources-manifest.json"] = json.dumps(manifest, indent=2) + "\n"
        parts = ["# Optional source cache — schema 1\n\nSnapshot, not authority.\n"]
        for path in binding["cache_selection"]:
            parts.append(f'\n## {path}\n\nSource: {base_url}{path}\n\n' + source.read(path).decode())
        artifacts["sources.md"] = "".join(parts)
    return artifacts


def compare(artifacts, baseline, baseline_kind):
    old = baseline.read_text(encoding="utf-8") if baseline else "```markdown\n```\n"
    new = artifacts["instructions.md"]
    require(old.startswith("```markdown\n") and old.endswith("```\n") and old.count("```") == 2,
            "Baseline must be the complete single-fence Instructions export")
    old_text, new_text = old[len("```markdown\n"):-len("```\n")], new[len("```markdown\n"):-len("```\n")]
    delta = "".join(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                        fromfile="baseline-instructions", tofile="proposed-instructions"))
    return {"schema": 1, "baseline_kind": baseline_kind,
            "settings_text": "NO_OP" if old == new else "CHANGED",
            "live_settings_verified": False,
            "baseline_provenance": "owner-supplied export; tool cannot verify UI" if baseline_kind == "owner-export"
                                   else "unverified " + baseline_kind,
            "application": "owner applies/readbacks; preserve unknown live rules"}, delta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True, help="Local Git object store; no fetch")
    parser.add_argument("--binding", type=Path, required=True)
    parser.add_argument("--accepted-sha", required=True, help="Independently verified authority, never inferred")
    parser.add_argument("--authority-anchor", required=True)
    parser.add_argument("--output", type=Path, required=True, help="New local review bundle directory")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--baseline-kind", required=True, choices=("assumed-empty", "candidate", "owner-export"))
    parser.add_argument("--previous-receipt", type=Path)
    parser.add_argument("--cache", action="store_true", help="Optional selected snapshot, never upload")
    args = parser.parse_args()
    try:
        require((args.baseline_kind == "assumed-empty") == (args.baseline is None), "Explicit baseline required")
        binding = json.loads(args.binding.read_text(encoding="utf-8"))
        artifacts = project(args.repository, binding, args.accepted_sha, args.authority_anchor, cache=args.cache)
        status, delta = compare(artifacts, args.baseline, args.baseline_kind)
        receipt = json.loads(artifacts["receipt.json"])
        status["source_changes"] = "UNKNOWN_NO_PREVIOUS_RECEIPT"
        if args.previous_receipt:
            previous = json.loads(args.previous_receipt.read_text(encoding="utf-8"))
            require(previous["repository"] == binding["repository"], "Previous receipt is for another project")
            before, after = previous["source_files"], receipt["source_files"]
            status["source_changes"] = [path for path in sorted(before.keys() | after.keys())
                                        if before.get(path) != after.get(path)]
        artifacts["settings.diff"] = delta or "No settings text change.\n"
        artifacts["maintenance.json"] = json.dumps(status, indent=2) + "\n"
        # Refuse overwriting existing bundles, source trees or unknown local files.
        args.output.mkdir(parents=True, exist_ok=False)
        for name, value in artifacts.items():
            (args.output / name).write_text(value, encoding="utf-8", newline="\n")
        print(json.dumps(status, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, "Projection refused: " + str(error) + "\n")


if __name__ == "__main__":
    main()
