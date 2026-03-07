"""Operational helpers for scenario-pack promotion and lifecycle tracking."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from .scenario_loader import load_json
from .suite_manifest import build_public_suite_manifest
from .suite_runner import load_scenario_suite
from .validation import validate_instance


def promote_suite_pack(path: Path, *, split: str, scenario_pack_version: str) -> dict:
    suite = load_scenario_suite(path)
    promoted = deepcopy(suite)
    promoted["split"] = split
    promoted["scenario_pack_version"] = scenario_pack_version

    for entry in promoted["scenarios"]:
        entry["mode"] = split

    result = {
        "suite": promoted,
        "validation": validate_instance(
            artifact_type="scenario-suite",
            instance=promoted,
            path=Path("scenario_suite.json"),
        ).to_dict(),
    }
    if split in {"test", "fresh"}:
        manifest_result = build_public_suite_manifest(promoted)
        result["public_manifest"] = manifest_result["manifest"]
        result["public_manifest_validation"] = manifest_result["validation"]
    return result


def validate_pack_changelog(path: Path) -> dict:
    changelog = load_json(path)
    return {
        "changelog": changelog,
        "validation": validate_instance(
            artifact_type="pack-changelog",
            instance=changelog,
            path=path,
        ).to_dict(),
    }


__all__ = ["promote_suite_pack", "validate_pack_changelog"]
