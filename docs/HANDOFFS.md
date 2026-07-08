# Handoffs abiertos

## Agente E2E futuro

- Entrada: `docs/FINAL_TEST_SUMMARY.md`, `docs/SAFE_DEMO_SCRIPT.md`, `app/frontend/`.
- Objetivo: automatizar recorridos completos.
- Cuidado: no inventar evidencia visual si el navegador local falla.

## Agente accesibilidad WCAG futuro

- Entrada: `docs/QA_ACCESSIBILITY_REPORT.md`, `app/frontend/`.
- Objetivo: auditoria WCAG formal y remediaciones.
- Cuidado: no afirmar cumplimiento completo sin evidencia.

## Agente backend/API futuro

- Entrada: `docs/TECHNICAL_REVIEW_GUIDE.md`, `docs/FINAL_TRACEABILITY_MATRIX.md`, mocks actuales.
- Objetivo: disenar API local y contratos.
- Cuidado: no conectar servicios reales sin autorizacion.

## Agente persistencia futura

- Entrada: `app/frontend/app.js`, `app/mocks/*.json`.
- Objetivo: reemplazar `sessionStorage` por persistencia local controlada.
- Cuidado: no guardar datos personales reales.

## Agente hardening futuro

- Entrada: `docs/FINAL_RISK_REGISTER.md`, `docs/TECHNICAL_REVIEW_GUIDE.md`.
- Objetivo: threat model, controles de sesion, headers, validaciones y monitoreo.
- Cuidado: distinguir demo de produccion.

## Agente CI/CD futuro

- Entrada: comandos de `docs/FINAL_TEST_SUMMARY.md`.
- Objetivo: ejecutar pytest, `node --check` y E2E futuro en pipeline.
- Cuidado: no agregar dependencias pesadas sin justificacion.

## Agente integracion real futura

- Entrada: contratos API futuros y autorizaciones institucionales.
- Objetivo: preparar integracion real con ClaveUnica, CasillaUnica y Plataforma de Notificaciones.
- Cuidado: requiere autorizacion formal, ambientes permitidos y gestion de secretos.
