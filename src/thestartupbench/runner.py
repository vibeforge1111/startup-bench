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


def _clamp(value: float, *, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _pressure_to_index(value: object) -> float:
    if isinstance(value, (int, float)):
        return _clamp(float(value))
    if isinstance(value, str):
        mapping = {
            "very_low": 0.1,
            "low": 0.25,
            "moderate": 0.5,
            "high": 0.75,
            "very_high": 0.9,
        }
        return mapping.get(value.lower(), 0.5)
    return 0.5


def _derive_segment_mix_index(customers: dict, *, fallback_trust: float, fallback_churn: float) -> float:
    segments = customers.get("segments", [])
    if not isinstance(segments, list) or not segments:
        return _clamp((fallback_trust * 0.6) + ((1.0 - fallback_churn * 4.0) * 0.4))

    weight_total = 0.0
    weighted_score = 0.0
    for index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            continue
        default_weight = 1.0 / max(len(segments), 1)
        weight = max(0.0, float(segment.get("revenue_share", default_weight)))
        trust = _clamp(float(segment.get("trust_score", fallback_trust)))
        churn = _clamp(float(segment.get("monthly_churn_rate", fallback_churn)), maximum=1.0)
        support_load = _clamp(float(segment.get("support_load_index", 0.3)))
        expansion = _clamp(float(segment.get("expansion_potential", 0.5)))
        competitor_pressure = _clamp(float(segment.get("competitor_pressure_index", 0.3)))
        retention_signal = _clamp(1.0 - (churn / 0.12))
        segment_score = _clamp(
            trust * 0.3
            + retention_signal * 0.35
            + (1.0 - support_load) * 0.1
            + expansion * 0.15
            + (1.0 - competitor_pressure) * 0.1
        )
        weighted_score += segment_score * weight
        weight_total += weight
        segment["segment_id"] = segment.get("segment_id", f"segment_{index + 1}")
        segment["health_index"] = round(segment_score, 4)

    if weight_total <= 0:
        return _clamp((fallback_trust * 0.6) + ((1.0 - fallback_churn * 4.0) * 0.4))
    return _clamp(weighted_score / weight_total)


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
    operations = world_state.setdefault("operations", {})
    team = world_state.setdefault("team", {})
    risk = world_state.setdefault("risk", {})
    market = world_state.setdefault("market", {})

    cash_usd = float(finance.get("cash_usd", 0))
    restricted_cash = max(0.0, float(finance.get("restricted_cash_usd", 0)))
    monthly_burn = float(finance.get("monthly_burn_usd", 0))
    monthly_revenue = float(finance.get("monthly_revenue_usd", 0))
    net_burn = monthly_burn - monthly_revenue
    finance["net_burn_usd"] = round(net_burn, 2)
    finance["liquid_cash_usd"] = round(max(0.0, cash_usd - restricted_cash), 2)
    if net_burn <= 0:
        finance["runway_weeks"] = 999.0
    else:
        finance["runway_weeks"] = round((finance["liquid_cash_usd"] / net_burn) * 4, 2)

    concentration = float(finance.get("treasury_concentration", 0))
    finance["treasury_concentration"] = round(max(0.0, min(1.0, concentration)), 4)

    competitor_pressure_index = _pressure_to_index(market.get("competitor_pressure", market.get("competitor_pressure_index", 0.3)))
    pricing_pressure_index = _pressure_to_index(market.get("pricing_pressure", market.get("pricing_pressure_index", 0.2)))
    demand_index = _clamp(float(market.get("demand_index", 0.85)), minimum=0.0, maximum=1.5)
    market["competitor_pressure_index"] = round(competitor_pressure_index, 4)
    market["pricing_pressure_index"] = round(pricing_pressure_index, 4)
    market["demand_index"] = round(demand_index, 4)

    churn = float(customers.get("monthly_churn_rate", 0))
    trust = float(customers.get("trust_score", 0.7))
    support_backlog = float(operations.get("support_backlog", 0))
    support_pressure = max(0.0, min(1.0, 1.0 - (support_backlog / 150.0)))
    morale = float(team.get("morale", 0.7))
    attrition_risk = float(team.get("attrition_risk", 0.2))
    regulatory_pressure = float(risk.get("regulatory_pressure", 0.0))
    segment_mix_index = _derive_segment_mix_index(customers, fallback_trust=trust, fallback_churn=churn)
    customers["segment_mix_index"] = round(segment_mix_index, 4)

    hiring = team.setdefault("hiring", {})
    open_roles = int(hiring.get("open_roles", team.get("open_roles", 0)))
    sourced_candidates = int(hiring.get("sourced_candidates", 0))
    onsite_candidates = int(hiring.get("onsite_candidates", 0))
    offers_out = int(hiring.get("offers_out", 0))
    headcount = int(team.get("headcount", 0))
    critical_roles_open = int(hiring.get("critical_roles_open", min(open_roles, 1 if open_roles else 0)))
    funnel_capacity = (
        min(1.0, sourced_candidates / max(open_roles * 6.0, 1.0)) * 0.35
        + min(1.0, onsite_candidates / max(open_roles * 2.0, 1.0)) * 0.35
        + min(1.0, offers_out / max(open_roles, 1.0)) * 0.3
    )
    hiring["open_roles"] = open_roles
    hiring["critical_roles_open"] = critical_roles_open
    hiring["hiring_capacity_index"] = round(_clamp(funnel_capacity), 4)
    hiring["funnel_depth"] = sourced_candidates + onsite_candidates + offers_out
    staffing_gap = _clamp((open_roles + critical_roles_open) / max(headcount + open_roles, 1), maximum=1.0)
    team["delivery_capacity_index"] = round(
        _clamp(
            (1.0 - float(team.get("bandwidth_load", 0.7))) * 0.35
            + (1.0 - attrition_risk) * 0.2
            + morale * 0.2
            + (1.0 - staffing_gap) * 0.15
            + hiring["hiring_capacity_index"] * 0.1
        ),
        4,
    )
    health_index = max(
        0.0,
        min(
            1.0,
            (1 - churn * 4.0) * 0.42
            + trust * 0.28
            + support_pressure * 0.15
            + morale * 0.1
            + (1.0 - attrition_risk) * 0.03
            + (1.0 - regulatory_pressure) * 0.01
            + segment_mix_index * 0.01
            + (1.0 - competitor_pressure_index) * 0.02
            - (pricing_pressure_index * 0.01)
            + ((demand_index / 1.5) * 0.01),
        ),
    )
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
