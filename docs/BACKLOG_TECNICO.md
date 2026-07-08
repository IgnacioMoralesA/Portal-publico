# Backlog tecnico

Fuente base: `project/runs/RUN-22673eb11025/traceability-matrix.md`.

Estado final del ciclo: prototipo funcional local/sandbox cerrado documentalmente. Los modulos estan implementados en frontend estatico con mocks y pruebas estaticas; no hay backend real ni integraciones reales.

## 1. Portal publico

- Objetivo: habilitar accesos publicos principales del servicio.
- Funcionalidades: activar cuenta, autenticar, recuperar acceso, ayuda y novedades.
- Criterios de aceptacion: existen accesos para activar, autenticar, recuperar, ayuda y novedades; el flujo queda trazado a S06:HU01 y S08:CU_001.
- Prioridad: alta.
- Estado: implementado en prototipo local.
- Evidencia: `app/frontend/index.html`, `app/frontend/app.js`, `docs/PROTOTYPE_EVIDENCE.md`, `tests/frontend/test_login_2fa_static.py`.
- Nota: portal visual/mock sin backend ni integracion real con ClaveUnica.

## 2. Login y 2FA

- Objetivo: permitir autenticacion con segundo factor demo.
- Funcionalidades: login simulado, credenciales demo, OTP demo obligatorio cuando el usuario mock tiene segundo factor activo.
- Criterios de aceptacion: login y OTP demo permiten llegar al dashboard; flujo trazado a S06:HU03 y S08:CU_003.
- Prioridad: alta.
- Estado: implementado en prototipo local.
- Evidencia: `app/mocks/user.json`, `app/frontend/app.js`, `docs/PROTOTYPE_EVIDENCE.md`, `tests/frontend/test_login_2fa_static.py`.
- Nota: no incluye backend, OAuth/OIDC/SAML, ClaveUnica real ni servicios externos.

## 3. Datos personales

- Objetivo: gestionar cambios de datos de contacto con control de seguridad demo.
- Funcionalidades: cambio local de telefono y correo; validacion mediante factor demo.
- Criterios de aceptacion: telefono y correo pueden modificarse solo con factor demo; flujo trazado a S06:HU02 y S08:CU_002.
- Prioridad: alta.
- Estado: implementado en prototipo local.
- Evidencia: `app/frontend/app.js`, `app/mocks/user.json`, `tests/frontend/test_personal_data_static.py`.
- Nota: los cambios viven solo en memoria de la sesion de navegador; usan factor de seguridad demo y no deben usar datos reales.

## 4. Sesiones y multisesion

- Objetivo: representar politica de multisesion y mitigacion conceptual de secuestro.
- Funcionalidades: sesion actual, sesiones remotas mock, cierre remoto simulado y advertencias.
- Criterios de aceptacion: existe lista de sesiones, identificacion de sesion actual y cierre remoto simulado; flujo trazado a S06:HU04 y S08:CU_004.
- Prioridad: alta.
- Estado: implementado en prototipo local.
- Evidencia: `app/mocks/sessions.json`, `app/frontend/app.js`, `tests/frontend/test_sessions_static.py`.
- Nota: existe gestion de sesiones activa ficticia; no hay proteccion productiva real, IPs reales, ubicaciones reales ni persistencia real.

## 5. DDU / Domicilio Digital Unico

- Objetivo: representar derivacion y gestion del DDU.
- Funcionalidades: alerta pendiente, modal, pasarela simulada, cancelacion, retorno y configuracion demo.
- Criterios de aceptacion: soporta derivacion, cancelacion, retorno y alerta pendiente; flujo trazado a S06:HU05-HU12, S07 y S08:CU_005-CU_012.
- Prioridad: alta.
- Estado: implementado en prototipo local.
- Evidencia: `app/mocks/ddu.json`, `app/frontend/app.js`, `tests/frontend/test_ddu_static.py`.
- Nota: usa `sessionStorage` para estado DDU demo; no configura DDU real ni conecta CasillaUnica.

## 6. Notificaciones / CasillaUnica

