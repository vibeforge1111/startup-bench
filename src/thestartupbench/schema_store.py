"""Schema loading and validation helpers."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .paths import schemas_dir


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def load_schema_documents() -> dict[str, dict]:
    documents: dict[str, dict] = {}
    for path in schemas_dir().glob("*.json"):
        doc = _load_json(path)
        documents[path.name] = doc
        schema_id = doc.get("$id")
        if isinstance(schema_id, str):
            documents[schema_id] = doc
    return documents


@lru_cache(maxsize=1)
def build_registry() -> Registry:
    registry = Registry()
    for schema in load_schema_documents().values():
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            continue
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry


def get_schema(schema_name: str) -> dict:
    documents = load_schema_documents()
    if schema_name not in documents:
        raise KeyError(f"Unknown schema: {schema_name}")
    return documents[schema_name]


def build_validator(schema_name: str) -> Draft202012Validator:
    schema = get_schema(schema_name)
    return Draft202012Validator(schema, registry=build_registry())


__all__ = ["build_registry", "build_validator", "get_schema", "load_schema_documents"]

