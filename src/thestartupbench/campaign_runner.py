"""Repeated-run campaign helpers for TheStartupBench."""

from __future__ import annotations

from pathlib import Path
from statistics import mean, pstdev

from . import __version__
from .baseline_runner import run_baseline
from .runner import run_dry_scenario
from .scenario_loader import load_scenario
from .script_runner import run_tool_script
from .validation import validate_instance


def _round_metric(value: float) -> float:
    return round(value, 4)


def _parse_seeds(seeds: str) -> list[int]:
    values = [item.strip() for item in seeds.split(",") if item.strip()]
    if not values:
        raise ValueError("At least one seed is required.")
    return [int(value) for value in values]


def run_campaign(
    *,
    scenario_path: Path,
    runner_type: str,
    seeds: list[int],
    baseline_id: str | None = None,
    tool_calls_path: Path | None = None,
    max_turns: int | None = None,
) -> dict:
    if not seeds:
        raise ValueError("At least one seed is required.")

    scenario = load_scenario(scenario_path)
    metadata = scenario["metadata"]
    run_summaries: list[dict] = []

    for seed in seeds:
        if runner_type == "dry":
            result = run_dry_scenario(scenario_path, seed=seed)
            runner_id = "dry-run"
        elif runner_type == "baseline":
            if not baseline_id:
                raise ValueError("baseline_id is required when runner_type='baseline'.")
            result = run_baseline(
                scenario_path=scenario_path,
                baseline_id=baseline_id,
                seed=seed,
                max_turns=max_turns,
            )
            runner_id = baseline_id
        elif runner_type == "script":
            if tool_calls_path is None:
                raise ValueError("tool_calls_path is required when runner_type='script'.")
            result = run_tool_script(
                scenario_path=scenario_path,
                tool_calls_path=tool_calls_path,
                seed=seed,
            )
            runner_id = str(tool_calls_path.name)
        else:
            raise ValueError("runner_type must be one of: dry, baseline, script.")

        score_report = result["score_report"]
        trace = result["trace"]
        run_summaries.append(
            {
                "run_id": result["run_id"],
                "seed": seed,
                "scenario_score": float(score_report["scenario_score"]),
                "outcome_score": float(score_report["outcome_score"]),
                "constraint_score": float(score_report["constraint_score"]),
                "pass": bool(score_report["pass"]),
                "total_tool_calls": int(trace["runtime"]["total_tool_calls"]),
            }
        )

    scenario_scores = [run["scenario_score"] for run in run_summaries]
    outcome_scores = [run["outcome_score"] for run in run_summaries]
    constraint_scores = [run["constraint_score"] for run in run_summaries]
    total_tool_calls = [run["total_tool_calls"] for run in run_summaries]
    pass_flags = [1.0 if run["pass"] else 0.0 for run in run_summaries]

    batch_report = {
        "report_version": "0.1.0",
        "benchmark": {
            "benchmark_name": "TheStartupBench",
            "benchmark_version": metadata["benchmark_version"],
            "scaffold_version": __version__,
        },
        "campaign": {
            "runner_type": runner_type,
            "runner_id": runner_id,
            "scenario_id": metadata["scenario_id"],
            "scenario_version": metadata["scenario_version"],
            "track": metadata["track"],
            "seeds": seeds,
            "run_count": len(run_summaries),
        },
        "aggregate_metrics": {
            "scenario_score_mean": _round_metric(mean(scenario_scores)),
            "scenario_score_stddev": _round_metric(pstdev(scenario_scores)),
            "scenario_score_min": _round_metric(min(scenario_scores)),
            "scenario_score_max": _round_metric(max(scenario_scores)),
            "outcome_score_mean": _round_metric(mean(outcome_scores)),
            "constraint_score_mean": _round_metric(mean(constraint_scores)),
            "pass_rate": _round_metric(mean(pass_flags)),
            "total_tool_calls_mean": _round_metric(mean(total_tool_calls)),
        },
        "runs": run_summaries,
    }
    return {
        "batch_report": batch_report,
        "validation": validate_instance(
            artifact_type="batch-report",
            instance=batch_report,
            path=Path("batch_report.json"),
        ).to_dict(),
    }


__all__ = ["_parse_seeds", "run_campaign"]
