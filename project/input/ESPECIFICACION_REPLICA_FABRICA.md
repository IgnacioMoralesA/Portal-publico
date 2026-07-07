# Especificacion para replicar la Fabrica Web ARNES SDD

Fecha de analisis: 2026-06-18

## 1. Proposito

Esta fabrica es un arnes local y deterministico para producir proyectos web mediante un ciclo SDD controlado. Su objetivo no es ejecutar agentes autonomos reales contra herramientas externas, sino estructurar el trabajo de agentes mediante:

- Work orders estrictos.
- Registro versionado de agentes, skills y herramientas.
- Ejecucion unica por `HarnessRunner.run_agent(agent_id, state)`.
- Evidencia trazable por `context-pack.json` y `evidence-register.json`.
- Memoria aislada por fabrica, proyecto y agente.
- Gates de schema, evidencia, policy, safety, consistencia, cobertura, budget, tool output y formato final.
- Observabilidad en JSONL, ledger de consumo y reportes de cierre.

Estado actual observado:

- Version de fabrica: `1.0.0`.
- Nombre: `Fabrica_Web_ARNES_SDD`.
- Paquete principal: `factory/`.
- Proyecto activo: `project/`.
- Ultimo run registrado: `project/runs/RUN-bacb52f15124`.
- Verificacion del ultimo run: `complete`.
- Agentes registrados: 13.
- Skills registradas: 15.
- Tools registradas: 27.

## 2. Estructura actual

```text
.
|-- Aprendizaje.md
|-- factory/
|   |-- __init__.py
|   |-- agents.py
|   |-- cli.py
|   |-- constants.py
|   |-- context.py
|   |-- harness.py
|   |-- memory.py
|   |-- observability.py
|   |-- orchestrator.py
|   |-- policy.py
|   |-- registry.py
|   |-- schemas.py
|   |-- utils.py
|   `-- validators.py
|-- tests/
|   `-- test_factory.py
`-- project/
    |-- README.md
    |-- Aprendizaje.md
    |-- latest-run.json
    |-- registry-summary.json
    |-- tool-availability.json
    |-- agent-memory/
    |-- cache/
    |-- index/
    |-- runs/
    |-- PROYECTO CINCO/
    `-- PROYECTO_CINCO_APP/
```

Para replicar la fabrica base, copiar principalmente:

- `factory/`
- `tests/`
- `Aprendizaje.md`
- Opcionalmente `project/README.md` como plantilla minima

No copiar como base limpia:

- `factory/__pycache__/`
- `tests/__pycache__/`
- `.pytest_cache/`
- `project/runs/`
- `project/cache/`
- `project/index/`
- `project/PROYECTO_CINCO_APP/` salvo que se quiera conservar la app de ejemplo
- `project/PROYECTO CINCO/` salvo que se quiera conservar el brief de ejemplo

## 3. Componentes principales

### 3.1 `factory/constants.py`

Define identidad, versiones, fases, documentos fuente y politicas globales.

Elementos clave:

- `FACTORY_NAME`
- `FACTORY_VERSION`
- `SCHEMA_VERSION`
- `POLICY_VERSION`
- `TOOL_REGISTRY_VERSION`
- `MEMORY_VERSION`
- `WORKFLOW_VERSION`
- `INDEX_VERSION`
- `RERANKER_VERSION`
- `MODEL_SNAPSHOT`
- `MODEL_SEED`
- `FINAL_STATUSES`
- `DESIGN_DOCS`
- `SDD_PHASES`
- `APPROVAL_REQUIRED_FOR`

Fases declaradas:

```text
intake
specify
clarify
checklist
context
plan
plan_validation
tasks
analyze
implement
validate
pr_deploy
observe
close
```

Nota: `DESIGN_DOCS` referencia varios documentos de diseno que no estan presentes en la raiz actual, por ejemplo `01_Constitucion_y_Especificacion_Fabrica.md`. El `ContextManager` ignora los ausentes y usa los que existen. Para una replica robusta, crear esos documentos o ajustar `DESIGN_DOCS`.

