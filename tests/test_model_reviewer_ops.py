from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.model_reviewer_ops import export_model_review_bundles, import_model_reviews
from thestartupbench.study_runner import run_calibration_study
from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"
STUDY_MANIFEST_PATH = EXAMPLES_DIR / "operator_calibration_study_manifest.json"
OPERATOR_REVIEW_PATH = EXAMPLES_DIR / "minimal_operator_review.json"


class ModelReviewerOpsTests(unittest.TestCase):
    def test_export_model_review_bundles_emits_valid_prompt_bundle_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            run_dir = temp_dir / "run"
            bundle_dir = temp_dir / "bundles"

            run_calibration_study(
                study_manifest_path=STUDY_MANIFEST_PATH,
                output_dir=run_dir,
            )
            result = export_model_review_bundles(
                study_run_dir=run_dir,
                output_dir=bundle_dir,
            )

            self.assertTrue(result["validation"]["ok"])
            manifest_path = bundle_dir / "model_review_prompt_export.json"
            validation = validate_artifact_file(
                artifact_type="model-review-prompt-export",
                path=manifest_path,
            )
            self.assertTrue(validation.ok)
            bundle = result["export"]["bundles"][0]
            prompt_path = Path(bundle["prompt_path"])
            context_path = Path(bundle["context_path"])
            template_path = Path(bundle["template_path"])
            self.assertTrue(prompt_path.exists())
            self.assertTrue(context_path.exists())
            self.assertTrue(template_path.exists())
            self.assertIn("TheStartupBench Synthetic Reviewer Prompt", prompt_path.read_text(encoding="utf-8"))
            template = json.loads(template_path.read_text(encoding="utf-8"))
            self.assertEqual(template["reviewer"]["role"], "model_reviewer")

    def test_import_model_reviews_accepts_fenced_json_and_reports_rejections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            raw_dir = temp_dir / "raw"
            imported_dir = temp_dir / "imported"
            raw_dir.mkdir(parents=True, exist_ok=True)

            review = json.loads(OPERATOR_REVIEW_PATH.read_text(encoding="utf-8"))
            review["reviewer"]["reviewer_id"] = "gpt_reviewer_001"
            fenced_path = raw_dir / "gpt_review.md"
            fenced_path.write_text(
                "Here is the review.\n```json\n" + json.dumps(review, indent=2) + "\n```\n",
                encoding="utf-8",
            )
            (raw_dir / "bad_review.txt").write_text("not valid json", encoding="utf-8")

            result = import_model_reviews(raw_dir=raw_dir, output_dir=imported_dir)

            self.assertTrue(result["validation"]["ok"])
            self.assertEqual(result["import_result"]["imported_review_count"], 1)
            self.assertEqual(result["import_result"]["rejected_count"], 1)
            imported_path = Path(result["import_result"]["imported_review_paths"][0])
            imported_validation = validate_artifact_file(
                artifact_type="operator-review",
                path=imported_path,
            )
            self.assertTrue(imported_validation.ok)
            manifest_validation = validate_artifact_file(
                artifact_type="model-review-import",
                path=imported_dir / "model_review_import.json",
            )
            self.assertTrue(manifest_validation.ok)


if __name__ == "__main__":
    unittest.main()
