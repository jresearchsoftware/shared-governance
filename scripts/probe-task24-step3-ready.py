#!/usr/bin/env python3
"""Final native ready-checkout/startup/restoration probe on supported Linux Codex."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibe", type=Path, required=True)
    parser.add_argument("--codex", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    base = Path(tempfile.mkdtemp(prefix="task24-step3-ready-"))
    work = base / "clean"
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "--no-hardlinks", str(ROOT), str(work)], check=True)
    subprocess.run(["git", "checkout", "-q", "--detach", revision], cwd=work, check=True)
    spec = importlib.util.spec_from_file_location("exporter", ROOT / "scripts/prepare-distribution.py")
    exporter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exporter)
    receipt = exporter.verify_producer(revision, work)
    observations = {"clean_ready_without_installation": "PASS"}
    cases = []
    result = dict(candidate_source=revision, production_accepted_authority="96d26c51b6d05ee5ec4576a44f541b904f0f13fb",
                  scope="isolated hypothetical future accepted checkout; no acceptance granted",
                  fixture=str(base), cases=cases, observations=observations)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    def save():
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    prompt = f"""Task 24 Step 3 isolated future-ready-startup qualification. This is not
independent acceptance. For this disposable probe ONLY, model a future independently
accepted checkout at fixture commit {revision}. The production authoring effort
retains independently accepted 96d26c51b6d05ee5ec4576a44f541b904f0f13fb; this probe
does not activate candidate guidance there. Resolve the fixture root AGENTS and
follow its native file-reading boot routes. No rule contents are supplied inline.
Assess a hypothetical governed producer task proposing an additional approval
command and a patch package correction. Read only applicable explicitly adopted
protocols through the committed slot routes, preserving conditional relative links.
Report files actually read, fixture identity, adoption conditions, protected
authority and whether a publication outage prevents accepted-source reading.
No edits, network, installation, bootstrap, host repair or independent approval.
Use the ordinary read-only sandbox; report a denied operation without bypass.
"""
    (args.output.parent / "ready-startup-prompt.txt").write_text(prompt, encoding="utf-8")
    argv = [str(args.codex), "exec", "--json", "-C", str(work), "--sandbox", "read-only", "--model", args.model, "--ephemeral", "-"]
    proc = subprocess.run(argv, input=prompt, text=True, capture_output=True, timeout=300)
    events = []
    for line in proc.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    cases.append(dict(label="real-native-file-startup", argv=argv, exit=proc.returncode, events=events, warnings=proc.stderr.splitlines()))
    save()
    print(json.dumps(dict(label="real-native-file-startup", exit=proc.returncode)), flush=True)
    # Deliberate recovery after startup, using fresh fixture-local settings.
    slot = work / exporter.slot(receipt["version"])
    protocol = slot / exporter.HANDOFF
    expected = protocol.read_bytes()
    for label in ("corrupt", "missing"):
        if label == "corrupt":
            protocol.write_text("Disposable damaged guidance\n")
        else:
            shutil.rmtree(slot)
        settings = base / (label + "-settings")
        env = dict(os.environ, VIBE_SETTINGS=str(settings), VIBEVM_USER_CONFIG=str(settings / "config.toml"))
        argv = [str(args.vibe), "--json", "reinstall", str(work), "--force", "--offline", "--assume-yes"]
        restored = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=120)
        cases.append(dict(label=label + "-pinned-native-restoration", argv=argv, exit=restored.returncode, stdout=restored.stdout, stderr=restored.stderr))
        try:
            exporter.verify_producer(revision, work)
            observations[label + "_canonical_restoration"] = "PASS" if protocol.read_bytes() == expected else "FAIL"
        except (ValueError, OSError) as error:
            observations[label + "_canonical_restoration"] = str(error)
        save()
        print(json.dumps(dict(label=label, result=observations[label + "_canonical_restoration"])), flush=True)
    result["vibe_sha256"] = hashlib.sha256(args.vibe.read_bytes()).hexdigest()
    result["codex_sha256"] = hashlib.sha256(args.codex.read_bytes()).hexdigest()
    save()


if __name__ == "__main__":
    main()
