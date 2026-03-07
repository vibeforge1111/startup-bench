from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.suite_runner import run_suite


REPO_ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = REPO_ROOT / "examples" / "dev_scenario_suite.json"


class SuiteRunnerTests(unittest.TestCase):
    def test_baseline_suite_emits_valid_report(self) -> None:
        result = run_suite(
            suite_path=SUITE_PATH,
            runner_type="baseline",
            seeds=[1, 2],
            baseline_id="heuristic_b2b_operator",
            max_turns=4,
        )

        self.assertTrue(result["validation"]["ok"])
        report = result["suite_report"]
        self.assertEqual(report["overall"]["scenario_count"], 2)
        self.assertEqual(len(report["scenario_reports"]), 2)
        tracks = {item["track"] for item in report["track_summaries"]}
        self.assertEqual(tracks, {"b2b_saas", "crisis"})


if __name__ == "__main__":
    unittest.main()
