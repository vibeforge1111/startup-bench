"""CLI entrypoint for TheStartupBench tooling."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .paths import examples_dir, repo_root, schemas_dir, spec_dir


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tsb", description="TheStartupBench reference tooling")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Print the installed package version")
    subparsers.add_parser("paths", help="Print important repository paths")

    validate_parser = subparsers.add_parser("validate", help="Validate an artifact against a benchmark schema")
    validate_parser.add_argument("artifact_type", help="Artifact type, e.g. scenario, trace, submission")
    validate_parser.add_argument("path", help="Path to the JSON artifact")

    inspect_parser = subparsers.add_parser("inspect-scenario", help="Print selected scenario metadata")
    inspect_parser.add_argument("path", help="Path to the scenario JSON file")

    run_parser = subparsers.add_parser("run-dry", help="Run a zero-action dry execution for a scenario")
    run_parser.add_argument("scenario_path", help="Path to the scenario JSON file")
    run_parser.add_argument("--seed", type=int, default=0, help="Seed used for the dry run")

    return parser


def _cmd_paths() -> int:
    payload = {
        "repo_root": str(repo_root()),
        "schemas_dir": str(schemas_dir()),
        "examples_dir": str(examples_dir()),
        "spec_dir": str(spec_dir()),
    }
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_validate(artifact_type: str, path: str) -> int:
    from .validation import validate_artifact_file

    result = validate_artifact_file(artifact_type=artifact_type, path=Path(path))
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


def _cmd_inspect_scenario(path: str) -> int:
    from .scenario_loader import load_scenario

    scenario = load_scenario(Path(path))
    metadata = scenario["metadata"]
    payload = {
        "scenario_id": metadata["scenario_id"],
        "scenario_version": metadata["scenario_version"],
        "benchmark_version": metadata["benchmark_version"],
        "track": metadata["track"],
        "mode": metadata["mode"],
        "title": metadata["title"],
        "summary": metadata["summary"],
        "tools": scenario["tools"],
        "observation_surface_count": len(scenario["observation_surfaces"]),
        "terminal_condition_count": len(scenario["terminal_conditions"]),
    }
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_run_dry(scenario_path: str, seed: int) -> int:
    from .runner import run_dry_scenario

    result = run_dry_scenario(Path(scenario_path), seed=seed)
    print(json.dumps(result, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0
    if args.command == "paths":
        return _cmd_paths()
    if args.command == "validate":
        return _cmd_validate(args.artifact_type, args.path)
    if args.command == "inspect-scenario":
        return _cmd_inspect_scenario(args.path)
    if args.command == "run-dry":
        return _cmd_run_dry(args.scenario_path, args.seed)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

