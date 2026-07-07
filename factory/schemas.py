"""Validador JSON Schema reducido y estricto, sin dependencias externas."""

from __future__ import annotations

from typing import Any


class SchemaError(ValueError):
    pass


def _type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    if value is None:
        return "null"
    return type(value).__name__


def validate_schema(data: Any, schema: dict[str, Any], path: str = "$") -> None:
    expected_type = schema.get("type")
    if expected_type:
        allowed = expected_type if isinstance(expected_type, list) else [expected_type]
        if _type_name(data) not in allowed:
            raise SchemaError(f"{path}: expected {allowed}, got {_type_name(data)}")

    if "enum" in schema and data not in schema["enum"]:
        raise SchemaError(f"{path}: value {data!r} not in enum {schema['enum']!r}")

    if isinstance(data, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                raise SchemaError(f"{path}: missing required key {key!r}")

        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(data) - set(props)
            if extra:
                raise SchemaError(f"{path}: additional properties not allowed: {sorted(extra)}")

        for key, value in data.items():
            if key in props:
                validate_schema(value, props[key], f"{path}.{key}")

    if isinstance(data, list) and "items" in schema:
        for idx, item in enumerate(data):
            validate_schema(item, schema["items"], f"{path}[{idx}]")


WORK_ORDER_SCHEMA = {
    "type": "object",
    "required": ["work_order_id", "objective", "economy_mode", "sources"],
    "additionalProperties": False,
    "properties": {
        "work_order_id": {"type": "string"},
        "objective": {"type": "string"},
        "economy_mode": {"type": "boolean"},
        "sources": {"type": "array", "items": {"type": "string"}},
        "constraints": {"type": "array", "items": {"type": "string"}},
        "acceptance": {"type": "array", "items": {"type": "string"}},
    },
}

AGENT_RESULT_SCHEMA = {
    "type": "object",
    "required": ["agent_id", "phase", "status", "outputs", "evidence", "token_ledger"],
    "additionalProperties": False,
    "properties": {
        "agent_id": {"type": "string"},
        "phase": {"type": "string"},
        "status": {"type": "string", "enum": ["complete", "needs_user_input", "not_answerable", "error"]},
        "outputs": {"type": "object"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "token_ledger": {"type": "object"},
    },
}
