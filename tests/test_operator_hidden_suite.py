from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.pack_ops import validate_suite_family
from thestartupbench.suite_runner import run_suite
from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"
TEST_SUITE_PATH = EXAMPLES_DIR / "private_operator_test_scenario_suite.json"
FRESH_SUITE_PATH = EXAMPLES_DIR / "private_operator_fresh_scenario_suite.json"


class OperatorHiddenSuiteTests(unittest.TestCase):
    def test_operator_hidden_test_suite_validates(self) -> None:
        validation = validate_artifact_file(
            artifact_type="scenario-suite",
            path=TEST_SUITE_PATH,
        )
        self.assertTrue(validation.ok)
        self.assertEqual(validation.issues, [])

    def test_operator_hidden_test_suite_runs(self) -> None:
        result = run_suite(
            suite_path=TEST_SUITE_PATH,
            runner_type="baseline",
            seeds=[1],
            baseline_id="heuristic_resilient_operator",
            max_turns=3,
        )

        self.assertTrue(result["validation"]["ok"])
        report = result["suite_report"]
        self.assertEqual(report["overall"]["scenario_count"], 7)
        tracks = {item["track"] for item in report["track_summaries"]}
        self.assertEqual(tracks, {"finance", "gtm", "people"})

    def test_operator_hidden_fresh_suite_validates_and_runs(self) -> None:
        validation = validate_artifact_file(
            artifact_type="scenario-suite",
            path=FRESH_SUITE_PATH,
        )
        self.assertTrue(validation.ok)
        self.assertEqual(validation.issues, [])

        result = run_suite(
            suite_path=FRESH_SUITE_PATH,
            runner_type="baseline",
            seeds=[1],
            baseline_id="heuristic_resilient_operator",
            max_turns=3,
        )

        self.assertTrue(result["validation"]["ok"])
        report = result["suite_report"]
        self.assertEqual(report["overall"]["scenario_count"], 7)
        tracks = {item["track"] for item in report["track_summaries"]}
        self.assertEqual(tracks, {"finance", "gtm", "people"})

    def test_operator_hidden_test_and_fresh_suites_are_distinct(self) -> None:
        result = validate_suite_family([TEST_SUITE_PATH, FRESH_SUITE_PATH])

        self.assertTrue(result["ok"])
        self.assertEqual(result["issues"], [])


if __name__ == "__main__":
    unittest.main()
