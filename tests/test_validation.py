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

    def test_zero_to_one_pmf_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_0to1_pmf_search_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_zero_to_one_false_signal_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_0to1_false_signal_scenario.json",
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

    def test_launch_distribution_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_launch_distribution_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_growth_experiment_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_growth_experiment_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_board_communication_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_board_communication_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_customer_communication_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_customer_communication_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_hiring_plan_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_hiring_plan_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_scale_sequencing_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_scale_sequencing_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_product_migration_sequence_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_product_migration_sequence_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_board_product_truth_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_board_product_truth_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_gtm_sequencing_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_gtm_sequencing_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_scale_finance_tradeoff_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_scale_finance_tradeoff_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_zero_to_one_repositioning_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_0to1_repositioning_scenario.json",
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

    def test_finance_bridge_terms_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_finance_bridge_terms_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_finance_fundraise_reset_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_finance_fundraise_reset_scenario.json",
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

    def test_people_leadership_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_people_leadership_scenario.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_product_scenario_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario",
            path=REPO_ROOT / "examples" / "minimal_product_scenario.json",
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

    def test_private_coverage_test_suite_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REPO_ROOT / "examples" / "private_coverage_test_scenario_suite.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_private_coverage_fresh_suite_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REPO_ROOT / "examples" / "private_coverage_fresh_scenario_suite.json",
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

    def test_strategy_public_test_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "strategy_public_test_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_strategy_public_fresh_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "strategy_public_fresh_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_operator_public_test_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "operator_public_test_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_operator_public_fresh_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "operator_public_fresh_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_canary_public_test_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "canary_public_test_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_coverage_public_test_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "coverage_public_test_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_coverage_public_fresh_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "coverage_public_fresh_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_canary_public_fresh_manifest_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="public-suite-manifest",
            path=REPO_ROOT / "examples" / "canary_public_fresh_manifest.json",
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

    def test_official_eval_window_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="official-eval-window",
            path=REPO_ROOT / "examples" / "official_eval_window_v0_9_0.json",
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

    def test_operator_review_summary_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="operator-review-summary",
            path=REPO_ROOT / "examples" / "minimal_operator_review_summary.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_calibration_report_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="calibration-report",
            path=REPO_ROOT / "examples" / "minimal_calibration_report.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_calibration_study_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="calibration-study",
            path=REPO_ROOT / "examples" / "operator_calibration_study_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_human_review_wave_002_strategy_suite_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="scenario-suite",
            path=REPO_ROOT / "examples" / "human_review_wave_002_strategy_suite.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_operator_human_review_wave_002_manifest_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="calibration-study",
            path=REPO_ROOT / "examples" / "operator_human_review_wave_002_manifest.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])


if __name__ == "__main__":
    unittest.main()
