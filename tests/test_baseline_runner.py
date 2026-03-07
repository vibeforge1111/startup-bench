from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.baseline_runner import list_baselines, run_baseline
from thestartupbench.runner import run_dry_scenario


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"
CRISIS_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_crisis_scenario.json"
GTM_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_gtm_scenario.json"
PRODUCT_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_product_scenario.json"
BOARD_STRATEGY_SCENARIO_PATH = REPO_ROOT / "examples" / "hidden_board_stakeholder_conflict_test_scenario.json"
BREX_TREASURY_SCENARIO_PATH = REPO_ROOT / "examples" / "real_world_brex_svb_treasury_shock_test_scenario.json"


class BaselineRunnerTests(unittest.TestCase):
    def test_list_baselines_contains_heuristic_operator(self) -> None:
        self.assertIn("heuristic_b2b_operator", list_baselines())
        self.assertIn("heuristic_governance_operator", list_baselines())
        self.assertIn("heuristic_liquidity_operator", list_baselines())
        self.assertIn("heuristic_long_horizon_operator", list_baselines())
        self.assertIn("heuristic_market_aware_operator", list_baselines())
        self.assertIn("heuristic_resilient_operator", list_baselines())

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

    def test_resilient_baseline_outperforms_b2b_baseline_on_crisis_scenario(self) -> None:
        b2b_style = run_baseline(
            scenario_path=CRISIS_SCENARIO_PATH,
            baseline_id="heuristic_b2b_operator",
            seed=41,
            max_turns=4,
        )
        resilient = run_baseline(
            scenario_path=CRISIS_SCENARIO_PATH,
            baseline_id="heuristic_resilient_operator",
            seed=41,
            max_turns=4,
        )

        self.assertGreater(
            resilient["score_report"]["scenario_score"],
            b2b_style["score_report"]["scenario_score"],
        )
        self.assertGreaterEqual(
            resilient["trace"]["state_snapshots"][-1]["state"]["operations"].get("incident_response_count", 0),
            1,
        )

    def test_market_aware_baseline_outperforms_b2b_baseline_on_gtm_scenario(self) -> None:
        b2b_style = run_baseline(
            scenario_path=GTM_SCENARIO_PATH,
            baseline_id="heuristic_b2b_operator",
            seed=17,
            max_turns=4,
        )
        market_aware = run_baseline(
            scenario_path=GTM_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=17,
            max_turns=4,
        )

        self.assertGreater(
            market_aware["score_report"]["scenario_score"],
            b2b_style["score_report"]["scenario_score"],
        )
        self.assertGreaterEqual(
            market_aware["trace"]["state_snapshots"][-1]["state"].get("market", {}).get("market_reads_count", 0),
            1,
        )

    def test_long_horizon_baseline_outperforms_b2b_on_product_scenario(self) -> None:
        b2b_style = run_baseline(
            scenario_path=PRODUCT_SCENARIO_PATH,
            baseline_id="heuristic_b2b_operator",
            seed=23,
            max_turns=5,
        )
        long_horizon = run_baseline(
            scenario_path=PRODUCT_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=23,
            max_turns=5,
        )

        self.assertGreater(
            long_horizon["score_report"]["scenario_score"],
            b2b_style["score_report"]["scenario_score"],
        )
        final_state = long_horizon["trace"]["state_snapshots"][-1]["state"]
        self.assertGreaterEqual(final_state.get("governance", {}).get("board_update_count", 0), 2)

    def test_long_horizon_baseline_board_updates_are_state_aware_on_board_track(self) -> None:
        result = run_baseline(
            scenario_path=BOARD_STRATEGY_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=1,
            max_turns=6,
        )

        board_updates = [
            action["arguments"]["summary"]
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.update"
        ]
        board_reads = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.read"
        ]

        self.assertGreaterEqual(len(board_updates), 2)
        self.assertGreater(len(set(board_updates)), 1)
        self.assertGreaterEqual(len(board_reads), 1)

    def test_governance_baseline_outperforms_long_horizon_on_board_conflict(self) -> None:
        long_horizon = run_baseline(
            scenario_path=BOARD_STRATEGY_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=1,
            max_turns=6,
        )
        governance = run_baseline(
            scenario_path=BOARD_STRATEGY_SCENARIO_PATH,
            baseline_id="heuristic_governance_operator",
            seed=1,
            max_turns=6,
        )

        self.assertGreater(
            governance["score_report"]["scenario_score"],
            long_horizon["score_report"]["scenario_score"],
        )
        governance_reads = [
            action
            for turn in governance["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.read"
        ]
        self.assertGreaterEqual(len(governance_reads), 2)

    def test_liquidity_baseline_outperforms_resilient_on_treasury_shock(self) -> None:
        resilient = run_baseline(
            scenario_path=BREX_TREASURY_SCENARIO_PATH,
            baseline_id="heuristic_resilient_operator",
            seed=1,
            max_turns=4,
        )
        liquidity = run_baseline(
            scenario_path=BREX_TREASURY_SCENARIO_PATH,
            baseline_id="heuristic_liquidity_operator",
            seed=1,
            max_turns=4,
        )

        self.assertGreater(
            liquidity["score_report"]["scenario_score"],
            resilient["score_report"]["scenario_score"],
        )
        final_state = liquidity["trace"]["state_snapshots"][-1]["state"]
        self.assertIn("last_raise_plan", final_state.get("finance", {}))


if __name__ == "__main__":
    unittest.main()
