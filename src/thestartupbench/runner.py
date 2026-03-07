"""Reference runner skeleton."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

from .artifacts import build_score_report, build_trace
from .evaluators import evaluate_dry_run
from .observations import project_surfaces
from .scenario_loader import load_scenario
from .tool_registry import tool_manifest_for_names
from .validation import validate_instance


def _parse_iso8601(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _format_iso8601(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _derive_horizon_end(*, current_time: str, time_horizon: dict) -> str:
    start = _parse_iso8601(current_time)
    unit = time_horizon["unit"]
    length = int(time_horizon["length"])

    if unit == "day":
        delta = timedelta(days=length)
    elif unit == "week":
        delta = timedelta(weeks=length)
    elif unit == "month":
        delta = timedelta(days=30 * length)
    elif unit == "quarter":
        delta = timedelta(days=91 * length)
    else:
        raise ValueError(f"Unsupported time horizon unit: {unit}")

    return _format_iso8601(start + delta)


def recalculate_derived_metrics(world_state: dict) -> None:
    finance = world_state.setdefault("finance", {})
    customers = world_state.setdefault("customers", {})

    cash_usd = float(finance.get("cash_usd", 0))
    monthly_burn = float(finance.get("monthly_burn_usd", 0))
    monthly_revenue = float(finance.get("monthly_revenue_usd", 0))
    net_burn = monthly_burn - monthly_revenue
    finance["net_burn_usd"] = round(net_burn, 2)
    if net_burn <= 0:
        finance["runway_weeks"] = 999.0
    else:
        finance["runway_weeks"] = round((cash_usd / net_burn) * 4, 2)

    churn = float(customers.get("monthly_churn_rate", 0))
    trust = float(customers.get("trust_score", 0.7))
    health_index = max(0.0, min(1.0, (1 - churn * 4.0) * 0.6 + trust * 0.4))
    customers["health_index"] = round(health_index, 4)


def initialize_world_state(scenario: dict, *, seed: int) -> dict:
    metadata = scenario["metadata"]
    initial = deepcopy(scenario["initial_state"])
    company_state = deepcopy(initial.get("company", {}))
    finance_state = deepcopy(initial.get("finance", {}))
    finance_keys = (
        "cash_usd",
        "monthly_burn_usd",
        "monthly_revenue_usd",
        "runway_weeks",
        "gross_margin_pct",
    )
    for key in finance_keys:
        if key in company_state and key not in finance_state:
            finance_state[key] = company_state.pop(key)

    current_time = initial.get("sim", {}).get("current_time", "2026-01-01T09:00:00Z")
    horizon_end = initial.get("sim", {}).get("horizon_end")
    if horizon_end is None:
        horizon_end = _derive_horizon_end(current_time=current_time, time_horizon=metadata["time_horizon"])

    state = {
        "company": company_state,
        "finance": finance_state,
        "product": initial.get("product", {}),
        "customers": initial.get("customers", {}),
        "market": initial.get("market", {}),
        "team": initial.get("team", {}),
        "growth": initial.get("growth", {}),
        "sales": initial.get("sales", {}),
        "operations": initial.get("operations", {}),
        "governance": initial.get("governance", {}),
        "policy": initial.get("policy", {}),
        "risk": initial.get("risk", {}),
        "sim": {
            "current_time": current_time,
            "current_turn": 0,
            "horizon_end": horizon_end,
            "seed": seed,
            "processed_event_ids": [],
            "pending_event_count": len(scenario.get("event_model", {}).get("scheduled_events", [])),
        },
    }
    recalculate_derived_metrics(state)
    return state


def build_observation_surfaces(scenario: dict, world_state: dict) -> list[dict]:
    return project_surfaces(scenario["observation_surfaces"], world_state)


def run_dry_scenario(path: Path, *, seed: int) -> dict:
    scenario = load_scenario(path)
    world_state = initialize_world_state(scenario, seed=seed)
    observations = build_observation_surfaces(scenario, world_state)
    tool_manifest = tool_manifest_for_names(scenario["tools"])
    run_id = f"dry-{uuid4()}"
    evaluation = evaluate_dry_run(scenario=scenario, world_state=world_state)
    trace = build_trace(
        scenario=scenario,
        seed=seed,
        run_id=run_id,
        model_id="dry-run",
        evaluation=evaluation,
        world_state=world_state,
    )
    score_report = build_score_report(scenario=scenario, run_id=run_id, evaluation=evaluation)
    trace_validation = validate_instance(artifact_type="trace", instance=trace, path=Path("trace.json"))
    score_validation = validate_instance(
        artifact_type="score-report",
        instance=score_report,
        path=Path("score_report.json"),
    )

    return {
        "run_id": run_id,
        "scenario_id": scenario["metadata"]["scenario_id"],
        "scenario_version": scenario["metadata"]["scenario_version"],
        "seed": seed,
        "observation_surfaces": observations,
        "tool_manifest": tool_manifest,
        "trace": trace,
        "score_report": score_report,
        "artifact_validation": {
            "trace": trace_validation.to_dict(),
            "score_report": score_validation.to_dict(),
            "tool_manifest": validate_instance(
                artifact_type="tool-manifest",
                instance=tool_manifest,
                path=Path("tool_manifest.json"),
            ).to_dict(),
        },
        "turn_count": 0,
    }


__all__ = ["build_observation_surfaces", "initialize_world_state", "recalculate_derived_metrics", "run_dry_scenario"]
