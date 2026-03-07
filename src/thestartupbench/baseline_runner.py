"""Heuristic baseline runners for TheStartupBench."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from .artifacts import build_score_report, build_trace
from .evaluators import evaluate_dry_run
from .runner import initialize_world_state
from .scenario_loader import load_scenario
from .runtime import RuntimeSession, execute_tool_call
from .tool_registry import tool_manifest_for_names
from .trace_validation import validate_trace_integrity
from .validation import validate_instance


_BASELINE_IDS = {"heuristic_b2b_operator", "heuristic_resilient_operator"}


def list_baselines() -> list[str]:
    return sorted(_BASELINE_IDS)


def _next_request_id(turn_index: int, action_index: int) -> str:
    return f"baseline_req_{turn_index:03d}_{action_index:02d}"


def _heuristic_b2b_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    actions: list[dict] = []
    action_index = 0

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    if float(finance.get("runway_weeks", 0)) < 32 and not finance.get("last_plan_update"):
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": -25000}},
            }
        )
        action_index += 1

    if float(product.get("onboarding_quality", 0.5)) < 0.68:
        actions.append(
            {
                "tool_name": "product.roadmap.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.08,
                    "major_incidents_delta": -1,
                    "budget_change_monthly_burn_usd": 8000,
                },
            }
        )
        action_index += 1

    if (
        float(customers.get("trust_score", 0.0)) > 0.68
        and float(sales.get("pricing", {}).get("current_price_index", 1.0)) < 1.08
    ):
        actions.append(
            {
                "tool_name": "sales.pricing.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"price_change_pct": 0.08},
            }
        )
        action_index += 1

    if float(sales.get("weighted_pipeline_usd", 0.0)) < float(finance.get("monthly_burn_usd", 0.0)) * 7.0:
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1,
                    "weighted_pipeline_usd_delta": 60000,
                },
            }
        )
        action_index += 1

    if int(governance.get("board_update_count", 0)) == 0 or (turn_index > 0 and turn_index % 4 == 0):
        actions.append(
            {
                "tool_name": "board.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "summary": "Tightened burn, improved onboarding focus, and monitored pricing elasticity.",
                    "forecast": {
                        "runway_weeks": finance.get("runway_weeks"),
                        "monthly_revenue_usd": finance.get("monthly_revenue_usd"),
                    },
                    "asks": ["maintain current hiring pace"],
                },
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _heuristic_resilient_actions(session: RuntimeSession, *, turn_index: int) -> list[dict]:
    finance = session.world_state.get("finance", {})
    product = session.world_state.get("product", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    team = session.world_state.get("team", {})
    risk = session.world_state.get("risk", {})
    actions: list[dict] = []
    action_index = 0

    actions.append(
        {
            "tool_name": "metrics.report",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {},
        }
    )
    action_index += 1

    if int(product.get("major_incidents_open", 0)) > 0:
        actions.append(
            {
                "tool_name": "ops.incident.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "incident_reduction": 1,
                    "trust_recovery": 0.06,
                    "churn_reduction": 0.01,
                    "monthly_burn_increase_usd": 9000,
                },
            }
        )
        action_index += 1

    if float(operations.get("support_backlog", 0.0)) > 35 or float(operations.get("support_sla_breach_risk", 0.0)) > 0.45:
        actions.append(
            {
                "tool_name": "ops.support.resolve",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "backlog_reduction": 16,
                    "sla_risk_reduction": 0.16,
                    "trust_recovery": 0.025,
                    "churn_reduction": 0.004,
                    "monthly_burn_increase_usd": 7000,
                },
            }
        )
        action_index += 1

    if float(risk.get("regulatory_pressure", 0.0)) > 0.55 or int(risk.get("active_legal_matters", 0)) > 0:
        actions.append(
            {
                "tool_name": "legal.compliance.respond",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pressure_reduction": 0.2,
                    "matters_reduction": 1,
                    "compliance_backlog_reduction": 6,
                    "trust_recovery": 0.02,
                    "monthly_burn_increase_usd": 11000,
                },
            }
        )
        action_index += 1

    if float(finance.get("treasury_concentration", 0.0)) > 0.78:
        actions.append(
            {
                "tool_name": "finance.treasury.rebalance",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "target_concentration": 0.45,
                    "rebalance_cost_usd": 8000,
                },
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 999.0)) < 18 or float(finance.get("liquid_cash_usd", finance.get("cash_usd", 0.0))) < float(finance.get("monthly_burn_usd", 0.0)) * 2.0:
        if not finance.get("last_raise_plan"):
            actions.append(
                {
                    "tool_name": "finance.raise.propose",
                    "request_id": _next_request_id(turn_index, action_index),
                    "arguments": {
                        "raise_amount_usd": max(600000.0, float(finance.get("monthly_burn_usd", 0.0)) * 6.0),
                        "dilution_pct": 0.12,
                        "monthly_burn_change_usd": 0,
                        "financing_risk_reduction": 0.28,
                        "transaction_cost_usd": 30000,
                    },
                }
            )
            action_index += 1

    if float(team.get("morale", 0.7)) < 0.58 or float(team.get("attrition_risk", 0.0)) > 0.5:
        actions.append(
            {
                "tool_name": "people.org.adjust",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "morale_delta": 0.08,
                    "attrition_risk_delta": -0.1,
                    "bandwidth_load_delta": -0.08,
                    "monthly_burn_change_usd": 9000,
                    "onboarding_quality_delta": 0.02,
                },
            }
        )
        action_index += 1

    if float(finance.get("runway_weeks", 0)) < 34 and not finance.get("last_plan_update"):
        actions.append(
            {
                "tool_name": "finance.plan.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"budget_changes": {"monthly_burn_usd": -18000}},
            }
        )
        action_index += 1

    if float(product.get("onboarding_quality", 0.5)) < 0.7 and int(product.get("major_incidents_open", 0)) <= 1:
        actions.append(
            {
                "tool_name": "product.roadmap.write",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "roadmap_items_delta": -1,
                    "onboarding_quality_delta": 0.07,
                    "major_incidents_delta": 0,
                    "budget_change_monthly_burn_usd": 5000,
                },
            }
        )
        action_index += 1

    if float(customers.get("trust_score", 0.0)) >= 0.7 and float(sales.get("pricing", {}).get("current_price_index", 1.0)) < 1.05:
        actions.append(
            {
                "tool_name": "sales.pricing.propose",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {"price_change_pct": 0.04},
            }
        )
        action_index += 1

    if float(sales.get("weighted_pipeline_usd", 0.0)) < float(finance.get("monthly_burn_usd", 0.0)) * 5.5:
        actions.append(
            {
                "tool_name": "sales.pipeline.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "pipeline_count_delta": 1,
                    "weighted_pipeline_usd_delta": 50000,
                },
            }
        )
        action_index += 1

    if turn_index % 3 == 0 or int(governance.get("board_update_count", 0)) < 2:
        actions.append(
            {
                "tool_name": "board.update",
                "request_id": _next_request_id(turn_index, action_index),
                "arguments": {
                    "summary": "Stabilized incidents first, protected trust, and tightened spend while recovering pipeline quality.",
                    "forecast": {
                        "runway_weeks": finance.get("runway_weeks"),
                        "major_incidents_open": product.get("major_incidents_open"),
                        "trust_score": customers.get("trust_score"),
                    },
                    "asks": ["support temporary incident-focused resource allocation"],
                },
            }
        )
        action_index += 1

    actions.append(
        {
            "tool_name": "sim.advance",
            "request_id": _next_request_id(turn_index, action_index),
            "arguments": {"advance_by": 1, "unit": "week"},
        }
    )
    return actions


def _proposed_actions_for_baseline(session: RuntimeSession, *, baseline_id: str, turn_index: int) -> list[dict]:
    if baseline_id == "heuristic_b2b_operator":
        return _heuristic_b2b_actions(session, turn_index=turn_index)
    if baseline_id == "heuristic_resilient_operator":
        return _heuristic_resilient_actions(session, turn_index=turn_index)
    raise ValueError(f"Unknown baseline_id '{baseline_id}'.")


def run_baseline(*, scenario_path: Path, baseline_id: str, seed: int, max_turns: int | None = None) -> dict:
    if baseline_id not in _BASELINE_IDS:
        raise ValueError(f"Unknown baseline_id '{baseline_id}'. Available baselines: {', '.join(list_baselines())}")

    scenario = load_scenario(scenario_path)
    declared_tools = set(scenario["tools"])
    horizon_length = int(scenario["metadata"]["time_horizon"]["length"])
    total_turns = max_turns if max_turns is not None else horizon_length
    total_turns = max(1, min(total_turns, horizon_length))

    world_state = initialize_world_state(scenario, seed=seed)
    session = RuntimeSession(scenario=scenario, world_state=world_state)
    turns: list[dict] = []
    snapshots: list[dict] = [
        {"snapshot_id": "initial", "kind": "initial", "state": deepcopy(session.world_state)}
    ]
    total_tool_calls = 0

    for turn_index in range(total_turns):
        before_time = session.world_state["sim"]["current_time"]
        observations = session.visible_observations()
        proposed_actions = _proposed_actions_for_baseline(session, baseline_id=baseline_id, turn_index=turn_index)
        events: list[dict] = []
        actions: list[dict] = []

        for tool_call in proposed_actions:
            if tool_call["tool_name"] not in declared_tools:
                continue
            response = execute_tool_call(session, tool_call)
            total_tool_calls += 1
            events.extend(response.get("result", {}).get("events_processed", []))
            actions.append(
                {
                    "tool_name": tool_call["tool_name"],
                    "request_id": tool_call["request_id"],
                    "arguments": tool_call.get("arguments", {}),
                    "response": response,
                    "status": "ok" if response.get("ok", False) else "error",
                }
            )

        after_time = session.world_state["sim"]["current_time"]
        turns.append(
            {
                "turn_index": turn_index,
                "sim_time_before": before_time,
                "sim_time_after": after_time,
                "observations": observations,
                "actions": actions,
                "events": events,
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

    run_id = f"baseline-{uuid4()}"
    evaluation = evaluate_dry_run(scenario=scenario, world_state=session.world_state)
    trace = build_trace(
        scenario=scenario,
        seed=seed,
        run_id=run_id,
        model_id=baseline_id,
        evaluation=evaluation,
        world_state=session.world_state,
    )
    trace["turns"] = turns
    trace["state_snapshots"] = snapshots + [{"snapshot_id": "final", "kind": "final", "state": deepcopy(session.world_state)}]
    trace["runtime"]["total_tool_calls"] = total_tool_calls
    trace["agent"]["provider"] = "baseline"
    trace["agent"]["agent_name"] = baseline_id

    score_report = build_score_report(scenario=scenario, run_id=run_id, evaluation=evaluation)
    return {
        "run_id": run_id,
        "baseline_id": baseline_id,
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


__all__ = ["list_baselines", "run_baseline"]