### 3.2 `factory/schemas.py`

Implementa un validador JSON Schema reducido y estricto:

- Bloquea propiedades adicionales cuando `additionalProperties` es `False`.
- Valida tipos.
- Valida enums.
- Valida objetos y arreglos anidados.

Contratos principales:

- `WORK_ORDER_SCHEMA`
- `CYCLE_STATE_SCHEMA`
- `AGENT_RESULT_SCHEMA`

Estados finales permitidos:

```text
complete
needs_user_input
not_answerable
error
```

### 3.3 `factory/registry.py`

Contiene los dataclasses y registros versionados.

Dataclasses:

- `ToolSpec`
- `SkillSpec`
- `AgentSpec`

Registros:

- `tool_registry()`
- `skill_registry()`
- `agent_registry()`

Herramientas prohibidas por defecto:

```text
shell.free
secrets.read
deploy.direct
memory.write_ungated
external.write_unapproved
db.write
```

La politica de modelo por agente es deterministica:

- `temperature: 0`
- `top_p: 1`
- `seed: 12345`
- `parallel_tool_calls: False`
- `response_format: strict_json_schema`

### 3.4 `factory/orchestrator.py`

Es el grafo de ejecucion de la fabrica.

Responsabilidades:

- Crear estructura de proyecto con `initialize_project()`.
- Normalizar objetivos a `work_order.json`.
- Crear `RUN-<hash>` por ejecucion.
- Escribir snapshots de registros en `registries/`.
- Ejecutar fases y agentes en orden fijo.
- Escribir `routing/CYC-xxx.json`.
- Delegar ejecucion real al arnes.
- Finalizar con `traceability-matrix.md`, `validation-report.json`, `final-report.json` y `CHECKLIST_APLICADO.md`.

Ruta actual:

| orden | fase | agentes |
|---:|---|---|
| 1 | specify | `agent.spec_detallada` |
| 2 | clarify | `agent.spec_detallada` |
| 3 | checklist | `agent.qa_checklist` |
| 4 | context | `agent.context_rag`, `agent.ocr_ui_analyst` |
| 5 | plan | `agent.architect_plan`, `agent.ui_web_modern`, `agent.api_security_docs` |
| 6 | plan_validation | `agent.security_policy`, `agent.qa_checklist` |
| 7 | tasks | `agent.architect_plan`, `agent.tests_coverage`, `agent.doc_tecnica_detalle` |
| 8 | analyze | `agent.qa_checklist`, `agent.security_policy` |
| 9 | implement | `agent.implementacion_doc_code` |
| 10 | validate | `agent.tests_coverage`, `agent.security_policy`, `agent.qa_checklist` |
| 11 | observe | `agent.token_billing`, `agent.observability_sre` |
| 12 | close | `agent.doc_tecnica_detalle`, `agent.token_billing`, `agent.qa_checklist` |

Aunque `SDD_PHASES` incluye `intake` y `pr_deploy`, la ruta actual no ejecuta agentes en `pr_deploy` y usa `intake` solo como estado inicial.

### 3.5 `factory/harness.py`

Es la puerta unica de ejecucion.

Flujo interno de `run_agent()`:

1. Valida `CycleState`.
2. Obtiene `AgentSpec`.
3. Ejecuta `PolicyEngine.check_agent()`.
4. Evalua side effects del estado.
5. Inicializa y reporta memoria con `MemoryGate`.
6. Construye `context-pack.json` y `evidence-register.json`.
7. Valida cada tool allowlisted con policy.
8. Ejecuta la funcion del agente en `AGENT_FUNCTIONS`.
9. Actualiza budget simulado.
10. Corre `ValidatorChain`.
11. Escribe `agent-results/`.
12. Escribe logs de agente, tools, billing y evento global.

Observacion importante: si `PolicyEngine.check_tool()` devuelve `needs_user_input` por side effects de tipo `write` o `external`, el arnes lo registra como bloqueado, pero no detiene el flujo porque solo corta con estados distintos de `complete` y `needs_user_input`. Si la replica requiere aprobaciones estrictas, cambiar esta condicion.

