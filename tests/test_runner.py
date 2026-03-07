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
        self.assertTrue(result["artifact_validation"]["trace"]["ok"])
        self.assertTrue(result["artifact_validation"]["score_report"]["ok"])

    def test_trace_integrity_passes_for_dry_run_trace(self) -> None:
        result = run_dry_scenario(SCENARIO_PATH, seed=13)
        integrity = validate_trace_integrity(result["trace"])
        self.assertTrue(integrity.ok)
        self.assertEqual(integrity.issues, [])


if __name__ == "__main__":
    unittest.main()

