"""Orquestador SDD de la fábrica."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .constants import FACTORY_NAME, FACTORY_VERSION, ROUTE, SOURCE_DOCUMENTS, TOKEN_ECONOMY_POLICY
from .context import build_context_pack, write_context_pack
from .harness import HarnessRunner
from .observability import append_jsonl, write_json
from .registry import registry_snapshot
from .validators import validate_agent_result, validate_required_run_artifacts, validate_work_order_file


def _run_id(objective: str) -> str:
    seed = f"{objective}|{datetime.now(timezone.utc).isoformat()}".encode()
    return "RUN-" + hashlib.sha256(seed).hexdigest()[:12]


def initialize_project(project_dir: Path) -> None:
    for rel in ["input", "runs", "agent-memory", "cache", "index"]:
        (project_dir / rel).mkdir(parents=True, exist_ok=True)
    readme = project_dir / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Proyecto Fábrica ClaveÚnica\n\nColoca documentos fuente en `input/` y ejecuta `python -m factory.cli run`.\n",
            encoding="utf-8",
        )


def create_work_order(project_dir: Path, objective: str, economy_mode: bool = True) -> dict[str, Any]:
    work_order = {
        "work_order_id": "WO-" + hashlib.sha256(objective.encode()).hexdigest()[:10],
        "objective": objective,
        "economy_mode": economy_mode,
        "sources": SOURCE_DOCUMENTS,
        "constraints": [
            "No ejecutar tools bloqueadas.",
            "No insertar documentos completos en cada prompt.",
            "Mantener trazabilidad por source_id, CU, FUN, RN, CH y EX.",
            "Validar presupuesto de tokens antes de cada agente.",
        ],
        "acceptance": [
            "Run con estado complete o needs_user_input justificado.",
            "Context-pack dentro de presupuesto.",
            "Matriz de trazabilidad creada.",
            "Reporte final y validación creados.",
        ],
    }
    return work_order


def run_project(project_dir: Path, objective: str, economy_mode: bool = True, max_context_tokens: int | None = None) -> Path:
    initialize_project(project_dir)
    max_context_tokens = max_context_tokens or TOKEN_ECONOMY_POLICY["max_context_tokens_per_agent"]
    rid = _run_id(objective)
    run_dir = project_dir / "runs" / rid
    run_dir.mkdir(parents=True, exist_ok=True)

    work_order = create_work_order(project_dir, objective, economy_mode=economy_mode)
    write_json(run_dir / "work_order.json", work_order)
    validate_work_order_file(run_dir / "work_order.json")

    write_json(run_dir / "registries" / "registry-snapshot.json", registry_snapshot())
    context_path = write_context_pack(project_dir, run_dir, objective, max_tokens=max_context_tokens)
    context_pack = json.loads(context_path.read_text(encoding="utf-8"))
    context_text = json.dumps(context_pack, ensure_ascii=False)

    runner = HarnessRunner(max_context_tokens=max_context_tokens)
    evidence: list[dict[str, Any]] = []
    agent_results: list[dict[str, Any]] = []

    for order, (phase, agents) in enumerate(ROUTE, start=1):
        routing = {"order": order, "phase": phase, "agents": agents}
        write_json(run_dir / "routing" / f"CYC-{order:03d}.json", routing)
        for agent_id in agents:
            result = runner.run_agent(agent_id, {
                "phase": phase,
                "objective": objective,
                "economy_mode": economy_mode,
                "context_text": context_text,
            })
            validate_agent_result(result)
            agent_results.append(result)
            evidence.append({
                "phase": phase,
                "agent_id": agent_id,
                "evidence": result["evidence"],
                "status": result["status"],
            })
            append_jsonl(run_dir / "observability.jsonl", {
                "event": "agent_completed",
                "phase": phase,
                "agent_id": agent_id,
                "status": result["status"],
                "token_ledger": result["token_ledger"],
            })

    write_json(run_dir / "agent-results.json", agent_results)
    write_json(run_dir / "evidence-register.json", evidence)
    _write_traceability(run_dir)
    _write_validation_report(run_dir, agent_results)
    _write_final_report(run_dir, objective, context_pack, agent_results)

    missing = validate_required_run_artifacts(run_dir)
    status = "complete" if not missing and all(r["status"] == "complete" for r in agent_results) else "needs_user_input"
    write_json(project_dir / "latest-run.json", {"run_id": rid, "path": str(run_dir), "status": status, "missing": missing})
    return run_dir


def _write_traceability(run_dir: Path) -> None:
    content = """# Matriz de trazabilidad

