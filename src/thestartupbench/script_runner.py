"""Scripted execution support for TheStartupBench."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from .artifacts import build_score_report, build_trace
from .evaluators import evaluate_dry_run
from .runner import initialize_world_state
from .scenario_loader import load_json, load_scenario
from .runtime import RuntimeSession, execute_tool_call
from .tool_registry import tool_manifest_for_names
from .trace_validation import validate_trace_integrity
from .validation import validate_instance


def run_tool_script(*, scenario_path: Path, tool_calls_path: Path, seed: int) -> dict:
    scenario = load_scenario(scenario_path)
    tool_calls = load_json(tool_calls_path)
    if not isinstance(tool_calls, list):
        raise ValueError("Tool script must be a JSON array of tool calls.")

    world_state = initialize_world_state(scenario, seed=seed)
    session = RuntimeSession(scenario=scenario, world_state=world_state)
    turns: list[dict] = []
    snapshots: list[dict] = [
        {"snapshot_id": "initial", "kind": "initial", "state": deepcopy(session.world_state)}
    ]

    for turn_index, tool_call in enumerate(tool_calls):
        before_time = session.world_state["sim"]["current_time"]
        observations = session.visible_observations()
        response = execute_tool_call(session, tool_call)
        after_time = session.world_state["sim"]["current_time"]
        turns.append(
            {
                "turn_index": turn_index,
                "sim_time_before": before_time,
                "sim_time_after": after_time,
                "observations": observations,
                "actions": [
                    {
                        "tool_name": tool_call["tool_name"],
                        "request_id": tool_call["request_id"],
                        "arguments": tool_call.get("arguments", {}),
                        "response": response,
                        "status": "ok",
                    }
                ],
                "events": response["result"].get("events_processed", []),
                "notes": [],
            }
        )
        snapshots.append(
            {
                "snapshot_id": f"turn_{turn_index}",
                "kind": "milestone",
                "state": deepcopy(session.world_state),
            }
        )

    run_id = f"script-{uuid4()}"
    evaluation = evaluate_dry_run(scenario=scenario, world_state=session.world_state)
    trace = build_trace(
        scenario=scenario,
        seed=seed,
        run_id=run_id,
        model_id="scripted-agent",
        evaluation=evaluation,
        world_state=session.world_state,
    )
    trace["turns"] = turns
    trace["state_snapshots"] = snapshots + [{"snapshot_id": "final", "kind": "final", "state": deepcopy(session.world_state)}]
    trace["runtime"]["total_tool_calls"] = len(tool_calls)

    score_report = build_score_report(scenario=scenario, run_id=run_id, evaluation=evaluation)
    return {
        "run_id": run_id,
        "tool_manifest": tool_manifest_for_names(scenario["tools"]),
        "trace": trace,
        "score_report": score_report,
        "artifact_validation": {
            "trace": validate_instance(artifact_type="trace", instance=trace, path=Path("trace.json")).to_dict(),
            "trace_integrity": validate_trace_integrity(trace).to_dict(),
            "score_report": validate_instance(
                artifact_type="score-report",
                instance=score_report,
                path=Path("score_report.json"),
            ).to_dict(),
        },
    }


__all__ = ["run_tool_script"]

