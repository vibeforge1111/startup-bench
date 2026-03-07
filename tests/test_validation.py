from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def test_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_b2b_saas_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_world_state_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="world-state",
            path=REPO_ROOT / "examples" / "minimal_world_state.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])


if __name__ == "__main__":
    unittest.main()