- Objetivo: mostrar notificaciones mock condicionadas por DDU.
- Funcionalidades: bloqueo con DDU pendiente, listado, detalle, derivacion simulada/local y marcado como leida.
- Criterios de aceptacion: usuario puede listar, ver detalle y marcar leida en estado local; flujo trazado a S06:HU09-HU11 y S07.
- Prioridad: media.
- Estado: implementado en prototipo local.
- Evidencia: `app/mocks/notifications.json`, `app/frontend/app.js`, `tests/frontend/test_notifications_static.py`.
- Nota: incluye derivacion simulada/local a CasillaUnica; no hay CasillaUnica real, Plataforma de Notificaciones real ni notificaciones reales.

## 7. Autorizaciones de datos sensibles

- Objetivo: gestionar autorizaciones mock asociadas a datos sensibles genericos.
- Funcionalidades: resumen, historial local, pendientes, aprobacion, rechazo y revocacion con factor demo.
- Criterios de aceptacion: se consultan historial y pendientes; se permite aprobar, rechazar y revocar con factor demo; flujo trazado a S06:HU13-HU16 y S08:CU_013-CU_016.
- Prioridad: alta.
- Estado: implementado en prototipo local.
- Evidencia: `app/mocks/authorizations.json`, `app/frontend/app.js`, `tests/frontend/test_authorizations_static.py`.
- Nota: mantiene historial local en `sessionStorage`; no hay datos sensibles reales, validez legal, backend ni integracion con servicios del Estado.

## 8. Calidad, accesibilidad y pruebas

- Objetivo: asegurar evidencia inicial de calidad del prototipo.
- Funcionalidades: pruebas estaticas frontend, validacion manual local, revision de accesibilidad basica y seguridad demo.
- Criterios de aceptacion: pruebas estaticas pasan; evidencia registrada; modulo trazado a S05.
- Prioridad: alta.
- Estado final: implementado parcialmente.
- Evidencia: `docs/QA_ACCESSIBILITY_REPORT.md`, `docs/FINAL_TEST_SUMMARY.md`, `tests/frontend/`.
- Nota: quedan pendientes E2E automatizado, auditoria WCAG formal, lector de pantalla y matriz real de dispositivos/navegadores.

## 9. Garantia y evidencia

- Objetivo: documentar cobertura de calidad, funcionamiento y seguridad demo.
- Funcionalidades: evidencia documental, checklist final, reporte final y handoff.
- Criterios de aceptacion: evidencia y cierre documental disponibles; modulo trazado a S05.
- Prioridad: alta.
- Estado final: implementado parcialmente.
- Evidencia: `docs/PROTOTYPE_EVIDENCE.md`, `docs/FINAL_CHECKLIST.md`, `docs/FINAL_PROTOTYPE_REPORT.md`, `docs/FINAL_HANDOFF.md`.
- Nota: no constituye garantia productiva real; faltan rendimiento, compatibilidad amplia, hardening, monitoreo y operacion.

## 10. Backend local/API mock y base de datos

- Objetivo: crear base extensible para API local y persistencia SQLite sin servicios reales.
- Funcionalidades: health check, estado API, login demo, OTP demo, usuario actual, DDU, sesiones, notificaciones, autorizaciones y esquema local extendido.
- Criterios de aceptacion: API FastAPI importa correctamente, crea SQLite local con seed ficticio, expone 9 endpoints iniciales, mantiene 40 tablas y supera 100 CHECK constraints.
- Prioridad: alta.
- Estado: base inicial implementada y esquema minimo cumplido en ciclo `database_40_tables_and_check_constraints_expansion`.
- Evidencia: `app/backend/`, `tests/backend/test_database_schema.py`, `tests/backend/test_database_constraints.py`, `tests/backend/test_seed_data.py`, `docs/SCOPE_COMPLIANCE_MATRIX.md`.
- Nota: no conecta ClaveUnica real, CasillaUnica real ni Plataforma de Notificaciones real. Persisten brechas de 31 endpoints, cobertura 100% y deploy Linux EC2 AWS.
