from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.reviewer_ops import assign_reviewer_taskforce, export_review_forms, import_review_forms
from thestartupbench.study_runner import run_calibration_study
from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"
STUDY_MANIFEST_PATH = EXAMPLES_DIR / "operator_calibration_study_manifest.json"
ROSTER_PATH = EXAMPLES_DIR / "reviewer_roster_template.csv"


class ReviewerOpsTests(unittest.TestCase):
    def test_assign_reviewer_taskforce_emits_valid_assignments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            run_dir = temp_dir / "run"
            assignment_dir = temp_dir / "assignments"
            run_calibration_study(
                study_manifest_path=STUDY_MANIFEST_PATH,
                output_dir=run_dir,
            )
            result = assign_reviewer_taskforce(
                study_manifest_path=STUDY_MANIFEST_PATH,
                study_run_dir=run_dir,
                roster_path=ROSTER_PATH,
                output_dir=assignment_dir,
            )

            self.assertTrue(result["validation"]["ok"])
            manifest_path = assignment_dir / "review_assignments.json"
            validation = validate_artifact_file(
                artifact_type="review-assignments",
                path=manifest_path,
            )
            self.assertTrue(validation.ok)

    def test_export_and_import_review_forms_round_trip_to_operator_reviews(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            run_dir = temp_dir / "run"
            assignment_dir = temp_dir / "assignments"
            forms_dir = temp_dir / "forms"
            imported_dir = temp_dir / "imported"
            run_calibration_study(
                study_manifest_path=STUDY_MANIFEST_PATH,
                output_dir=run_dir,
            )
            assign_reviewer_taskforce(
                study_manifest_path=STUDY_MANIFEST_PATH,
                study_run_dir=run_dir,
                roster_path=ROSTER_PATH,
                output_dir=assignment_dir,
            )
            export_result = export_review_forms(
                assignment_manifest_path=assignment_dir / "review_assignments.json",
                output_dir=forms_dir,
            )

            self.assertTrue(export_result["validation"]["ok"])
            reviewer_export = export_result["export"]["exports"][0]
            csv_path = Path(reviewer_export["csv_path"])
            rows = []
            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["startup_stage_focus"] = "seed_to_series_b"
            rows[0]["years_experience"] = "9"
            rows[0]["survival_and_risk"] = "4"
            rows[0]["capital_allocation"] = "3"
            rows[0]["customer_trust"] = "4"
            rows[0]["people_leadership"] = "3"
            rows[0]["strategic_quality"] = "4"
            rows[0]["overall_recommendation"] = "pass"
            rows[0]["strengths"] = "Protected trust | Stayed disciplined"
            rows[0]["weaknesses"] = "Board communication not explicit"
            rows[0]["recommended_actions"] = "Send a board note"
            rows[0]["benchmark_gaming_signals"] = ""
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

            import_result = import_review_forms(forms_dir=forms_dir, output_dir=imported_dir)

            self.assertTrue(import_result["validation"]["ok"])
            self.assertEqual(import_result["import_result"]["review_count"], 1)
            review_path = Path(import_result["import_result"]["review_paths"][0])
            review = json.loads(review_path.read_text(encoding="utf-8"))
            self.assertEqual(review["rubric"]["overall_recommendation"], "pass")
            self.assertEqual(review["notes"]["strengths"], ["Protected trust", "Stayed disciplined"])
            validation = validate_artifact_file(artifact_type="operator-review", path=review_path)
            self.assertTrue(validation.ok)


if __name__ == "__main__":
    unittest.main()
