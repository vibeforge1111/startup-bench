from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.study_runner import compile_calibration_study, run_calibration_study
from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"
STUDY_MANIFEST_PATH = EXAMPLES_DIR / "operator_calibration_study_manifest.json"
HUMAN_WAVE_002_MANIFEST_PATH = EXAMPLES_DIR / "operator_human_review_wave_002_manifest.json"
MODEL_WAVE_001_MANIFEST_PATH = EXAMPLES_DIR / "operator_model_review_wave_001_manifest.json"
OPERATOR_REVIEW_PATH = EXAMPLES_DIR / "minimal_operator_review.json"


class StudyRunnerTests(unittest.TestCase):
    def test_run_calibration_study_emits_valid_packets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            result = run_calibration_study(
                study_manifest_path=STUDY_MANIFEST_PATH,
                output_dir=output_dir,
            )

            self.assertTrue(result["validation"]["ok"])
            self.assertEqual(result["study_run"]["target_count"], 3)
            packet_path = output_dir / "targets" / "canary-test-wave" / "review_packet.json"
            self.assertTrue(packet_path.exists())
            packet_validation = validate_artifact_file(
                artifact_type="review-packet",
                path=packet_path,
            )
            self.assertTrue(packet_validation.ok)
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            first_scenario = packet["scenarios"][0]
            self.assertTrue(Path(first_scenario["trace_path"]).exists())
            self.assertTrue(Path(first_scenario["score_report_path"]).exists())

    def test_compile_calibration_study_emits_partial_study_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            run_dir = temp_dir / "run"
            report_dir = temp_dir / "report"
            run_calibration_study(
                study_manifest_path=STUDY_MANIFEST_PATH,
                output_dir=run_dir,
            )
            result = compile_calibration_study(
                study_manifest_path=STUDY_MANIFEST_PATH,
                study_run_dir=run_dir,
                review_paths=[OPERATOR_REVIEW_PATH],
                output_dir=report_dir,
            )

            self.assertTrue(result["validation"]["ok"])
            study_report = result["study_report"]
            self.assertEqual(study_report["completed_target_count"], 1)
            self.assertEqual(study_report["pending_target_count"], 2)
            completed = [item for item in study_report["target_reports"] if item["status"] == "completed"]
            self.assertEqual(completed[0]["target_id"], "canary-test-wave")
            stored = json.loads((report_dir / "calibration_study_report.json").read_text(encoding="utf-8"))
            self.assertEqual(stored["study_id"], study_report["study_id"])

    def test_run_human_wave_002_calibration_study_emits_valid_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            result = run_calibration_study(
                study_manifest_path=HUMAN_WAVE_002_MANIFEST_PATH,
                output_dir=output_dir,
            )

            self.assertTrue(result["validation"]["ok"])
            self.assertEqual(result["study_run"]["target_count"], 1)
            packet_path = output_dir / "targets" / "human-strategy-wave-002" / "review_packet.json"
            self.assertTrue(packet_path.exists())
            packet_validation = validate_artifact_file(
                artifact_type="review-packet",
                path=packet_path,
            )
            self.assertTrue(packet_validation.ok)
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            self.assertEqual(len(packet["scenarios"]), 7)
            self.assertEqual(packet["scenarios"][0]["scenario_id"], "hidden_board_financing_truth_test_001")

    def test_run_model_wave_001_calibration_study_emits_valid_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            result = run_calibration_study(
                study_manifest_path=MODEL_WAVE_001_MANIFEST_PATH,
                output_dir=output_dir,
            )

            self.assertTrue(result["validation"]["ok"])
            self.assertEqual(result["study_run"]["target_count"], 1)
            packet_path = output_dir / "targets" / "model-strategy-shadow-wave-001" / "review_packet.json"
            self.assertTrue(packet_path.exists())
            packet_validation = validate_artifact_file(
                artifact_type="review-packet",
                path=packet_path,
            )
            self.assertTrue(packet_validation.ok)
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            self.assertEqual(len(packet["scenarios"]), 7)
            self.assertEqual(packet["scenarios"][0]["scenario_id"], "hidden_board_financing_truth_test_001")


if __name__ == "__main__":
    unittest.main()