### 3.6 `factory/agents.py`

Define agentes como funciones deterministicas que escriben artefactos Markdown/JSON.

No hay llamadas reales a modelos ni herramientas externas. Cada agente produce una salida estructurada con:

- `agent_id`
- `phase`
- `generated_at`
- `evidence_refs`
- `critical_claims`
- `policy_findings`
- `artifacts`
- `coverage`

Mapa final:

```python
AGENT_FUNCTIONS = {
    "agent.spec_detallada": spec_detallada,
    "agent.context_rag": context_rag,
    "agent.architect_plan": architect_plan,
    "agent.ui_web_modern": ui_web_modern,
    "agent.api_security_docs": api_security_docs,
    "agent.implementacion_doc_code": implementacion_doc_code,
    "agent.tests_coverage": tests_coverage,
    "agent.qa_checklist": qa_checklist,
    "agent.doc_tecnica_detalle": doc_tecnica_detalle,
    "agent.ocr_ui_analyst": ocr_ui_analyst,
    "agent.security_policy": security_policy,
    "agent.token_billing": token_billing,
    "agent.observability_sre": observability_sre,
}
```

### 3.7 `factory/context.py`

Implementa recuperacion local deterministica.

Proceso:

1. Lee documentos autorizados en `DESIGN_DOCS`.
2. Divide por encabezados `##`.
3. Calcula hashes SHA-256.
4. Rankea por coincidencia de terminos.
5. Aplica rerank fijo.
6. Deduplica por fuente y hash.
7. Si no hay matches, usa fallback minimo de documentos autorizados.
8. Escribe:
   - `context-pack.json`
   - `evidence-register.json`

Este modulo es clave para la politica de "no inventar": los claims criticos deben referenciar evidencia.

### 3.8 `factory/memory.py`

Gobierna memoria persistente.

Archivos y directorios:

- `Aprendizaje.md` en raiz de fabrica.
- `project/Aprendizaje.md` por proyecto.
- `project/agent-memory/` para memoria por agente.

Reglas:

- Solo memoria aprobada, limpia, vigente y relevante.
- Separacion entre scope de fabrica, proyecto y agente.
- Propuestas de memoria pasan por schema, aprobacion y taint status.

### 3.9 `factory/policy.py`

Aplica controles de seguridad y permisos.

Bloqueos:

- Ningun agente puede desplegar.
- Ningun agente puede leer secretos.
- Toda tool debe existir en `tool_registry`.
- La tool debe estar en `allowed_tools` del agente.
- Tools globalmente prohibidas quedan bloqueadas.
- Tests deben requerir sandbox.
- Side effects `write` y `external` requieren aprobacion.

### 3.10 `factory/validators.py`

Cadena de validadores:

1. `SchemaValidator`
2. `EvidenceValidator`
3. `PolicyValidator`
4. `SafetyValidator`
5. `ConsistencyValidator`
6. `CoverageValidator`
7. `BudgetValidator`
8. `ToolOutputValidator`
9. `FinalFormatValidator`

Codigos que cortan:

```text
policy_denied
missing_critical_evidence
unsafe_action
budget_exceeded
schema_unrecoverable
```

Marcadores simples de secreto:

```text
BEGIN RSA PRIVATE KEY
OPENAI_API_KEY
password=
Authorization: Bearer
```

### 3.11 `factory/observability.py`

Escribe trazas operativas:

- `log.jsonl`
- `agent-logs/<agent_id>.jsonl`
- `tool-logs/<tool_id>.jsonl`
- `billing-ledger.json`

El ledger usa costo estimado `0` porque no hay pricing real configurado.

### 3.12 `factory/cli.py`

Comandos disponibles:

```powershell
python -m factory.cli init-project --project project
python -m factory.cli run --project project --objective "<objetivo>"
python -m factory.cli verify --project project
python -m factory.cli verify --project project --run project/runs/RUN-xxxx
python -m factory.cli list
python -m factory.cli list --output project/registry-summary.json
```

`init-project` crea:

