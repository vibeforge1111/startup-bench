"""Scenario loading helpers."""

from __future__ import annotations

import json
from pathlib import Path

from .validation import raise_if_invalid


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_scenario(path: Path) -> dict:
    scenario = load_json(path)
    raise_if_invalid(artifact_type="scenario", instance=scenario, path=path)
    return scenario


__all__ = ["load_json", "load_scenario"]

