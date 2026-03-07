"""Operational helpers for scenario-pack promotion and lifecycle tracking."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from .scenario_loader import load_json
from .suite_manifest import build_public_suite_manifest
from .suite_runner import load_scenario_suite
from .validation import validate_instance


def promote_suite_pack(
    path: Path,
    *,
    split: str,
    scenario_pack_version: str,
    allow_split_clone: bool = False,
) -> dict:
    suite = load_scenario_suite(path)
    if split in {"test", "fresh"} and not allow_split_clone:
        raise ValueError(
            "promote-suite refuses to clone into hidden splits by default. "
            "Use distinct hidden scenarios for official packs, or pass allow_split_clone=True for draft-only use."
        )

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


def validate_suite_family(paths: list[Path]) -> dict:
    if len(paths) < 2:
        raise ValueError("At least two suite paths are required.")

    suites = [{"path": path, "suite": load_scenario_suite(path)} for path in paths]
    issues: list[dict] = []
    seen_hidden_ids: dict[str, dict] = {}
    seen_hidden_paths: dict[str, dict] = {}

    for item in suites:
        suite_path = item["path"]
        suite = item["suite"]
        split = suite["split"]

        for index, entry in enumerate(suite["scenarios"]):
            mode = entry.get("mode", split)
            if mode != split:
                issues.append(
                    {
                        "code": "mode_mismatch",
                        "suite_path": str(suite_path),
                        "scenario_id": entry["scenario_id"],
                        "message": f"Scenario mode '{mode}' does not match suite split '{split}'.",
                        "path": ["scenarios", str(index), "mode"],
                    }
                )

            if split not in {"test", "fresh"}:
                continue

            scenario_id = entry["scenario_id"]
            scenario_path = str((suite_path.parent / entry["path"]).resolve())

            prior_id = seen_hidden_ids.get(scenario_id)
            if prior_id:
                issues.append(
                    {
                        "code": "duplicate_hidden_scenario_id",
                        "suite_path": str(suite_path),
                        "scenario_id": scenario_id,
                        "message": f"Hidden scenario id '{scenario_id}' is reused across hidden suites.",
                        "path": ["scenarios", str(index), "scenario_id"],
                        "conflicts_with": prior_id,
                    }
                )
            else:
                seen_hidden_ids[scenario_id] = {
                    "suite_path": str(suite_path),
                    "split": split,
                }

            prior_path = seen_hidden_paths.get(scenario_path)
            if prior_path:
                issues.append(
                    {
                        "code": "duplicate_hidden_scenario_path",
                        "suite_path": str(suite_path),
                        "scenario_id": scenario_id,
                        "message": f"Hidden scenario file '{entry['path']}' is reused across hidden suites.",
                        "path": ["scenarios", str(index), "path"],
                        "conflicts_with": prior_path,
                    }
                )
            else:
                seen_hidden_paths[scenario_path] = {
                    "suite_path": str(suite_path),
                    "split": split,
                }

    return {
        "ok": not issues,
        "suite_count": len(suites),
        "checked_suites": [str(item["path"]) for item in suites],
        "issues": issues,
    }


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


__all__ = ["promote_suite_pack", "validate_pack_changelog", "validate_suite_family"]