- `project/runs/`
- `project/cache/`
- `project/index/`
- `project/agent-memory/`
- `project/Aprendizaje.md`
- `project/README.md`
- `project/tool-availability.json`

`run` crea un run y escribe `project/latest-run.json`.

`verify` comprueba artefactos minimos y registra `verification-summary.json`.

## 4. Agentes actuales

| agente | responsabilidad |
|---|---|
| `agent.spec_detallada` | Convertir work order en especificacion, requisitos y aclaraciones. |
| `agent.context_rag` | Recuperar contexto y generar evidencia. |
| `agent.architect_plan` | Crear plan tecnico, contratos y tareas trazables. |
| `agent.ui_web_modern` | Definir buenas practicas UI web. |
| `agent.api_security_docs` | Generar contrato OpenAPI y guia de API segura. |
| `agent.implementacion_doc_code` | Reportar implementacion documentada. |
| `agent.tests_coverage` | Plan de pruebas y reporte de cobertura. |
| `agent.qa_checklist` | Checklist, analisis y aprobacion de cierre. |
| `agent.doc_tecnica_detalle` | Documentacion tecnica, decisiones, estado y errores. |
| `agent.ocr_ui_analyst` | Analisis de pantallas autorizadas. |
| `agent.security_policy` | Revision de seguridad y permisos. |
| `agent.token_billing` | Ledger de tokens, tools, latencia y costo. |
| `agent.observability_sre` | Observabilidad, logs y operabilidad. |

## 5. Tools actuales

Categorias:

- Archivos: `tool.files.read`, `tool.files.write_dry_run`
- Recuperacion/cache: `tool.index.query`, `tool.cache.get`, `tool.cache.set`, `tool.repo.ast.parse`, `tool.sql.parse`, `tool.db.metadata.readonly`
- Tests: `tool.test.pytest`, `tool.test.vitest`, `tool.test.playwright`
- Lint/typecheck: `tool.lint.eslint`, `tool.lint.ruff`, `tool.typecheck.tsc`, `tool.typecheck.pyright`
- Seguridad: `tool.security.semgrep`, `tool.security.trivy`, `tool.security.gitleaks`, `tool.security.pip_audit`, `tool.security.npm_audit`
- API: `tool.api.openapi.validate`
- OCR: `tool.ocr.screen`
- Observabilidad: `tool.obs.billing`
- Validadores: `tool.validator.schema`, `tool.validator.final_format`
- Memoria: `tool.memory.propose`

Disponibilidad detectada en `project/tool-availability.json`:

- Disponibles con comando: `npm`, `pytest`.
- No disponibles actualmente: `gitleaks`, `semgrep`, `trivy`.
- Varias tools son logicas internas sin comando externo y se marcan disponibles.

## 6. Skills actuales

| skill | proposito |
|---|---|
| `skill.normalize_work_order` | Normalizar brief a WorkOrder. |
| `skill.chunk_and_hash` | Chunking deterministico con hash. |
| `skill.retrieve_context` | Recuperacion con threshold, rerank y dedupe. |
| `skill.compact_context` | Compactar contexto con evidencia. |
| `skill.validate_schema` | Validar JSON schema estricto. |
| `skill.validate_evidence` | Validar claims criticos. |
| `skill.plan_tests` | Crear matriz de pruebas por riesgo. |
| `skill.run_unit_tests` | Ejecutar unit tests sandbox. |
| `skill.run_e2e_tests` | Ejecutar E2E UI. |
| `skill.scan_security` | Escaneo SAST, secretos y dependencias. |
| `skill.ocr_screen` | Analizar imagen autorizada. |
| `skill.generate_openapi` | Generar contrato OpenAPI. |
| `skill.write_docs` | Escribir docs markdown. |
| `skill.record_billing` | Consolidar ledger. |
| `skill.propose_memory` | Proponer memoria gobernada. |

## 7. Artefactos esperados por run

Archivos raiz de un run completo:

