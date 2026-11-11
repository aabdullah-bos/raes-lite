from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

from helpers import copy_fixture, error_codes, initialize_git, run_git


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from inspect_result import _repository_state, capture_baseline, inspect_result  # noqa: E402
from preflight import preflight_project  # noqa: E402


GITIGNORE = "__pycache__/\n*.pyc\n.env\n*.local\n"


def review_validation() -> list[dict]:
    return [
        {
            "command": "git status --porcelain",
            "source": "selected slice",
            "exit_code": 0,
            "result": "passed",
            "output": "",
        }
    ]


def ignored_warnings(result: dict) -> list[str]:
    return sorted(
        warning["path"]
        for warning in result["scope_review"]["warnings"]
        if warning["code"] == "IGNORED_PATH_CHANGED"
    )


def all_changed(result: dict) -> set[str]:
    changes = result["changes"]
    paths = set(changes["modified"]) | set(changes["added"]) | set(changes["deleted"]) | set(changes["untracked"])
    for rename in changes["renamed"]:
        paths.update((rename["from"], rename["to"]))
    return paths


class IgnoredPathTests(unittest.TestCase):
    """Untracked gitignored paths are reported separately and never block a slice."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = copy_fixture(Path(self.temp.name))
        # Accept S-0002 so the selected slice is the fixture's review slice (S-0003).
        pipeline = self.project / "docs" / "pipeline.md"
        pipeline.write_text(pipeline.read_text().replace("- [ ] S-0002", "- [x] S-0002", 1))
        (self.project / ".gitignore").write_text(GITIGNORE)
        (self.project / ".env").write_text("TOKEN=before\n")
        (self.project / "settings.local").write_text("tracked despite ignore rule\n")
        initialize_git(self.project)
        run_git(self.project, "add", "-f", "settings.local")
        run_git(self.project, "commit", "-qm", "track an ignored-pattern file")
        self.preflight = preflight_project(self.project)
        self.assertEqual("review", self.preflight["slice"]["type"])
        self.baseline = capture_baseline(self.project)

    def inspect(self) -> dict:
        return inspect_result(
            self.project,
            self.baseline,
            self.preflight,
            review_validation(),
            scope_decision="in_scope",
        )

    def test_new_pycache_file_does_not_block_review_or_change_fingerprint(self) -> None:
        cache = self.project / "src" / "__pycache__"
        cache.mkdir()
        (cache / "calculator.cpython-312.pyc").write_bytes(b"\x00bytecode")
        result = self.inspect()
        self.assertEqual("validated", result["status"], result["errors"])
        self.assertNotIn("REVIEW_SLICE_CHANGED_UNPERMITTED_PATH", error_codes(result))
        self.assertEqual(result["baseline_fingerprint"], result["repository_fingerprint"])
        self.assertEqual(self.baseline["repository"]["fingerprint"], _repository_state(self.project)["fingerprint"])
        self.assertNotIn("src/__pycache__/calculator.cpython-312.pyc", all_changed(result))
        self.assertNotIn("src/__pycache__/calculator.cpython-312.pyc", self.baseline["repository"]["files"])
        self.assertEqual(["src/__pycache__/calculator.cpython-312.pyc"], ignored_warnings(result))

    def test_editing_ignored_file_produces_non_blocking_warning(self) -> None:
        (self.project / ".env").write_text("TOKEN=after\n")
        result = self.inspect()
        self.assertEqual([".env"], ignored_warnings(result))
        self.assertNotIn(".env", all_changed(result))
        self.assertEqual("validated", result["status"], result["errors"])

    def test_deleting_ignored_file_produces_warning(self) -> None:
        (self.project / ".env").unlink()
        result = self.inspect()
        self.assertEqual([".env"], ignored_warnings(result))
        self.assertEqual("validated", result["status"], result["errors"])

    def test_unchanged_ignored_file_produces_no_warning(self) -> None:
        result = self.inspect()
        self.assertEqual([], ignored_warnings(result))
        self.assertIn(".env", self.baseline["repository"]["ignored_files"])

    def test_tracked_file_matching_ignore_rule_is_still_reported_as_modified(self) -> None:
        (self.project / "settings.local").write_text("changed\n")
        result = self.inspect()
        self.assertIn("settings.local", result["changes"]["modified"])
        self.assertEqual([], ignored_warnings(result))
        self.assertIn("REVIEW_SLICE_CHANGED_UNPERMITTED_PATH", error_codes(result))
        self.assertEqual("blocked", result["status"])

    def test_untracked_not_ignored_file_still_blocks_review(self) -> None:
        (self.project / "notes.txt").write_text("scratch\n")
        result = self.inspect()
        self.assertIn("notes.txt", result["changes"]["untracked"])
        self.assertEqual("blocked", result["status"])


class NoGitIgnoreTests(unittest.TestCase):
    """Without git, every file is walked, including ones a .gitignore would exclude."""

    def test_repo_without_git_walks_every_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = copy_fixture(Path(temp))
            (project / ".gitignore").write_text(GITIGNORE)
            baseline = capture_baseline(project)
            self.assertEqual("none", baseline["repository"]["version_control"])
            cache = project / "src" / "__pycache__"
            cache.mkdir()
            (cache / "calculator.cpython-312.pyc").write_bytes(b"\x00bytecode")
            state = _repository_state(project)
            self.assertIn("src/__pycache__/calculator.cpython-312.pyc", state["files"])
            self.assertNotEqual(baseline["repository"]["fingerprint"], state["fingerprint"])


if __name__ == "__main__":
    unittest.main()
