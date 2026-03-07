from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.primitive_engine import apply_operations, get_dotted_value, resolve_event_operations
from thestartupbench.scenario_loader import load_scenario


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"


class PrimitiveEngineTests(unittest.TestCase):
    def test_apply_operations_supports_increment_and_clamp(self) -> None:
        state = {"sales": {"pipeline_count": 1}}
        deltas = apply_operations(
            state,
            [
                {"op": "increment", "path": "sales.pipeline_count", "value": -2},
                {"op": "clamp", "path": "sales.pipeline_count", "min": 0},
            ],
        )

        self.assertEqual(state["sales"]["pipeline_count"], 0)
        self.assertEqual(deltas[0]["before"], 1)
        self.assertEqual(deltas[1]["after"], 0)

    def test_resolve_event_operations_reads_primitive_catalog(self) -> None:
        scenario = load_scenario(SCENARIO_PATH)
        event = scenario["event_model"]["scheduled_events"][0]
        operations = resolve_event_operations(scenario=scenario, event=event)

        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["path"], "finance.monthly_burn_usd")
        self.assertEqual(operations[0]["value"], 18000)

    def test_get_dotted_value_reads_nested_paths(self) -> None:
        state = {"sales": {"pricing": {"current_price_index": 1.08}}}
        self.assertEqual(get_dotted_value(state, "sales.pricing.current_price_index"), 1.08)


if __name__ == "__main__":
    unittest.main()
