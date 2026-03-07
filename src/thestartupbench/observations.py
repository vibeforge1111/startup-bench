"""Observation projection utilities."""

from __future__ import annotations


def _flatten_world_state(world_state: dict) -> dict[str, object]:
    flat: dict[str, object] = {}
    for partition, value in world_state.items():
        if isinstance(value, dict):
            for key, nested_value in value.items():
                flat[f"{partition}.{key}"] = nested_value
                flat[key] = nested_value
        else:
            flat[partition] = value
    return flat


def project_surface(surface: dict, world_state: dict) -> dict:
    flat = _flatten_world_state(world_state)
    values = {}
    for field in surface["visible_fields"]:
        values[field] = flat.get(field)
    return {
        "surface_id": surface["surface_id"],
        "surface_type": surface["surface_type"],
        "refresh_policy": surface["refresh_policy"],
        "values": values,
    }


def project_surfaces(surfaces: list[dict], world_state: dict) -> list[dict]:
    return [project_surface(surface, world_state) for surface in surfaces]


__all__ = ["project_surface", "project_surfaces"]

