"""Ejecución determinística de agentes."""

from __future__ import annotations

from typing import Any

from .registry import agent_registry
from .token_budget import TokenLedger, estimate_tokens


class HarnessRunner:
    """Runner local. No ejecuta agentes autónomos externos; normaliza trabajo y artefactos."""

    def __init__(self, max_context_tokens: int = 3500) -> None:
        self.max_context_tokens = max_context_tokens
        self.agents = agent_registry()

    def run_agent(self, agent_id: str, state: dict[str, Any]) -> dict[str, Any]:
        if agent_id not in self.agents:
            raise ValueError(f"Agente no registrado: {agent_id}")

        phase = state.get("phase", "unknown")
        context_text = state.get("context_text", "")
        objective = state.get("objective", "")
        ledger = TokenLedger(
            estimated_input_tokens=estimate_tokens(context_text + objective),
            estimated_output_tokens=300,
            max_context_tokens=self.max_context_tokens,
            economy_mode=state.get("economy_mode", True),
        )

        outputs = self._outputs_for(agent_id, state, ledger)
        return {
            "agent_id": agent_id,
            "phase": phase,
            "status": "complete" if ledger.within_budget else "needs_user_input",
            "outputs": outputs,
            "evidence": outputs.get("evidence", ["source-manifest.json", "context-pack.json"]),
            "token_ledger": ledger.as_dict(),
        }

    def _outputs_for(self, agent_id: str, state: dict[str, Any], ledger: TokenLedger) -> dict[str, Any]:
        if agent_id == "agent.spec_detallada":
            return {
                "summary": "Portal Ciudadano de ClaveÚnica con experiencia pública, privada, DDU, notificaciones, 2FA, sesiones y autorizaciones de datos sensibles.",
                "must_cover": ["CU_001-CU_021", "FUN_001+", "RN/CH/EX aplicables"],
                "evidence": ["S01", "S06", "S07", "S08"],
                "token_note": "Usar requerimientos ya deduplicados en S08; no releer anexos completos salvo brecha.",
            }
        if agent_id == "agent.context_rag":
            return {
                "summary": "Contexto mínimo curado desde manifest y especificación funcional.",
                "context_strategy": "source_manifest + excerpts + IDs de evidencia",
                "evidence": ["context-pack.json"],
            }
        if agent_id == "agent.token_economizer":
            return {
                "summary": "Economía de tokens aplicada.",
                "rules": [
                    "Máximo contexto por agente controlado por gate.",
                    "Reutilizar context-pack.json.",
                    "Citar source_id/chunk_id en vez de pegar texto largo.",
                    "Responder con deltas y listas breves.",
                ],
                "estimated_total_tokens": ledger.total,
                "within_budget": ledger.within_budget,
                "evidence": ["TOKEN_ECONOMY_POLICY", "context-pack.json"],
            }
        if agent_id == "agent.architect_plan":
            return {
                "summary": "Plan por módulos: portal público, autenticación/2FA, datos personales, sesiones, DDU/notificaciones, autorizaciones, ayuda institucional.",
                "deliverables": ["architecture.md", "task-backlog.md", "traceability-matrix.md"],
                "evidence": ["S08:CU_001-CU_021"],
            }
        if agent_id == "agent.ui_web_modern":
            return {
                "summary": "UX orientada a accesos claros: activar, autenticarse, recuperar, ayuda, novedades y secciones privadas.",
                "screens": ["Home pública", "Login/2FA", "Perfil", "DDU", "Notificaciones", "Autorizaciones"],
                "evidence": ["S06:HU01-HU16", "S07"],
            }
        if agent_id == "agent.security_policy":
            return {
                "summary": "Controles principales: 2FA opcional/obligatorio si activo, validación para cambios de contacto, política multisesión y datos sensibles.",
                "risks": ["Secuestro de sesión", "Cambio indebido de contacto", "Autorizaciones no trazadas"],
                "evidence": ["S06:HU02-HU04", "S08"],
            }
        if agent_id == "agent.tests_coverage":
            return {
                "summary": "Pruebas funcionales, prototipo y accesibilidad, con evidencia de ejecución.",
                "coverage_targets": ["CU_001-CU_021", "2FA", "DDU", "Notificaciones", "Autorizaciones", "Accesibilidad"],
                "evidence": ["S05", "S08"],
            }
        if agent_id == "agent.token_billing":
            return {
                "summary": "Ledger de consumo estimado generado.",
                "estimated_input_tokens": ledger.estimated_input_tokens,
                "estimated_output_tokens": ledger.estimated_output_tokens,
                "evidence": ["token-ledger.jsonl"],
            }
        return {
            "summary": f"{agent_id} ejecutado de forma determinística.",
            "evidence": ["context-pack.json", "source-manifest.json"],
        }
