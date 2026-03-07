"""Artifact builders for traces and score reports."""

from __future__ import annotations

from datetime import datetime, timezone

from . import __version__


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_trace(*, scenario: dict, seed: int, run_id: str, model_id: str, evaluation: dict, world_state: dict) -> dict:
    metadata = scenario["metadata"]
    now = utc_now_iso()
    return {
        "trace_version": "0.1.0",
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
            "seed": seed,
        },
        "agent": {
            "model_id": model_id,
            "provider": "dry-run",
            "agent_config_hash": "dry-run",
            "system_prompt_hash": "dry-run",
            "agent_name": "TheStartupBench Dry Runner",
            "agent_version": __version__,
        },
        "runtime": {
            "started_at": now,
            "ended_at": now,
            "wall_clock_seconds": 0.0,
            "api_cost_usd": 0.0,
            "total_tool_calls": 0,
        },
        "turns": [],
        "state_snapshots": [
            {
                "snapshot_id": "initial",
                "kind": "initial",
                "state": world_state,
            },
            {
                "snapshot_id": "final",
                "kind": "final",
                "state": world_state,
            },
        ],
        "evaluation": {
            "scenario_score": evaluation["scenario_score"],
            "outcome_score": evaluation["outcome_score"],
            "constraint_score": evaluation["constraint_score"],
            "subscores": evaluation["subscores"],
            "violations": evaluation["violations"],
            "pass": evaluation["pass"],
            "judge_versions": [],
            "judge_inputs_hashes": [],
        },
    }


def build_score_report(*, scenario: dict, run_id: str, evaluation: dict) -> dict:
    metadata = scenario["metadata"]
    return {
        "scenario_id": metadata["scenario_id"],
        "scenario_version": metadata["scenario_version"],
        "run_id": run_id,
        "scenario_score": evaluation["scenario_score"],
        "outcome_score": evaluation["outcome_score"],
        "constraint_score": evaluation["constraint_score"],
        "subscores": evaluation["subscores"],
        "violations": evaluation["violations"],
        "pass": evaluation["pass"],
        "evaluator_results": evaluation["evaluator_results"],
    }


__all__ = ["build_score_report", "build_trace", "utc_now_iso"]

