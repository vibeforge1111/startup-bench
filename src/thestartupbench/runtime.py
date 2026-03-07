"""Minimal stateful runtime for scripted benchmark execution."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from .observations import project_surfaces
from .runner import recalculate_derived_metrics


def _parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _format_iso8601(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


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
        "result": result,
        "state_delta_summary": state_delta_summary or {},
    }


def _set_dotted_value(target: dict, dotted_path: str, delta_or_value) -> None:
    parts = dotted_path.split(".")
    cursor = target
    for part in parts[:-1]:
        cursor = cursor.setdefault(part, {})
    leaf = parts[-1]
    current = cursor.get(leaf)
    if isinstance(delta_or_value, (int, float)) and isinstance(current, (int, float)):
        cursor[leaf] = current + delta_or_value
    else:
        cursor[leaf] = delta_or_value


def _apply_event_effects(session: RuntimeSession, effects: dict) -> None:
    for path, delta_or_value in effects.items():
        _set_dotted_value(session.world_state, path, delta_or_value)


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
        _apply_event_effects(session, event.get("effects", {}))
        visible_event = {
            "event_type": event.get("event_type", "scheduled_event"),
            "event_id": event_id,
            "message": event.get("visible_message", ""),
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
    monthly_revenue = float(finance.get("monthly_revenue_usd", 0))
    monthly_burn = float(finance.get("monthly_burn_usd", 0))
    cash = float(finance.get("cash_usd", 0))
    cash += ((monthly_revenue - monthly_burn) / 4.0) * weeks
    finance["cash_usd"] = round(cash, 2)

    paying_accounts = int(customers.get("paying_accounts", 0))
    churn = float(customers.get("monthly_churn_rate", 0))
    accounts_lost = int(round(paying_accounts * (churn / 4.0) * weeks))
    customers["paying_accounts"] = max(0, paying_accounts - accounts_lost)


def _build_metric_report(session: RuntimeSession) -> dict:
    finance = session.world_state.get("finance", {})
    customers = session.world_state.get("customers", {})
    sales = session.world_state.get("sales", {})
    governance = session.world_state.get("governance", {})
    sim = session.world_state.get("sim", {})

    alerts = []
    if float(finance.get("runway_weeks", 0)) < 20:
        alerts.append("runway_below_20_weeks")
    if float(customers.get("monthly_churn_rate", 0)) > 0.05:
        alerts.append("churn_above_5pct")
    if float(customers.get("trust_score", 1.0)) < 0.6:
        alerts.append("trust_score_below_0_6")
    if int(sim.get("pending_event_count", 0)) > 0:
        alerts.append("pending_scheduled_events")

    return {
        "headline": {
            "cash_usd": finance.get("cash_usd"),
            "runway_weeks": finance.get("runway_weeks"),
            "monthly_revenue_usd": finance.get("monthly_revenue_usd"),
            "net_burn_usd": finance.get("net_burn_usd"),
        },
        "customers": {
            "paying_accounts": customers.get("paying_accounts"),
            "monthly_churn_rate": customers.get("monthly_churn_rate"),
            "trust_score": customers.get("trust_score"),
            "health_index": customers.get("health_index"),
        },
        "sales": {
            "pipeline_count": sales.get("pipeline_count"),
            "weighted_pipeline_usd": sales.get("weighted_pipeline_usd"),
            "pricing": sales.get("pricing", {}),
        },
        "governance": {
            "board_update_count": governance.get("board_update_count", 0),
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

        product["roadmap_items"] = max(0, int(product.get("roadmap_items", 0)) + roadmap_items_delta)
        product["onboarding_quality"] = round(
            max(0.0, min(1.0, float(product.get("onboarding_quality", 0.5)) + onboarding_quality_delta)),
            4,
        )
        product["major_incidents_open"] = max(0, int(product.get("major_incidents_open", 0)) + major_incidents_delta)
        if budget_change:
            finance["monthly_burn_usd"] = round(float(finance.get("monthly_burn_usd", 0)) + budget_change, 2)
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

    if tool_name == "finance.plan.read":
        return _tool_result(tool_name, request_id, result={"finance": deepcopy(session.world_state["finance"])})

    if tool_name == "finance.plan.write":
        budget_changes = arguments.get("budget_changes", {})
        state_delta = {}
        for key, delta in budget_changes.items():
            current = float(session.world_state["finance"].get(key, 0))
            session.world_state["finance"][key] = round(current + float(delta), 2)
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

    if tool_name == "sales.pipeline.read":
        return _tool_result(tool_name, request_id, result={"sales": deepcopy(session.world_state["sales"])})

    if tool_name == "sales.pipeline.update":
        sales = session.world_state.setdefault("sales", {})
        finance = session.world_state.setdefault("finance", {})
        pipeline_count_delta = int(arguments.get("pipeline_count_delta", 0))
        weighted_pipeline_usd_delta = float(arguments.get("weighted_pipeline_usd_delta", 0))
        closed_won_revenue_delta = float(arguments.get("closed_won_revenue_delta_usd", 0))

        sales["pipeline_count"] = max(0, int(sales.get("pipeline_count", 0)) + pipeline_count_delta)
        sales["weighted_pipeline_usd"] = round(float(sales.get("weighted_pipeline_usd", 0)) + weighted_pipeline_usd_delta, 2)
        if closed_won_revenue_delta:
            finance["monthly_revenue_usd"] = round(
                float(finance.get("monthly_revenue_usd", 0)) + closed_won_revenue_delta,
                2,
            )
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
