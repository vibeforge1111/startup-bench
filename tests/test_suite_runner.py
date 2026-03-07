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
        self.assertEqual(report["overall"]["scenario_count"], 9)
        self.assertIn("scenario_score_ci95_low", report["overall"])
        self.assertIn("scenario_score_ci95_high", report["overall"])
        self.assertEqual(len(report["scenario_reports"]), 9)
        self.assertIn("scenario_score_sem", report["scenario_reports"][0])
        tracks = {item["track"] for item in report["track_summaries"]}
        self.assertEqual(tracks, {"0to1", "b2b_saas", "board", "crisis", "finance", "gtm", "people", "product", "scale"})

    def test_resilient_baseline_improves_suite_pass_rate(self) -> None:
        b2b_style = run_suite(
            suite_path=SUITE_PATH,
            runner_type="baseline",
            seeds=[1, 2],
            baseline_id="heuristic_b2b_operator",
            max_turns=4,
        )
        resilient = run_suite(
            suite_path=SUITE_PATH,
            runner_type="baseline",
            seeds=[1, 2],
            baseline_id="heuristic_resilient_operator",
            max_turns=4,
        )

        self.assertGreaterEqual(
            resilient["suite_report"]["overall"]["pass_rate_mean"],
            b2b_style["suite_report"]["overall"]["pass_rate_mean"],
        )


if __name__ == "__main__":
    unittest.main()
