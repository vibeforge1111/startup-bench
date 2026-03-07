from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.runner import run_dry_scenario
from thestartupbench.trace_validation import validate_trace_integrity


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"


class RunnerTests(unittest.TestCase):
    def test_run_dry_emits_valid_artifacts(self) -> None:
        result = run_dry_scenario(SCENARIO_PATH, seed=11)

        self.assertEqual(result["scenario_id"], "b2b_saas_runway_pricing_001")
        self.assertEqual(result["turn_count"], 0)
        self.assertGreater(result["score_report"]["scenario_score"], 0.0)
        self.assertTrue(result["artifact_validation"]["trace"]["ok"])
        self.assertTrue(result["artifact_validation"]["score_report"]["ok"])
        self.assertTrue(result["artifact_validation"]["tool_manifest"]["ok"])

    def test_trace_integrity_passes_for_dry_run_trace(self) -> None:
        result = run_dry_scenario(SCENARIO_PATH, seed=13)
        integrity = validate_trace_integrity(result["trace"])
        self.assertTrue(integrity.ok)
        self.assertEqual(integrity.issues, [])

    def test_observation_projection_includes_values(self) -> None:
        result = run_dry_scenario(SCENARIO_PATH, seed=17)
        finance_surface = result["observation_surfaces"][0]
        self.assertEqual(finance_surface["surface_id"], "finance_dashboard")
        self.assertEqual(finance_surface["values"]["cash_usd"], 920000)
        final_state = result["trace"]["state_snapshots"][-1]["state"]
        self.assertEqual(final_state["sim"]["pending_event_count"], 2)
        self.assertAlmostEqual(final_state["finance"]["runway_weeks"], 27.46, places=2)

    def test_tool_manifest_contains_declared_tools(self) -> None:
        result = run_dry_scenario(SCENARIO_PATH, seed=19)
        tool_names = [tool["tool_name"] for tool in result["tool_manifest"]["tools"]]
        self.assertIn("metrics.query", tool_names)
        self.assertIn("sim.advance", tool_names)


if __name__ == "__main__":
    unittest.main()
