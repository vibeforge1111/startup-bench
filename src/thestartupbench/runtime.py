"""Minimal stateful runtime for scripted benchmark execution."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from .observations import project_surfaces
from .primitive_engine import apply_operations, resolve_event_operations
from .runner import recalculate_derived_metrics


def _parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _format_iso8601(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _clamp(value: float, *, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _advance_time(value: str, *, amount: int, unit: str) -> str:
    current = _parse_iso8601(value)
    if unit == "day":
        delta = timedelta(days=amount)
    elif unit == "week":
        delta = timedelta(weeks=amount)
    elif unit == "month":
        delta = timedelta(days=30 * amount)
    elif unit == "quarter":
        delta = timedelta(days=91 * amount)
    else:
        raise ValueError(f"Unsupported advance unit: {unit}")
    return _format_iso8601(current + delta)


def _flatten_world_state(world_state: dict) -> dict[str, object]:
    flat: dict[str, object] = {}
    stack: list[tuple[str, object]] = [("", world_state)]
    while stack:
        prefix, value = stack.pop()
        if isinstance(value, dict):
            for key, nested_value in value.items():
                dotted = f"{prefix}.{key}" if prefix else key
                stack.append((dotted, nested_value))
        else:
            flat[prefix] = value
            flat[prefix.split(".")[-1]] = value
    return flat


@dataclass
class RuntimeSession:
    scenario: dict
    world_state: dict
    notes: list[str] = field(default_factory=list)
    event_log: list[dict] = field(default_factory=list)

    def visible_observations(self) -> list[dict]:
        return project_surfaces(self.scenario["observation_surfaces"], self.world_state)


def _tool_result(tool_name: str, request_id: str, *, result: dict, state_delta_summary: dict | None = None) -> dict:
    return {
        "ok": True,
        "request_id": request_id,
        "tool_name": tool_name,
        "timestamp": _format_iso8601(datetime.now(timezone.utc)),
        "result": deepcopy(result),
        "state_delta_summary": deepcopy(state_delta_summary or {}),
    }


def _process_due_events(session: RuntimeSession) -> list[dict]:
    current_turn = int(session.world_state["sim"]["current_turn"])
    processed_ids = set(session.world_state["sim"].setdefault("processed_event_ids", []))
    emitted: list[dict] = []
    for event in session.scenario.get("event_model", {}).get("scheduled_events", []):
        event_id = event["event_id"]
        if event_id in processed_ids:
            continue
        if int(event.get("at_turn", 0)) > current_turn:
            continue
        operation_deltas = apply_operations(
            session.world_state,
            resolve_event_operations(scenario=session.scenario, event=event),
        )
        visible_event = {
            "event_type": event.get("event_type", "scheduled_event"),
            "event_id": event_id,
            "message": event.get("visible_message", ""),
            "operation_count": len(operation_deltas),
        }
        processed_ids.add(event_id)
        emitted.append(visible_event)
        session.event_log.append(visible_event)
    session.world_state["sim"]["processed_event_ids"] = sorted(processed_ids)
    total_events = len(session.scenario.get("event_model", {}).get("scheduled_events", []))
    session.world_state["sim"]["pending_event_count"] = total_events - len(processed_ids)
    return emitted


def _apply_weekly_business_drift(session: RuntimeSession, *, weeks: int) -> None:
    finance = session.world_state.setdefault("finance", {})
    customers = session.world_state.setdefault("customers", {})
    operations = session.world_state.setdefault("operations", {})
    team = session.world_state.setdefault("team", {})
    risk = session.world_state.setdefault("risk", {})
    product = session.world_state.setdefault("product", {})
    sales = session.world_state.setdefault("sales", {})
    market = session.world_state.setdefault("market", {})
    monthly_revenue = float(finance.get("monthly_revenue_usd", 0))
    monthly_burn = float(finance.get("monthly_burn_usd", 0))
    cash = float(finance.get("cash_usd", 0))
    cash += ((monthly_revenue - monthly_burn) / 4.0) * weeks
    finance["cash_usd"] = round(cash, 2)

    paying_accounts = int(customers.get("paying_accounts", 0))
    churn = float(customers.get("monthly_churn_rate", 0))
    accounts_lost = int(round(paying_accounts * (churn / 4.0) * weeks))
    customers["paying_accounts"] = max(0, paying_accounts - accounts_lost)
    segment_states = customers.get("segments", [])
    if isinstance(segment_states, list):
        for segment in segment_states:
            if not isinstance(segment, dict):
                continue
            segment_churn = float(segment.get("monthly_churn_rate", churn))
            segment_accounts = int(segment.get("accounts", 0))
            segment_accounts_lost = int(round(segment_accounts * (segment_churn / 4.0) * weeks))
            segment["accounts"] = max(0, segment_accounts - segment_accounts_lost)

    support_backlog = float(operations.get("support_backlog", 0))
    if support_backlog > 40:
        customers["trust_score"] = round(
            _clamp(float(customers.get("trust_score", 0.7)) - min(0.02 * weeks, support_backlog / 3000.0), minimum=0.0, maximum=1.0),
            4,
        )
        customers["monthly_churn_rate"] = round(
            _clamp(float(customers.get("monthly_churn_rate", 0.0)) + min(0.003 * weeks, support_backlog / 20000.0), minimum=0.0, maximum=1.0),
            4,
        )

    morale = float(team.get("morale", 0.7))
    if morale < 0.55:
        product["onboarding_quality"] = round(
            _clamp(float(product.get("onboarding_quality", 0.7)) - (0.01 * weeks), minimum=0.0, maximum=1.0),
            4,
        )
        sales["weighted_pipeline_usd"] = round(max(0.0, float(sales.get("weighted_pipeline_usd", 0)) - (15000 * weeks)), 2)

    attrition_risk = float(team.get("attrition_risk", 0.0))
    if attrition_risk > 0.6:
        customers["trust_score"] = round(
            _clamp(float(customers.get("trust_score", 0.7)) - (0.01 * weeks), minimum=0.0, maximum=1.0),
            4,
        )

    competitor_pressure = float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.3)))
    pricing_pressure = float(market.get("pricing_pressure_index", market.get("pricing_pressure", 0.2)))
    demand_index = float(market.get("demand_index", 0.85))
    if competitor_pressure > 0.65:
        sales["weighted_pipeline_usd"] = round(
            max(0.0, float(sales.get("weighted_pipeline_usd", 0.0)) - ((15000 + 18000 * pricing_pressure) * weeks)),
            2,
        )
        customers["trust_score"] = round(
            _clamp(float(customers.get("trust_score", 0.7)) - (0.006 * weeks), minimum=0.0, maximum=1.0),
            4,
        )
    if demand_index < 0.72:
        revenue_drag = (0.78 - max(0.0, demand_index)) * 18000 * weeks
        finance["monthly_revenue_usd"] = round(max(0.0, float(finance.get("monthly_revenue_usd", 0.0)) - revenue_drag), 2)
        sales["weighted_pipeline_usd"] = round(max(0.0, float(sales.get("weighted_pipeline_usd", 0.0)) - (20000 * weeks)), 2)

    if isinstance(segment_states, list):
        for segment in segment_states:
            if not isinstance(segment, dict):
                continue
            segment_competitor_pressure = float(segment.get("competitor_pressure_index", competitor_pressure))
            segment_support_load = float(segment.get("support_load_index", 0.3))
            segment["competitor_pressure_index"] = round(
                _clamp(segment_competitor_pressure, minimum=0.0, maximum=1.0),
                4,
            )
            if segment_competitor_pressure > 0.65:
                segment["monthly_churn_rate"] = round(
                    _clamp(float(segment.get("monthly_churn_rate", churn)) + (0.0025 * weeks), minimum=0.0, maximum=1.0),
                    4,
                )
            if support_backlog > 40:
                segment["support_load_index"] = round(
                    _clamp(segment_support_load + min(0.02 * weeks, support_backlog / 2500.0), minimum=0.0, maximum=1.0),
                    4,
                )
            segment["trust_score"] = round(
                _clamp(float(segment.get("trust_score", customers.get("trust_score", 0.7))), minimum=0.0, maximum=1.0),
                4,
            )

    hiring = team.setdefault("hiring", {})
    open_roles = int(hiring.get("open_roles", team.get("open_roles", 0)))
    critical_roles_open = int(hiring.get("critical_roles_open", 0))
    hiring_capacity_index = float(hiring.get("hiring_capacity_index", 0.0))
    if open_roles > 0 and float(team.get("bandwidth_load", 0.7)) > 0.78:
        team["morale"] = round(
            _clamp(float(team.get("morale", 0.7)) - (0.008 * weeks) - (0.004 * critical_roles_open), minimum=0.0, maximum=1.0),
            4,
        )
        team["attrition_risk"] = round(
            _clamp(float(team.get("attrition_risk", 0.2)) + (0.01 * weeks), minimum=0.0, maximum=1.0),
            4,
        )
        operations["support_backlog"] = round(max(0.0, float(operations.get("support_backlog", 0.0)) + ((2 + critical_roles_open) * weeks)), 2)
    if open_roles > 0 and hiring_capacity_index < 0.4:
        sales["weighted_pipeline_usd"] = round(max(0.0, float(sales.get("weighted_pipeline_usd", 0.0)) - (12000 * weeks)), 2)

    if float(team.get("delivery_capacity_index", 0.6)) < 0.45:
        product["onboarding_quality"] = round(
            _clamp(float(product.get("onboarding_quality", 0.7)) - (0.012 * weeks), minimum=0.0, maximum=1.0),
            4,
        )

    regulatory_pressure = float(risk.get("regulatory_pressure", 0.0))
    if regulatory_pressure > 0.65:
        sales["weighted_pipeline_usd"] = round(max(0.0, float(sales.get("weighted_pipeline_usd", 0)) - (20000 * weeks)), 2)
        customers["trust_score"] = round(
            _clamp(float(customers.get("trust_score", 0.7)) - (0.012 * weeks), minimum=0.0, maximum=1.0),
            4,
        )

    treasury_concentration = float(finance.get("treasury_concentration", 0.0))
    counterparty_risk = float(risk.get("counterparty_risk", 0.0))
    if treasury_concentration > 0.85 and counterparty_risk > 0.75:
        finance["restricted_cash_usd"] = round(
            max(float(finance.get("restricted_cash_usd", 0.0)), float(finance.get("cash_usd", 0.0)) * 0.12),
            2,
        )


def _build_metric_report(session: RuntimeSession) -> dict:
    finance = session.world_state.get("finance", {})
    customers = session.world_state.get("customers", {})
    growth = session.world_state.get("growth", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    operations = session.world_state.get("operations", {})
    product = session.world_state.get("product", {})
    team = session.world_state.get("team", {})
    risk = session.world_state.get("risk", {})
    market = session.world_state.get("market", {})
    sim = session.world_state.get("sim", {})
    hiring = team.get("hiring", {})

    alerts = []
    if float(finance.get("runway_weeks", 0)) < 20:
        alerts.append("runway_below_20_weeks")
    if float(finance.get("runway_weeks", 0)) < 18 and not finance.get("last_raise_plan"):
        alerts.append("fundraising_action_recommended")
    if float(customers.get("monthly_churn_rate", 0)) > 0.05:
        alerts.append("churn_above_5pct")
    if float(customers.get("trust_score", 1.0)) < 0.6:
        alerts.append("trust_score_below_0_6")
    if float(operations.get("support_backlog", 0)) > 50:
        alerts.append("support_backlog_above_50")
    if float(team.get("morale", 1.0)) < 0.55:
        alerts.append("morale_below_0_55")
    if float(risk.get("regulatory_pressure", 0.0)) > 0.65:
        alerts.append("regulatory_pressure_high")
    if float(finance.get("treasury_concentration", 0.0)) > 0.8:
        alerts.append("treasury_concentration_high")
    if int(hiring.get("critical_roles_open", 0)) > 0:
        alerts.append("critical_roles_open")
    if float(market.get("competitor_pressure_index", market.get("competitor_pressure", 0.0))) > 0.7:
        alerts.append("competitor_pressure_high")
    if float(market.get("demand_index", 1.0)) < 0.72:
        alerts.append("market_demand_softening")
    if int(sim.get("pending_event_count", 0)) > 0:
        alerts.append("pending_scheduled_events")

    return {
        "headline": {
            "cash_usd": finance.get("cash_usd"),
            "liquid_cash_usd": finance.get("liquid_cash_usd"),
            "runway_weeks": finance.get("runway_weeks"),
            "monthly_revenue_usd": finance.get("monthly_revenue_usd"),
            "net_burn_usd": finance.get("net_burn_usd"),
        },
        "finance": {
            "treasury_concentration": finance.get("treasury_concentration"),
            "restricted_cash_usd": finance.get("restricted_cash_usd", 0.0),
            "dilution_index": finance.get("dilution_index", 0.0),
            "financing_events_count": finance.get("financing_events_count", 0),
        },
        "customers": {
            "paying_accounts": customers.get("paying_accounts"),
            "monthly_churn_rate": customers.get("monthly_churn_rate"),
            "trust_score": customers.get("trust_score"),
            "health_index": customers.get("health_index"),
            "segment_mix_index": customers.get("segment_mix_index"),
        },
        "sales": {
            "pipeline_count": sales.get("pipeline_count"),
            "weighted_pipeline_usd": sales.get("weighted_pipeline_usd"),
            "pricing": sales.get("pricing", {}),
        },
        "growth": {
            "activation_index": growth.get("activation_index"),
            "experiment_count": growth.get("experiment_count", 0),
            "active_experiment_count": growth.get("active_experiment_count", 0),
            "launch_count": growth.get("launch_count", product.get("launch_count", 0)),
            "latest_experiment": growth.get("latest_experiment"),
        },
        "governance": {
            "board_update_count": governance.get("board_update_count", 0),
        },
        "operations": {
            "support_backlog": operations.get("support_backlog", 0),
            "support_sla_breach_risk": operations.get("support_sla_breach_risk", 0.0),
        },
        "team": {
            "morale": team.get("morale"),
            "attrition_risk": team.get("attrition_risk"),
            "bandwidth_load": team.get("bandwidth_load"),
            "delivery_capacity_index": team.get("delivery_capacity_index"),
            "headcount": team.get("headcount"),
            "hiring": {
                "open_roles": hiring.get("open_roles", 0),
                "critical_roles_open": hiring.get("critical_roles_open", 0),
                "hiring_capacity_index": hiring.get("hiring_capacity_index", 0.0),
                "offers_out": hiring.get("offers_out", 0),
            },
        },
        "risk": {
            "regulatory_pressure": risk.get("regulatory_pressure", 0.0),
            "active_legal_matters": risk.get("active_legal_matters", 0),
            "counterparty_risk": risk.get("counterparty_risk", 0.0),
        },
        "market": {
            "competitor_pressure_index": market.get("competitor_pressure_index", market.get("competitor_pressure")),
            "pricing_pressure_index": market.get("pricing_pressure_index", market.get("pricing_pressure")),
            "demand_index": market.get("demand_index"),
            "latest_market_note": market.get("latest_market_note"),
        },
        "alerts": alerts,
    }


def execute_tool_call(session: RuntimeSession, tool_call: dict) -> dict:
    tool_name = tool_call["tool_name"]
    request_id = tool_call["request_id"]
    arguments = tool_call.get("arguments", {})

    if tool_name == "metrics.query":
        metric_ids = arguments.get("metric_ids", [])
        flat = _flatten_world_state(session.world_state)
        result = {"items": {metric_id: flat.get(metric_id) for metric_id in metric_ids}}
        return _tool_result(tool_name, request_id, result=result)

    if tool_name == "metrics.report":
        return _tool_result(tool_name, request_id, result={"report": _build_metric_report(session)})

    if tool_name == "product.roadmap.read":
        return _tool_result(tool_name, request_id, result={"product": deepcopy(session.world_state["product"])})

    if tool_name == "product.roadmap.write":
        product = session.world_state.setdefault("product", {})
        finance = session.world_state.setdefault("finance", {})
        roadmap_items_delta = int(arguments.get("roadmap_items_delta", 0))
        onboarding_quality_delta = float(arguments.get("onboarding_quality_delta", 0))
        major_incidents_delta = int(arguments.get("major_incidents_delta", 0))
        budget_change = float(arguments.get("budget_change_monthly_burn_usd", 0))
        operations = [
            {"op": "increment", "path": "product.roadmap_items", "value": roadmap_items_delta},
            {"op": "clamp", "path": "product.roadmap_items", "min": 0},
            {"op": "increment", "path": "product.onboarding_quality", "value": onboarding_quality_delta},
            {"op": "clamp", "path": "product.onboarding_quality", "min": 0.0, "max": 1.0},
            {"op": "increment", "path": "product.major_incidents_open", "value": major_incidents_delta},
            {"op": "clamp", "path": "product.major_incidents_open", "min": 0},
        ]
        if budget_change:
            operations.append({"op": "increment", "path": "finance.monthly_burn_usd", "value": budget_change})
        apply_operations(session.world_state, operations)
        product["onboarding_quality"] = round(float(product.get("onboarding_quality", 0.5)), 4)
        if "monthly_burn_usd" in finance:
            finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0)), 2)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={"product": deepcopy(product), "finance": deepcopy(finance)},
            state_delta_summary={
                "product.roadmap_items": product["roadmap_items"],
                "product.onboarding_quality": product["onboarding_quality"],
                "product.major_incidents_open": product["major_incidents_open"],
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
            },
        )

    if tool_name == "product.launch":
        product = session.world_state.setdefault("product", {})
        finance = session.world_state.setdefault("finance", {})
        customers = session.world_state.setdefault("customers", {})
        sales = session.world_state.setdefault("sales", {})
        operations = session.world_state.setdefault("operations", {})
        market = session.world_state.setdefault("market", {})
        growth = session.world_state.setdefault("growth", {})

        launch_name = str(arguments.get("launch_name", f"launch_turn_{session.world_state['sim']['current_turn']}"))
        monthly_revenue_delta_usd = float(arguments.get("monthly_revenue_delta_usd", 0.0))
        pipeline_count_delta = int(arguments.get("pipeline_count_delta", 0))
        weighted_pipeline_usd_delta = float(arguments.get("weighted_pipeline_usd_delta", 0.0))
        demand_index_delta = float(arguments.get("demand_index_delta", 0.0))
        trust_delta = float(arguments.get("trust_delta", 0.0))
        onboarding_quality_delta = float(arguments.get("onboarding_quality_delta", 0.0))
        support_backlog_delta = float(arguments.get("support_backlog_delta", 0.0))
        monthly_burn_change_usd = float(arguments.get("monthly_burn_change_usd", 0.0))
        major_incidents_delta = int(arguments.get("major_incidents_delta", 0))
        activation_delta = float(arguments.get("activation_delta", 0.0))

        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "product.launch_count", "value": 1},
                {"op": "increment", "path": "growth.launch_count", "value": 1},
                {"op": "increment", "path": "finance.monthly_revenue_usd", "value": monthly_revenue_delta_usd},
                {"op": "increment", "path": "sales.pipeline_count", "value": pipeline_count_delta},
                {"op": "clamp", "path": "sales.pipeline_count", "min": 0},
                {"op": "increment", "path": "sales.weighted_pipeline_usd", "value": weighted_pipeline_usd_delta},
                {"op": "clamp", "path": "sales.weighted_pipeline_usd", "min": 0.0},
                {"op": "increment", "path": "market.demand_index", "value": demand_index_delta},
                {"op": "clamp", "path": "market.demand_index", "min": 0.0, "max": 1.5},
                {"op": "increment", "path": "customers.trust_score", "value": trust_delta},
                {"op": "clamp", "path": "customers.trust_score", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "product.onboarding_quality", "value": onboarding_quality_delta},
                {"op": "clamp", "path": "product.onboarding_quality", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "operations.support_backlog", "value": support_backlog_delta},
                {"op": "clamp", "path": "operations.support_backlog", "min": 0.0},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": monthly_burn_change_usd},
                {"op": "increment", "path": "product.major_incidents_open", "value": major_incidents_delta},
                {"op": "clamp", "path": "product.major_incidents_open", "min": 0},
                {"op": "increment", "path": "growth.activation_index", "value": activation_delta},
                {"op": "clamp", "path": "growth.activation_index", "min": 0.0, "max": 1.0},
            ],
        )
        product["last_launch"] = {
            "launch_name": launch_name,
            "timestamp": session.world_state["sim"]["current_time"],
        }
        finance["monthly_revenue_usd"] = round(float(finance.get("monthly_revenue_usd", 0.0)), 2)
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0.0)), 2)
        customers["trust_score"] = round(float(customers.get("trust_score", 0.0)), 4)
        product["onboarding_quality"] = round(float(product.get("onboarding_quality", 0.0)), 4)
        market["demand_index"] = round(float(market.get("demand_index", 0.0)), 4)
        growth["activation_index"] = round(float(growth.get("activation_index", 0.0)), 4)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "launch_state": {
                    "launch_name": launch_name,
                    "launch_count": product.get("launch_count", 0),
                    "monthly_revenue_usd": finance.get("monthly_revenue_usd"),
                    "weighted_pipeline_usd": sales.get("weighted_pipeline_usd"),
                    "support_backlog": operations.get("support_backlog", 0),
                    "activation_index": growth.get("activation_index", 0.0),
                }
            },
            state_delta_summary={
                "product.launch_count": product.get("launch_count", 0),
                "growth.launch_count": growth.get("launch_count", 0),
                "finance.monthly_revenue_usd": finance.get("monthly_revenue_usd"),
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
                "sales.weighted_pipeline_usd": sales.get("weighted_pipeline_usd"),
                "market.demand_index": market.get("demand_index"),
            },
        )

    if tool_name == "finance.plan.read":
        return _tool_result(tool_name, request_id, result={"finance": deepcopy(session.world_state["finance"])})

    if tool_name == "finance.plan.write":
        budget_changes = arguments.get("budget_changes", {})
        state_delta = {}
        for key, delta in budget_changes.items():
            apply_operations(session.world_state, [{"op": "increment", "path": f"finance.{key}", "value": float(delta)}])
            session.world_state["finance"][key] = round(float(session.world_state["finance"].get(key, 0)), 2)
            state_delta[f"finance.{key}"] = session.world_state["finance"][key]
        session.world_state["finance"]["last_plan_update"] = {
            "budget_changes": budget_changes,
        }
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={"finance": deepcopy(session.world_state["finance"])},
            state_delta_summary=state_delta,
        )

    if tool_name == "finance.raise.propose":
        finance = session.world_state.setdefault("finance", {})
        risk = session.world_state.setdefault("risk", {})
        raise_amount_usd = max(0.0, float(arguments.get("raise_amount_usd", 0.0)))
        dilution_pct = _clamp(float(arguments.get("dilution_pct", 0.1)), minimum=0.0, maximum=1.0)
        monthly_burn_change_usd = float(arguments.get("monthly_burn_change_usd", 0.0))
        financing_risk_reduction = max(0.0, float(arguments.get("financing_risk_reduction", 0.2)))
        trust_delta = float(arguments.get("trust_delta", 0.0))
        transaction_cost_usd = max(0.0, float(arguments.get("transaction_cost_usd", raise_amount_usd * 0.02)))

        net_cash_added = max(0.0, raise_amount_usd - transaction_cost_usd)
        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "finance.cash_usd", "value": net_cash_added},
                {"op": "increment", "path": "finance.dilution_index", "value": dilution_pct},
                {"op": "increment", "path": "finance.financing_events_count", "value": 1},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": monthly_burn_change_usd},
                {"op": "increment", "path": "risk.financing_pressure", "value": -financing_risk_reduction},
                {"op": "clamp", "path": "risk.financing_pressure", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "customers.trust_score", "value": trust_delta},
                {"op": "clamp", "path": "customers.trust_score", "min": 0.0, "max": 1.0}
            ],
        )
        finance["cash_usd"] = round(float(finance.get("cash_usd", 0.0)), 2)
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0.0)), 2)
        finance["dilution_index"] = round(float(finance.get("dilution_index", 0.0)), 4)
        risk["financing_pressure"] = round(float(risk.get("financing_pressure", 0.0)), 4)
        finance["last_raise_plan"] = {
            "raise_amount_usd": round(raise_amount_usd, 2),
            "transaction_cost_usd": round(transaction_cost_usd, 2),
            "net_cash_added_usd": round(net_cash_added, 2),
            "dilution_pct": round(dilution_pct, 4),
        }
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "financing": {
                    "cash_usd": finance.get("cash_usd"),
                    "liquid_cash_usd": finance.get("liquid_cash_usd"),
                    "runway_weeks": finance.get("runway_weeks"),
                    "dilution_index": finance.get("dilution_index"),
                    "financing_pressure": risk.get("financing_pressure", 0.0),
                }
            },
            state_delta_summary={
                "finance.cash_usd": finance.get("cash_usd"),
                "finance.runway_weeks": finance.get("runway_weeks"),
                "finance.dilution_index": finance.get("dilution_index"),
                "risk.financing_pressure": risk.get("financing_pressure", 0.0),
            },
        )

    if tool_name == "finance.treasury.read":
        finance = session.world_state.setdefault("finance", {})
        risk = session.world_state.setdefault("risk", {})
        return _tool_result(
            tool_name,
            request_id,
            result={
                "treasury": {
                    "cash_usd": finance.get("cash_usd"),
                    "liquid_cash_usd": finance.get("liquid_cash_usd"),
                    "restricted_cash_usd": finance.get("restricted_cash_usd", 0.0),
                    "treasury_concentration": finance.get("treasury_concentration", 0.0),
                    "counterparty_risk": risk.get("counterparty_risk", 0.0),
                }
            },
        )

    if tool_name == "finance.treasury.rebalance":
        finance = session.world_state.setdefault("finance", {})
        target_concentration = _clamp(float(arguments.get("target_concentration", 0.5)), minimum=0.0, maximum=1.0)
        rebalance_cost_usd = max(0.0, float(arguments.get("rebalance_cost_usd", 8000)))
        previous_concentration = float(finance.get("treasury_concentration", 0.0))
        finance["treasury_concentration"] = round(target_concentration, 4)
        finance["cash_usd"] = round(max(0.0, float(finance.get("cash_usd", 0.0)) - rebalance_cost_usd), 2)
        finance["restricted_cash_usd"] = round(
            max(0.0, float(finance.get("restricted_cash_usd", 0.0)) * target_concentration),
            2,
        )
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "treasury": {
                    "treasury_concentration": finance.get("treasury_concentration"),
                    "cash_usd": finance.get("cash_usd"),
                    "liquid_cash_usd": finance.get("liquid_cash_usd"),
                    "previous_concentration": round(previous_concentration, 4),
                }
            },
            state_delta_summary={
                "finance.treasury_concentration": finance.get("treasury_concentration"),
                "finance.cash_usd": finance.get("cash_usd"),
                "finance.liquid_cash_usd": finance.get("liquid_cash_usd"),
            },
        )

    if tool_name == "sales.pipeline.read":
        return _tool_result(tool_name, request_id, result={"sales": deepcopy(session.world_state["sales"])})

    if tool_name == "sales.pipeline.update":
        sales = session.world_state.setdefault("sales", {})
        finance = session.world_state.setdefault("finance", {})
        pipeline_count_delta = int(arguments.get("pipeline_count_delta", 0))
        weighted_pipeline_usd_delta = float(arguments.get("weighted_pipeline_usd_delta", 0))
        closed_won_revenue_delta = float(arguments.get("closed_won_revenue_delta_usd", 0))
        operations = [
            {"op": "increment", "path": "sales.pipeline_count", "value": pipeline_count_delta},
            {"op": "clamp", "path": "sales.pipeline_count", "min": 0},
            {"op": "increment", "path": "sales.weighted_pipeline_usd", "value": weighted_pipeline_usd_delta},
        ]
        if closed_won_revenue_delta:
            operations.append({"op": "increment", "path": "finance.monthly_revenue_usd", "value": closed_won_revenue_delta})
        apply_operations(session.world_state, operations)
        sales["weighted_pipeline_usd"] = round(float(sales.get("weighted_pipeline_usd", 0)), 2)
        if "monthly_revenue_usd" in finance:
            finance["monthly_revenue_usd"] = round(float(finance.get("monthly_revenue_usd", 0)), 2)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={"sales": deepcopy(sales), "finance": deepcopy(finance)},
            state_delta_summary={
                "sales.pipeline_count": sales["pipeline_count"],
                "sales.weighted_pipeline_usd": sales["weighted_pipeline_usd"],
                "finance.monthly_revenue_usd": finance.get("monthly_revenue_usd"),
            },
        )

    if tool_name == "sales.pricing.propose":
        change_pct = float(arguments.get("price_change_pct", 0))
        max_auto = float(session.world_state.get("policy", {}).get("max_auto_price_increase_pct", 0.2))
        if change_pct > max_auto:
            return {
                "ok": False,
                "request_id": request_id,
                "tool_name": tool_name,
                "timestamp": _format_iso8601(datetime.now(timezone.utc)),
                "result": {},
                "error_code": "approval_required",
                "error_message": f"price_change_pct {change_pct} exceeds auto-approval limit {max_auto}",
                "state_delta_summary": {},
            }

        pricing = session.world_state.setdefault("sales", {}).setdefault("pricing", {"current_price_index": 1.0})
        pricing["current_price_index"] = round(float(pricing.get("current_price_index", 1.0)) * (1.0 + change_pct), 4)
        finance = session.world_state.setdefault("finance", {})
        customers = session.world_state.setdefault("customers", {})
        finance["monthly_revenue_usd"] = round(float(finance.get("monthly_revenue_usd", 0)) * (1.0 + change_pct * 0.55), 2)
        customers["monthly_churn_rate"] = round(float(customers.get("monthly_churn_rate", 0)) + max(0.0, change_pct) * 0.01, 4)
        customers["trust_score"] = round(max(0.0, float(customers.get("trust_score", 0.7)) - max(0.0, change_pct) * 0.08), 4)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={"pricing": deepcopy(pricing), "finance": deepcopy(finance), "customers": deepcopy(customers)},
            state_delta_summary={
                "sales.pricing.current_price_index": pricing["current_price_index"],
                "finance.monthly_revenue_usd": finance["monthly_revenue_usd"],
                "customers.monthly_churn_rate": customers["monthly_churn_rate"],
                "customers.trust_score": customers["trust_score"],
            },
        )

    if tool_name == "ops.incident.read":
        product = session.world_state.setdefault("product", {})
        operations = session.world_state.setdefault("operations", {})
        customers = session.world_state.setdefault("customers", {})
        return _tool_result(
            tool_name,
            request_id,
            result={
                "incident_state": {
                    "major_incidents_open": product.get("major_incidents_open", 0),
                    "trust_score": customers.get("trust_score"),
                    "monthly_churn_rate": customers.get("monthly_churn_rate"),
                    "incident_response_count": operations.get("incident_response_count", 0),
                    "last_incident_response": deepcopy(operations.get("last_incident_response")),
                }
            },
        )

    if tool_name == "ops.support.read":
        operations = session.world_state.setdefault("operations", {})
        customers = session.world_state.setdefault("customers", {})
        return _tool_result(
            tool_name,
            request_id,
            result={
                "support_state": {
                    "support_backlog": operations.get("support_backlog", 0),
                    "support_sla_breach_risk": operations.get("support_sla_breach_risk", 0.0),
                    "trust_score": customers.get("trust_score"),
                    "monthly_churn_rate": customers.get("monthly_churn_rate"),
                }
            },
        )

    if tool_name == "ops.support.resolve":
        operations = session.world_state.setdefault("operations", {})
        customers = session.world_state.setdefault("customers", {})
        finance = session.world_state.setdefault("finance", {})
        backlog_reduction = max(0, int(arguments.get("backlog_reduction", 12)))
        sla_risk_reduction = max(0.0, float(arguments.get("sla_risk_reduction", 0.12)))
        trust_recovery = max(0.0, float(arguments.get("trust_recovery", 0.03)))
        churn_reduction = max(0.0, float(arguments.get("churn_reduction", 0.004)))
        burn_increase = max(0.0, float(arguments.get("monthly_burn_increase_usd", 7000)))
        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "operations.support_backlog", "value": -backlog_reduction},
                {"op": "clamp", "path": "operations.support_backlog", "min": 0},
                {"op": "increment", "path": "operations.support_sla_breach_risk", "value": -sla_risk_reduction},
                {"op": "clamp", "path": "operations.support_sla_breach_risk", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "customers.trust_score", "value": trust_recovery},
                {"op": "clamp", "path": "customers.trust_score", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "customers.monthly_churn_rate", "value": -churn_reduction},
                {"op": "clamp", "path": "customers.monthly_churn_rate", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": burn_increase},
                {"op": "increment", "path": "operations.support_actions_taken", "value": 1},
            ],
        )
        operations["support_sla_breach_risk"] = round(float(operations.get("support_sla_breach_risk", 0.0)), 4)
        customers["trust_score"] = round(float(customers.get("trust_score", 0.0)), 4)
        customers["monthly_churn_rate"] = round(float(customers.get("monthly_churn_rate", 0.0)), 4)
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0.0)), 2)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "support_state": {
                    "support_backlog": operations.get("support_backlog", 0),
                    "support_sla_breach_risk": operations.get("support_sla_breach_risk", 0.0),
                    "trust_score": customers.get("trust_score"),
                    "monthly_churn_rate": customers.get("monthly_churn_rate"),
                }
            },
            state_delta_summary={
                "operations.support_backlog": operations.get("support_backlog", 0),
                "operations.support_sla_breach_risk": operations.get("support_sla_breach_risk", 0.0),
                "customers.trust_score": customers.get("trust_score"),
                "customers.monthly_churn_rate": customers.get("monthly_churn_rate"),
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
            },
        )

    if tool_name == "ops.incident.respond":
        product = session.world_state.setdefault("product", {})
        customers = session.world_state.setdefault("customers", {})
        finance = session.world_state.setdefault("finance", {})
        operations = session.world_state.setdefault("operations", {})
        response_plan = {
            "incident_reduction": int(arguments.get("incident_reduction", 1)),
            "trust_recovery": float(arguments.get("trust_recovery", 0.05)),
            "churn_reduction": float(arguments.get("churn_reduction", 0.008)),
            "monthly_burn_increase_usd": float(arguments.get("monthly_burn_increase_usd", 12000)),
        }
        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "product.major_incidents_open", "value": -response_plan["incident_reduction"]},
                {"op": "clamp", "path": "product.major_incidents_open", "min": 0},
                {"op": "increment", "path": "customers.trust_score", "value": response_plan["trust_recovery"]},
                {"op": "clamp", "path": "customers.trust_score", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "customers.monthly_churn_rate", "value": -response_plan["churn_reduction"]},
                {"op": "clamp", "path": "customers.monthly_churn_rate", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": response_plan["monthly_burn_increase_usd"]},
                {"op": "increment", "path": "operations.incident_response_count", "value": 1},
            ],
        )
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0)), 2)
        customers["trust_score"] = round(float(customers.get("trust_score", 0)), 4)
        customers["monthly_churn_rate"] = round(float(customers.get("monthly_churn_rate", 0)), 4)
        operations["last_incident_response"] = response_plan
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "incident_state": {
                    "major_incidents_open": product.get("major_incidents_open", 0),
                    "trust_score": customers.get("trust_score"),
                    "monthly_churn_rate": customers.get("monthly_churn_rate"),
                    "monthly_burn_usd": finance.get("monthly_burn_usd"),
                    "incident_response_count": operations.get("incident_response_count", 0),
                }
            },
            state_delta_summary={
                "product.major_incidents_open": product.get("major_incidents_open", 0),
                "customers.trust_score": customers.get("trust_score"),
                "customers.monthly_churn_rate": customers.get("monthly_churn_rate"),
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
                "operations.incident_response_count": operations.get("incident_response_count", 0),
            },
        )

    if tool_name == "people.org.read":
        team = session.world_state.setdefault("team", {})
        return _tool_result(
            tool_name,
            request_id,
            result={
                "team_state": {
                    "morale": team.get("morale", 0.7),
                    "attrition_risk": team.get("attrition_risk", 0.2),
                    "bandwidth_load": team.get("bandwidth_load", 0.6),
                    "headcount": team.get("headcount"),
                }
            },
        )

    if tool_name == "people.org.propose":
        team = session.world_state.setdefault("team", {})
        proposal = {
            "summary": arguments.get("summary", ""),
            "target_function": arguments.get("target_function"),
            "expected_morale_delta": float(arguments.get("expected_morale_delta", 0.0)),
            "expected_bandwidth_load_delta": float(arguments.get("expected_bandwidth_load_delta", 0.0)),
            "expected_monthly_burn_change_usd": float(arguments.get("expected_monthly_burn_change_usd", 0.0)),
            "timestamp": session.world_state["sim"]["current_time"],
        }
        team["last_org_proposal"] = proposal
        team["org_proposal_count"] = int(team.get("org_proposal_count", 0)) + 1
        return _tool_result(
            tool_name,
            request_id,
            result={"proposal": deepcopy(proposal)},
            state_delta_summary={
                "team.org_proposal_count": team.get("org_proposal_count", 0),
                "team.last_org_proposal": "updated",
            },
        )

    if tool_name == "people.org.adjust":
        team = session.world_state.setdefault("team", {})
        finance = session.world_state.setdefault("finance", {})
        product = session.world_state.setdefault("product", {})
        morale_delta = float(arguments.get("morale_delta", 0.06))
        attrition_risk_delta = float(arguments.get("attrition_risk_delta", -0.08))
        bandwidth_load_delta = float(arguments.get("bandwidth_load_delta", -0.07))
        burn_delta = float(arguments.get("monthly_burn_change_usd", 9000))
        onboarding_delta = float(arguments.get("onboarding_quality_delta", 0.03))
        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "team.morale", "value": morale_delta},
                {"op": "clamp", "path": "team.morale", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "team.attrition_risk", "value": attrition_risk_delta},
                {"op": "clamp", "path": "team.attrition_risk", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "team.bandwidth_load", "value": bandwidth_load_delta},
                {"op": "clamp", "path": "team.bandwidth_load", "min": 0.0, "max": 1.5},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": burn_delta},
                {"op": "increment", "path": "product.onboarding_quality", "value": onboarding_delta},
                {"op": "clamp", "path": "product.onboarding_quality", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "team.org_changes_count", "value": 1},
            ],
        )
        team["morale"] = round(float(team.get("morale", 0.0)), 4)
        team["attrition_risk"] = round(float(team.get("attrition_risk", 0.0)), 4)
        team["bandwidth_load"] = round(float(team.get("bandwidth_load", 0.0)), 4)
        product["onboarding_quality"] = round(float(product.get("onboarding_quality", 0.0)), 4)
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0.0)), 2)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "team_state": {
                    "morale": team.get("morale"),
                    "attrition_risk": team.get("attrition_risk"),
                    "bandwidth_load": team.get("bandwidth_load"),
                    "onboarding_quality": product.get("onboarding_quality"),
                }
            },
            state_delta_summary={
                "team.morale": team.get("morale"),
                "team.attrition_risk": team.get("attrition_risk"),
                "team.bandwidth_load": team.get("bandwidth_load"),
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
                "product.onboarding_quality": product.get("onboarding_quality"),
            },
        )

    if tool_name == "people.hiring.read":
        team = session.world_state.setdefault("team", {})
        hiring = team.setdefault("hiring", {})
        return _tool_result(
            tool_name,
            request_id,
            result={
                "hiring_state": {
                    "headcount": team.get("headcount", 0),
                    "open_roles": hiring.get("open_roles", team.get("open_roles", 0)),
                    "critical_roles_open": hiring.get("critical_roles_open", 0),
                    "sourced_candidates": hiring.get("sourced_candidates", 0),
                    "onsite_candidates": hiring.get("onsite_candidates", 0),
                    "offers_out": hiring.get("offers_out", 0),
                    "hiring_capacity_index": hiring.get("hiring_capacity_index", 0.0),
                    "time_to_fill_weeks": hiring.get("time_to_fill_weeks", 8),
                }
            },
        )

    if tool_name == "people.hiring.update":
        team = session.world_state.setdefault("team", {})
        hiring = team.setdefault("hiring", {})
        finance = session.world_state.setdefault("finance", {})
        operations = session.world_state.setdefault("operations", {})
        product = session.world_state.setdefault("product", {})

        sourced_candidates_delta = int(arguments.get("sourced_candidates_delta", 0))
        onsite_candidates_delta = int(arguments.get("onsite_candidates_delta", 0))
        offers_out_delta = int(arguments.get("offers_out_delta", 0))
        accepted_hires = max(0, int(arguments.get("accepted_hires", 0)))
        open_roles_delta = int(arguments.get("open_roles_delta", 0))
        critical_roles_delta = int(arguments.get("critical_roles_delta", 0))
        recruiting_spend = max(0.0, float(arguments.get("monthly_burn_change_usd", accepted_hires * 14000 + max(0, sourced_candidates_delta) * 900)))
        morale_delta = float(arguments.get("morale_delta", 0.015 * accepted_hires))
        bandwidth_delta = float(arguments.get("bandwidth_load_delta", -0.05 * accepted_hires))
        support_backlog_delta = float(arguments.get("support_backlog_delta", -3 * accepted_hires))
        onboarding_delta = float(arguments.get("onboarding_quality_delta", 0.015 * accepted_hires))

        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "team.hiring.open_roles", "value": open_roles_delta - accepted_hires},
                {"op": "clamp", "path": "team.hiring.open_roles", "min": 0},
                {"op": "increment", "path": "team.hiring.critical_roles_open", "value": critical_roles_delta - accepted_hires},
                {"op": "clamp", "path": "team.hiring.critical_roles_open", "min": 0},
                {"op": "increment", "path": "team.hiring.sourced_candidates", "value": sourced_candidates_delta - accepted_hires},
                {"op": "clamp", "path": "team.hiring.sourced_candidates", "min": 0},
                {"op": "increment", "path": "team.hiring.onsite_candidates", "value": onsite_candidates_delta - accepted_hires},
                {"op": "clamp", "path": "team.hiring.onsite_candidates", "min": 0},
                {"op": "increment", "path": "team.hiring.offers_out", "value": offers_out_delta - accepted_hires},
                {"op": "clamp", "path": "team.hiring.offers_out", "min": 0},
                {"op": "increment", "path": "team.headcount", "value": accepted_hires},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": recruiting_spend},
                {"op": "increment", "path": "team.morale", "value": morale_delta},
                {"op": "clamp", "path": "team.morale", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "team.attrition_risk", "value": -0.035 * accepted_hires},
                {"op": "clamp", "path": "team.attrition_risk", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "team.bandwidth_load", "value": bandwidth_delta},
                {"op": "clamp", "path": "team.bandwidth_load", "min": 0.0, "max": 1.5},
                {"op": "increment", "path": "operations.support_backlog", "value": support_backlog_delta},
                {"op": "clamp", "path": "operations.support_backlog", "min": 0},
                {"op": "increment", "path": "product.onboarding_quality", "value": onboarding_delta},
                {"op": "clamp", "path": "product.onboarding_quality", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "team.hiring.hiring_actions_count", "value": 1},
            ],
        )
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0.0)), 2)
        team["morale"] = round(float(team.get("morale", 0.0)), 4)
        team["attrition_risk"] = round(float(team.get("attrition_risk", 0.0)), 4)
        team["bandwidth_load"] = round(float(team.get("bandwidth_load", 0.0)), 4)
        product["onboarding_quality"] = round(float(product.get("onboarding_quality", 0.0)), 4)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "hiring_state": {
                    "headcount": team.get("headcount", 0),
                    "open_roles": hiring.get("open_roles", 0),
                    "critical_roles_open": hiring.get("critical_roles_open", 0),
                    "sourced_candidates": hiring.get("sourced_candidates", 0),
                    "onsite_candidates": hiring.get("onsite_candidates", 0),
                    "offers_out": hiring.get("offers_out", 0),
                    "hiring_capacity_index": hiring.get("hiring_capacity_index", 0.0),
                    "delivery_capacity_index": team.get("delivery_capacity_index", 0.0),
                }
            },
            state_delta_summary={
                "team.headcount": team.get("headcount", 0),
                "team.hiring.open_roles": hiring.get("open_roles", 0),
                "team.hiring.critical_roles_open": hiring.get("critical_roles_open", 0),
                "team.bandwidth_load": team.get("bandwidth_load", 0.0),
                "team.delivery_capacity_index": team.get("delivery_capacity_index", 0.0),
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
            },
        )

    if tool_name == "growth.experiment.create":
        growth = session.world_state.setdefault("growth", {})
        finance = session.world_state.setdefault("finance", {})
        sales = session.world_state.setdefault("sales", {})
        market = session.world_state.setdefault("market", {})
        customers = session.world_state.setdefault("customers", {})

        experiments = growth.setdefault("experiments", [])
        experiment_id = str(arguments.get("experiment_id", f"exp_{len(experiments) + 1:03d}"))
        experiment_name = str(arguments.get("experiment_name", experiment_id))
        channel = str(arguments.get("channel", "unassigned"))
        budget_change_monthly_burn_usd = float(arguments.get("budget_change_monthly_burn_usd", 0.0))
        monthly_revenue_delta_usd = float(arguments.get("monthly_revenue_delta_usd", 0.0))
        pipeline_count_delta = int(arguments.get("pipeline_count_delta", 0))
        weighted_pipeline_usd_delta = float(arguments.get("weighted_pipeline_usd_delta", 0.0))
        demand_index_delta = float(arguments.get("demand_index_delta", 0.0))
        trust_delta = float(arguments.get("trust_delta", 0.0))
        activation_delta = float(arguments.get("activation_delta", 0.0))

        experiment = {
            "experiment_id": experiment_id,
            "experiment_name": experiment_name,
            "channel": channel,
            "status": "active",
            "created_at": session.world_state["sim"]["current_time"],
        }
        experiments.append(experiment)
        growth["latest_experiment"] = experiment_name
        growth["active_channels"] = list(dict.fromkeys([*growth.get("active_channels", []), channel]))

        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "growth.experiment_count", "value": 1},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": budget_change_monthly_burn_usd},
                {"op": "increment", "path": "finance.monthly_revenue_usd", "value": monthly_revenue_delta_usd},
                {"op": "increment", "path": "sales.pipeline_count", "value": pipeline_count_delta},
                {"op": "clamp", "path": "sales.pipeline_count", "min": 0},
                {"op": "increment", "path": "sales.weighted_pipeline_usd", "value": weighted_pipeline_usd_delta},
                {"op": "clamp", "path": "sales.weighted_pipeline_usd", "min": 0.0},
                {"op": "increment", "path": "market.demand_index", "value": demand_index_delta},
                {"op": "clamp", "path": "market.demand_index", "min": 0.0, "max": 1.5},
                {"op": "increment", "path": "customers.trust_score", "value": trust_delta},
                {"op": "clamp", "path": "customers.trust_score", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "growth.activation_index", "value": activation_delta},
                {"op": "clamp", "path": "growth.activation_index", "min": 0.0, "max": 1.0},
            ],
        )
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0.0)), 2)
        finance["monthly_revenue_usd"] = round(float(finance.get("monthly_revenue_usd", 0.0)), 2)
        customers["trust_score"] = round(float(customers.get("trust_score", 0.0)), 4)
        market["demand_index"] = round(float(market.get("demand_index", 0.0)), 4)
        growth["activation_index"] = round(float(growth.get("activation_index", 0.0)), 4)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "growth_state": {
                    "experiment_id": experiment_id,
                    "experiment_name": experiment_name,
                    "active_experiment_count": growth.get("active_experiment_count", 0),
                    "experiment_count": growth.get("experiment_count", 0),
                    "activation_index": growth.get("activation_index", 0.0),
                    "weighted_pipeline_usd": sales.get("weighted_pipeline_usd"),
                }
            },
            state_delta_summary={
                "growth.experiment_count": growth.get("experiment_count", 0),
                "growth.active_experiment_count": growth.get("active_experiment_count", 0),
                "growth.activation_index": growth.get("activation_index", 0.0),
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
                "sales.weighted_pipeline_usd": sales.get("weighted_pipeline_usd"),
            },
        )

    if tool_name == "growth.experiment.review":
        growth = session.world_state.setdefault("growth", {})
        return _tool_result(
            tool_name,
            request_id,
            result={
                "growth_state": {
                    "activation_index": growth.get("activation_index", 0.0),
                    "experiment_count": growth.get("experiment_count", 0),
                    "active_experiment_count": growth.get("active_experiment_count", 0),
                    "latest_experiment": growth.get("latest_experiment"),
                    "experiments": deepcopy(growth.get("experiments", [])),
                    "active_channels": deepcopy(growth.get("active_channels", [])),
                }
            },
        )

    if tool_name == "research.market.read":
        market = session.world_state.setdefault("market", {})
        customers = session.world_state.setdefault("customers", {})
        market["market_reads_count"] = int(market.get("market_reads_count", 0)) + 1
        return _tool_result(
            tool_name,
            request_id,
            result={
                "market_state": {
                    "competitor_pressure": market.get("competitor_pressure", market.get("competitor_pressure_index", 0.0)),
                    "competitor_pressure_index": market.get("competitor_pressure_index", 0.0),
                    "pricing_pressure_index": market.get("pricing_pressure_index", market.get("pricing_pressure", 0.0)),
                    "demand_index": market.get("demand_index", 0.0),
                    "segment_signals": deepcopy(market.get("segment_signals", [])),
                    "latest_market_note": market.get("latest_market_note"),
                    "segment_mix_index": customers.get("segment_mix_index"),
                    "market_reads_count": market.get("market_reads_count", 0),
                }
            },
            state_delta_summary={"market.market_reads_count": market.get("market_reads_count", 0)},
        )

    if tool_name == "notes.read":
        return _tool_result(tool_name, request_id, result={"notes": list(session.notes)})

    if tool_name == "notes.write":
        content = arguments.get("content", "")
        session.notes.append(str(content))
        return _tool_result(
            tool_name,
            request_id,
            result={"notes": list(session.notes)},
            state_delta_summary={"notes_count": len(session.notes)},
        )

    if tool_name == "board.read":
        return _tool_result(tool_name, request_id, result={"governance": deepcopy(session.world_state["governance"])})

    if tool_name == "board.update":
        update = {
            "summary": arguments.get("summary", ""),
            "forecast": arguments.get("forecast"),
            "asks": arguments.get("asks", []),
        }
        session.world_state["governance"]["latest_board_update"] = update
        session.world_state["governance"]["board_update_count"] = int(
            session.world_state["governance"].get("board_update_count", 0)
        ) + 1
        return _tool_result(
            tool_name,
            request_id,
            result={"board_update": update},
            state_delta_summary={
                "governance.latest_board_update": "updated",
                "governance.board_update_count": session.world_state["governance"]["board_update_count"],
            },
        )

    if tool_name == "legal.compliance.read":
        risk = session.world_state.setdefault("risk", {})
        return _tool_result(
            tool_name,
            request_id,
            result={
                "compliance_state": {
                    "regulatory_pressure": risk.get("regulatory_pressure", 0.0),
                    "active_legal_matters": risk.get("active_legal_matters", 0),
                    "compliance_backlog": risk.get("compliance_backlog", 0),
                    "counterparty_risk": risk.get("counterparty_risk", 0.0),
                }
            },
        )

    if tool_name == "legal.compliance.respond":
        risk = session.world_state.setdefault("risk", {})
        customers = session.world_state.setdefault("customers", {})
        finance = session.world_state.setdefault("finance", {})
        pressure_reduction = max(0.0, float(arguments.get("pressure_reduction", 0.18)))
        matters_reduction = max(0, int(arguments.get("matters_reduction", 1)))
        backlog_reduction = max(0, int(arguments.get("compliance_backlog_reduction", 4)))
        trust_recovery = max(0.0, float(arguments.get("trust_recovery", 0.02)))
        burn_increase = max(0.0, float(arguments.get("monthly_burn_increase_usd", 11000)))
        apply_operations(
            session.world_state,
            [
                {"op": "increment", "path": "risk.regulatory_pressure", "value": -pressure_reduction},
                {"op": "clamp", "path": "risk.regulatory_pressure", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "risk.active_legal_matters", "value": -matters_reduction},
                {"op": "clamp", "path": "risk.active_legal_matters", "min": 0},
                {"op": "increment", "path": "risk.compliance_backlog", "value": -backlog_reduction},
                {"op": "clamp", "path": "risk.compliance_backlog", "min": 0},
                {"op": "increment", "path": "customers.trust_score", "value": trust_recovery},
                {"op": "clamp", "path": "customers.trust_score", "min": 0.0, "max": 1.0},
                {"op": "increment", "path": "finance.monthly_burn_usd", "value": burn_increase},
                {"op": "increment", "path": "risk.legal_responses_count", "value": 1},
            ],
        )
        risk["regulatory_pressure"] = round(float(risk.get("regulatory_pressure", 0.0)), 4)
        customers["trust_score"] = round(float(customers.get("trust_score", 0.0)), 4)
        finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0.0)), 2)
        recalculate_derived_metrics(session.world_state)
        return _tool_result(
            tool_name,
            request_id,
            result={
                "compliance_state": {
                    "regulatory_pressure": risk.get("regulatory_pressure", 0.0),
                    "active_legal_matters": risk.get("active_legal_matters", 0),
                    "compliance_backlog": risk.get("compliance_backlog", 0),
                    "trust_score": customers.get("trust_score"),
                }
            },
            state_delta_summary={
                "risk.regulatory_pressure": risk.get("regulatory_pressure", 0.0),
                "risk.active_legal_matters": risk.get("active_legal_matters", 0),
                "risk.compliance_backlog": risk.get("compliance_backlog", 0),
                "customers.trust_score": customers.get("trust_score"),
                "finance.monthly_burn_usd": finance.get("monthly_burn_usd"),
            },
        )

    if tool_name == "sim.advance":
        amount = int(arguments.get("advance_by", 1))
        unit = arguments.get("unit", "week")
        before = session.world_state["sim"]["current_time"]
        after = _advance_time(before, amount=amount, unit=unit)
        weeks = amount
        if unit == "day":
            weeks = max(1, amount // 7)
        elif unit == "month":
            weeks = amount * 4
        elif unit == "quarter":
            weeks = amount * 13
        _apply_weekly_business_drift(session, weeks=weeks)
        session.world_state["sim"]["current_time"] = after
        session.world_state["sim"]["current_turn"] = int(session.world_state["sim"]["current_turn"]) + 1
        visible_events = [{
            "event_type": "time_advanced",
            "before": before,
            "after": after,
            "unit": unit,
            "amount": amount,
        }]
        visible_events.extend(_process_due_events(session))
        recalculate_derived_metrics(session.world_state)
        session.event_log.extend(visible_events)
        return _tool_result(
            tool_name,
            request_id,
            result={"sim_time_before": before, "sim_time_after": after, "events_processed": visible_events},
            state_delta_summary={
                "sim.current_time": after,
                "sim.current_turn": session.world_state["sim"]["current_turn"],
                "finance.cash_usd": session.world_state["finance"].get("cash_usd"),
                "finance.runway_weeks": session.world_state["finance"].get("runway_weeks"),
            },
        )

    raise KeyError(f"Tool not implemented in reference runtime: {tool_name}")


__all__ = ["RuntimeSession", "execute_tool_call"]
