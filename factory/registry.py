"""Registro versionado de tools, skills y agentes."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .constants import MODEL_SEED


@dataclass(frozen=True)
class ToolSpec:
    tool_id: str
    description: str
    allowed: bool = True
    requires_approval: bool = False


@dataclass(frozen=True)
class SkillSpec:
    skill_id: str
    description: str
    token_cost: str = "low"


@dataclass(frozen=True)
class AgentSpec:
    agent_id: str
    role: str
    skills: list[str]
    tools: list[str]
    output_contract: str = "strict_json"
    model_policy: dict[str, Any] | None = None


def deterministic_model_policy() -> dict[str, Any]:
    return {
        "temperature": 0,
        "top_p": 1,
        "seed": MODEL_SEED,
        "parallel_tool_calls": False,
        "response_format": "strict_json_schema",
        "economy_first": True,
    }


def tool_registry() -> dict[str, ToolSpec]:
    allowed = {
        "fs.read": "Lectura de archivos del proyecto",
        "fs.write_project": "Escritura acotada dentro de project/",
        "json.validate": "Validación de contratos JSON",
        "markdown.write": "Generación de documentación markdown",
        "token.estimate": "Estimación heurística de tokens",
        "context.pack": "Construcción de paquetes de contexto",
        "evidence.write": "Registro de evidencia trazable",
        "ledger.write": "Registro de consumo",
        "test.run": "Ejecución de pruebas locales",
    }
    blocked = {
        "shell.free": "Ejecución libre de shell",
        "secrets.read": "Lectura de secretos",
        "deploy.direct": "Despliegue directo",
        "memory.write_ungated": "Escritura de memoria sin gate",
        "external.write_unapproved": "Escritura externa no aprobada",
        "db.write": "Escritura en base de datos",
    }
    registry = {k: ToolSpec(k, v, True, False) for k, v in allowed.items()}
    registry.update({k: ToolSpec(k, v, False, True) for k, v in blocked.items()})
    return registry


def skill_registry() -> dict[str, SkillSpec]:
    skills = {
        "requirements_extraction": "Extrae casos de uso, reglas, restricciones y criterios de aceptación.",
        "context_retrieval": "Busca contexto mínimo suficiente por source_id y chunk_id.",
        "frontend_architecture": "Diseña arquitectura frontend y experiencia pública/privada.",
        "security_review": "Revisa controles de seguridad, 2FA, sesiones y datos sensibles.",
        "qa_checklist": "Construye checklist de completitud y aceptación.",
        "test_design": "Define pruebas funcionales, accesibilidad y prototipo.",
        "technical_docs": "Genera documentación técnica trazable.",
        "observability": "Genera logs, métricas y reporte de ejecución.",
        "token_accounting": "Calcula consumo estimado por fase y agente.",
        "token_context_compaction": "Reduce contexto repetido, limita salidas y prioriza IDs de evidencia.",
    }
    return {k: SkillSpec(k, v, "low" if "token" in k or "context" in k else "medium") for k, v in skills.items()}


def agent_registry() -> dict[str, AgentSpec]:
    mp = deterministic_model_policy
    specs = [
        AgentSpec("agent.spec_detallada", "Especificador funcional", ["requirements_extraction"], ["fs.read", "json.validate", "evidence.write"], model_policy=mp()),
        AgentSpec("agent.qa_checklist", "QA de completitud", ["qa_checklist"], ["json.validate", "markdown.write"], model_policy=mp()),
        AgentSpec("agent.context_rag", "Curador de contexto", ["context_retrieval", "token_context_compaction"], ["fs.read", "context.pack", "token.estimate"], model_policy=mp()),
        AgentSpec("agent.ocr_ui_analyst", "Analista de anexos visuales", ["requirements_extraction"], ["fs.read", "evidence.write"], model_policy=mp()),
        AgentSpec("agent.architect_plan", "Arquitecto de solución", ["frontend_architecture"], ["markdown.write", "evidence.write"], model_policy=mp()),
        AgentSpec("agent.ui_web_modern", "Diseñador UX/UI", ["frontend_architecture"], ["markdown.write"], model_policy=mp()),
        AgentSpec("agent.api_security_docs", "Documentador de contratos e integración", ["technical_docs", "security_review"], ["markdown.write"], model_policy=mp()),
        AgentSpec("agent.security_policy", "Revisor de seguridad", ["security_review"], ["json.validate", "markdown.write"], model_policy=mp()),
        AgentSpec("agent.tests_coverage", "Diseñador de cobertura de pruebas", ["test_design"], ["test.run", "markdown.write"], model_policy=mp()),
        AgentSpec("agent.implementacion_doc_code", "Implementador documental/código", ["technical_docs"], ["fs.write_project", "markdown.write"], model_policy=mp()),
        AgentSpec("agent.token_billing", "Auditor de consumo", ["token_accounting"], ["token.estimate", "ledger.write"], model_policy=mp()),
        AgentSpec("agent.observability_sre", "Observabilidad SRE", ["observability"], ["ledger.write", "markdown.write"], model_policy=mp()),
        AgentSpec("agent.doc_tecnica_detalle", "Documentador técnico final", ["technical_docs"], ["markdown.write", "evidence.write"], model_policy=mp()),
        AgentSpec("agent.token_economizer", "Optimizador de tokens", ["token_context_compaction", "token_accounting"], ["token.estimate", "context.pack", "ledger.write"], model_policy=mp()),
    ]
    return {s.agent_id: s for s in specs}


def registry_snapshot() -> dict[str, Any]:
    return {
        "tools": {k: asdict(v) for k, v in tool_registry().items()},
        "skills": {k: asdict(v) for k, v in skill_registry().items()},
        "agents": {k: asdict(v) for k, v in agent_registry().items()},
    }
