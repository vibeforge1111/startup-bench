from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.suite_manifest import redact_suite_manifest


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SUITE_PATH = REPO_ROOT / "examples" / "private_test_scenario_suite.json"


class SuiteManifestTests(unittest.TestCase):
    def test_redact_suite_manifest_hides_paths_and_validates(self) -> None:
        result = redact_suite_manifest(PRIVATE_SUITE_PATH)

        self.assertTrue(result["validation"]["ok"])
        manifest = result["manifest"]
        self.assertEqual(manifest["split"], "test")
        self.assertEqual(manifest["scenario_count"], 5)
        self.assertNotIn("path", manifest["scenarios"][0])
        self.assertEqual(manifest["scenarios"][0]["hidden_ref"], "test_000")


if __name__ == "__main__":
    unittest.main()
