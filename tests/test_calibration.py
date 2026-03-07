from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.calibration import build_calibration_report
from thestartupbench.suite_runner import run_suite
from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"
CANARY_SUITE_PATH = EXAMPLES_DIR / "private_canary_test_scenario_suite.json"
OPERATOR_REVIEW_PATH = EXAMPLES_DIR / "minimal_operator_review.json"


class CalibrationTests(unittest.TestCase):
    def test_build_calibration_report_aligns_operator_review_with_suite_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            suite_result = run_suite(
                suite_path=CANARY_SUITE_PATH,
                runner_type="baseline",
                seeds=[1],
                baseline_id="heuristic_market_aware_operator",
                max_turns=4,
            )
            suite_report_path = temp_dir / "suite_report.json"
            suite_report_path.write_text(
                json.dumps(suite_result["suite_report"], indent=2),
                encoding="utf-8",
            )

            result = build_calibration_report(
                suite_report_path=suite_report_path,
                review_paths=[OPERATOR_REVIEW_PATH],
            )

        self.assertTrue(result["validation"]["ok"])
        report = result["report"]
        assert report is not None
        self.assertEqual(report["matched_scenario_count"], 1)
        self.assertEqual(report["review_count"], 1)
        self.assertEqual(report["scenario_alignments"][0]["scenario_id"], "hidden_canary_pricing_trap_test_001")
        self.assertEqual(report["scenario_alignments"][0]["benchmark_recommendation"], "pass")

    def test_validation_accepts_example_calibration_report(self) -> None:
        result = validate_artifact_file(
            artifact_type="calibration-report",
            path=EXAMPLES_DIR / "minimal_calibration_report.json",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])


if __name__ == "__main__":
    unittest.main()
