from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.scenario_lint import lint_scenario_instance
from thestartupbench.scenario_loader import load_scenario
from thestartupbench.suite_runner import run_suite
from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"
REAL_WORLD_SCENARIOS = [
    "real_world_airbnb_emergency_financing_scenario.json",
    "real_world_airbnb_demand_shock_scenario.json",
    "real_world_brex_svb_treasury_shock_scenario.json",
    "real_world_buffer_runway_crunch_scenario.json",
    "real_world_zoom_security_freeze_scenario.json",
    "real_world_robinhood_volatility_outage_scenario.json",
    "real_world_dropbox_phishing_scenario.json",
    "real_world_github_failover_scenario.json",
    "real_world_atlassian_restoration_scenario.json",
    "real_world_shopify_peak_readiness_scenario.json",
]
REAL_WORLD_SUITE_PATH = EXAMPLES_DIR / "real_world_crisis_scenario_suite.json"


class RealWorldScenarioTests(unittest.TestCase):
    def test_real_world_scenarios_validate(self) -> None:
        for filename in REAL_WORLD_SCENARIOS:
            with self.subTest(filename=filename):
                result = validate_artifact_file(
                    artifact_type="scenario",
                    path=EXAMPLES_DIR / filename,
                )
                self.assertTrue(result.ok)
                self.assertEqual(result.issues, [])

    def test_real_world_scenarios_pass_lint(self) -> None:
        for filename in REAL_WORLD_SCENARIOS:
            with self.subTest(filename=filename):
                scenario = load_scenario(EXAMPLES_DIR / filename)
                result = lint_scenario_instance(scenario)
                self.assertTrue(result.ok)
                self.assertEqual(result.issues, [])

    def test_real_world_suite_validates_and_runs(self) -> None:
        validation = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REAL_WORLD_SUITE_PATH,
        )
        self.assertTrue(validation.ok)
        self.assertEqual(validation.issues, [])

        result = run_suite(
            suite_path=REAL_WORLD_SUITE_PATH,
            runner_type="baseline",
            seeds=[1],
            baseline_id="heuristic_resilient_operator",
            max_turns=3,
        )

        self.assertTrue(result["validation"]["ok"])
        report = result["suite_report"]
        self.assertEqual(report["overall"]["scenario_count"], 10)
        self.assertEqual(len(report["scenario_reports"]), 10)
        tracks = {item["track"] for item in report["track_summaries"]}
        self.assertEqual(tracks, {"board", "crisis", "scale"})


if __name__ == "__main__":
    unittest.main()
