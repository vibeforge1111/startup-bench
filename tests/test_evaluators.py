from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.baseline_runner import run_baseline
from thestartupbench.evaluators import evaluate_dry_run
from thestartupbench.runner import initialize_world_state
from thestartupbench.runtime import RuntimeSession, execute_tool_call
from thestartupbench.scenario_loader import load_scenario


REPO_ROOT = Path(__file__).resolve().parents[1]
GTM_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_gtm_scenario.json"
PEOPLE_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_people_scenario.json"
CANARY_GTM_SCENARIO_PATH = REPO_ROOT / "examples" / "hidden_canary_pricing_trap_test_scenario.json"
CANARY_PEOPLE_SCENARIO_PATH = REPO_ROOT / "examples" / "hidden_canary_hiring_trap_test_scenario.json"
ZOOM_CRISIS_SCENARIO_PATH = REPO_ROOT / "examples" / "real_world_zoom_security_freeze_test_scenario.json"
BREX_CRISIS_SCENARIO_PATH = REPO_ROOT / "examples" / "real_world_brex_svb_treasury_shock_test_scenario.json"


class EvaluatorTests(unittest.TestCase):
    def test_market_and_segment_pressure_reduce_gtm_scores(self) -> None:
        scenario = load_scenario(GTM_SCENARIO_PATH)
        healthy_world = initialize_world_state(scenario, seed=7)
        stressed_world = initialize_world_state(scenario, seed=7)
        stressed_world["market"]["competitor_pressure_index"] = 0.9
        stressed_world["market"]["pricing_pressure_index"] = 0.82
        stressed_world["market"]["demand_index"] = 0.61
        stressed_world["sales"]["weighted_pipeline_usd"] = 510000
        stressed_world["customers"]["trust_score"] = 0.59
        stressed_world["customers"]["monthly_churn_rate"] = 0.044
        for segment in stressed_world["customers"]["segments"]:
            segment["competitor_pressure_index"] = min(1.0, float(segment["competitor_pressure_index"]) + 0.18)
            segment["monthly_churn_rate"] = round(float(segment["monthly_churn_rate"]) + 0.008, 4)
            segment["trust_score"] = round(float(segment["trust_score"]) - 0.05, 4)

        healthy = evaluate_dry_run(scenario=scenario, world_state=healthy_world)
        stressed = evaluate_dry_run(scenario=scenario, world_state=stressed_world)

        self.assertLess(stressed["subscores"]["revenue_quality"], healthy["subscores"]["revenue_quality"])
        self.assertLess(stressed["subscores"]["customer_health"], healthy["subscores"]["customer_health"])
        self.assertLess(stressed["scenario_score"], healthy["scenario_score"])

    def test_people_track_rewards_hiring_and_market_response(self) -> None:
        scenario = load_scenario(PEOPLE_SCENARIO_PATH)
        world_state = initialize_world_state(scenario, seed=11)
        before = evaluate_dry_run(scenario=scenario, world_state=world_state)

        session = RuntimeSession(scenario=scenario, world_state=world_state)
        execute_tool_call(
            session,
            {
                "tool_name": "research.market.read",
                "request_id": "req_market_eval_001",
                "arguments": {},
            },
        )
        execute_tool_call(
            session,
            {
                "tool_name": "people.hiring.update",
                "request_id": "req_hiring_eval_001",
                "arguments": {
                    "sourced_candidates_delta": 4,
                    "onsite_candidates_delta": 2,
                    "offers_out_delta": 1,
                    "accepted_hires": 1,
                    "monthly_burn_change_usd": 15000,
                    "morale_delta": 0.04,
                    "bandwidth_load_delta": -0.08,
                    "support_backlog_delta": -5,
                    "onboarding_quality_delta": 0.02,
                },
            },
        )
        after = evaluate_dry_run(scenario=scenario, world_state=session.world_state)

        self.assertGreater(after["subscores"]["strategic_coherence"], before["subscores"]["strategic_coherence"])
        self.assertGreater(after["subscores"]["customer_health"], before["subscores"]["customer_health"])
        self.assertGreater(after["scenario_score"], before["scenario_score"])

    def test_canary_pricing_trap_penalizes_unanswered_backlash_loop(self) -> None:
        result = run_baseline(
            scenario_path=CANARY_GTM_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=1,
            max_turns=4,
        )

        score_report = result["score_report"]
        outcome_evaluator = score_report["evaluator_results"][0]
        strategic_details = outcome_evaluator["outputs"]["component_details"]["strategic_coherence"]

        self.assertLess(score_report["scenario_score"], 0.55)
        self.assertFalse(score_report["pass"])
        self.assertGreater(strategic_details["behavioral_penalty"], 0.0)
        self.assertGreaterEqual(strategic_details["unanswered_adverse_events"], 1)
        self.assertGreaterEqual(strategic_details["support_alert_turn_count"], 2)

    def test_canary_hiring_trap_penalizes_passive_soft_demand_loop(self) -> None:
        result = run_baseline(
            scenario_path=CANARY_PEOPLE_SCENARIO_PATH,
            baseline_id="heuristic_market_aware_operator",
            seed=1,
            max_turns=4,
        )

        score_report = result["score_report"]
        outcome_evaluator = score_report["evaluator_results"][0]
        strategic_details = outcome_evaluator["outputs"]["component_details"]["strategic_coherence"]

        self.assertLess(score_report["scenario_score"], 0.625)
        self.assertLess(score_report["subscores"]["strategic_coherence"], 0.46)
        self.assertGreater(strategic_details["behavioral_penalty"], 0.0)
        self.assertGreaterEqual(strategic_details["soft_demand_alert_turn_count"], 3)
        self.assertGreaterEqual(strategic_details["pipeline_decline_ratio"], 0.2)
        self.assertEqual(strategic_details["hiring_response_count"], 0)
        self.assertEqual(strategic_details["finance_response_count"], 0)

    def test_zoom_security_freeze_penalizes_missing_security_tradeoff_response(self) -> None:
        result = run_baseline(
            scenario_path=ZOOM_CRISIS_SCENARIO_PATH,
            baseline_id="heuristic_resilient_operator",
            seed=1,
            max_turns=3,
        )

        score_report = result["score_report"]
        outcome_evaluator = score_report["evaluator_results"][0]
        strategic_details = outcome_evaluator["outputs"]["component_details"]["strategic_coherence"]

        self.assertLess(score_report["scenario_score"], 0.625)
        self.assertGreater(strategic_details["behavioral_penalty"], 0.0)
        self.assertGreaterEqual(strategic_details["adverse_event_count"], 1)
        self.assertEqual(strategic_details["product_response_count"], 0)
        self.assertEqual(strategic_details["board_update_after_crisis_count"], 0)
        self.assertEqual(strategic_details["legal_follow_up_count"], 0)

    def test_brex_treasury_shock_penalizes_rebalance_only_liquidity_response(self) -> None:
        result = run_baseline(
            scenario_path=BREX_CRISIS_SCENARIO_PATH,
            baseline_id="heuristic_resilient_operator",
            seed=1,
            max_turns=3,
        )

        score_report = result["score_report"]
        outcome_evaluator = score_report["evaluator_results"][0]
        strategic_details = outcome_evaluator["outputs"]["component_details"]["strategic_coherence"]

        self.assertLess(score_report["scenario_score"], 0.625)
        self.assertGreater(strategic_details["behavioral_penalty"], 0.0)
        self.assertTrue(strategic_details["liquidity_crisis_detected"])
        self.assertEqual(strategic_details["finance_follow_up_count"], 0)
        self.assertGreaterEqual(strategic_details["final_financing_pressure"], 0.85)
        self.assertLessEqual(strategic_details["liquid_cash_months"], 4.0)


if __name__ == "__main__":
    unittest.main()
