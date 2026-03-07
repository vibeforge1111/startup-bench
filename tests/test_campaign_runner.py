from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.campaign_runner import _parse_seeds, run_campaign


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"


class CampaignRunnerTests(unittest.TestCase):
    def test_parse_seeds_parses_csv(self) -> None:
        self.assertEqual(_parse_seeds("1, 2,3"), [1, 2, 3])

    def test_baseline_campaign_emits_valid_batch_report(self) -> None:
        result = run_campaign(
            scenario_path=SCENARIO_PATH,
            runner_type="baseline",
            seeds=[41, 43, 47],
            baseline_id="heuristic_b2b_operator",
            max_turns=6,
        )

        self.assertTrue(result["validation"]["ok"])
        report = result["batch_report"]
        self.assertEqual(report["campaign"]["run_count"], 3)
        self.assertEqual(report["campaign"]["runner_type"], "baseline")
        self.assertEqual(report["aggregate_metrics"]["pass_rate"], 1.0)
        self.assertGreater(report["aggregate_metrics"]["scenario_score_mean"], 0.6)


if __name__ == "__main__":
    unittest.main()
