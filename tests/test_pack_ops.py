from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.pack_ops import promote_suite_pack, validate_pack_changelog


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_REAL_WORLD_SUITE_PATH = REPO_ROOT / "examples" / "private_real_world_test_scenario_suite.json"
PACK_CHANGELOG_PATH = REPO_ROOT / "examples" / "public_pack_changelog.json"


class PackOpsTests(unittest.TestCase):
    def test_promote_suite_pack_to_fresh_emits_valid_suite_and_manifest(self) -> None:
        result = promote_suite_pack(
            PRIVATE_REAL_WORLD_SUITE_PATH,
            split="fresh",
            scenario_pack_version="real-world-fresh-pack-0.1.0",
        )

        self.assertTrue(result["validation"]["ok"])
        suite = result["suite"]
        self.assertEqual(suite["split"], "fresh")
        self.assertEqual(suite["scenario_pack_version"], "real-world-fresh-pack-0.1.0")
        self.assertTrue(all(entry["mode"] == "fresh" for entry in suite["scenarios"]))

        self.assertTrue(result["public_manifest_validation"]["ok"])
        manifest = result["public_manifest"]
        self.assertEqual(manifest["split"], "fresh")
        self.assertEqual(manifest["scenario_count"], 5)
        self.assertEqual(manifest["scenarios"][0]["hidden_ref"], "fresh_000")

    def test_validate_pack_changelog(self) -> None:
        result = validate_pack_changelog(PACK_CHANGELOG_PATH)

        self.assertTrue(result["validation"]["ok"])
        changelog = result["changelog"]
        self.assertEqual(changelog["entries"][0]["action"], "retired")
        self.assertEqual(changelog["entries"][-1]["split"], "fresh")


if __name__ == "__main__":
    unittest.main()