| Bloque | Cobertura esperada | Evidencia base | Agentes responsables |
|---|---|---|---|
| Portal público | Accesos activar, autenticar, recuperar, ayuda y novedades | S06:HU01, S08:CU_001 | spec, ui, qa |
| Datos personales | Cambio de teléfono/correo con factor de seguridad | S06:HU02, S08:CU_002 | spec, security, tests |
| 2FA | Activación opcional y exigencia al login si está activo | S06:HU03, S08:CU_003 | spec, security, tests |
| Sesiones | Política de multisesión y mitigación de secuestro | S06:HU04, S08:CU_004 | security, qa |
| DDU | Derivación, cancelación, retorno y alerta pendiente | S06:HU05-HU12, S07, S08:CU_005-CU_012 | architect, api, tests |
| Notificaciones | Listado y detalle desde CasillaÚnica | S06:HU09-HU11, S07 | ui, api, tests |
| Autorizaciones | Historial, pendientes, aprobación, rechazo y revocación | S06:HU13-HU16, S08:CU_013-CU_016 | architect, security, tests |
| Calidad | Pruebas frontend, prototipo, accesibilidad y evidencia | S05 | tests, qa |
| Garantía | Cobertura mínima de calidad, funcionamiento, compatibilidad, rendimiento, seguridad y estabilidad | S05 | doc, qa |
"""
    (run_dir / "traceability-matrix.md").write_text(content, encoding="utf-8")


def _write_validation_report(run_dir: Path, results: list[dict[str, Any]]) -> None:
    report = {
        "status": "complete" if all(r["status"] == "complete" for r in results) else "needs_user_input",
        "agents": len(results),
        "complete": sum(1 for r in results if r["status"] == "complete"),
        "needs_user_input": sum(1 for r in results if r["status"] == "needs_user_input"),
        "token_budget_ok": all(r["token_ledger"]["within_budget"] for r in results),
    }
    write_json(run_dir / "validation-report.json", report)


def _write_final_report(run_dir: Path, objective: str, context_pack: dict[str, Any], results: list[dict[str, Any]]) -> None:
    total_tokens = sum(r["token_ledger"]["total"] for r in results)
    content = f"""# Reporte final de fábrica

## Objetivo

{objective}

## Estado

- Fábrica: {FACTORY_NAME} {FACTORY_VERSION}
- Estado: {'complete' if all(r['status'] == 'complete' for r in results) else 'needs_user_input'}
- Agentes ejecutados: {len(results)}
- Contexto estimado: {context_pack.get('estimated_tokens')} tokens
- Consumo total estimado de agentes: {total_tokens} tokens
- Economía de tokens: activa

## Decisiones

1. El documento funcional consolidado es la fuente prioritaria para CU/FUN/RN/CH/EX.
2. Los anexos visuales y administrativos se mantienen como evidencia de apoyo.
3. El trabajo de agentes se controla con gates de schema, evidencia, seguridad, presupuesto y formato final.
4. No se deben reenviar documentos completos a cada agente.

## Próximos pasos

1. Revisar `traceability-matrix.md`.
2. Convertir cobertura en backlog técnico.
3. Implementar prototipo por módulos.
4. Ejecutar pruebas de accesibilidad y prototipo.
"""
    (run_dir / "final-report.json").write_text(json.dumps({
        "objective": objective,
        "factory": FACTORY_NAME,
        "version": FACTORY_VERSION,
        "status": "complete" if all(r["status"] == "complete" for r in results) else "needs_user_input",
        "estimated_total_tokens": total_tokens,
        "summary_markdown": content,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    (run_dir / "final-report.md").write_text(content, encoding="utf-8")