```text
work_order.json
state.json
spec.md
clarifications.md
checklist.md
context-pack.json
context-pack.md
evidence-register.json
plan.md
contracts.md
tasks.md
analyze-report.json
test-plan.md
test-report.md
coverage-report.json
security-review.md
validation-report.json
traceability-matrix.md
final-report.json
RUN_STATE.md
DECISIONS.md
ERRORS.md
billing-ledger.json
CHECKLIST_APLICADO.md
verification-summary.json
```

Directorios de un run:

```text
agent-logs/
agent-results/
docs/
registries/
routing/
tool-logs/
```

Registros congelados por run:

```text
registries/agents.json
registries/tools.json
registries/skills.json
```

La verificacion CLI exige los artefactos minimos y que `final-report.json.status` sea `complete`.

## 8. WorkOrder base

`normalize_work_order(objective)` produce un objeto con:

- `work_order_id`: `WO-` + hash del objetivo.
- `objective`: texto del usuario.
- `work_type`: actualmente `factory_bootstrap`.
- `scope.include`: `fabrica`, `arnes`, `agentes`, `skills`, `tools`, `qa`, `logs`, `project`.
- `scope.exclude`: `deploy`, `merge`, `db_write`, `secret_read`, `external_write`.
- `inputs`: brief de usuario y docs locales.
- `constraints`: `no_web`, `dry_run`, `sandbox_required`, max retries, riesgo, costo y latencia.
- `expected_outputs`: project ready, agentes registrados, QA, trazabilidad y reporte final.
- `approval_required_for`: writes, deploy, merge, API externa, secretos, infra, costos, data access, produccion y DB write.

Para otros tipos de fabrica, cambiar:

- `work_type`
- `scope`
- `inputs`
- `constraints`
- `expected_outputs`
- `approval_required_for`
- Schema si se agregan campos nuevos.

## 9. Proyecto de ejemplo generado

`project/PROYECTO_CINCO_APP/` es una salida de ejemplo de la fabrica.

Patron observado:

- App local sin servicios externos.
- Backend Python stdlib.
- API REST bajo `/api/v1`.
- Frontend SPA en `web/`.
- Persistencia JSON local en `data/erp.json`.
- Tests en `tests/test_app.py`.
- Documentacion tecnica en `docs/`.
- Golden set browser en `tests/golden-set-runner.js` y `web/golden-set.html`.

Este proyecto no es necesario para replicar la fabrica base, pero sirve como referencia de artefactos de producto.

## 10. Como replicar con cambios

### Paso 1 - Crear copia limpia

Copiar:

```text
factory/
tests/
Aprendizaje.md
```

Crear un `project/` vacio o dejar que CLI lo cree.

Evitar copiar runs y caches.

### Paso 2 - Cambiar identidad y versiones

Editar `factory/constants.py`:

- `FACTORY_NAME`
- `FACTORY_VERSION`
- `WORKFLOW_VERSION`
- `POLICY_VERSION`
- `MODEL_SNAPSHOT`
- `MODEL_SEED`
- `DESIGN_DOCS`
- `SDD_PHASES`
- `APPROVAL_REQUIRED_FOR`

Si se cambia el flujo de aprobaciones, actualizar tests de policy.

### Paso 3 - Definir documentos fuente

Crear o ajustar los documentos en `DESIGN_DOCS`.

Recomendacion minima:

```text
01_Constitucion_y_Especificacion_Fabrica.md
02_Arquitectura_Stack_y_Flujos_SDD.md
03_Agentes_Skills_Herramientas_y_Permisos.md
04_Orquestador_Ciclo_Operabilidad.md
CHECKLIST.md
buenas_practicas.md
```

Cada documento debe usar encabezados `##` para mejorar el chunking deterministico.

### Paso 4 - Cambiar o agregar tools

Editar `tool_registry()` en `factory/registry.py`.

Para cada tool definir:

- `tool_id`
- `name`
- `version`
- `purpose`
- `type`
- `permissions`
- `side_effects`
- `sandbox_required`
- `idempotent`
- `timeout_ms`
- `max_retries`
- `cost_class`
- `available_command` si corresponde

Actualizar:

- Allowed tools de agentes.
- `PolicyEngine` si hay reglas nuevas.
- Tests de registry y policy.
- `tool-availability.json` ejecutando `init-project`.

