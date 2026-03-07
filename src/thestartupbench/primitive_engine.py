"""Generic state-transition primitives for TheStartupBench."""

from __future__ import annotations

from copy import deepcopy


def get_dotted_value(target: dict, dotted_path: str, default=None):
    cursor = target
    for part in dotted_path.split("."):
        if not isinstance(cursor, dict) or part not in cursor:
            return default
        cursor = cursor[part]
    return cursor


def set_dotted_value(target: dict, dotted_path: str, value) -> None:
    parts = dotted_path.split(".")
    cursor = target
    for part in parts[:-1]:
        cursor = cursor.setdefault(part, {})
    cursor[parts[-1]] = value


def apply_operation(target: dict, operation: dict) -> dict:
    op = operation["op"]
    path = operation["path"]
    before = get_dotted_value(target, path)

    if op == "set":
        after = operation.get("value")
    elif op == "increment":
        after = float(before or 0) + float(operation.get("value", 0))
    elif op == "multiply":
        base = before if before is not None else 1
        after = float(base) * float(operation.get("value", 1))
    elif op == "clamp":
        base = float(before or 0)
        minimum = operation.get("min")
        maximum = operation.get("max")
        after = base
        if minimum is not None:
            after = max(float(minimum), after)
        if maximum is not None:
            after = min(float(maximum), after)
    elif op == "append_unique":
        items = list(before or [])
        value = operation.get("value")
        if value not in items:
            items.append(value)
        after = items
    else:
        raise ValueError(f"Unsupported primitive operation '{op}'.")

    if before is not None and isinstance(before, int) and not isinstance(before, bool) and isinstance(after, float):
        if after.is_integer():
            after = int(after)
    set_dotted_value(target, path, after)
    return {
        "path": path,
        "op": op,
        "before": deepcopy(before),
        "after": deepcopy(after),
    }


def _normalize_effects_to_operations(effects: dict) -> list[dict]:
    operations = []
    for path, value in effects.items():
        operations.append({"op": "increment", "path": path, "value": value})
    return operations


def resolve_event_operations(*, scenario: dict, event: dict) -> list[dict]:
    primitive_id = event.get("primitive_id")
    operations: list[dict] = []

    if primitive_id:
        catalog = scenario.get("event_model", {}).get("primitive_catalog", {})
        primitive = catalog.get(primitive_id)
        if primitive is None:
            raise KeyError(f"Unknown event primitive '{primitive_id}'.")
        operations.extend(deepcopy(primitive.get("operations", [])))

    if "operations" in event:
        operations.extend(deepcopy(event["operations"]))
    elif "effects" in event:
        operations.extend(_normalize_effects_to_operations(event["effects"]))

    return operations


def apply_operations(target: dict, operations: list[dict]) -> list[dict]:
    deltas = []
    for operation in operations:
        deltas.append(apply_operation(target, operation))
    return deltas


__all__ = [
    "apply_operation",
    "apply_operations",
    "get_dotted_value",
    "resolve_event_operations",
    "set_dotted_value",
]
