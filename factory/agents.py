"""Compatibilidad: acceso central a agentes registrados."""

from .registry import agent_registry

AGENTS = agent_registry()
