"""Exercise the actual hook command in isolated new and existing projects."""

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "hooks/hooks.json").read_text())
REGISTRATION = CONFIG["hooks"]["SessionStart"][0]


class SessionStartTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vibe-wise-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.project = self.root / "project with spaces"
        self.project.mkdir()
        (self.project / ".git").mkdir()

    def state(self, project=None, mode="active"):
        directory = (project or self.project) / ".vibe-wise"
        directory.mkdir()
        (directory / "profile.md").write_text(
            f"# Learner Profile\nLearning mode: {mode}\nOnboarding: complete\n"
            "Checkpoint frequency: Light\nQuestion style: Open-ended\n"
            "Implementation style: AI writes code\n"
            "Strong concepts: HTTP request flow\n", encoding="utf-8"
        )
        (directory / "project-map.md").write_text(
            "# Project Map\nCLI → service.py → SQLite\n", encoding="utf-8"
        )
        (directory / "progress.md").write_text(
            "# Learning Progress\n## Transactions\n"
            "Demonstrated understanding: two writes must succeed together.\n"
            "## Queues\nNeeds reinforcement: retries.\n", encoding="utf-8"
        )
        return directory

    def run_hook(self, cwd=None, source="startup", raw=None):
        payload = raw if raw is not None else json.dumps({
            "hook_event_name": "SessionStart", "source": source,
            "cwd": str(cwd or self.project),
        })
        result = subprocess.run(
            REGISTRATION["hooks"][0]["command"], shell=True,
            input=payload, text=True, capture_output=True, timeout=5,
            env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(ROOT)}, cwd=self.root,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout) if result.stdout else None

    def context(self, **kwargs):
        result = self.run_hook(**kwargs)["hookSpecificOutput"]
        self.assertEqual(result["hookEventName"], "SessionStart")
        return result["additionalContext"]

    def test_fresh_project_is_inactive_and_hook_writes_nothing(self):
        self.assertIsNone(self.run_hook())
        self.assertEqual(list(self.project.iterdir()), [self.project / ".git"])

    def test_restore_all_registered_session_lifecycles(self):
        self.state()
        for source in ("startup", "resume", "clear", "compact", "fork"):
            with self.subTest(source=source):
                self.assertTrue(re.fullmatch(REGISTRATION["matcher"], source))
                context = self.context(source=source)
                self.assertIn("Checkpoint frequency: Light", context)
                self.assertIn("CLI → service.py → SQLite", context)
                self.assertIn("🧠 BUILD CHECKPOINT", context)
                self.assertIn("💬 DECISION CHECKPOINT", context)
                self.assertIn("HTTP request flow", context)
                self.assertIn("## Transactions", context)
                self.assertNotIn("two writes must succeed together", context)

    def test_existing_repo_restores_from_nested_working_directory(self):
        self.state()
        nested = self.project / "src" / "services"
        nested.mkdir(parents=True)
        (nested / "service.py").write_text("def run():\n    return 'ok'\n")
        self.assertIn(str(self.project / ".vibe-wise"), self.context(cwd=nested))

    def test_no_git_project_restores(self):
        project = self.root / "fresh-no-git"
        project.mkdir()
        self.state(project)
        self.assertIn("Checkpoint frequency: Light", self.context(cwd=project))

    def test_legacy_notes_restore_without_migration(self):
        state = self.state()
        legacy = state.with_name(".sensible-vibes")
        state.rename(legacy)
        before = {p.name: p.read_bytes() for p in legacy.iterdir()}
        context = self.context(source="compact")
        self.assertIn("VibeWise is active", context)
        self.assertIn(str(legacy), context)
        self.assertIn("Checkpoint frequency: Light", context)
        self.assertFalse(state.exists())
        self.assertEqual(before, {p.name: p.read_bytes() for p in legacy.iterdir()})

    def test_new_notes_take_precedence_over_legacy_at_same_location(self):
        self.state().rename(self.project / ".sensible-vibes")
        self.state(mode="paused")
        self.assertIsNone(self.run_hook())

    def test_nearest_legacy_notes_take_precedence_over_parent_notes(self):
        self.state()
        child = self.project / "package"
        child.mkdir()
        self.state(child, mode="paused").rename(child / ".sensible-vibes")
        self.assertIsNone(self.run_hook(cwd=child))

    def test_legacy_notes_respect_worktree_boundary(self):
        self.state().rename(self.project / ".sensible-vibes")
        child = self.project / "worktree"
        child.mkdir()
        (child / ".git").write_text("gitdir: /another/repo/.git/worktrees/test")
        self.assertIsNone(self.run_hook(cwd=child))

    def test_symlinked_new_state_does_not_fall_back_to_legacy(self):
        self.state().rename(self.project / ".sensible-vibes")
        (self.project / ".vibe-wise").symlink_to(self.root / "missing", target_is_directory=True)
        self.assertIsNone(self.run_hook())

    def test_nested_repository_and_worktree_do_not_borrow_parent_profile(self):
        self.state()
        for name, git_is_file in (("nested-repo", False), ("worktree", True)):
            child = self.project / name
            child.mkdir()
            if git_is_file:
                (child / ".git").write_text("gitdir: /some/other/repo/.git/worktrees/test")
            else:
                (child / ".git").mkdir()
            self.assertIsNone(self.run_hook(cwd=child))

    def test_nearest_state_wins(self):
        self.state()
        child = self.project / "package"
        child.mkdir()
        self.state(child, mode="paused")
        self.assertIsNone(self.run_hook(cwd=child))

    def test_paused_state_is_not_reactivated_by_compaction(self):
        self.state(mode="paused")
        self.assertIsNone(self.run_hook(source="compact"))

    def test_incomplete_onboarding_survives_restart(self):
        state = self.state()
        (state / "profile.md").write_text(
            "Learning mode: active\nOnboarding: incomplete\n"
            "Remaining onboarding: stack familiarity\n"
        )
        self.assertIn("Remaining onboarding: stack familiarity", self.context())

    def test_missing_map_and_progress_do_not_discard_preferences(self):
        state = self.state()
        (state / "project-map.md").unlink()
        (state / "progress.md").unlink()
        self.assertIn("Checkpoint frequency: Light", self.context())

    def test_oversized_state_is_bounded_and_signals_excerpt(self):
        state = self.state()
        with (state / "profile.md").open("a") as stream:
            stream.write("a" * 100000)
        (state / "project-map.md").write_text("b" * 100000)
        context = self.context()
        self.assertLess(len(context), 10000)
        self.assertIn("Excerpt", context)
        self.assertIn("Checkpoint frequency: Light", context)

    def test_malformed_inputs_exit_cleanly(self):
        for raw in ("", "{", "[]", "null", "42", '{"cwd": 4}',
                    '{"hook_event_name":"SessionStart","cwd":"relative"}'):
            with self.subTest(raw=raw):
                self.assertIsNone(self.run_hook(raw=raw))

    def test_unreadable_or_empty_profile_does_not_activate(self):
        state = self.state()
        for content in (b"", b"\xff\xfe"):
            (state / "profile.md").write_bytes(content)
            self.assertIsNone(self.run_hook())

    def test_symlinked_profile_is_not_read(self):
        state = self.state()
        outside = self.root / "outside.md"
        outside.write_text("Learning mode: active\nPRIVATE")
        (state / "profile.md").unlink()
        (state / "profile.md").symlink_to(outside)
        self.assertIsNone(self.run_hook())

    def test_symlinked_state_directory_is_not_read(self):
        state = self.state()
        alternate = self.root / "alternate"
        alternate.mkdir()
        (alternate / ".vibe-wise").symlink_to(state, target_is_directory=True)
        self.assertIsNone(self.run_hook(cwd=alternate))

    def test_hook_never_changes_state(self):
        state = self.state()
        before = {p.name: p.read_bytes() for p in state.iterdir()}
        self.run_hook(source="compact")
        after = {p.name: p.read_bytes() for p in state.iterdir()}
        self.assertEqual(before, after)

    def test_compaction_points_to_pending_decision_without_inventing_approval(self):
        state = self.state()
        with (state / "progress.md").open("a") as stream:
            stream.write("## Pending decision\nUse SQLite. Awaiting Implement or a question.\n"
                         "- Pending decision: JSON storage; waiting for Implement.\n")
        context = self.context(source="compact")
        self.assertIn("## Pending decision", context)
        self.assertIn("before coding", context)
        self.assertIn("await implementation approval", context)
        self.assertIn("JSON storage; waiting for Implement", context)


if __name__ == "__main__":
    unittest.main()
