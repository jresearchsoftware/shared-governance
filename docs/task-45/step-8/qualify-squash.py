#!/usr/bin/env python3
"""One-time Step 8 proof: candidate tree on accepted history without PR objects."""
import argparse
import io
from pathlib import Path
import subprocess
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[3]
ACCEPTED = "ec048fb39ae28cf2d747101466a603ddd062b1b0"
STEP6 = "b76ea98e6ee2645be674690094f88a6fa265d77d"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-ref", required=True, help="committed candidate tree to squash")
    parser.add_argument("--focused-only", action="store_true", help="run only the history regression")
    args = parser.parse_args()
    candidate = subprocess.check_output(
        ["git", "rev-parse", args.source_ref + "^{commit}"], cwd=ROOT, text=True).strip()
    archive = subprocess.check_output(["git", "archive", candidate], cwd=ROOT)
    with tempfile.TemporaryDirectory(prefix="task45-step8-squash-") as temporary:
        fixture = Path(temporary)

        def run(*command):
            print("+ " + " ".join(command), flush=True)
            subprocess.run(command, cwd=fixture, check=True)

        run("git", "init", "-q")
        # Fetch only accepted ancestry; no clone hardlinks, task refs or alternates.
        run("git", "fetch", "--no-tags", str(ROOT), ACCEPTED)
        run("git", "checkout", "-qb", "main", "FETCH_HEAD")
        for key, value in (("user.name", "Disposable squash fixture"),
                           ("user.email", "squash@example.invalid"),
                           ("commit.gpgsign", "false"), ("core.autocrlf", "false"),
                           ("core.hooksPath", str(fixture / "no-hooks"))):
            run("git", "config", key, value)
        # Remove the accepted tracked tree through Git, retaining only its history.
        run("git", "rm", "-qr", ".")
        # This archive is produced from the identified local repository tree.
        with tarfile.open(fileobj=io.BytesIO(archive)) as snapshot:
            for member in snapshot.getmembers():
                assert member.isfile() or member.isdir(), "Unexpected archive member type"
                assert (fixture / member.name).resolve().is_relative_to(fixture)
            snapshot.extractall(fixture)
        run("git", "add", ".")
        run("git", "commit", "-qm", "Synthetic owner squash of candidate tree")
        print("Candidate tree: " + candidate, flush=True)
        run("git", "rev-parse", "HEAD", "HEAD^", "HEAD^{tree}")
        expected_tree = subprocess.check_output(
            ["git", "rev-parse", candidate + "^{tree}"], cwd=ROOT, text=True).strip()
        actual_tree = subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=fixture, text=True).strip()
        assert actual_tree == expected_tree, "Synthetic squash changed candidate bytes/modes"
        assert not (fixture / ".git/objects/info/alternates").exists()
        for revision in {STEP6, candidate}:
            result = subprocess.run(["git", "cat-file", "-e", revision + "^{commit}"],
                                    cwd=fixture, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert result.returncode != 0, "PR-only commit unexpectedly available: " + revision
            print("ABSENT commit object: " + revision, flush=True)
        if args.focused_only:
            run("python3", "scripts/test-distribution.py",
                "DistributionTests.test_pr_readiness_rule_keeps_prior_addresses_and_its_lifecycle_owner")
        else:
            # Same commands as candidate.yml's main-push path, with its before SHA.
            run("python3", "scripts/qualify.py", "--export-ref", "HEAD")
            for script in ("test-distribution.py", "test-release.py", "test-self-adoption.py",
                           "test-chatgpt-projection.py"):
                run("python3", "scripts/" + script)
            run("python3", "scripts/package-release.py", "--source-ref", "HEAD", "--base", ACCEPTED)
            run("git", "diff", "--check", ACCEPTED, "HEAD")
        print("PASS: synthetic fresh-main history qualification", flush=True)


if __name__ == "__main__":
    main()
