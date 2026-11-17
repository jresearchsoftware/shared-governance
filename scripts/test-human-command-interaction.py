#!/usr/bin/env python3
"""Execute the published guide's blocks; no services, privileges or external effects."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "packages/development-governance/vibevm/vibespecs/guides/human-command-interaction.md"
TEXT = GUIDE.read_text(encoding="utf-8")
BASH, = re.findall(r"^```bash\n(.*?)^```", TEXT, re.M | re.S)
POWERSHELL, SERVICE = re.findall(r"^```powershell\n(.*?)^```", TEXT, re.M | re.S)
PWSH = None


class Examples(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="human-command-", dir=ROOT / ".vibe")
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def assert_report(self, output, failed=False):
        self.assertEqual(output.count("BEGIN environment report"), 1)
        self.assertEqual(output.count("END environment report"), 1)
        self.assertTrue(output.startswith("BEGIN environment report\n"), output)
        self.assertTrue(output.rstrip().endswith("END environment report"), output)
        self.assertIn("OVERALL=" + str(int(failed)), output)

    def bash(self, overrides=None):
        environment = os.environ.copy()
        if overrides is not None:
            binaries = self.directory / "bin"
            binaries.mkdir()
            # A wrapper, not a symlink/import of external workspace content.
            overrides = {"bash": 'exec /bin/bash "$@"\n', **overrides}
            for name, body in overrides.items():
                executable = binaries / name
                executable.write_text("#!/bin/sh\n" + body, encoding="utf-8")
                executable.chmod(0o700)
            environment["PATH"] = str(binaries)
        return subprocess.run(["/bin/bash", "-c", BASH], cwd=self.directory,
                              env=environment, capture_output=True, text=True, timeout=30)

    def powershell(self, block=POWERSHELL, prefix="", suffix=""):
        if not PWSH:
            self.skipTest("PowerShell unavailable; supply --pwsh for runtime proof")
        script = self.directory / "example.ps1"
        script.write_text(prefix + "\n" + block + "\n" + suffix, encoding="utf-8")
        return subprocess.run([PWSH, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(script)],
                              cwd=self.directory, capture_output=True, text=True, timeout=30)

    def test_bash_real_diagnostics(self):
        result = self.bash()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(result.stderr, "")
        self.assert_report(result.stdout)
        self.assertEqual(result.stdout.count("STATUS=0"), 3)
        self.assertLess(result.stdout.index("[OS]"), result.stdout.index("[User ID]"))
        self.assertLess(result.stdout.index("[User ID]"), result.stdout.index("[Current filesystem"))

    def test_bash_multiple_failures_keep_errors_and_later_success(self):
        result = self.bash({"uname": "echo 'fixture OS error' >&2\nexit 7\n",
                            "id": "echo 'fixture numeric id'\n",
                            "df": "echo 'fixture disk denied' >&2\nexit 9\n"})
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assert_report(result.stdout, failed=True)
        for expected in ("fixture OS error", "STATUS=7", "fixture numeric id", "STATUS=0",
                         "fixture disk denied", "STATUS=9"):
            self.assertIn(expected, result.stdout)

    def test_bash_missing_command_is_not_silent_success(self):
        result = self.bash({"uname": "echo fixture-os\n", "id": "echo 42\n"})
        self.assertEqual(result.returncode, 1)
        self.assert_report(result.stdout, failed=True)
        self.assertIn("command not found", result.stdout)
        self.assertIn("STATUS=127", result.stdout)

    def test_bash_child_failure_does_not_close_parent_shell(self):
        block = BASH.replace("check 'OS' uname -s", "check 'OS' false")
        result = subprocess.run(["/bin/bash", "-c", block + '\nprintf "PARENT child-status=%s\\n" "$?"\n'],
                                cwd=self.directory, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0)
        self.assertIn("OVERALL=1", result.stdout)
        self.assertIn("PARENT child-status=1", result.stdout)

    def test_powershell_real_diagnostics(self):
        result = self.powershell()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assert_report(result.stdout)
        self.assertEqual(result.stdout.count("STATUS=0"), 3)
        self.assertIn(str(self.directory), result.stdout)
        self.assertIn("[Filesystem drives (bytes)]", result.stdout)

    def test_powershell_nonterminating_error_preserves_later_sections(self):
        prefix = """
