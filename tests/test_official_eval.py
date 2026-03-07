from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.official_eval import build_run_manifest, load_official_eval_profile
from thestartupbench.suite_runner import run_suite


REPO_ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = REPO_ROOT / "examples" / "official_eval_profile.json"
SUITE_PATH = REPO_ROOT / "examples" / "dev_scenario_suite.json"


class OfficialEvalTests(unittest.TestCase):
    def test_load_official_eval_profile(self) -> None:
        profile = load_official_eval_profile(PROFILE_PATH)

        self.assertEqual(profile["profile_id"], "official-hosted-v0.1.0")
        self.assertTrue(profile["hosted_evaluation"])

    def test_build_run_manifest_for_baseline(self) -> None:
        result = build_run_manifest(
            suite_path=SUITE_PATH,
            profile_path=PROFILE_PATH,
            runner_type="baseline",
            seeds=[1, 2, 3, 4, 5],
            baseline_id="heuristic_resilient_operator",
            max_turns=8,
        )

        self.assertTrue(result["validation"]["ok"])
        manifest = result["run_manifest"]
        self.assertEqual(manifest["official_profile"]["profile_id"], "official-hosted-v0.1.0")
        self.assertEqual(manifest["run_configuration"]["repeated_run_count"], 5)
        self.assertEqual(manifest["run_configuration"]["runner_id"], "heuristic_resilient_operator")

    def test_run_suite_output_dir_can_emit_run_manifest(self) -> None:
        suite_result = run_suite(
            suite_path=SUITE_PATH,
            runner_type="baseline",
            seeds=[1, 2],
            baseline_id="heuristic_resilient_operator",
            max_turns=4,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir)
            (out_dir / "suite_report.json").write_text(json.dumps(suite_result["suite_report"], indent=2), encoding="utf-8")
            manifest_result = build_run_manifest(
                suite_path=SUITE_PATH,
                profile_path=PROFILE_PATH,
                runner_type="baseline",
                seeds=[1, 2],
                baseline_id="heuristic_resilient_operator",
                max_turns=4,
            )
            (out_dir / "run_manifest.json").write_text(json.dumps(manifest_result["run_manifest"], indent=2), encoding="utf-8")

            manifest = json.loads((out_dir / "run_manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["run_configuration"]["repeated_run_count"], 2)
        self.assertEqual(manifest["suite_path"], str(SUITE_PATH))

    def test_build_run_manifest_rejects_disallowed_runner_type(self) -> None:
        with self.assertRaisesRegex(ValueError, "not allowed by profile"):
            build_run_manifest(
                suite_path=SUITE_PATH,
                profile_path=PROFILE_PATH,
                runner_type="dry",
                seeds=[1, 2, 3],
            )


if __name__ == "__main__":
    unittest.main()
