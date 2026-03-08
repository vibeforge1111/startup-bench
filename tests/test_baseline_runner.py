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
PMF_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_0to1_false_signal_scenario.json"
FINANCE_BRIDGE_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_finance_bridge_terms_scenario.json"
FINANCE_FUNDRAISE_RESET_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_finance_fundraise_reset_scenario.json"
PEOPLE_LEADERSHIP_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_people_leadership_scenario.json"
LAUNCH_DISTRIBUTION_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_launch_distribution_scenario.json"
GROWTH_EXPERIMENT_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_growth_experiment_scenario.json"
BOARD_COMMUNICATION_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_board_communication_scenario.json"
CUSTOMER_COMMUNICATION_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_customer_communication_scenario.json"
HIRING_PLAN_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_hiring_plan_scenario.json"
SCALE_SEQUENCING_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_scale_sequencing_scenario.json"
PRODUCT_MIGRATION_SEQUENCE_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_product_migration_sequence_scenario.json"
BOARD_PRODUCT_TRUTH_SCENARIO_PATH = REPO_ROOT / "examples" / "hidden_board_product_truth_test_scenario.json"
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

    def test_market_aware_baseline_improves_on_dry_run_for_false_signal_pmf_scenario(self) -> None:
        dry_result = run_dry_scenario(PMF_SCENARIO_PATH, seed=13)
        market_aware = run_baseline(
            scenario_path=PMF_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=13,
            max_turns=5,
        )

        self.assertGreater(
            market_aware["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )
        final_state = market_aware["trace"]["state_snapshots"][-1]["state"]
        self.assertGreaterEqual(final_state.get("market", {}).get("market_reads_count", 0), 1)

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

    def test_governance_baseline_uses_truthful_board_and_product_actions_on_board_product_truth(self) -> None:
        governance = run_baseline(
            scenario_path=BOARD_PRODUCT_TRUTH_SCENARIO_PATH,
            baseline_id="heuristic_governance_operator",
            seed=1,
            max_turns=6,
        )

        governance_reads = [
            action
            for turn in governance["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.read"
        ]
        roadmap_updates = [
            action
            for turn in governance["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "product.roadmap.write"
        ]
        board_updates = [
            action
            for turn in governance["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.update"
        ]
        strategic_details = governance["score_report"]["evaluator_results"][0]["outputs"]["component_details"][
            "strategic_coherence"
        ]

        self.assertGreaterEqual(len(governance_reads), 2)
        self.assertGreaterEqual(len(roadmap_updates), 1)
        self.assertGreaterEqual(len(board_updates), 2)
        self.assertEqual(strategic_details["board_update_quality_penalty"], 0.0)

    def test_liquidity_baseline_outperforms_b2b_on_bridge_terms_finance_scenario(self) -> None:
        b2b_style = run_baseline(
            scenario_path=FINANCE_BRIDGE_SCENARIO_PATH,
            baseline_id="heuristic_b2b_operator",
            seed=7,
            max_turns=5,
        )
        liquidity = run_baseline(
            scenario_path=FINANCE_BRIDGE_SCENARIO_PATH,
            baseline_id="heuristic_liquidity_operator",
            seed=7,
            max_turns=5,
        )

        self.assertGreater(
            liquidity["score_report"]["scenario_score"],
            b2b_style["score_report"]["scenario_score"],
        )
        liquidity_finance = liquidity["trace"]["state_snapshots"][-1]["state"].get("finance", {})
        b2b_finance = b2b_style["trace"]["state_snapshots"][-1]["state"].get("finance", {})
        self.assertIn("last_plan_update", liquidity_finance)
        self.assertGreater(liquidity_finance.get("runway_weeks", 0), b2b_finance.get("runway_weeks", 0))

    def test_liquidity_baseline_improves_on_dry_run_for_fundraise_reset_scenario(self) -> None:
        dry_result = run_dry_scenario(FINANCE_FUNDRAISE_RESET_SCENARIO_PATH, seed=29)
        liquidity = run_baseline(
            scenario_path=FINANCE_FUNDRAISE_RESET_SCENARIO_PATH,
            baseline_id="heuristic_liquidity_operator",
            seed=29,
            max_turns=6,
        )

        self.assertGreater(
            liquidity["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )
        final_state = liquidity["trace"]["state_snapshots"][-1]["state"]
        self.assertIn("last_raise_plan", final_state.get("finance", {}))
        self.assertGreaterEqual(final_state.get("governance", {}).get("board_update_count", 0), 2)

    def test_liquidity_baseline_uses_raise_and_board_tools_on_fundraise_reset_scenario(self) -> None:
        result = run_baseline(
            scenario_path=FINANCE_FUNDRAISE_RESET_SCENARIO_PATH,
            baseline_id="heuristic_liquidity_operator",
            seed=29,
            max_turns=6,
        )

        financing_actions = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "finance.raise.propose"
        ]
        board_updates = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.update"
        ]

        self.assertGreaterEqual(len(financing_actions), 1)
        self.assertGreaterEqual(len(board_updates), 2)
        self.assertIn("dilution_pct", financing_actions[0]["arguments"])

    def test_long_horizon_baseline_improves_on_dry_run_for_people_leadership_scenario(self) -> None:
        dry_result = run_dry_scenario(PEOPLE_LEADERSHIP_SCENARIO_PATH, seed=11)
        long_horizon = run_baseline(
            scenario_path=PEOPLE_LEADERSHIP_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=11,
            max_turns=6,
        )

        self.assertGreater(
            long_horizon["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )
        final_state = long_horizon["trace"]["state_snapshots"][-1]["state"]
        self.assertGreaterEqual(final_state.get("team", {}).get("org_changes_count", 0), 1)

    def test_long_horizon_baseline_sequences_capacity_actions_on_scale_sequencing_scenario(self) -> None:
        dry_result = run_dry_scenario(SCALE_SEQUENCING_SCENARIO_PATH, seed=29)
        long_horizon = run_baseline(
            scenario_path=SCALE_SEQUENCING_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=29,
            max_turns=6,
        )

        self.assertGreater(
            long_horizon["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )

        roadmap_updates = [
            action
            for turn in long_horizon["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "product.roadmap.write"
        ]
        hiring_updates = [
            action
            for turn in long_horizon["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "people.hiring.update"
        ]
        board_updates = [
            action
            for turn in long_horizon["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.update"
        ]

        self.assertGreaterEqual(len(roadmap_updates), 1)
        self.assertGreaterEqual(len(hiring_updates), 1)
        self.assertGreaterEqual(len(board_updates), 2)
        self.assertTrue(all("hiring_plan" in action["arguments"] for action in hiring_updates))

    def test_long_horizon_baseline_stabilizes_product_migration_sequence(self) -> None:
        dry_result = run_dry_scenario(PRODUCT_MIGRATION_SEQUENCE_SCENARIO_PATH, seed=33)
        long_horizon = run_baseline(
            scenario_path=PRODUCT_MIGRATION_SEQUENCE_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=33,
            max_turns=6,
        )

        self.assertGreater(
            long_horizon["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )

        roadmap_updates = [
            action
            for turn in long_horizon["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "product.roadmap.write"
        ]
        incident_responses = [
            action
            for turn in long_horizon["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "ops.incident.respond"
        ]
        support_actions = [
            action
            for turn in long_horizon["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "ops.support.resolve"
        ]

        self.assertGreaterEqual(len(roadmap_updates), 1)
        self.assertGreaterEqual(len(incident_responses), 1)
        self.assertGreaterEqual(len(support_actions), 1)
        self.assertTrue(all("customer_comms_plan" in action["arguments"] for action in incident_responses))

    def test_market_aware_baseline_improves_on_dry_run_for_launch_distribution_scenario(self) -> None:
        dry_result = run_dry_scenario(LAUNCH_DISTRIBUTION_SCENARIO_PATH, seed=19)
        market_aware = run_baseline(
            scenario_path=LAUNCH_DISTRIBUTION_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=19,
            max_turns=6,
        )

        self.assertGreater(
            market_aware["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )
        final_state = market_aware["trace"]["state_snapshots"][-1]["state"]
        self.assertGreaterEqual(final_state.get("product", {}).get("launch_count", 0), 1)
        self.assertGreaterEqual(final_state.get("growth", {}).get("experiment_count", 0), 1)

    def test_market_aware_baseline_uses_launch_and_experiment_tools_on_launch_distribution_scenario(self) -> None:
        result = run_baseline(
            scenario_path=LAUNCH_DISTRIBUTION_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=19,
            max_turns=6,
        )

        launches = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "product.launch"
        ]
        experiments = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "growth.experiment.create"
        ]

        self.assertGreaterEqual(len(launches), 1)
        self.assertGreaterEqual(len(experiments), 1)
        self.assertTrue(launches[0]["arguments"]["launch_name"])
        self.assertTrue(experiments[0]["arguments"]["experiment_name"])

    def test_market_aware_baseline_improves_on_dry_run_for_growth_experiment_scenario(self) -> None:
        dry_result = run_dry_scenario(GROWTH_EXPERIMENT_SCENARIO_PATH, seed=31)
        market_aware = run_baseline(
            scenario_path=GROWTH_EXPERIMENT_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=31,
            max_turns=6,
        )

        self.assertGreater(
            market_aware["score_report"]["scenario_score"],
            dry_result["score_report"]["scenario_score"],
        )
        final_state = market_aware["trace"]["state_snapshots"][-1]["state"]
        self.assertGreaterEqual(final_state.get("growth", {}).get("experiment_count", 0), 1)
        self.assertGreaterEqual(final_state.get("market", {}).get("market_reads_count", 0), 1)

    def test_market_aware_baseline_uses_experiment_loop_on_growth_experiment_scenario(self) -> None:
        result = run_baseline(
            scenario_path=GROWTH_EXPERIMENT_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=31,
            max_turns=6,
        )

        experiment_creates = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "growth.experiment.create"
        ]
        experiment_reviews = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "growth.experiment.review"
        ]

        self.assertGreaterEqual(len(experiment_creates), 1)
        self.assertGreaterEqual(len(experiment_reviews), 1)
        self.assertTrue(experiment_creates[0]["arguments"]["experiment_name"])

    def test_governance_baseline_keeps_board_update_quality_penalty_zero_on_board_communication_scenario(self) -> None:
        result = run_baseline(
            scenario_path=BOARD_COMMUNICATION_SCENARIO_PATH,
            baseline_id="heuristic_governance_operator",
            seed=23,
            max_turns=6,
        )

        board_updates = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "board.update"
        ]
        strategic_details = result["score_report"]["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]

        self.assertGreaterEqual(len(board_updates), 2)
        self.assertTrue(all("forecast" in action["arguments"] for action in board_updates))
        self.assertTrue(all("asks" in action["arguments"] for action in board_updates))
        self.assertEqual(strategic_details["board_update_quality_penalty"], 0.0)

    def test_resilient_baseline_uses_customer_comms_plan_on_customer_communication_scenario(self) -> None:
        result = run_baseline(
            scenario_path=CUSTOMER_COMMUNICATION_SCENARIO_PATH,
            baseline_id="heuristic_resilient_operator",
            seed=23,
            max_turns=6,
        )

        incident_responses = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "ops.incident.respond"
        ]
        strategic_details = result["score_report"]["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]

        self.assertGreaterEqual(len(incident_responses), 1)
        self.assertTrue(all("customer_comms_plan" in action["arguments"] for action in incident_responses))
        self.assertEqual(strategic_details["customer_comms_quality_penalty"], 0.0)

    def test_long_horizon_baseline_uses_hiring_plan_on_hiring_plan_scenario(self) -> None:
        result = run_baseline(
            scenario_path=HIRING_PLAN_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=23,
            max_turns=6,
        )

        hiring_updates = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "people.hiring.update"
        ]
        strategic_details = result["score_report"]["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]

        self.assertGreaterEqual(len(hiring_updates), 1)
        self.assertTrue(all("hiring_plan" in action["arguments"] for action in hiring_updates))
        self.assertEqual(strategic_details["hiring_plan_quality_penalty"], 0.0)

    def test_long_horizon_baseline_uses_org_proposal_on_people_leadership_scenario(self) -> None:
        result = run_baseline(
            scenario_path=PEOPLE_LEADERSHIP_SCENARIO_PATH,
            baseline_id="heuristic_long_horizon_operator",
            seed=11,
            max_turns=6,
        )

        org_proposals = [
            action
            for turn in result["trace"]["turns"]
            for action in turn["actions"]
            if action["tool_name"] == "people.org.propose"
        ]

        self.assertGreaterEqual(len(org_proposals), 1)
        self.assertIn(org_proposals[0]["arguments"]["target_function"], {"customer_ops", "product", "operations"})
        self.assertTrue(org_proposals[0]["arguments"]["summary"])
        final_state = result["trace"]["state_snapshots"][-1]["state"]
        self.assertGreaterEqual(final_state.get("team", {}).get("org_proposal_count", 0), 1)

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
