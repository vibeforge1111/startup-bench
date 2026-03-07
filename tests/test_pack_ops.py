from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.pack_ops import promote_suite_pack, validate_pack_changelog, validate_suite_family


REPO_ROOT = Path(__file__).resolve().parents[1]
PRIVATE_REAL_WORLD_SUITE_PATH = REPO_ROOT / "examples" / "private_real_world_test_scenario_suite.json"
PRIVATE_REAL_WORLD_FRESH_SUITE_PATH = REPO_ROOT / "examples" / "private_real_world_fresh_scenario_suite.json"
PACK_CHANGELOG_PATH = REPO_ROOT / "examples" / "public_pack_changelog.json"


class PackOpsTests(unittest.TestCase):
    def test_promote_suite_pack_rejects_hidden_split_clone_by_default(self) -> None:
        with self.assertRaisesRegex(ValueError, "refuses to clone into hidden splits"):
            promote_suite_pack(
                PRIVATE_REAL_WORLD_SUITE_PATH,
                split="fresh",
                scenario_pack_version="real-world-fresh-pack-0.1.0",
            )

    def test_promote_suite_pack_allows_hidden_split_clone_only_when_explicit(self) -> None:
        result = promote_suite_pack(
            PRIVATE_REAL_WORLD_SUITE_PATH,
            split="fresh",
            scenario_pack_version="real-world-fresh-pack-0.1.0",
            allow_split_clone=True,
        )

        self.assertTrue(result["validation"]["ok"])
        suite = result["suite"]
        self.assertEqual(suite["split"], "fresh")
        self.assertEqual(suite["scenario_pack_version"], "real-world-fresh-pack-0.1.0")
        self.assertTrue(all(entry["mode"] == "fresh" for entry in suite["scenarios"]))

        self.assertTrue(result["public_manifest_validation"]["ok"])
        manifest = result["public_manifest"]
        self.assertEqual(manifest["split"], "fresh")
        self.assertEqual(manifest["scenario_count"], 7)
        self.assertEqual(manifest["scenarios"][0]["hidden_ref"], "fresh_000")

    def test_validate_suite_family_accepts_distinct_hidden_test_and_fresh_packs(self) -> None:
        result = validate_suite_family([PRIVATE_REAL_WORLD_SUITE_PATH, PRIVATE_REAL_WORLD_FRESH_SUITE_PATH])

        self.assertTrue(result["ok"])
        self.assertEqual(result["suite_count"], 2)
        self.assertEqual(result["issues"], [])

    def test_validate_suite_family_rejects_duplicated_hidden_ids_and_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            duplicate_suite_path = temp_dir / "duplicate_suite.json"
            suite = json.loads(PRIVATE_REAL_WORLD_SUITE_PATH.read_text(encoding="utf-8"))
            suite["scenario_pack_version"] = "duplicate-pack-0.1.0"
            suite["split"] = "fresh"
            for entry in suite["scenarios"]:
                entry["mode"] = "fresh"
                entry["path"] = str((REPO_ROOT / "examples" / entry["path"]).resolve())
            duplicate_suite_path.write_text(json.dumps(suite, indent=2), encoding="utf-8")

            result = validate_suite_family([PRIVATE_REAL_WORLD_SUITE_PATH, duplicate_suite_path])

        self.assertFalse(result["ok"])
        issue_codes = {issue["code"] for issue in result["issues"]}
        self.assertIn("duplicate_hidden_scenario_id", issue_codes)
        self.assertIn("duplicate_hidden_scenario_path", issue_codes)

    def test_validate_pack_changelog(self) -> None:
        result = validate_pack_changelog(PACK_CHANGELOG_PATH)

        self.assertTrue(result["validation"]["ok"])
        changelog = result["changelog"]
        self.assertEqual(changelog["entries"][0]["action"], "retired")
        self.assertEqual(changelog["entries"][-1]["split"], "fresh")


if __name__ == "__main__":
    unittest.main()
