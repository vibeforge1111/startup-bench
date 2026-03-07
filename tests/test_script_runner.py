from __future__ import annotations

import json
import sys
import tempfile
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
        self.assertEqual(final_state["finance"]["cash_usd"], 886500.0)
        self.assertGreater(result["score_report"]["scenario_score"], 0.0)

    def test_script_runner_rejects_undeclared_tool_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            script_path = Path(tmp_dir) / "bad_script.json"
            script_path.write_text(
                json.dumps(
                    [
                        {
                            "tool_name": "finance.raise.propose",
                            "request_id": "req_bad_001",
                            "arguments": {},
                        }
                    ]
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "not declared by scenario"):
                run_tool_script(
                    scenario_path=SCENARIO_PATH,
                    tool_calls_path=script_path,
                    seed=31,
                )


if __name__ == "__main__":
    unittest.main()
