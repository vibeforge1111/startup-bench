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

    def test_model_wave_minimum_reviewer_gate_uses_unique_reviewers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            run_dir = temp_dir / "run"
            report_dir = temp_dir / "report"
            reviews_dir = temp_dir / "reviews"
            run_calibration_study(
                study_manifest_path=MODEL_WAVE_001_MANIFEST_PATH,
                output_dir=run_dir,
            )

            packet = json.loads(
                (run_dir / "targets" / "model-strategy-shadow-wave-001" / "review_packet.json").read_text(encoding="utf-8")
            )
            review_paths = []
            for scenario in packet["scenarios"]:
                review = {
                    "review_version": "0.1.0",
                    "benchmark_version": packet["benchmark_version"],
                    "reviewer": {
                        "reviewer_id": "codex_reviewer_001",
                        "role": "model_reviewer",
                        "functional_domain": "synthetic_panel",
                        "years_experience": 0,
                        "startup_stage_focus": "synthetic_panel",
                    },
                    "scenario": {
                        "scenario_id": scenario["scenario_id"],
                        "track": scenario["track"],
                        "split": packet["split"],
                        "scenario_pack_version": packet["scenario_pack_version"],
                    },
                    "run": {
                        "runner_type": packet["runner_type"],
                        "runner_id": packet["runner_id"],
                        "seed": packet["seed"],
                        "trace_path": scenario["trace_path"],
                        "score_report_path": scenario["score_report_path"],
                    },
                    "rubric": {
                        "survival_and_risk": 4,
                        "capital_allocation": 4,
                        "customer_trust": 4,
                        "people_leadership": 4,
                        "strategic_quality": 4,
                        "overall_recommendation": "pass",
                    },
                    "notes": {
                        "strengths": ["Strong enough for regression coverage."],
                        "weaknesses": ["Synthetic single-reviewer sample only."],
                        "recommended_actions": ["Add the remaining model reviewers before promotion."],
                        "benchmark_gaming_signals": [],
                    },
                }
                review_path = reviews_dir / f"{scenario['scenario_id']}.json"
                review_path.parent.mkdir(parents=True, exist_ok=True)
                review_path.write_text(json.dumps(review, indent=2), encoding="utf-8")
                review_paths.append(review_path)

            result = compile_calibration_study(
                study_manifest_path=MODEL_WAVE_001_MANIFEST_PATH,
                study_run_dir=run_dir,
                review_paths=review_paths,
                output_dir=report_dir,
            )

            self.assertTrue(result["validation"]["ok"])
            study_report = result["study_report"]
            self.assertEqual(study_report["completed_target_count"], 1)
            self.assertFalse(study_report["promotion_gate_status"]["minimum_reviewers_per_target_met"])
            self.assertFalse(study_report["promotion_gate_status"]["ready_for_promotion"])
            self.assertEqual(study_report["target_reports"][0]["review_count"], 7)
            self.assertEqual(study_report["target_reports"][0]["reviewer_count"], 1)


if __name__ == "__main__":
    unittest.main()
