"""Validation of events against the contracts in contracts/events/.

Two checks are applied to every event:

1. JSON Schema: the shared envelope, plus the type-specific schema when one
   exists for the event's type and version.
2. No direct identifiers anywhere in the payload. The schema only forbids
   them at the top level; this module also rejects them when nested.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SCHEMA_DIR = Path(__file__).resolve().parents[2] / "contracts" / "events"
ENVELOPE_ID = "https://optata.dk/contracts/events/_envelope.v1.json"

# Keys that must never appear in an event payload, at any depth.
FORBIDDEN_PAYLOAD_KEYS = frozenset(
    {"cpr", "name", "full_name", "email", "phone", "document", "message_body"}
)


class EventValidationError(ValueError):
    """Raised when an event does not satisfy its contract."""


@lru_cache(maxsize=1)
def _load() -> tuple[Registry, dict[tuple[str, str | None], dict[str, Any]]]:
    registry = Registry()
    by_type: dict[tuple[str, str | None], dict[str, Any]] = {}
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        resource = Resource.from_contents(schema, default_specification=DRAFT202012)
        registry = registry.with_resource(schema["$id"], resource)
        props = schema.get("properties", {})
        event_type = props.get("type", {}).get("const")
        if event_type:
            version = props.get("schema_version", {}).get("const")
            by_type[(event_type, version)] = schema
    return registry, by_type


def _find_forbidden(value: Any, path: str = "payload") -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in FORBIDDEN_PAYLOAD_KEYS:
                return f"{path}.{key}"
            found = _find_forbidden(child, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found = _find_forbidden(child, f"{path}[{index}]")
            if found:
                return found
    return None


def validate_event(event: dict[str, Any]) -> None:
    """Raise EventValidationError unless `event` satisfies its contract."""
    registry, by_type = _load()
    key = (event.get("type"), event.get("schema_version"))
    schema = by_type.get(key) or by_type.get((key[0], None))
    if schema is None:
        schema = registry.get_or_retrieve(ENVELOPE_ID).value.contents
    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(event), key=lambda e: list(e.path))
    if errors:
        first = errors[0]
        location = "/".join(str(p) for p in first.path) or "<root>"
        raise EventValidationError(f"{location}: {first.message}")
    forbidden = _find_forbidden(event.get("payload", {}))
    if forbidden:
        raise EventValidationError(f"direct identifier in event payload: {forbidden}")
