from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.scenario_lint import lint_scenario_instance
from thestartupbench.scenario_loader import load_scenario


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"
PMF_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_0to1_pmf_search_scenario.json"
FALSE_SIGNAL_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_0to1_false_signal_scenario.json"
FINANCE_BRIDGE_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_finance_bridge_terms_scenario.json"
FINANCE_FUNDRAISE_RESET_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_finance_fundraise_reset_scenario.json"
PEOPLE_LEADERSHIP_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_people_leadership_scenario.json"
LAUNCH_DISTRIBUTION_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_launch_distribution_scenario.json"
GROWTH_EXPERIMENT_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_growth_experiment_scenario.json"
BOARD_COMMUNICATION_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_board_communication_scenario.json"


class ScenarioLintTests(unittest.TestCase):
    def test_example_scenario_passes_lint(self) -> None:
        scenario = load_scenario(SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_pmf_scenario_passes_lint(self) -> None:
        scenario = load_scenario(PMF_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_false_signal_scenario_passes_lint(self) -> None:
        scenario = load_scenario(FALSE_SIGNAL_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_finance_bridge_scenario_passes_lint(self) -> None:
        scenario = load_scenario(FINANCE_BRIDGE_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_finance_fundraise_reset_scenario_passes_lint(self) -> None:
        scenario = load_scenario(FINANCE_FUNDRAISE_RESET_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_people_leadership_scenario_passes_lint(self) -> None:
        scenario = load_scenario(PEOPLE_LEADERSHIP_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_launch_distribution_scenario_passes_lint(self) -> None:
        scenario = load_scenario(LAUNCH_DISTRIBUTION_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_growth_experiment_scenario_passes_lint(self) -> None:
        scenario = load_scenario(GROWTH_EXPERIMENT_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_board_communication_scenario_passes_lint(self) -> None:
        scenario = load_scenario(BOARD_COMMUNICATION_SCENARIO_PATH)
        result = lint_scenario_instance(scenario)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_lint_catches_unknown_primitive_reference(self) -> None:
        scenario = load_scenario(SCENARIO_PATH)
        scenario["event_model"]["scheduled_events"][0]["primitive_id"] = "missing_primitive"
        result = lint_scenario_instance(scenario)

        self.assertFalse(result.ok)
        self.assertEqual(result.issues[0].path, ["event_model", "scheduled_events", "0", "primitive_id"])


if __name__ == "__main__":
    unittest.main()
