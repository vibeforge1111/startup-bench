from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.submission_builder import build_submission
from thestartupbench.suite_runner import run_suite


REPO_ROOT = Path(__file__).resolve().parents[1]
SUITE_PATH = REPO_ROOT / "examples" / "dev_scenario_suite.json"


class SubmissionBuilderTests(unittest.TestCase):
    def test_build_submission_from_suite_report(self) -> None:
        suite_result = run_suite(
            suite_path=SUITE_PATH,
            runner_type="baseline",
            seeds=[1, 2],
            baseline_id="heuristic_b2b_operator",
            max_turns=4,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            report_path = Path(tmp_dir) / "suite_report.json"
            report_path.write_text(json.dumps(suite_result["suite_report"]), encoding="utf-8")

            result = build_submission(
                suite_report_paths=[report_path],
                model_id="heuristic_b2b_operator",
                provider="baseline",
                contamination_flag="clean",
            )

        self.assertTrue(result["validation"]["ok"])
        submission = result["submission"]
        self.assertEqual(submission["evaluation"]["repeat_count"], 2)
        tracks = {item["track"] for item in submission["evaluation"]["track_summaries"]}
        self.assertEqual(tracks, {"0to1", "b2b_saas", "board", "crisis", "scale"})


if __name__ == "__main__":
    unittest.main()
