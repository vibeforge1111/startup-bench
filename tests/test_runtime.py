from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.runner import initialize_world_state
from thestartupbench.runtime import RuntimeSession, execute_tool_call
from thestartupbench.scenario_loader import load_scenario


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"


class RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = load_scenario(SCENARIO_PATH)
        self.world_state = initialize_world_state(self.scenario, seed=31)
        self.session = RuntimeSession(scenario=self.scenario, world_state=self.world_state)

    def test_finance_plan_write_updates_derived_metrics(self) -> None:
        initial_runway = self.session.world_state["finance"]["runway_weeks"]
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "finance.plan.write",
                "request_id": "req_fin_001",
                "arguments": {"budget_changes": {"monthly_burn_usd": -25000}},
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 180000.0)
        self.assertEqual(self.session.world_state["finance"]["net_burn_usd"], 109000.0)
        self.assertGreater(self.session.world_state["finance"]["runway_weeks"], initial_runway)
        self.assertIn("last_plan_update", self.session.world_state["finance"])

    def test_metrics_query_supports_nested_dotted_paths(self) -> None:
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "metrics.query",
                "request_id": "req_metrics_001",
                "arguments": {"metric_ids": ["sales.pricing.current_price_index", "health_index"]},
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(response["result"]["items"]["sales.pricing.current_price_index"], 1.0)
        self.assertEqual(response["result"]["items"]["health_index"], 0.853)

    def test_metrics_report_surfaces_alerts_and_headline_metrics(self) -> None:
        self.session.world_state["operations"]["support_backlog"] = 58
        self.session.world_state["risk"]["regulatory_pressure"] = 0.71
        self.session.world_state["finance"]["treasury_concentration"] = 0.84
        self.session.world_state["team"]["morale"] = 0.5
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "metrics.report",
                "request_id": "req_metrics_002",
                "arguments": {},
            },
        )

        self.assertTrue(response["ok"])
        report = response["result"]["report"]
        self.assertEqual(report["headline"]["cash_usd"], 920000)
        self.assertIn("pending_scheduled_events", report["alerts"])
        self.assertIn("support_backlog_above_50", report["alerts"])
        self.assertIn("regulatory_pressure_high", report["alerts"])
        self.assertIn("treasury_concentration_high", report["alerts"])
        self.assertIn("morale_below_0_55", report["alerts"])

    def test_read_tool_responses_are_immutable_snapshots(self) -> None:
        initial_report = execute_tool_call(
            self.session,
            {
                "tool_name": "metrics.report",
                "request_id": "req_metrics_003",
                "arguments": {},
            },
        )
        execute_tool_call(
            self.session,
            {
                "tool_name": "sales.pricing.propose",
                "request_id": "req_price_003",
                "arguments": {"price_change_pct": 0.08},
            },
        )

        self.assertEqual(initial_report["result"]["report"]["sales"]["pricing"]["current_price_index"], 1.0)

    def test_product_roadmap_write_updates_product_and_burn(self) -> None:
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "product.roadmap.write",
                "request_id": "req_prod_001",
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.08,
                    "major_incidents_delta": -1,
                    "budget_change_monthly_burn_usd": 12000,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["product"]["roadmap_items"], 4)
        self.assertEqual(self.session.world_state["product"]["onboarding_quality"], 0.63)
        self.assertEqual(self.session.world_state["product"]["major_incidents_open"], 0)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 217000.0)

    def test_product_launch_updates_growth_revenue_and_support_state(self) -> None:
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "product.launch",
                "request_id": "req_launch_001",
                "arguments": {
                    "launch_name": "Guided onboarding",
                    "monthly_revenue_delta_usd": 12000,
                    "weighted_pipeline_usd_delta": 45000,
                    "pipeline_count_delta": 1,
                    "demand_index_delta": 0.05,
                    "activation_delta": 0.08,
                    "trust_delta": 0.02,
                    "support_backlog_delta": 6,
                    "monthly_burn_change_usd": 9000,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["product"]["launch_count"], 1)
        self.assertEqual(self.session.world_state["growth"]["launch_count"], 1)
        self.assertEqual(self.session.world_state["finance"]["monthly_revenue_usd"], 83000.0)
        self.assertEqual(self.session.world_state["sales"]["weighted_pipeline_usd"], 425000.0)
        self.assertEqual(self.session.world_state["operations"]["support_backlog"], 6.0)
        self.assertEqual(self.session.world_state["growth"]["activation_index"], 0.63)

    def test_growth_experiment_tools_track_active_experiments(self) -> None:
        create = execute_tool_call(
            self.session,
            {
                "tool_name": "growth.experiment.create",
                "request_id": "req_growth_001",
                "arguments": {
                    "experiment_id": "exp_onboarding_001",
                    "experiment_name": "Lifecycle email experiment",
                    "channel": "lifecycle_email",
                    "budget_change_monthly_burn_usd": 4000,
                    "weighted_pipeline_usd_delta": 25000,
                    "demand_index_delta": 0.03,
                    "activation_delta": 0.05,
                },
            },
        )

        self.assertTrue(create["ok"])
        self.assertEqual(self.session.world_state["growth"]["experiment_count"], 1)
        self.assertEqual(self.session.world_state["growth"]["active_experiment_count"], 1)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 209000.0)
        self.assertEqual(self.session.world_state["sales"]["weighted_pipeline_usd"], 405000.0)

        review = execute_tool_call(
            self.session,
            {
                "tool_name": "growth.experiment.review",
                "request_id": "req_growth_002",
                "arguments": {},
            },
        )

        self.assertTrue(review["ok"])
        growth_state = review["result"]["growth_state"]
        self.assertEqual(growth_state["latest_experiment"], "Lifecycle email experiment")
        self.assertEqual(growth_state["active_channels"], ["lifecycle_email"])
        self.assertEqual(growth_state["experiments"][0]["experiment_id"], "exp_onboarding_001")

    def test_sales_pipeline_update_changes_pipeline_and_revenue(self) -> None:
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "sales.pipeline.update",
                "request_id": "req_sales_001",
                "arguments": {
                    "pipeline_count_delta": 2,
                    "weighted_pipeline_usd_delta": 90000,
                    "closed_won_revenue_delta_usd": 15000,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["sales"]["pipeline_count"], 16)
        self.assertEqual(self.session.world_state["sales"]["weighted_pipeline_usd"], 470000.0)
        self.assertEqual(self.session.world_state["finance"]["monthly_revenue_usd"], 86000.0)

    def test_sales_pricing_propose_rejects_unapproved_change(self) -> None:
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "sales.pricing.propose",
                "request_id": "req_price_001",
                "arguments": {"price_change_pct": 0.25},
            },
        )

        self.assertFalse(response["ok"])
        self.assertEqual(response["error_code"], "approval_required")
        self.assertEqual(self.session.world_state["sales"]["pricing"]["current_price_index"], 1.0)

    def test_sales_pricing_propose_updates_revenue_and_customer_metrics(self) -> None:
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "sales.pricing.propose",
                "request_id": "req_price_002",
                "arguments": {"price_change_pct": 0.1},
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["sales"]["pricing"]["current_price_index"], 1.1)
        self.assertEqual(self.session.world_state["finance"]["monthly_revenue_usd"], 74905.0)
        self.assertEqual(self.session.world_state["customers"]["monthly_churn_rate"], 0.033)
        self.assertEqual(self.session.world_state["customers"]["trust_score"], 0.732)

    def test_sim_advance_processes_due_events(self) -> None:
        execute_tool_call(
            self.session,
            {
                "tool_name": "sim.advance",
                "request_id": "req_adv_001",
                "arguments": {"advance_by": 1, "unit": "week"},
            },
        )
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "sim.advance",
                "request_id": "req_adv_002",
                "arguments": {"advance_by": 1, "unit": "week"},
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["sim"]["current_turn"], 2)
        self.assertEqual(self.session.world_state["finance"]["cash_usd"], 853000.0)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 223000.0)
        self.assertEqual(self.session.world_state["sim"]["processed_event_ids"], ["ev_001"])
        self.assertEqual(self.session.world_state["sim"]["pending_event_count"], 1)
        self.assertEqual(response["result"]["events_processed"][1]["event_id"], "ev_001")
        self.assertEqual(response["result"]["events_processed"][1]["operation_count"], 1)

    def test_board_read_and_update_track_governance_state(self) -> None:
        read_before = execute_tool_call(
            self.session,
            {
                "tool_name": "board.read",
                "request_id": "req_board_001",
                "arguments": {},
            },
        )
        self.assertTrue(read_before["ok"])
        self.assertEqual(read_before["result"]["governance"]["board_update_count"], 0)

        update = execute_tool_call(
            self.session,
            {
                "tool_name": "board.update",
                "request_id": "req_board_002",
                "arguments": {
                    "summary": "Reset burn and tighten onboarding execution.",
                    "forecast": {"runway_weeks": 32},
                    "asks": ["approval to hold headcount flat"],
                },
            },
        )
        self.assertTrue(update["ok"])
        self.assertEqual(self.session.world_state["governance"]["board_update_count"], 1)
        self.assertEqual(
            self.session.world_state["governance"]["latest_board_update"]["summary"],
            "Reset burn and tighten onboarding execution.",
        )

    def test_ops_incident_read_and_respond_updates_crisis_state(self) -> None:
        read_before = execute_tool_call(
            self.session,
            {
                "tool_name": "ops.incident.read",
                "request_id": "req_ops_001",
                "arguments": {},
            },
        )
        self.assertTrue(read_before["ok"])
        self.assertEqual(read_before["result"]["incident_state"]["major_incidents_open"], 1)

        response = execute_tool_call(
            self.session,
            {
                "tool_name": "ops.incident.respond",
                "request_id": "req_ops_002",
                "arguments": {
                    "incident_reduction": 1,
                    "trust_recovery": 0.04,
                    "churn_reduction": 0.006,
                    "monthly_burn_increase_usd": 10000,
                    "customer_comms_plan": {
                        "summary": "We identified the incident and will share the next update within six hours.",
                        "delivery_channels": ["status_page", "email"],
                        "affected_segments": ["enterprise"],
                        "support_path": "route affected accounts to the incident queue",
                        "next_update_hours": 6,
                    },
                },
            },
        )
        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["product"]["major_incidents_open"], 0)
        self.assertEqual(self.session.world_state["customers"]["trust_score"], 0.78)
        self.assertEqual(self.session.world_state["customers"]["monthly_churn_rate"], 0.026)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 215000.0)
        self.assertIn("customer_comms_plan", self.session.world_state["operations"]["last_incident_response"])
        self.assertEqual(
            self.session.world_state["operations"]["last_incident_response"]["customer_comms_plan"]["next_update_hours"],
            6,
        )

    def test_support_tools_reduce_backlog_and_improve_customer_state(self) -> None:
        self.session.world_state["operations"]["support_backlog"] = 72
        self.session.world_state["operations"]["support_sla_breach_risk"] = 0.68

        read_before = execute_tool_call(
            self.session,
            {
                "tool_name": "ops.support.read",
                "request_id": "req_support_001",
                "arguments": {},
            },
        )
        self.assertTrue(read_before["ok"])
        self.assertEqual(read_before["result"]["support_state"]["support_backlog"], 72)

        response = execute_tool_call(
            self.session,
            {
                "tool_name": "ops.support.resolve",
                "request_id": "req_support_002",
                "arguments": {
                    "backlog_reduction": 20,
                    "sla_risk_reduction": 0.2,
                    "trust_recovery": 0.03,
                    "churn_reduction": 0.005,
                    "monthly_burn_increase_usd": 6000,
                },
            },
        )
        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["operations"]["support_backlog"], 52)
        self.assertEqual(self.session.world_state["operations"]["support_sla_breach_risk"], 0.48)
        self.assertEqual(self.session.world_state["customers"]["trust_score"], 0.77)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 211000.0)

    def test_treasury_rebalance_improves_liquidity_profile(self) -> None:
        self.session.world_state["finance"]["treasury_concentration"] = 0.91
        self.session.world_state["finance"]["restricted_cash_usd"] = 210000
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "finance.treasury.rebalance",
                "request_id": "req_treasury_001",
                "arguments": {
                    "target_concentration": 0.45,
                    "rebalance_cost_usd": 5000,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["finance"]["treasury_concentration"], 0.45)
        self.assertEqual(self.session.world_state["finance"]["cash_usd"], 915000.0)
        self.assertEqual(self.session.world_state["finance"]["restricted_cash_usd"], 94500.0)
        self.assertGreater(self.session.world_state["finance"]["liquid_cash_usd"], 800000)

    def test_finance_raise_propose_improves_cash_and_reduces_financing_pressure(self) -> None:
        self.session.world_state["risk"]["financing_pressure"] = 0.86
        self.session.world_state["finance"]["cash_usd"] = 250000.0
        self.session.world_state["finance"]["monthly_burn_usd"] = 205000.0
        self.session.world_state["finance"]["monthly_revenue_usd"] = 90000.0
        execute_tool_call(
            self.session,
            {
                "tool_name": "finance.plan.write",
                "request_id": "req_fin_raise_prep",
                "arguments": {"budget_changes": {}},
            },
        )
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "finance.raise.propose",
                "request_id": "req_raise_001",
                "arguments": {
                    "raise_amount_usd": 1200000,
                    "dilution_pct": 0.14,
                    "monthly_burn_change_usd": 0,
                    "financing_risk_reduction": 0.3,
                    "transaction_cost_usd": 24000,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["finance"]["cash_usd"], 1426000.0)
        self.assertEqual(self.session.world_state["finance"]["dilution_index"], 0.14)
        self.assertEqual(self.session.world_state["risk"]["financing_pressure"], 0.56)
        self.assertEqual(self.session.world_state["finance"]["financing_events_count"], 1)
        self.assertIn("last_raise_plan", self.session.world_state["finance"])

    def test_people_org_adjust_reduces_attrition_and_improves_product_health(self) -> None:
        self.session.world_state["team"]["morale"] = 0.49
        self.session.world_state["team"]["attrition_risk"] = 0.62
        self.session.world_state["team"]["bandwidth_load"] = 0.91
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "people.org.adjust",
                "request_id": "req_people_001",
                "arguments": {
                    "morale_delta": 0.09,
                    "attrition_risk_delta": -0.12,
                    "bandwidth_load_delta": -0.1,
                    "monthly_burn_change_usd": 7000,
                    "onboarding_quality_delta": 0.04,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["team"]["morale"], 0.58)
        self.assertEqual(self.session.world_state["team"]["attrition_risk"], 0.5)
        self.assertEqual(self.session.world_state["product"]["onboarding_quality"], 0.59)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 212000.0)

    def test_people_hiring_update_increases_headcount_and_capacity(self) -> None:
        self.session.world_state["team"]["headcount"] = 9
        self.session.world_state["team"]["bandwidth_load"] = 0.92
        self.session.world_state["team"]["hiring"] = {
            "open_roles": 3,
            "critical_roles_open": 1,
            "sourced_candidates": 8,
            "onsite_candidates": 2,
            "offers_out": 1,
        }
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "people.hiring.update",
                "request_id": "req_hiring_001",
                "arguments": {
                    "accepted_hires": 1,
                    "monthly_burn_change_usd": 15000,
                    "morale_delta": 0.03,
                    "bandwidth_load_delta": -0.08,
                    "support_backlog_delta": -4,
                    "onboarding_quality_delta": 0.02,
                    "hiring_plan": {
                        "summary": "Fill the customer-ops lead first, then reassess engineering capacity.",
                        "priority_roles": ["customer_ops_lead", "senior_engineer"],
                        "owner": "vp_ops",
                        "success_metrics": ["time_to_fill_under_8_weeks", "support_backlog_down"],
                        "hiring_pace": "one critical role at a time",
                        "risk_guardrail": "freeze noncritical roles until delivery capacity recovers",
                    },
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["team"]["headcount"], 10)
        self.assertEqual(self.session.world_state["team"]["hiring"]["open_roles"], 2)
        self.assertEqual(self.session.world_state["team"]["hiring"]["critical_roles_open"], 0)
        self.assertEqual(self.session.world_state["team"]["bandwidth_load"], 0.84)
        self.assertGreater(self.session.world_state["team"]["delivery_capacity_index"], 0.0)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 220000.0)
        self.assertIn("last_hiring_plan", self.session.world_state["team"]["hiring"])
        self.assertEqual(self.session.world_state["team"]["hiring"]["last_hiring_plan"]["owner"], "vp_ops")

    def test_people_org_propose_records_pending_change_without_mutating_team_state(self) -> None:
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "people.org.propose",
                "request_id": "req_org_proposal_001",
                "arguments": {
                    "summary": "Consolidate support and onboarding under one manager.",
                    "target_function": "customer_ops",
                    "expected_morale_delta": 0.03,
                    "expected_bandwidth_load_delta": -0.05,
                    "expected_monthly_burn_change_usd": 0,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["team"]["org_proposal_count"], 1)
        self.assertEqual(
            self.session.world_state["team"]["last_org_proposal"]["summary"],
            "Consolidate support and onboarding under one manager.",
        )
        self.assertNotIn("morale", self.session.world_state["team"])

    def test_market_read_returns_competitor_and_segment_state(self) -> None:
        self.session.world_state["market"] = {
            "competitor_pressure": "high",
            "competitor_pressure_index": 0.75,
            "pricing_pressure_index": 0.62,
            "demand_index": 0.71,
            "segment_signals": [{"segment_id": "mid_market", "signal": "slowing"}],
            "latest_market_note": "A larger competitor launched aggressive bundle pricing.",
        }
        self.session.world_state["customers"]["segment_mix_index"] = 0.58
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "research.market.read",
                "request_id": "req_market_001",
                "arguments": {},
            },
        )

        self.assertTrue(response["ok"])
        state = response["result"]["market_state"]
        self.assertEqual(state["competitor_pressure_index"], 0.75)
        self.assertEqual(state["demand_index"], 0.71)
        self.assertEqual(state["segment_mix_index"], 0.58)
        self.assertEqual(self.session.world_state["market"]["market_reads_count"], 1)

    def test_metrics_report_includes_growth_summary(self) -> None:
        execute_tool_call(
            self.session,
            {
                "tool_name": "growth.experiment.create",
                "request_id": "req_growth_metrics_001",
                "arguments": {
                    "experiment_name": "Paid search funnel refresh",
                    "channel": "paid_search",
                    "activation_delta": 0.04,
                },
            },
        )
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "metrics.report",
                "request_id": "req_metrics_growth_001",
                "arguments": {},
            },
        )

        self.assertTrue(response["ok"])
        growth_report = response["result"]["report"]["growth"]
        self.assertEqual(growth_report["experiment_count"], 1)
        self.assertEqual(growth_report["active_experiment_count"], 1)
        self.assertEqual(growth_report["latest_experiment"], "Paid search funnel refresh")

    def test_sim_advance_applies_market_and_hiring_drift(self) -> None:
        self.session.world_state["team"]["headcount"] = 8
        self.session.world_state["team"]["bandwidth_load"] = 0.9
        self.session.world_state["team"]["hiring"] = {
            "open_roles": 3,
            "critical_roles_open": 1,
            "sourced_candidates": 1,
            "onsite_candidates": 0,
            "offers_out": 0,
        }
        self.session.world_state["market"] = {
            "competitor_pressure_index": 0.78,
            "pricing_pressure_index": 0.66,
            "demand_index": 0.69,
        }
        initial_revenue = self.session.world_state["finance"]["monthly_revenue_usd"]
        initial_pipeline = self.session.world_state["sales"]["weighted_pipeline_usd"]

        response = execute_tool_call(
            self.session,
            {
                "tool_name": "sim.advance",
                "request_id": "req_adv_market_001",
                "arguments": {"advance_by": 1, "unit": "week"},
            },
        )

        self.assertTrue(response["ok"])
        self.assertLess(self.session.world_state["finance"]["monthly_revenue_usd"], initial_revenue)
        self.assertLess(self.session.world_state["sales"]["weighted_pipeline_usd"], initial_pipeline)
        self.assertGreater(self.session.world_state["operations"]["support_backlog"], 0)
        self.assertLess(self.session.world_state["team"]["morale"], 0.74)

    def test_legal_compliance_respond_reduces_regulatory_pressure(self) -> None:
        self.session.world_state["risk"]["regulatory_pressure"] = 0.82
        self.session.world_state["risk"]["active_legal_matters"] = 2
        self.session.world_state["risk"]["compliance_backlog"] = 9
        response = execute_tool_call(
            self.session,
            {
                "tool_name": "legal.compliance.respond",
                "request_id": "req_legal_001",
                "arguments": {
                    "pressure_reduction": 0.22,
                    "matters_reduction": 1,
                    "compliance_backlog_reduction": 5,
                    "trust_recovery": 0.015,
                    "monthly_burn_increase_usd": 12000,
                },
            },
        )

        self.assertTrue(response["ok"])
        self.assertEqual(self.session.world_state["risk"]["regulatory_pressure"], 0.6)
        self.assertEqual(self.session.world_state["risk"]["active_legal_matters"], 1)
        self.assertEqual(self.session.world_state["risk"]["compliance_backlog"], 4)
        self.assertEqual(self.session.world_state["customers"]["trust_score"], 0.755)
        self.assertEqual(self.session.world_state["finance"]["monthly_burn_usd"], 217000.0)


if __name__ == "__main__":
    unittest.main()