### Paso 5 - Cambiar o agregar skills

Editar `skill_registry()` en `factory/registry.py`.

Para cada skill definir:

- `skill_id`
- `type`
- `purpose`
- `tool_id`
- `cache_key`
- `gates`

Si una skill empieza a ejecutar codigo real, mover la logica a un modulo propio y mantener el output validable por schema.

### Paso 6 - Cambiar o agregar agentes

Para agregar un agente:

1. Crear una funcion en `factory/agents.py` con firma:

```python
def mi_agente(agent: AgentSpec, state: dict[str, Any], run_dir: Path, context_pack: dict[str, Any]) -> dict[str, Any]:
    ...
```

2. Devolver un output compatible con los validadores.
3. Registrar la funcion en `AGENT_FUNCTIONS`.
4. Agregar `AgentSpec` en `agent_registry()`.
5. Incluirlo en `OrchestratorGraph.ROUTE`.
6. Agregar pruebas.

Campos criticos de `AgentSpec`:

- `agent_id`
- `purpose`
- `single_responsibility`
- `use_when`
- `do_not_use_when`
- `allowed_tools`
- `forbidden_tools`
- `permissions`
- `model_policy`
- `budget`
- `memory`
- `gates`

### Paso 7 - Cambiar la ruta SDD

Editar `OrchestratorGraph.ROUTE`.

Reglas recomendadas:

- Mantener fases cortas y auditables.
- No mezclar implementacion, validacion y cierre en un mismo agente.
- Agregar `routing/CYC-xxx.json` por cada decision.
- Si se agrega una fase nueva, incluirla tambien en `SDD_PHASES`.
- Si se usa `pr_deploy`, exigir aprobacion humana.

### Paso 8 - Ajustar schemas

Editar `factory/schemas.py` cuando se agreguen campos o contratos.

Regla de compatibilidad:

- Todo campo nuevo debe aparecer en `properties`.
- Si es obligatorio, agregarlo en `required`.
- Mantener `additionalProperties: False` para contratos cerrados.
- Actualizar tests negativos.

### Paso 9 - Ajustar validadores

Editar `factory/validators.py` si cambian gates o estados.

Casos tipicos:

- Agregar validador de dependencia.
- Hacer bloqueante `needs_user_input`.
- Validar formato de nuevos artefactos.
- Validar hashes de outputs.
- Validar cobertura minima real.

### Paso 10 - Inicializar y ejecutar

```powershell
python -m factory.cli init-project --project project
python -m factory.cli run --project project --objective "Preparar nueva fabrica con cambios X"
python -m factory.cli verify --project project
```

### Paso 11 - Probar

Suite base:

```powershell
python -m pytest -q tests -p no:cacheprovider
```

Agregar pruebas para:

- Schema positivo/negativo.
- Registry con agentes, tools y skills esperadas.
- Policy de tools no permitidas.
- Bloqueo de secretos.
- Context pack deterministico.
- Memoria por proyecto.
- Run completo del orquestador.
- Verify CLI.

## 11. Puntos de cambio frecuentes

| objetivo de cambio | archivos | pruebas minimas |
|---|---|---|
| Cambiar nombre/version de fabrica | `factory/constants.py`, `factory/__init__.py` | `test_orchestrator_bootstrap_run` |
| Agregar una fase | `constants.py`, `orchestrator.py` | schema de `CycleState`, run completo |
| Agregar agente | `registry.py`, `agents.py`, `orchestrator.py` | registry, run completo, artefactos |
| Agregar herramienta | `registry.py`, `policy.py` | policy allow/deny, tool availability |
| Cambiar aprobaciones | `constants.py`, `policy.py`, `harness.py` | side effects, deploy, secrets |
| Cambiar evidencia/RAG | `constants.py`, `context.py` | determinismo, evidence register |
| Cambiar memoria | `memory.py`, `Aprendizaje.md` | aislamiento por proyecto |
| Agregar artefacto final | `agents.py`, `orchestrator.py`, `cli.py` | verify, final format |
| Pasar de templates a LLM real | `harness.py`, nuevos adapters | schema, budget, retries, mocks |

