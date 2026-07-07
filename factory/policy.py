"""Políticas y gates de ejecución."""

from __future__ import annotations

from .constants import APPROVAL_REQUIRED_FOR, TOKEN_ECONOMY_POLICY
from .registry import tool_registry


class PolicyError(RuntimeError):
    pass


def assert_tool_allowed(tool_id: str) -> None:
    registry = tool_registry()
    if tool_id not in registry:
        raise PolicyError(f"Tool no registrada: {tool_id}")
    spec = registry[tool_id]
    if not spec.allowed:
        raise PolicyError(f"Tool bloqueada por política: {tool_id}")


def assert_budget(context_tokens: int, max_tokens: int | None = None) -> None:
    limit = max_tokens or TOKEN_ECONOMY_POLICY["max_context_tokens_per_agent"]
    if context_tokens > limit:
        raise PolicyError(f"Presupuesto de tokens excedido: {context_tokens} > {limit}")


def requires_approval(action_id: str) -> bool:
    return action_id in APPROVAL_REQUIRED_FOR
