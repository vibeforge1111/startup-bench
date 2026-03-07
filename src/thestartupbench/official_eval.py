"""Official evaluation profile and run-manifest helpers."""

from __future__ import annotations

from pathlib import Path

from . import __version__
from .scenario_loader import load_json
from .suite_runner import load_scenario_suite
from .validation import raise_if_invalid, validate_instance


def load_official_eval_profile(path: Path) -> dict:
    profile = load_json(path)
    raise_if_invalid(artifact_type="official-eval-profile", instance=profile, path=path)
    return profile


def build_run_manifest(
    *,
    suite_path: Path,
    profile_path: Path,
    runner_type: str,
    seeds: list[int],
    baseline_id: str | None = None,
    tool_calls_path: Path | None = None,
    max_turns: int | None = None,
) -> dict:
    suite = load_scenario_suite(suite_path)
    profile = load_official_eval_profile(profile_path)

    if runner_type not in profile["allowed_runner_types"]:
        allowed = ", ".join(profile["allowed_runner_types"])
        raise ValueError(f"Runner type '{runner_type}' is not allowed by profile '{profile['profile_id']}'. Allowed: {allowed}")

    runner_id = baseline_id if runner_type == "baseline" else (tool_calls_path.name if tool_calls_path else runner_type)
    if runner_type == "baseline" and not baseline_id:
        raise ValueError("baseline_id is required when runner_type='baseline'.")
    if runner_type == "script" and tool_calls_path is None:
        raise ValueError("tool_calls_path is required when runner_type='script'.")

    manifest = {
        "manifest_version": "0.1.0",
        "benchmark_version": suite["benchmark_version"],
        "scenario_pack_version": suite["scenario_pack_version"],
        "scaffold_version": __version__,
        "split": suite["split"],
        "suite_path": str(suite_path),
        "official_profile": {
            "profile_id": profile["profile_id"],
            "profile_version": profile["profile_version"],
            "source_path": str(profile_path),
            "hosted_evaluation": bool(profile["hosted_evaluation"]),
        },
        "policy_bundle": profile["policy_bundle"],
        "run_configuration": {
            "runner_type": runner_type,
            "runner_id": runner_id,
            "seeds": seeds,
            "repeated_run_count": len(seeds),
            "max_turns": max_turns if max_turns is not None else int(profile["evaluation_defaults"]["max_turns_default"]),
            "timeout_seconds": int(profile["evaluation_defaults"]["timeout_seconds"]),
            **({"tool_calls_path": str(tool_calls_path)} if tool_calls_path else {}),
        },
        "provenance": {
            "generator": "thestartupbench",
            "generated_by": "emit-run-manifest",
        },
    }
    return {
        "run_manifest": manifest,
        "validation": validate_instance(
            artifact_type="run-manifest",
            instance=manifest,
            path=Path("run_manifest.json"),
        ).to_dict(),
    }


__all__ = ["build_run_manifest", "load_official_eval_profile"]
