from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.human_eval import aggregate_operator_reviews
from thestartupbench.validation import validate_artifact_file


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"
REVIEW_PATH = EXAMPLES_DIR / "minimal_operator_review.json"
SUMMARY_PATH = EXAMPLES_DIR / "minimal_operator_review_summary.json"


class HumanEvalTests(unittest.TestCase):
    def test_operator_review_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="operator-review",
            path=REVIEW_PATH,
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_operator_review_summary_example_validates(self) -> None:
        result = validate_artifact_file(
            artifact_type="operator-review-summary",
            path=SUMMARY_PATH,
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_aggregate_operator_reviews_emits_summary_and_disagreement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir = Path(tmp_dir)
            second_review_path = temp_dir / "second_review.json"
            second_review = json.loads(REVIEW_PATH.read_text(encoding="utf-8"))
            second_review["reviewer"]["reviewer_id"] = "ops_lead_002"
            second_review["reviewer"]["role"] = "vp_operations"
            second_review["reviewer"]["functional_domain"] = "operations"
            second_review["rubric"]["capital_allocation"] = 2
            second_review["rubric"]["overall_recommendation"] = "borderline"
            second_review_path.write_text(json.dumps(second_review, indent=2), encoding="utf-8")

            result = aggregate_operator_reviews([REVIEW_PATH, second_review_path])

        self.assertTrue(result["validation"]["ok"])
        summary = result["summary"]
        self.assertEqual(summary["review_count"], 2)
        self.assertEqual(summary["reviewer_count"], 2)
        self.assertEqual(summary["scenario_count"], 1)
        self.assertEqual(summary["overall"]["recommendation_distribution"]["pass"], 1)
        self.assertEqual(summary["overall"]["recommendation_distribution"]["borderline"], 1)
        self.assertTrue(summary["scenario_summaries"][0]["disagreement_flag"])


if __name__ == "__main__":
    unittest.main()
