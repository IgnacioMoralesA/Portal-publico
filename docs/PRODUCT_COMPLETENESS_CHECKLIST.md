# Checklist de completitud del producto

Estados permitidos: cumple, parcial, pendiente, no aplica.

| Criterio minimo | Estado | Evidencia | Archivo relacionado | Observacion | Accion pendiente |
|---|---|---|---|---|---|
| Documento de especificacion minimo 6 paginas | cumple | Especificacion sistemica consolidada creada para entrega academica. | `docs/SYSTEM_SPECIFICATION.md` | Debe renderizarse/preview antes de entrega formal. | Exportar a PDF si el evaluador lo solicita. |
| 10 casos de uso | cumple | Catalogo con 12 casos de uso `CU-`. | `docs/USE_CASE_CATALOG.md` | Supera minimo requerido. | Mantener trazabilidad si cambian flujos. |
| 30 funcionalidades/flujos | cumple | Catalogo con 44 flujos `FUN-`. | `docs/FUNCTIONAL_FLOW_CATALOG.md` | Incluye frontend, API y evidencia. | Actualizar ante nuevos endpoints o pantallas. |
| 40 tablas | cumple | Modelo SQLAlchemy/SQLite con 40 `__tablename__`. | `app/backend/models/__init__.py`, `tests/backend/test_database_schema.py` | Criterio tecnico ya cumplido. | Mantener prueba de esquema. |
| 40 endpoints API | cumple | 55 endpoints metodo+ruta bajo `/api/`, mas `/health`. | `app/backend/routers/`, `tests/backend/test_api_endpoint_inventory.py` | API local/mock. | No agregar integraciones reales sin autorizacion. |
| 30 pantallas | cumple | Inventario con 35 pantallas/vistas/estados `UI-`. | `docs/SCREEN_INVENTORY.md`, `app/frontend/app.js` | Incluye estados UI y vistas API/docs. | Capturar screenshots si se requiere evidencia visual. |
| 60 reglas de negocio | cumple | Catalogo con 64 reglas `RN-`. | `docs/BUSINESS_RULES_CATALOG.md` | Cubre auth, 2FA, DDU, notificaciones, autorizaciones, mocks y no produccion. | Mantener enlaces a CHECK/endpoints. |
| 100 validaciones/CHECK | cumple | 115 `CheckConstraint` implementados y probados. | `app/backend/models/__init__.py`, `tests/backend/test_database_constraints.py` | Supera minimo requerido. | Agregar validaciones Pydantic si crece API. |
| Checklist de completitud | cumple | Checklist formal generado. | `docs/PRODUCT_COMPLETENESS_CHECKLIST.md` | Reemplaza conteo informal para evaluacion. | Revisar antes de entrega final. |
| Pruebas automatizadas con cobertura 100% | cumple | Backend Python local/mock con `89 passed` y cobertura `100.00%` sobre `app/backend`. | `tests/`, `pyproject.toml`, `docs/TEST_COVERAGE_REPORT.md` | Alcance instrumentado: backend Python. Frontend validado por pruebas estaticas y `node --check`, sin cobertura JS instrumentada. | Mantener reporte; incorporar coverage JS solo con herramienta real. |
| Sistema funcionando online en Linux sobre EC2 AWS | pendiente | Target EC2 documentado como pendiente. | `docs/SCOPE_COMPLIANCE_MATRIX.md`, `app/backend/routers/evidence.py` | No se afirma produccion real ni despliegue real. | Preparar infra y deploy sandbox con secretos seguros. |
| Sandbox/no produccion documentado | cumple | Advertencias en README, app README, backend README y especificacion. | `README.md`, `app/README.md`, `app/backend/README.md`, `docs/SYSTEM_SPECIFICATION.md` | No conecta servicios reales. | Mantener advertencias visibles. |
