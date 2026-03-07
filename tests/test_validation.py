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

    def test_crisis_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_crisis_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_zero_to_one_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_0to1_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_board_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_board_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_scale_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_scale_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_gtm_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_gtm_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_finance_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_finance_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_people_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_people_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_scenario_suite_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REPO_ROOT / "examples" / "dev_scenario_suite.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_private_test_suite_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REPO_ROOT / "examples" / "private_test_scenario_suite.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_private_real_world_test_suite_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REPO_ROOT / "examples" / "private_real_world_test_scenario_suite.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_private_real_world_fresh_suite_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REPO_ROOT / "examples" / "private_real_world_fresh_scenario_suite.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_public_suite_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "minimal_public_suite_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_real_world_public_test_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "real_world_public_test_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_real_world_public_fresh_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "real_world_public_fresh_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_public_pack_changelog_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="pack-changelog",
            path=REPO_ROOT / "examples" / "public_pack_changelog.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_official_eval_profile_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="official-eval-profile",
            path=REPO_ROOT / "examples" / "official_eval_profile.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_run_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="run-manifest",
            path=REPO_ROOT / "examples" / "minimal_run_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_submission_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="submission",
            path=REPO_ROOT / "examples" / "minimal_submission.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])


if __name__ == "__main__":
    unittest.main()
