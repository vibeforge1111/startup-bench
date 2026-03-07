"""Public manifest helpers for redacted scenario-suite packaging."""

from __future__ import annotations

from pathlib import Path

from .suite_runner import load_scenario_suite
from .validation import validate_instance


def build_public_suite_manifest(suite: dict) -> dict:
    scenarios = []
    for index, entry in enumerate(suite["scenarios"]):
        scenarios.append(
            {
                "scenario_id": entry["scenario_id"],
                "track": entry.get("track", "unknown"),
                "mode": entry.get("mode", suite["split"]),
                "hidden_ref": f"{suite['split']}_{index:03d}",
            }
        )

    manifest = {
        "manifest_version": "0.1.0",
        "benchmark_version": suite["benchmark_version"],
        "scenario_pack_version": suite["scenario_pack_version"],
        "split": suite["split"],
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
    }
    return {
        "manifest": manifest,
        "validation": validate_instance(
            artifact_type="public-suite-manifest",
            instance=manifest,
            path=Path("public_suite_manifest.json"),
        ).to_dict(),
    }


def redact_suite_manifest(path: Path) -> dict:
    suite = load_scenario_suite(path)
    return build_public_suite_manifest(suite)


__all__ = ["build_public_suite_manifest", "redact_suite_manifest"]
