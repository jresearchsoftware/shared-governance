#!/usr/bin/env python3
"""Exercise the producer workflow's real shell resolution without GitHub or secrets."""
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / ".github/workflows/publish.yml").read_text()


def step_script(name):
    step = WORKFLOW.split("      - name: " + name + "\n", 1)[1]
    body = step.split("        run: |\n", 1)[1]
    lines = []
    for line in body.splitlines():
        if line and not line.startswith("          "):
            break
        lines.append(line)
    return textwrap.dedent("\n".join(lines))


class Dispatch(unittest.TestCase):
    def resolve(self, **overrides):
        env = dict(os.environ, EVENT_NAME="workflow_dispatch", DISPATCH_REF="refs/heads/main",
                   DISPATCH_SHA="a" * 40, INPUT_SOURCE_SHA="", RUN_SOURCE_SHA="b" * 40,
                   RUN_EVENT="push", RUN_BRANCH="main", RUN_REPOSITORY="owner/repository",
                   REPOSITORY="owner/repository")
        env.update(overrides)
        env = {key: value for key, value in env.items() if value is not None}
        with tempfile.TemporaryDirectory() as directory:
            output, summary = (Path(directory) / item for item in ("output", "summary"))
            env.update(GITHUB_OUTPUT=str(output), GITHUB_STEP_SUMMARY=str(summary))
            result = subprocess.run(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c",
                                     step_script("Resolve the exact accepted source revision")],
                                    env=env, capture_output=True, text=True)
            return result.returncode, output.read_text() if output.exists() else "", summary.read_text()

    def test_blank_dispatch_freezes_event_sha(self):
        status, output, summary = self.resolve()
        self.assertEqual(status, 0)
        self.assertEqual(output, "source_sha=" + "a" * 40 + "\n")
        self.assertIn("`" + "a" * 40 + "`", summary)

    def test_omitted_dispatch_input_freezes_event_sha(self):
        status, output, _ = self.resolve(INPUT_SOURCE_SHA=None)
        self.assertEqual(status, 0)
        self.assertEqual(output, "source_sha=" + "a" * 40 + "\n")

    def test_explicit_dispatch_keeps_old_exact_sha(self):
        status, output, _ = self.resolve(INPUT_SOURCE_SHA="c" * 40)
        self.assertEqual(status, 0)
        self.assertEqual(output, "source_sha=" + "c" * 40 + "\n")

    def test_workflow_run_uses_its_head_not_current_main(self):
        status, output, _ = self.resolve(EVENT_NAME="workflow_run")
        self.assertEqual(status, 0)
        self.assertEqual(output, "source_sha=" + "b" * 40 + "\n")

    def test_rejects_malformed_non_main_and_inconsistent_inputs(self):
        for override in ({"INPUT_SOURCE_SHA": value} for value in
                         ("main", "A" * 40, "a" * 39, "a" * 41, " " * 40, "a" * 40 + "\n")):
            with self.subTest(override=override):
                status, output, summary = self.resolve(**override)
                self.assertNotEqual(status, 0)
                self.assertEqual(output, "")
                self.assertIn("Source resolution rejected", summary)
        for override in ({"DISPATCH_REF": "refs/heads/topic"}, {"DISPATCH_SHA": "main"},
                         {"EVENT_NAME": "workflow_run", "RUN_BRANCH": "topic"},
                         {"EVENT_NAME": "workflow_run", "RUN_EVENT": "pull_request"},
                         {"EVENT_NAME": "workflow_run", "RUN_REPOSITORY": "other/repository"},
                         {"EVENT_NAME": "workflow_run", "RUN_SOURCE_SHA": "main"},
                         {"EVENT_NAME": "workflow_run", "INPUT_SOURCE_SHA": "c" * 40}):
            with self.subTest(override=override):
                status, output, summary = self.resolve(**override)
                self.assertNotEqual(status, 0)
                self.assertEqual(output, "")
                self.assertIn("Source resolution rejected", summary)

    def test_all_consumers_use_resolved_output(self):
        downstream = WORKFLOW.split("  readiness:\n", 1)[1]
        self.assertNotIn("inputs.source_sha", downstream)
        self.assertNotIn("workflow_run.head_sha", downstream)
        self.assertNotIn("github.sha", downstream)
        self.assertIn("ref: ${{ needs.resolve.outputs.source_sha }}", downstream)
        self.assertIn("SOURCE_SHA: ${{ needs.resolve.outputs.source_sha }}", downstream)
        self.assertIn("source_sha: ${{ needs.resolve.outputs.source_sha }}", downstream)
        self.assertIn("group: package-publication-${{ needs.resolve.outputs.source_sha }}", downstream)
        self.assertIn("required: false", WORKFLOW.split("permissions:", 1)[0])

    def test_source_checkout_mismatch_and_non_main_commit_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            producer = Path(directory) / "producer"
            producer.mkdir()
            def git(*args):
                return subprocess.check_output(["git", "-C", str(producer), *args], text=True).strip()
            git("init", "-q", "-b", "main")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-qm", "main")
            main = git("rev-parse", "HEAD")
            git("update-ref", "refs/remotes/origin/main", main)
            script = step_script("Verify the exact source checkout belongs to main")
            def check(revision):
                return subprocess.run(["bash", "-e", "-o", "pipefail", "-c", script],
                                      cwd=directory, env=dict(os.environ, SOURCE_SHA=revision),
                                      capture_output=True).returncode
            self.assertEqual(check(main), 0)
            self.assertNotEqual(check("0" * 40), 0)
            # main moves after dispatch; checkout retains the captured event SHA.
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-qm", "later main")
            git("update-ref", "refs/remotes/origin/main", git("rev-parse", "HEAD"))
            git("checkout", "--detach", main)
            self.assertEqual(check(main), 0)
            git("checkout", "-qb", "topic")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-qm", "topic")
            self.assertNotEqual(check(git("rev-parse", "HEAD")), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
