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
FINANCE_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_finance_scenario.json"
PMF_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_0to1_pmf_search_scenario.json"
FINANCE_BRIDGE_SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_finance_bridge_terms_scenario.json"
CANARY_GTM_SCENARIO_PATH = REPO_ROOT / "examples" / "hidden_canary_pricing_trap_test_scenario.json"
CANARY_PEOPLE_SCENARIO_PATH = REPO_ROOT / "examples" / "hidden_canary_hiring_trap_test_scenario.json"
ZOOM_CRISIS_SCENARIO_PATH = REPO_ROOT / "examples" / "real_world_zoom_security_freeze_test_scenario.json"
BREX_CRISIS_SCENARIO_PATH = REPO_ROOT / "examples" / "real_world_brex_svb_treasury_shock_test_scenario.json"
BOARD_STRATEGY_SCENARIO_PATH = REPO_ROOT / "examples" / "hidden_board_stakeholder_conflict_test_scenario.json"


class EvaluatorTests(unittest.TestCase):
    def test_pmf_scenario_weights_product_and_team_health(self) -> None:
        scenario = load_scenario(PMF_SCENARIO_PATH)
        weighted_components = {component["component_id"] for component in scenario["evaluation"]["outcome_components"]}

        self.assertTrue({"product_health", "team_health", "risk_management"}.issubset(weighted_components))

        healthy_world = initialize_world_state(scenario, seed=3)
        stressed_world = initialize_world_state(scenario, seed=3)
        stressed_world["product"]["onboarding_quality"] = 0.29
        stressed_world["growth"]["activation_index"] = 0.21
        stressed_world["team"]["morale"] = 0.43
        stressed_world["team"]["attrition_risk"] = 0.68
        stressed_world["team"]["bandwidth_load"] = 1.01
        stressed_world["team"]["hiring"] = {"open_roles": 5, "hiring_capacity_index": 0.1}
        stressed_world["risk"]["financing_pressure"] = 0.61

        healthy = evaluate_dry_run(scenario=scenario, world_state=healthy_world)
        stressed = evaluate_dry_run(scenario=scenario, world_state=stressed_world)

        self.assertLess(stressed["subscores"]["product_health"], healthy["subscores"]["product_health"])
        self.assertLess(stressed["subscores"]["team_health"], healthy["subscores"]["team_health"])
        self.assertLess(stressed["scenario_score"], healthy["scenario_score"])

    def test_product_team_and_risk_subscores_drop_under_operational_stress(self) -> None:
        scenario = load_scenario(FINANCE_SCENARIO_PATH)
        healthy_world = initialize_world_state(scenario, seed=5)
        stressed_world = initialize_world_state(scenario, seed=5)
        stressed_world["product"]["onboarding_quality"] = 0.34
        stressed_world["product"]["major_incidents_open"] = 2
        stressed_world["operations"]["support_sla_breach_risk"] = 0.68
        stressed_world["team"]["morale"] = 0.46
        stressed_world["team"]["attrition_risk"] = 0.69
        stressed_world["team"]["bandwidth_load"] = 1.02
        stressed_world["team"]["hiring"] = {"open_roles": 6, "hiring_capacity_index": 0.15}
        stressed_world["risk"]["financing_pressure"] = 0.91
        stressed_world["risk"]["regulatory_pressure"] = 0.82
        stressed_world["risk"]["counterparty_risk"] = 0.93
        stressed_world["risk"]["active_legal_matters"] = 3
        stressed_world["finance"]["treasury_concentration"] = 0.92

        healthy = evaluate_dry_run(scenario=scenario, world_state=healthy_world)
        stressed = evaluate_dry_run(scenario=scenario, world_state=stressed_world)

        self.assertLess(stressed["subscores"]["product_health"], healthy["subscores"]["product_health"])
        self.assertLess(stressed["subscores"]["team_health"], healthy["subscores"]["team_health"])
        self.assertLess(stressed["subscores"]["risk_management"], healthy["subscores"]["risk_management"])

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
        execute_tool_call(
            session,
            {
                "tool_name": "people.org.adjust",
                "request_id": "req_people_eval_002",
                "arguments": {
                    "morale_delta": 0.08,
                    "attrition_risk_delta": -0.1,
                    "bandwidth_load_delta": -0.09,
                    "monthly_burn_change_usd": 6000,
                    "onboarding_quality_delta": 0.02,
                },
            },
        )
        after = evaluate_dry_run(scenario=scenario, world_state=session.world_state)

        self.assertGreater(after["subscores"]["strategic_coherence"], before["subscores"]["strategic_coherence"])
        self.assertGreater(after["subscores"]["customer_health"], before["subscores"]["customer_health"])
        self.assertGreater(after["subscores"]["team_health"], before["subscores"]["team_health"])
        self.assertGreater(after["scenario_score"], before["scenario_score"])

    def test_people_track_penalizes_incomplete_hiring_plan_under_financing_and_demand_stress(self) -> None:
        scenario = load_scenario(PEOPLE_SCENARIO_PATH)
        world_state = initialize_world_state(scenario, seed=1)
        world_state["market"]["demand_index"] = 0.74
        world_state["sales"]["weighted_pipeline_usd"] = 610000
        world_state["risk"]["financing_pressure"] = 0.61
        world_state["team"]["hiring"] = {
            "open_roles": 4,
            "critical_roles_open": 2,
            "sourced_candidates": 3,
            "onsite_candidates": 1,
            "offers_out": 0,
            "hiring_capacity_index": 0.22,
        }

        def _people_trace(hiring_plan: dict | None) -> dict:
            return {
                "turns": [
                    {
                        "turn_index": 0,
                        "actions": [
                            {
                                "tool_name": "metrics.report",
                                "arguments": {},
                                "response": {
                                    "result": {
                                        "report": {
                                            "market": {"demand_index": 0.82},
                                            "sales": {"weighted_pipeline_usd": 980000},
                                            "alerts": ["market_demand_softening"],
                                        }
                                    }
                                },
                            },
                            {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                        ],
                        "events": [],
                    },
                    {
                        "turn_index": 1,
                        "actions": [
                            {
                                "tool_name": "metrics.report",
                                "arguments": {},
                                "response": {
                                    "result": {
                                        "report": {
                                            "market": {"demand_index": 0.79},
                                            "sales": {"weighted_pipeline_usd": 860000},
                                            "alerts": ["market_demand_softening"],
                                        }
                                    }
                                },
                            },
                            {
                                "tool_name": "people.hiring.update",
                                "arguments": {
                                    "sourced_candidates_delta": 4,
                                    "onsite_candidates_delta": 2,
                                    "offers_out_delta": 1,
                                    "accepted_hires": 0,
                                    "monthly_burn_change_usd": 4000,
                                    "hiring_plan": hiring_plan,
                                },
                            },
                            {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                        ],
                        "events": [],
                    },
                    {
                        "turn_index": 2,
                        "actions": [
                            {
                                "tool_name": "metrics.report",
                                "arguments": {},
                                "response": {
                                    "result": {
                                        "report": {
                                            "market": {"demand_index": 0.76},
                                            "sales": {"weighted_pipeline_usd": 730000},
                                            "alerts": ["market_demand_softening"],
                                        }
                                    }
                                },
                            },
                            {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                        ],
                        "events": [],
                    },
                ]
            }

        incomplete_result = evaluate_dry_run(
            scenario=scenario,
            world_state=world_state,
            trace_evidence=_people_trace({"summary": "We should keep hiring."}),
        )
        complete_result = evaluate_dry_run(
            scenario=scenario,
            world_state=world_state,
            trace_evidence=_people_trace(
                {
                    "summary": "Prioritize the critical customer-ops and engineering roles while tying hiring pace to cash and delivery recovery.",
                    "priority_roles": ["customer_ops_lead", "senior_engineer"],
                    "owner": "vp_ops",
                    "success_metrics": ["time_to_fill_under_8_weeks", "delivery_capacity_index_up", "support_backlog_down"],
                    "hiring_pace": "advance one critical role at a time",
                    "risk_guardrail": "freeze noncritical roles until demand and financing recover",
                }
            ),
        )

        incomplete_details = incomplete_result["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]
        complete_details = complete_result["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]

        self.assertGreater(incomplete_details["hiring_plan_quality_penalty"], 0.0)
        self.assertTrue(incomplete_details["latest_hiring_plan_has_plan"])
        self.assertEqual(
            incomplete_details["required_hiring_plan_fields"],
            ["hiring_pace", "owner", "priority_roles", "risk_guardrail", "success_metrics", "summary"],
        )
        self.assertEqual(complete_details["hiring_plan_quality_penalty"], 0.0)
        self.assertEqual(complete_details["latest_hiring_plan_missing_required_fields"], [])
        self.assertGreater(
            incomplete_details["behavioral_penalty"],
            complete_details["behavioral_penalty"],
        )

    def test_extended_component_weights_affect_outcome_score(self) -> None:
        scenario = load_scenario(FINANCE_SCENARIO_PATH)
        scenario["evaluation"]["outcome_components"] = [
            {"component_id": "cash_efficiency", "weight": 0.2, "direction": "maximize"},
            {"component_id": "revenue_quality", "weight": 0.12, "direction": "maximize"},
            {"component_id": "customer_health", "weight": 0.1, "direction": "maximize"},
            {"component_id": "product_health", "weight": 0.16, "direction": "maximize"},
            {"component_id": "team_health", "weight": 0.16, "direction": "maximize"},
            {"component_id": "risk_management", "weight": 0.16, "direction": "maximize"},
            {"component_id": "strategic_coherence", "weight": 0.1, "direction": "maximize"},
        ]

        healthy_world = initialize_world_state(scenario, seed=9)
        stressed_world = initialize_world_state(scenario, seed=9)
        stressed_world["product"]["onboarding_quality"] = 0.31
        stressed_world["product"]["major_incidents_open"] = 2
        stressed_world["operations"]["support_sla_breach_risk"] = 0.72
        stressed_world["team"]["morale"] = 0.43
        stressed_world["team"]["attrition_risk"] = 0.75
        stressed_world["team"]["bandwidth_load"] = 1.05
        stressed_world["team"]["hiring"] = {"open_roles": 7, "hiring_capacity_index": 0.1}
        stressed_world["risk"]["financing_pressure"] = 0.94
        stressed_world["risk"]["regulatory_pressure"] = 0.79
        stressed_world["risk"]["counterparty_risk"] = 0.88
        stressed_world["risk"]["active_legal_matters"] = 2
        stressed_world["finance"]["treasury_concentration"] = 0.93

        healthy = evaluate_dry_run(scenario=scenario, world_state=healthy_world)
        stressed = evaluate_dry_run(scenario=scenario, world_state=stressed_world)

        self.assertIn("product_health", healthy["subscores"])
        self.assertIn("team_health", healthy["subscores"])
        self.assertIn("risk_management", healthy["subscores"])
        self.assertLess(stressed["outcome_score"], healthy["outcome_score"])
        self.assertLess(stressed["scenario_score"], healthy["scenario_score"])

    def test_finance_bridge_scenario_weights_risk_management(self) -> None:
        scenario = load_scenario(FINANCE_BRIDGE_SCENARIO_PATH)
        weighted_components = {component["component_id"] for component in scenario["evaluation"]["outcome_components"]}

        self.assertTrue({"product_health", "team_health", "risk_management"}.issubset(weighted_components))

        healthy_world = initialize_world_state(scenario, seed=15)
        stressed_world = initialize_world_state(scenario, seed=15)
        stressed_world["risk"]["financing_pressure"] = 0.95
        stressed_world["risk"]["regulatory_pressure"] = 0.74
        stressed_world["risk"]["counterparty_risk"] = 0.87
        stressed_world["risk"]["active_legal_matters"] = 2
        stressed_world["finance"]["treasury_concentration"] = 0.94
        stressed_world["team"]["morale"] = 0.47
        stressed_world["product"]["major_incidents_open"] = 1

        healthy = evaluate_dry_run(scenario=scenario, world_state=healthy_world)
        stressed = evaluate_dry_run(scenario=scenario, world_state=stressed_world)

        self.assertLess(stressed["subscores"]["risk_management"], healthy["subscores"]["risk_management"])
        self.assertLess(stressed["subscores"]["team_health"], healthy["subscores"]["team_health"])
        self.assertLess(stressed["scenario_score"], healthy["scenario_score"])

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

        self.assertLess(score_report["scenario_score"], 0.6)
        self.assertLess(score_report["subscores"]["strategic_coherence"], 0.45)
        self.assertGreater(strategic_details["behavioral_penalty"], 0.0)
        self.assertGreaterEqual(strategic_details["unanswered_adverse_events"], 1)
        self.assertGreaterEqual(strategic_details["support_alert_turn_count"], 1)

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

    def test_board_track_penalizes_repeated_boilerplate_without_governance_follow_through(self) -> None:
        scenario = load_scenario(BOARD_STRATEGY_SCENARIO_PATH)
        world_state = initialize_world_state(scenario, seed=1)
        world_state["product"]["major_incidents_open"] = 1
        world_state["operations"]["support_backlog"] = 31
        world_state["risk"] = {"financing_pressure": 0.79, "regulatory_pressure": 0.18}

        trace_evidence = {
            "turns": [
                {
                    "turn_index": 0,
                    "actions": [
                        {"tool_name": "metrics.report", "arguments": {}, "response": {"result": {"report": {"customers": {"trust_score": 0.67}}}}},
                        {"tool_name": "board.update", "arguments": {"summary": "Stay the course and keep the board confident."}},
                        {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                    ],
                    "events": [],
                },
                {
                    "turn_index": 1,
                    "actions": [
                        {"tool_name": "metrics.report", "arguments": {}, "response": {"result": {"report": {"customers": {"trust_score": 0.65}}}}},
                        {"tool_name": "board.update", "arguments": {"summary": "Stay the course and keep the board confident."}},
                        {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                    ],
                    "events": [{"event_type": "board_growth_push"}],
                },
                {
                    "turn_index": 2,
                    "actions": [
                        {"tool_name": "metrics.report", "arguments": {}, "response": {"result": {"report": {"customers": {"trust_score": 0.61}}}}},
                        {"tool_name": "sales.pipeline.update", "arguments": {"pipeline_count_delta": 1}},
                        {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                    ],
                    "events": [{"event_type": "customer_pushback"}],
                },
            ]
        }

        result = evaluate_dry_run(scenario=scenario, world_state=world_state, trace_evidence=trace_evidence)
        strategic_details = result["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]

        self.assertGreater(strategic_details["behavioral_penalty"], 0.0)
        self.assertTrue(strategic_details["repeated_board_update"])
        self.assertEqual(strategic_details["board_update_after_governance_count"], 0)
        self.assertEqual(strategic_details["support_follow_up_count"], 0)
        self.assertEqual(strategic_details["incident_follow_up_count"], 0)
        self.assertEqual(strategic_details["board_read_count"], 0)
        self.assertLess(result["subscores"]["strategic_coherence"], 0.55)

    def test_board_track_penalizes_incomplete_board_update_artifacts_under_stress(self) -> None:
        scenario = load_scenario(BOARD_STRATEGY_SCENARIO_PATH)
        world_state = initialize_world_state(scenario, seed=1)
        world_state["customers"]["trust_score"] = 0.61
        world_state["product"]["major_incidents_open"] = 1
        world_state["operations"]["support_backlog"] = 33
        world_state["risk"] = {"financing_pressure": 0.82, "regulatory_pressure": 0.18}

        common_turns = [
            {
                "turn_index": 0,
                "actions": [
                    {
                        "tool_name": "metrics.report",
                        "arguments": {},
                        "response": {"result": {"report": {"customers": {"trust_score": 0.72}}}},
                    },
                    {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                ],
                "events": [],
            },
            {
                "turn_index": 1,
                "actions": [
                    {"tool_name": "board.read", "arguments": {}},
                    {"tool_name": "research.market.read", "arguments": {}},
                    {"tool_name": "ops.support.resolve", "arguments": {"tickets_resolved": 9}},
                    {"tool_name": "ops.incident.respond", "arguments": {"severity": "high", "trust_delta": 0.02}},
                    {
                        "tool_name": "finance.raise.propose",
                        "arguments": {"raise_amount_usd": 800000, "dilution_pct": 0.08},
                    },
                    {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                ],
                "events": [{"event_type": "board_growth_push"}],
            },
        ]

        incomplete_trace = {
            "turns": common_turns
            + [
                {
                    "turn_index": 2,
                    "actions": [
                        {
                            "tool_name": "board.update",
                            "arguments": {
                                "summary": "We are addressing the immediate issues without overcommitting."
                            },
                        },
                        {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                    ],
                    "events": [{"event_type": "customer_pushback"}],
                }
            ]
        }
        complete_trace = {
            "turns": common_turns
            + [
                {
                    "turn_index": 2,
                    "actions": [
                        {
                            "tool_name": "board.update",
                            "arguments": {
                                "summary": "Board update reflects the support, liquidity, and trust recovery plan.",
                                "forecast": {
                                    "runway_weeks": 20,
                                    "financing_pressure": 0.82,
                                    "trust_score": 0.61,
                                    "support_backlog": 33,
                                    "major_incidents_open": 1,
                                },
                                "asks": ["support the recovery plan before pushing for acceleration"],
                            },
                        },
                        {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                    ],
                    "events": [{"event_type": "customer_pushback"}],
                }
            ]
        }

        incomplete_result = evaluate_dry_run(
            scenario=scenario,
            world_state=world_state,
            trace_evidence=incomplete_trace,
        )
        complete_result = evaluate_dry_run(
            scenario=scenario,
            world_state=world_state,
            trace_evidence=complete_trace,
        )

        incomplete_details = incomplete_result["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]
        complete_details = complete_result["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]

        self.assertGreater(incomplete_details["board_update_quality_penalty"], 0.0)
        self.assertFalse(incomplete_details["latest_board_update_has_forecast"])
        self.assertFalse(incomplete_details["latest_board_update_has_asks"])
        self.assertEqual(
            incomplete_details["required_board_forecast_fields"],
            ["financing_pressure", "major_incidents_open", "runway_weeks", "support_backlog", "trust_score"],
        )
        self.assertEqual(complete_details["board_update_quality_penalty"], 0.0)
        self.assertTrue(complete_details["latest_board_update_has_forecast"])
        self.assertTrue(complete_details["latest_board_update_has_asks"])
        self.assertEqual(complete_details["latest_board_update_missing_required_forecast_fields"], [])
        self.assertLess(
            incomplete_result["subscores"]["strategic_coherence"],
            complete_result["subscores"]["strategic_coherence"],
        )

    def test_crisis_track_penalizes_incomplete_customer_comms_plan_under_security_stress(self) -> None:
        scenario = load_scenario(ZOOM_CRISIS_SCENARIO_PATH)
        world_state = initialize_world_state(scenario, seed=1)
        world_state["customers"]["trust_score"] = 0.58
        world_state["operations"]["support_backlog"] = 46
        world_state["product"]["major_incidents_open"] = 1

        common_turns = [
            {
                "turn_index": 0,
                "actions": [
                    {
                        "tool_name": "metrics.report",
                        "arguments": {},
                        "response": {"result": {"report": {"customers": {"trust_score": 0.68}, "risk": {"financing_pressure": 0.24}}}},
                    },
                    {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                ],
                "events": [],
            },
            {
                "turn_index": 1,
                "actions": [
                    {"tool_name": "research.market.read", "arguments": {}},
                    {
                        "tool_name": "board.update",
                        "arguments": {
                            "summary": "We are treating trust repair as the primary operating constraint.",
                            "forecast": {"trust_score": 0.58, "major_incidents_open": 1},
                            "asks": ["support the recovery plan before restarting growth pushes"],
                        },
                    },
                    {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                ],
                "events": [{"event_type": "trust_shock"}],
            },
        ]

        incomplete_trace = {
            "turns": common_turns
            + [
                {
                    "turn_index": 2,
                    "actions": [
                        {
                            "tool_name": "ops.incident.respond",
                            "arguments": {
                                "incident_reduction": 1,
                                "trust_recovery": 0.05,
                                "churn_reduction": 0.007,
                                "monthly_burn_increase_usd": 9000,
                                "customer_comms_plan": {
                                    "summary": "We will keep customers posted.",
                                },
                            },
                        },
                        {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                    ],
                    "events": [{"event_type": "security_backlash"}],
                }
            ]
        }
        complete_trace = {
            "turns": common_turns
            + [
                {
                    "turn_index": 2,
                    "actions": [
                        {
                            "tool_name": "ops.incident.respond",
                            "arguments": {
                                "incident_reduction": 1,
                                "trust_recovery": 0.05,
                                "churn_reduction": 0.007,
                                "monthly_burn_increase_usd": 9000,
                                "customer_comms_plan": {
                                    "summary": "We identified the affected systems, are contacting impacted customers directly, and will post the next update within four hours.",
                                    "delivery_channels": ["status_page", "email"],
                                    "affected_segments": ["enterprise", "mid_market"],
                                    "support_path": "route affected accounts to the incident queue and customer success follow-up",
                                    "next_update_hours": 4,
                                },
                            },
                        },
                        {"tool_name": "sim.advance", "arguments": {"advance_by": 1, "unit": "week"}},
                    ],
                    "events": [{"event_type": "security_backlash"}],
                }
            ]
        }

        incomplete_result = evaluate_dry_run(
            scenario=scenario,
            world_state=world_state,
            trace_evidence=incomplete_trace,
        )
        complete_result = evaluate_dry_run(
            scenario=scenario,
            world_state=world_state,
            trace_evidence=complete_trace,
        )

        incomplete_details = incomplete_result["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]
        complete_details = complete_result["evaluator_results"][0]["outputs"]["component_details"]["strategic_coherence"]

        self.assertGreater(incomplete_details["customer_comms_quality_penalty"], 0.0)
        self.assertTrue(incomplete_details["latest_customer_comms_has_plan"])
        self.assertEqual(
            incomplete_details["required_customer_comms_fields"],
            ["affected_segments", "delivery_channels", "next_update_hours", "summary", "support_path"],
        )
        self.assertEqual(complete_details["customer_comms_quality_penalty"], 0.0)
        self.assertEqual(complete_details["latest_customer_comms_missing_required_fields"], [])
        self.assertGreater(
            incomplete_details["behavioral_penalty"],
            complete_details["behavioral_penalty"],
        )


if __name__ == "__main__":
    unittest.main()
