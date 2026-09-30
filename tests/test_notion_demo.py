"""Check demo isolation and smoke-run failure handling without calling an LLM."""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("notion_demo", ROOT / "scripts/notion_demo.py")
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


def response(text="A checkpoint question", result="success"):
    return "\n".join(json.dumps(row) for row in [
        {"type": "system", "subtype": "init", "model": "fixture-model"},
        {"type": "assistant", "message": {"content": [
            {"type": "thinking", "thinking": "omitted from artifacts"},
            {"type": "text", "text": text},
        ]}},
        {"type": "result", "subtype": result},
    ])


class NotionDemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.parent = Path(self.temp.name)

    def test_fresh_runs_are_empty_unique_and_preserve_previous_work(self):
        first, _, _ = demo.prepare("fresh", self.parent)
        self.assertEqual(list((first / "project").iterdir()), [])
        (first / "project/app.py").write_text("keep my work")
        second, _, _ = demo.prepare("fresh", self.parent)
        self.assertNotEqual(first, second)
        self.assertEqual(list((second / "project").iterdir()), [])
        self.assertEqual((first / "project/app.py").read_text(), "keep my work")

    def test_staged_scenes_copy_only_notes_not_future_answers(self):
        scenario = demo.load_scenario()
        for name in ("folders", "data-model", "sign-in"):
            with self.subTest(scene=name):
                run, scene, metadata = demo.prepare(name, self.parent)
                project = run / "project"
                state = project / ".vibe-wise"
                self.assertEqual({p.name for p in state.iterdir()},
                                 {"profile.md", "progress.md", "project-map.md"})
                content = "\n".join(p.read_text() for p in state.iterdir())
                for prompt in scene["turns"]:
                    self.assertNotIn(prompt, content)
                self.assertEqual(demo.application_files(project), [])
                self.assertTrue((run / "review.json").is_file())
                self.assertEqual(metadata["scene"], name)
                self.assertEqual(metadata["plugin_version"],
                                 json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["version"])
                self.assertTrue(metadata["guide_hashes"])
        self.assertNotIn("links table", scenario["scenes"]["data-model"]["files"]["project-map.md"])

    @patch.object(demo.subprocess, "run")
    def test_check_resumes_same_session_and_writes_reviewable_artifacts(self, run_cli):
        run, scene, metadata = demo.prepare("data-model", self.parent)
        run_cli.return_value = subprocess.CompletedProcess([], 0, response(), "")
        with patch("builtins.print"):
            demo.check(run, scene, metadata, "claude", 1, 180)
        self.assertEqual(run_cli.call_count, 2)
        first, second = [call.args[0] for call in run_cli.call_args_list]
        self.assertIn("--session-id", first)
        self.assertIn("--resume", second)
        for command in (first, second):
            self.assertIn(metadata["session_id"], command)
            self.assertNotIn("--dangerously-skip-permissions", command)
            self.assertNotIn("Bash", command[command.index("--tools") + 1])
        saved = json.loads((run / "turn-02.json").read_text())
        self.assertEqual(saved["user"], scene["turns"][1])
        self.assertEqual(saved["model"], "fixture-model")
        self.assertNotIn("omitted from artifacts", (run / "conversation.txt").read_text())

    @patch.object(demo.subprocess, "run")
    def test_budget_failure_is_not_a_pass(self, run_cli):
        run, scene, metadata = demo.prepare("fresh", self.parent)
        run_cli.return_value = subprocess.CompletedProcess(
            [], 0, response(result="error_max_budget_usd"), "")
        with patch("builtins.print"), self.assertRaises(RuntimeError):
            demo.check(run, scene, metadata, "claude", 1, 180)
        self.assertTrue((run / "turn-01.json").exists())

    @patch.object(demo.subprocess, "run")
    def test_unapproved_application_file_fails_the_check(self, run_cli):
        run, scene, metadata = demo.prepare("folders", self.parent)

        def premature_code(*args, **kwargs):
            (run / "project/app.py").write_text("# premature implementation")
            return subprocess.CompletedProcess([], 0, response(), "")

        run_cli.side_effect = premature_code
        with patch("builtins.print"), self.assertRaisesRegex(RuntimeError, "before approval"):
            demo.check(run, scene, metadata, "claude", 1, 180)
        self.assertEqual(run_cli.call_count, 1)


if __name__ == "__main__":
    unittest.main()
