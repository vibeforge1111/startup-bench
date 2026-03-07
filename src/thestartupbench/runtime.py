"""Minimal stateful runtime for scripted benchmark execution."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from .observations import project_surfaces


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
    for partition, value in world_state.items():
        if isinstance(value, dict):
            for key, nested_value in value.items():
                flat[f"{partition}.{key}"] = nested_value
                flat[key] = nested_value
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


def execute_tool_call(session: RuntimeSession, tool_call: dict) -> dict:
    tool_name = tool_call["tool_name"]
    request_id = tool_call["request_id"]
    arguments = tool_call.get("arguments", {})

    if tool_name == "metrics.query":
        metric_ids = arguments.get("metric_ids", [])
        flat = _flatten_world_state(session.world_state)
        result = {"items": {metric_id: flat.get(metric_id) for metric_id in metric_ids}}
        return _tool_result(tool_name, request_id, result=result)

    if tool_name == "finance.plan.read":
        return _tool_result(tool_name, request_id, result={"finance": deepcopy(session.world_state["finance"])})

    if tool_name == "sales.pipeline.read":
        return _tool_result(tool_name, request_id, result={"sales": deepcopy(session.world_state["sales"])})

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

    if tool_name == "board.update":
        update = {
            "summary": arguments.get("summary", ""),
            "forecast": arguments.get("forecast"),
            "asks": arguments.get("asks", []),
        }
        session.world_state["governance"]["latest_board_update"] = update
        return _tool_result(
            tool_name,
            request_id,
            result={"board_update": update},
            state_delta_summary={"governance.latest_board_update": "updated"},
        )

    if tool_name == "sim.advance":
        amount = int(arguments.get("advance_by", 1))
        unit = arguments.get("unit", "week")
        before = session.world_state["sim"]["current_time"]
        after = _advance_time(before, amount=amount, unit=unit)
        session.world_state["sim"]["current_time"] = after
        session.world_state["sim"]["current_turn"] = int(session.world_state["sim"]["current_turn"]) + 1
        visible_event = {
            "event_type": "time_advanced",
            "before": before,
            "after": after,
            "unit": unit,
            "amount": amount,
        }
        session.event_log.append(visible_event)
        return _tool_result(
            tool_name,
            request_id,
            result={"sim_time_before": before, "sim_time_after": after, "events_processed": [visible_event]},
            state_delta_summary={"sim.current_time": after, "sim.current_turn": session.world_state["sim"]["current_turn"]},
        )

    raise KeyError(f"Tool not implemented in reference runtime: {tool_name}")


__all__ = ["RuntimeSession", "execute_tool_call"]

