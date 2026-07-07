"""Validadores de gates principales."""

from __future__ import annotations

import json
from pathlib import Path

from .schemas import AGENT_RESULT_SCHEMA, WORK_ORDER_SCHEMA, validate_schema


def validate_work_order_file(path: Path) -> None:
    validate_schema(json.loads(path.read_text(encoding="utf-8")), WORK_ORDER_SCHEMA)


def validate_agent_result(result: dict) -> None:
    validate_schema(result, AGENT_RESULT_SCHEMA)


def validate_required_run_artifacts(run_dir: Path) -> list[str]:
    required = [
        "work_order.json",
        "context-pack.json",
        "evidence-register.json",
        "traceability-matrix.md",
        "validation-report.json",
        "final-report.json",
    ]
    missing = [name for name in required if not (run_dir / name).exists()]
    return missing
