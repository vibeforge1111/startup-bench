from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from thestartupbench.baseline_runner import run_baseline
from thestartupbench.script_runner import run_tool_script
from thestartupbench.self_improvement_export import (
    SCHEMA_VERSION,
    build_and_validate_self_improvement_export,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = REPO_ROOT / "examples" / "minimal_0to1_scenario.json"
TOOL_SCRIPT_PATH = REPO_ROOT / "examples" / "minimal_tool_script.json"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class SelfImprovementExportTests(unittest.TestCase):
    def _write_fixture_runs(self, root: Path) -> dict[str, Path]:
        baseline = run_baseline(
            scenario_path=SCENARIO_PATH,
            baseline_id="heuristic_resilient_operator",
            seed=7,
            max_turns=2,
        )
        candidate = run_tool_script(
            scenario_path=SCENARIO_PATH,
            tool_calls_path=TOOL_SCRIPT_PATH,
            seed=7,
            max_turns=2,
        )
        paths = {
            "baseline_trace": root / "baseline" / "trace.json",
            "baseline_score": root / "baseline" / "score_report.json",
            "candidate_trace": root / "candidate" / "trace.json",
            "candidate_score": root / "candidate" / "score_report.json",
        }
        _write_json(paths["baseline_trace"], baseline["trace"])
        _write_json(paths["baseline_score"], baseline["score_report"])
        _write_json(paths["candidate_trace"], candidate["trace"])
        _write_json(paths["candidate_score"], candidate["score_report"])
        return paths

    def test_export_validates_and_keeps_claims_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            paths = self._write_fixture_runs(Path(tmp_dir))
            result = build_and_validate_self_improvement_export(
                scenario_path=SCENARIO_PATH,
                baseline_trace_path=paths["baseline_trace"],
                baseline_score_report_path=paths["baseline_score"],
                candidate_trace_path=paths["candidate_trace"],
                candidate_score_report_path=paths["candidate_score"],
                tool_calls_path=TOOL_SCRIPT_PATH,
                baseline_id="heuristic_resilient_operator",
                candidate_id="minimal-tool-script",
                seed=7,
                max_turns=2,
            )

            self.assertTrue(result["validation"]["ok"])
            packet = result["export"]
            self.assertEqual(packet["schema_version"], SCHEMA_VERSION)
            self.assertEqual(packet["run_signature"]["payload"]["seeds"], [7])
            self.assertEqual(
                packet["candidate_lock"]["target_sha256"],
                packet["run_signature"]["payload"]["tool_calls_sha256"],
            )
            self.assertEqual(packet["comparison"]["metric"], "scenario_score")
            self.assertFalse(packet["claim_boundary"]["score_claim_allowed"])
            self.assertFalse(packet["claim_boundary"]["improvement_claim_allowed"])
            self.assertFalse(packet["claim_boundary"]["public_ready"])
            self.assertFalse(packet["claim_boundary"]["network_absorbable"])
            self.assertIn(
                "bind_export_into_immutable_spark_qa_proof_bundle",
                packet["claim_boundary"]["required_before_claim"],
            )
            self.assertEqual(packet["heldout"]["status"], "not_supplied")
            self.assertFalse(packet["heldout"]["candidate_visible"])
            self.assertEqual(packet["trap"]["status"], "not_supplied")
            self.assertGreaterEqual(len(packet["raw_artifacts"]), 6)

    def test_run_signature_changes_when_candidate_lock_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            paths = self._write_fixture_runs(Path(tmp_dir))
            first = build_and_validate_self_improvement_export(
                scenario_path=SCENARIO_PATH,
                baseline_trace_path=paths["baseline_trace"],
                baseline_score_report_path=paths["baseline_score"],
                candidate_trace_path=paths["candidate_trace"],
                candidate_score_report_path=paths["candidate_score"],
                tool_calls_path=TOOL_SCRIPT_PATH,
                baseline_id="heuristic_resilient_operator",
                seed=7,
                max_turns=2,
            )["export"]
            alternate_tool_calls = Path(tmp_dir) / "alternate_tool_script.json"
            alternate_tool_calls.write_text(
                json.dumps(
                    [
                        {
                            "tool_name": "sim.advance",
                            "request_id": "alternate_req_001",
                            "arguments": {"days": 7},
                        }
                    ]
                ),
                encoding="utf-8",
            )
            second = build_and_validate_self_improvement_export(
                scenario_path=SCENARIO_PATH,
                baseline_trace_path=paths["baseline_trace"],
                baseline_score_report_path=paths["baseline_score"],
                candidate_trace_path=paths["candidate_trace"],
                candidate_score_report_path=paths["candidate_score"],
                tool_calls_path=alternate_tool_calls,
                baseline_id="heuristic_resilient_operator",
                seed=7,
                max_turns=2,
            )["export"]

            self.assertNotEqual(
                first["run_signature"]["digest"],
                second["run_signature"]["digest"],
            )
            self.assertNotEqual(
                first["candidate_lock"]["target_sha256"],
                second["candidate_lock"]["target_sha256"],
            )

    def test_optional_heldout_and_trap_artifacts_are_exported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            paths = self._write_fixture_runs(root)
            heldout_path = root / "hidden_heldout_report.json"
            trap_path = root / "trap_report.json"
            heldout_path.write_text('{"status":"passed"}', encoding="utf-8")
            trap_path.write_text('{"status":"passed"}', encoding="utf-8")

            result = build_and_validate_self_improvement_export(
                scenario_path=SCENARIO_PATH,
                baseline_trace_path=paths["baseline_trace"],
                baseline_score_report_path=paths["baseline_score"],
                candidate_trace_path=paths["candidate_trace"],
                candidate_score_report_path=paths["candidate_score"],
                tool_calls_path=TOOL_SCRIPT_PATH,
                baseline_id="heuristic_resilient_operator",
                seed=7,
                max_turns=2,
                heldout_artifact_path=heldout_path,
                trap_artifact_path=trap_path,
            )

            self.assertTrue(result["validation"]["ok"])
            packet = result["export"]
            self.assertEqual(packet["heldout"]["status"], "passed")
            self.assertTrue(packet["heldout"]["pass"])
            self.assertFalse(packet["heldout"]["candidate_visible"])
            self.assertEqual(packet["heldout"]["artifact_ref"], str(heldout_path.resolve()))
            self.assertEqual(packet["trap"]["status"], "passed")
            self.assertTrue(packet["trap"]["pass"])
            self.assertEqual(packet["trap"]["artifact_ref"], str(trap_path.resolve()))

    def test_cli_writes_self_improvement_export(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            paths = self._write_fixture_runs(root)
            output_dir = root / "export"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "thestartupbench",
                    "export-self-improvement",
                    "--scenario-path",
                    str(SCENARIO_PATH),
                    "--baseline-trace",
                    str(paths["baseline_trace"]),
                    "--baseline-score-report",
                    str(paths["baseline_score"]),
                    "--candidate-trace",
                    str(paths["candidate_trace"]),
                    "--candidate-score-report",
                    str(paths["candidate_score"]),
                    "--tool-calls-path",
                    str(TOOL_SCRIPT_PATH),
                    "--baseline-id",
                    "heuristic_resilient_operator",
                    "--candidate-id",
                    "minimal-tool-script",
                    "--seed",
                    "7",
                    "--max-turns",
                    "2",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=REPO_ROOT,
                env={"PYTHONPATH": str(REPO_ROOT / "src")},
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            packet_path = output_dir / "self_improvement_export.json"
            self.assertTrue(packet_path.exists())
            packet = json.loads(packet_path.read_text(encoding="utf-8"))
            self.assertEqual(packet["schema_version"], SCHEMA_VERSION)
            self.assertFalse(packet["claim_boundary"]["improvement_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
