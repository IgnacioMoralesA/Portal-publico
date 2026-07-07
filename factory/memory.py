"""Memoria aislada por fábrica, proyecto y agente."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def memory_path(project_dir: Path, agent_id: str) -> Path:
    safe = agent_id.replace(".", "_")
    return project_dir / "agent-memory" / f"{safe}.json"


def read_memory(project_dir: Path, agent_id: str) -> dict[str, Any]:
    p = memory_path(project_dir, agent_id)
    if not p.exists():
        return {"agent_id": agent_id, "items": []}
    return json.loads(p.read_text(encoding="utf-8"))


def write_memory(project_dir: Path, agent_id: str, item: dict[str, Any]) -> None:
    p = memory_path(project_dir, agent_id)
    data = read_memory(project_dir, agent_id)
    data.setdefault("items", []).append(item)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
