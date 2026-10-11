"""Picker regressions; run with python3 -m unittest discover -s tests."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PickerTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="fmenu-test-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.log = self.root / "fzf.json"
        self.env = os.environ.copy()
        for key in ("FZF_DEFAULT_COMMAND", "FZF_DEFAULT_OPTS", "FZF_DEFAULT_OPTS_FILE"):
            self.env.pop(key, None)
        self.env.update(
            PATH=f"{self.bin}{os.pathsep}{self.env['PATH']}",
            XDG_CONFIG_HOME=str(self.root / "config"),
            FMENU_TEST_LOG=str(self.log),
        )
        self.script("fzf", """import json, os, sys
from pathlib import Path
Path(os.environ['FMENU_TEST_LOG']).write_text(json.dumps({
    'args': sys.argv[1:],
    'command': os.environ.get('FZF_DEFAULT_COMMAND'),
    'options': os.environ.get('FZF_DEFAULT_OPTS'),
}))
sys.exit(130)
""")

    def script(self, name, source):
        path = self.bin / name
        path.write_text("#!/usr/bin/env python3\n" + source)
        path.chmod(0o755)
        return path

    def picker(self, name):
        result = subprocess.run(
            [str(ROOT / name)], env=self.env, cwd=self.root,
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=5,
        )
        self.assertTrue(self.log.exists(), result.stderr)
        return json.loads(self.log.read_text())

    def test_without_optional_config(self):
        for picker, mode in (("vfzf", "edit"), ("zfzf", "document")):
            with self.subTest(picker=picker):
                self.log.unlink(missing_ok=True)
                self.assertEqual(self.picker(picker)["command"], f"fzf-files {mode}")

    def test_config_can_append_unset_options(self):
        config = self.root / "config/fzf/config.sh"
        config.parent.mkdir(parents=True)
        config.write_text('export FZF_DEFAULT_OPTS="$FZF_DEFAULT_OPTS --multi"\n')
        for picker in ("vfzf", "zfzf"):
            with self.subTest(picker=picker):
                self.log.unlink(missing_ok=True)
                self.assertEqual(self.picker(picker)["options"], " --multi")

    def editor_action(self, shell, name="mock editor"):
        editor = self.script(name, "import json, sys\nprint(json.dumps(sys.argv[1:]))\n")
        self.env.update(EDITOR=f"{shlex.quote(str(editor))} --clean 'two words'", SHELL=shell)
        args = self.picker("vfzf")["args"]
        prefix = "--bind=enter:become:"
        action = next(arg.removeprefix(prefix) for arg in args if arg.startswith(prefix))
        self.assertIn("--bind=ctrl-l:become:" + action, args)
        files = ["a b.txt", "a'\"$()*.txt", "line\nbreak.txt", "-leading-dash"]
        action = action.replace("{+}", " ".join(shlex.quote(file) for file in files))
        result = subprocess.run(
            [shell, "-c", action], env=self.env, capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), ["--clean", "two words", "-O", "--", *files])

    def test_editor_command_and_filenames_in_sh(self):
        self.editor_action(shutil.which("sh"))

    @unittest.skipUnless(shutil.which("zsh"), "zsh is not installed")
    def test_editor_command_and_filenames_in_zsh(self):
        self.editor_action(shutil.which("zsh"))

    def test_editor_punctuation(self):
        self.editor_action(shutil.which("sh"), "editor)name,:+ '")

    @unittest.skipUnless(shutil.which("fzf"), "fzf is not installed")
    def test_real_fzf_binding_parser(self):
        self.env["EDITOR"] = "'/editor),ctrl-a:abort' --clean 'two words'"
        args = self.picker("vfzf")["args"]
        result = subprocess.run(
            [shutil.which("fzf"), *args, "--filter=one"],
            env=self.env, input="one\0", capture_output=True, text=True, timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "one\n")


if __name__ == "__main__":
    unittest.main()
