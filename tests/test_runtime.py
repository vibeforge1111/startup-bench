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


if __name__ == "__main__":
    unittest.main()
