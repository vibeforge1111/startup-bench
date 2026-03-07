from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.script_runner import run_tool_script


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json"
TOOL_SCRIPT_PATH = REPO_ROOT / "examples" / "minimal_tool_script.json"


class ScriptRunnerTests(unittest.TestCase):
    def test_script_runner_emits_valid_trace(self) -> None:
        result = run_tool_script(
            scenario_path=SCENARIO_PATH,
            tool_calls_path=TOOL_SCRIPT_PATH,
            seed=23,
        )
        self.assertTrue(result["artifact_validation"]["trace"]["ok"])
        self.assertTrue(result["artifact_validation"]["trace_integrity"]["ok"])
        self.assertTrue(result["artifact_validation"]["score_report"]["ok"])

    def test_script_runner_advances_time(self) -> None:
        result = run_tool_script(
            scenario_path=SCENARIO_PATH,
            tool_calls_path=TOOL_SCRIPT_PATH,
            seed=29,
        )
        final_state = result["trace"]["state_snapshots"][-1]["state"]
        self.assertEqual(final_state["sim"]["current_time"], "2026-01-08T09:00:00Z")
        self.assertEqual(final_state["sim"]["current_turn"], 1)


if __name__ == "__main__":
    unittest.main()

