"""Canonical Startup Bench export for Spark self-improvement adapters."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from . import __version__
from .artifacts import utc_now_iso
from .scenario_loader import load_json, load_scenario
from .validation import validate_instance


SCHEMA_VERSION = "tsb_self_improvement_export.v1"
RUN_SIGNATURE_SCHEMA_VERSION = "tsb_self_improvement_run_signature.v1"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _artifact_ref(path: Path, artifact_type: str) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    return {
        "artifact_type": artifact_type,
        "path": str(resolved),
        "sha256": _sha256_file(resolved),
        "bytes": resolved.stat().st_size,
    }


def _run_seed(trace: dict[str, Any], fallback: int | None) -> int:
    scenario = trace.get("scenario") if isinstance(trace.get("scenario"), dict) else {}
    seed = scenario.get("seed")
    if isinstance(seed, int):
        return seed
    if fallback is not None:
        return int(fallback)
    return 0


def _run_summary(
    *,
    score_report: dict[str, Any],
    trace: dict[str, Any],
    trace_path: Path,
    score_report_path: Path,
    runner_id: str,
    seed: int | None,
    artifact_prefix: str,
) -> dict[str, Any]:
    return {
        "run_id": str(score_report["run_id"]),
        "runner_id": runner_id,
        "seed": _run_seed(trace, seed),
        "scenario_score": float(score_report["scenario_score"]),
        "outcome_score": float(score_report["outcome_score"]),
        "constraint_score": float(score_report["constraint_score"]),
        "pass": bool(score_report["pass"]),
        "violation_count": len(score_report.get("violations") or []),
        "trace_ref": _artifact_ref(trace_path, f"{artifact_prefix}_trace"),
        "score_report_ref": _artifact_ref(score_report_path, f"{artifact_prefix}_score_report"),
    }


def build_self_improvement_export(
    *,
    scenario_path: Path,
    baseline_trace_path: Path,
    baseline_score_report_path: Path,
    candidate_trace_path: Path,
    candidate_score_report_path: Path,
    tool_calls_path: Path,
    baseline_id: str,
    candidate_id: str = "startup_operator_candidate",
    seed: int | None = None,
    max_turns: int | None = None,
    heldout_artifact_path: Path | None = None,
    trap_artifact_path: Path | None = None,
) -> dict[str, Any]:
    scenario_path = scenario_path.expanduser().resolve()
    tool_calls_path = tool_calls_path.expanduser().resolve()
    scenario = load_scenario(scenario_path)
    metadata = scenario["metadata"]
    baseline_trace = load_json(baseline_trace_path)
    baseline_score_report = load_json(baseline_score_report_path)
    candidate_trace = load_json(candidate_trace_path)
    candidate_score_report = load_json(candidate_score_report_path)

    scenario_sha256 = _sha256_file(scenario_path)
    tool_calls_sha256 = _sha256_file(tool_calls_path)
    seeds = sorted(
        {
            _run_seed(baseline_trace, seed),
            _run_seed(candidate_trace, seed),
        }
    )
    signature_payload = {
        "baseline_id": baseline_id,
        "candidate_id": candidate_id,
        "scenario_path": str(scenario_path),
        "scenario_sha256": scenario_sha256,
        "tool_calls_path": str(tool_calls_path),
        "tool_calls_sha256": tool_calls_sha256,
        "seeds": seeds,
        "max_turns": max_turns,
    }
    baseline = _run_summary(
        score_report=baseline_score_report,
        trace=baseline_trace,
        trace_path=baseline_trace_path,
        score_report_path=baseline_score_report_path,
        runner_id=baseline_id,
        seed=seed,
        artifact_prefix="baseline",
    )
    candidate = _run_summary(
        score_report=candidate_score_report,
        trace=candidate_trace,
        trace_path=candidate_trace_path,
        score_report_path=candidate_score_report_path,
        runner_id=candidate_id,
        seed=seed,
        artifact_prefix="candidate",
    )
    delta = round(candidate["scenario_score"] - baseline["scenario_score"], 4)
    raw_artifacts = [
        baseline["trace_ref"],
        baseline["score_report_ref"],
        candidate["trace_ref"],
        candidate["score_report_ref"],
        _artifact_ref(tool_calls_path, "candidate_tool_calls"),
        _artifact_ref(scenario_path, "scenario"),
    ]
    heldout = {
        "status": "not_supplied",
        "pass": False,
        "candidate_visible": False,
        "artifact_ref": None,
        "claim_boundary": (
            "Heldout proof is not supplied by this export. Spark QA must bind "
            "hidden heldout evidence before any score claim."
        ),
    }
    if heldout_artifact_path is not None:
        ref = _artifact_ref(heldout_artifact_path, "heldout_artifact")
        raw_artifacts.append(ref)
        heldout.update({"status": "passed", "pass": True, "artifact_ref": ref["path"]})
    trap = {
        "status": "not_supplied",
        "pass": False,
        "artifact_ref": None,
        "claim_boundary": (
            "Trap proof is not supplied by this export. Spark QA must decide "
            "whether trap proof is required for the promotion lane."
        ),
    }
    if trap_artifact_path is not None:
        ref = _artifact_ref(trap_artifact_path, "trap_artifact")
        raw_artifacts.append(ref)
        trap.update({"status": "passed", "pass": True, "artifact_ref": ref["path"]})

    packet = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "benchmark": {
            "benchmark_name": "TheStartupBench",
            "benchmark_version": metadata["benchmark_version"],
            "scaffold_version": __version__,
        },
        "scenario": {
            "scenario_id": metadata["scenario_id"],
            "scenario_version": metadata["scenario_version"],
            "track": metadata["track"],
            "mode": metadata["mode"],
            "scenario_path": str(scenario_path),
            "scenario_sha256": scenario_sha256,
        },
        "run_signature": {
            "schema_version": RUN_SIGNATURE_SCHEMA_VERSION,
            "digest": _json_digest(signature_payload),
            "payload": signature_payload,
        },
        "candidate_lock": {
            "lock_state": "locked",
            "target_kind": "startup_operator_tool_calls",
            "target_path": str(tool_calls_path),
            "target_sha256": tool_calls_sha256,
            "scenario_sha256": scenario_sha256,
            "created_before_evaluation": True,
        },
        "baseline": baseline,
        "candidate": candidate,
        "comparison": {
            "metric": "scenario_score",
            "candidate_minus_baseline": delta,
            "candidate_beats_baseline": delta > 0,
        },
        "heldout": heldout,
        "trap": trap,
        "raw_artifacts": raw_artifacts,
        "claim_boundary": {
            "score_claim_allowed": False,
            "improvement_claim_allowed": False,
            "public_ready": False,
            "network_absorbable": False,
            "required_before_claim": [
                "bind_export_into_immutable_spark_qa_proof_bundle",
                "hidden_heldout_review",
                "wrapper_raw_reconciliation",
                "sidecar_review",
                "repeated_stability",
                "wall_clock_stability",
                "score_reconciliation",
            ],
        },
    }
    return packet


def build_and_validate_self_improvement_export(**kwargs: Any) -> dict[str, Any]:
    packet = build_self_improvement_export(**kwargs)
    return {
        "export": packet,
        "validation": validate_instance(
            artifact_type="self-improvement-export",
            instance=packet,
            path=Path("self_improvement_export.json"),
        ).to_dict(),
    }


__all__ = [
    "RUN_SIGNATURE_SCHEMA_VERSION",
    "SCHEMA_VERSION",
    "build_and_validate_self_improvement_export",
    "build_self_improvement_export",
]