## 12. Reglas para mantener la fabrica replicable

- Un solo punto de ejecucion de agentes: `harness.run_agent`.
- Ninguna tool fuera de `tool_registry`.
- Ningun agente con permisos de deploy o secretos.
- Todo output critico debe tener evidencia.
- Todo run debe congelar registros en `registries/`.
- Los contratos deben ser cerrados.
- La memoria persistente no se escribe directo: se propone y se aprueba.
- Los artefactos deben ser idempotentes y regenerables.
- Los hashes deben calcularse con JSON estable.
- No mezclar artefactos de ejemplo con la plantilla base.

## 13. Observaciones y riesgos actuales

1. Faltan varios documentos fuente declarados en `DESIGN_DOCS`. El sistema funciona porque ignora ausentes y usa fallback, pero una replica deberia incluirlos.
2. Los agentes son funciones deterministicas. Para usar agentes reales con LLM, falta un adapter de modelo, manejo de errores, retries, limites de tokens reales y mocks de prueba.
3. `needs_user_input` en policy de tool no detiene el flujo actual. Para una fabrica estricta, bloquear hasta aprobacion.
4. `project/PROYECTO_CINCO_APP/docs/architecture-components.md` contiene contenido duplicado y bloques Mermaid anidados; conviene corregir el generador de docs si se usa como referencia.
5. `utils.env_hash()` usa `python3 --version`, lo que puede fallar o variar en Windows. Conviene usar `sys.version` si se formaliza.
6. No hay `pyproject.toml` ni `requirements.txt`. La fabrica base usa stdlib, pero las pruebas requieren `pytest`.
7. La disponibilidad de herramientas de seguridad externas no es completa: `gitleaks`, `semgrep` y `trivy` aparecen como no disponibles.
8. La verificacion CLI cubre artefactos, pero no valida contenido profundo de cada Markdown.
9. El contrato textual en `agents.py` menciona `analyze-report.md`, pero el artefacto real es `analyze-report.json`. Mantener nombres alineados en una replica.

## 14. Plantilla minima de nueva fabrica

```text
NUEVA_FABRICA/
|-- Aprendizaje.md
|-- factory/
|   |-- __init__.py
|   |-- agents.py
|   |-- cli.py
|   |-- constants.py
|   |-- context.py
|   |-- harness.py
|   |-- memory.py
|   |-- observability.py
|   |-- orchestrator.py
|   |-- policy.py
|   |-- registry.py
|   |-- schemas.py
|   |-- utils.py
|   `-- validators.py
|-- tests/
|   `-- test_factory.py
|-- docs/
|   |-- 01_constitucion.md
|   |-- 02_arquitectura.md
|   |-- 03_agentes_tools_permisos.md
|   |-- 04_operabilidad.md
|   `-- checklist.md
`-- project/
    `-- README.md
```

## 15. Checklist de replica

Antes de considerar lista una copia modificada:

- [ ] `FACTORY_NAME` y versiones actualizadas.
- [ ] `DESIGN_DOCS` existe y apunta a documentos reales.
- [ ] `agent_registry()` coincide con `AGENT_FUNCTIONS`.
- [ ] Cada agente tiene tools permitidas y permisos minimos.
- [ ] `OrchestratorGraph.ROUTE` solo usa agentes registrados.
- [ ] `WORK_ORDER_SCHEMA`, `CYCLE_STATE_SCHEMA` y `AGENT_RESULT_SCHEMA` validan los nuevos contratos.
- [ ] `PolicyEngine` bloquea secretos, deploy, DB write y tools no registradas.
- [ ] `ValidatorChain` cubre los gates nuevos.
- [ ] `MemoryGate` mantiene separacion fabrica/proyecto/agente.
- [ ] `ContextManager` genera evidence register util.
- [ ] `verify` exige los artefactos finales correctos.
- [ ] Tests pasan.
- [ ] Un run de prueba termina en `final-report.json.status = complete`.

