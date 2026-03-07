from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.baseline_runner import list_baselines, run_baseline
from thestartupbench.runner import run_dry_scenario


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"


class BaselineRunnerTests(unittest.TestCase):
    def test_list_baselines_contains_heuristic_operator(self) -> None:
        self.assertIn("heuristic_b2b_operator", list_baselines())

    def test_baseline_run_emits_valid_artifacts_and_improves_on_dry_run(self) -> None:
        dry_result = run_dry_scenario(SCENARIO_PATH, seed=37)
        baseline_result = run_baseline(
            scenario_path=SCENARIO_PATH,
            baseline_id="heuristic_b2b_operator",
            seed=37,
            max_turns=6,
        )

        self.assertTrue(baseline_result["artifact_validation"]["trace"]["ok"])
        self.assertTrue(baseline_result["artifact_validation"]["trace_integrity"]["ok"])
        self.assertTrue(baseline_result["artifact_validation"]["score_report"]["ok"])
        self.assertGreater(
            baseline_result["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )
        self.assertTrue(any(turn["actions"] for turn in baseline_result["trace"]["turns"]))


if __name__ == "__main__":
    unittest.main()
