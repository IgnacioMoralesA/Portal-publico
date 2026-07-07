# Blueprint de la Fábrica ClaveÚnica ARNES SDD

## Propósito

Implementar una fábrica local y determinística que organice el desarrollo del Portal Ciudadano de ClaveÚnica mediante work orders, agentes versionados, evidencia, gates y reportes.

## Alcance funcional base

El sistema objetivo es el Portal Ciudadano de ClaveÚnica, compuesto por experiencia pública y experiencia privada autenticada. Debe cubrir:

- Acceso público claro a activación, autenticación, recuperación, ayuda y novedades.
- Administración de datos personales con factor adicional de seguridad.
- Segundo factor de autenticación configurable.
- Gestión segura de sesiones/multisesión.
- Integración con Plataforma de Notificaciones/CasillaÚnica para DDU.
- Visualización de notificaciones pendientes y derivación a detalle.
- Gestión e historial de autorizaciones de uso de datos sensibles.
- Ayuda para instituciones integradas.
- Pruebas funcionales, prototipo, accesibilidad y evidencia.
- Garantía mínima de software según bases.

## Ruta SDD

1. specify
2. clarify
3. checklist
4. context
5. plan
6. plan_validation
7. tasks
8. analyze
9. implement
10. validate
11. observe
12. close

## Economía de tokens

La fábrica incorpora una capa transversal llamada `token_economizer`:

- Presupuesto por agente.
- Compactación de contexto.
- `context-pack.json` reutilizable.
- Evidencia por `source_id` y no por citas extensas.
- Respuestas por delta.
- Registro de consumo en ledger.
- Gate duro si se excede el presupuesto.

## Agentes clave

- `agent.spec_detallada`
- `agent.context_rag`
- `agent.ocr_ui_analyst`
- `agent.architect_plan`
- `agent.ui_web_modern`
- `agent.api_security_docs`
- `agent.security_policy`
- `agent.tests_coverage`
- `agent.implementacion_doc_code`
- `agent.token_billing`
- `agent.observability_sre`
- `agent.doc_tecnica_detalle`
- `agent.token_economizer`

## Criterio de éxito

Un run es aceptable cuando genera:

- `work_order.json`
- `context-pack.json`
- `evidence-register.json`
- `traceability-matrix.md`
- `validation-report.json`
- `final-report.json`
- `observability.jsonl`