function Get-Date { Write-Error 'fixture clock denied' }
function Get-Location { [pscustomobject]@{Path='fixture location'} }
function Get-PSDrive { [pscustomobject]@{Name='Fixture';Used=42;Free=99} }
"""
        result = self.powershell(prefix=prefix)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assert_report(result.stdout, failed=True)
        self.assertIn("ERROR: fixture clock denied", result.stdout)
        self.assertEqual(result.stdout.count("STATUS=1"), 1)
        self.assertEqual(result.stdout.count("STATUS=0"), 2)
        self.assertIn("fixture location", result.stdout)
        self.assertIn("Fixture", result.stdout)
        self.assertIn("42", result.stdout)
        self.assertIn("99", result.stdout)

    def test_powershell_scope_and_single_string_copyback(self):
        prefix = "$ErrorActionPreference = 'Continue'\n$captured = @(\n"
        suffix = """
)
if ($captured.Count -ne 1 -or $captured[0] -isnot [string]) { throw 'not one string' }
if ($ErrorActionPreference -ne 'Continue') { throw 'preference leaked' }
if (Get-Command Add-Check -ErrorAction SilentlyContinue) { throw 'helper leaked' }
$captured[0]
'PARENT still running'
"""
        result = self.powershell(prefix=prefix, suffix=suffix)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OVERALL=0", result.stdout)
        self.assertIn("PARENT still running", result.stdout)

    def test_powershell_native_adaptation_captures_nonzero_exit(self):
        # Exercise the guide's native-status advice inside its reporting helper.
        # This Linux-only fixture is not a claim about Windows native streams.
        if os.name != "posix":
            self.skipTest("POSIX native-executable fixture")
        tool = self.directory / "native-failure"
        tool.write_text("#!/bin/sh\necho fixture-native-output\nexit 23\n")
        tool.chmod(0o700)
        native = """Add-Check 'Native fixture' {
        & './native-failure'
        $nativeStatus = $LASTEXITCODE
        if ($nativeStatus -ne 0) { throw "native exited $nativeStatus" }
    }"""
        adapted = POWERSHELL.replace("Add-Check 'Time' { Get-Date -Format o }", native)
        result = self.powershell(block=adapted)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assert_report(result.stdout, failed=True)
        self.assertIn("native exited 23", result.stdout)
        self.assertIn("fixture-native-output", result.stdout)
        self.assertEqual(result.stdout.count("STATUS=0"), 2)

    def test_protected_first_action_never_restarts_service(self):
        # Actual guide action, with a fixture service; no host service is touched.
        for status in ("Running", "Stopped", "Missing"):
            with self.subTest(status=status):
                prefix = """
function Restart-Service { throw 'UNAUTHORIZED RESTART' }
function Get-Service {
    param($Name)
    if ($Name -ne 'Spooler') { throw 'unexpected service' }
""" + ("    throw 'fixture service missing'\n" if status == "Missing" else
       "    [pscustomobject]@{Name='Spooler';Status='" + status + "'}\n") + "}\n"
                result = self.powershell(block=SERVICE, prefix=prefix)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertNotIn("UNAUTHORIZED RESTART", result.stdout)
                self.assertIn("BEGIN print service report", result.stdout)
                self.assertIn("END print service report", result.stdout)
                self.assertIn("OVERALL=" + str(int(status == "Missing")), result.stdout)
                self.assertIn("fixture service missing" if status == "Missing" else status, result.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pwsh", default=shutil.which("pwsh"), help="PowerShell executable for runtime checks")
    args, rest = parser.parse_known_args()
    PWSH = str(Path(args.pwsh).resolve()) if args.pwsh else None
    (ROOT / ".vibe").mkdir(exist_ok=True)
    unittest.main(argv=[__file__, *rest])
