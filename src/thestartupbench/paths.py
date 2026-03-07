"""Repository path helpers."""

from __future__ import annotations

from pathlib import Path


def package_root() -> Path:
    return Path(__file__).resolve().parent


def repo_root() -> Path:
    # src/thestartupbench -> repo root
    return package_root().parents[1]


def schemas_dir() -> Path:
    return repo_root() / "schemas"


def examples_dir() -> Path:
    return repo_root() / "examples"


def spec_dir() -> Path:
    return repo_root() / "spec"


__all__ = ["examples_dir", "package_root", "repo_root", "schemas_dir", "spec_dir"]

