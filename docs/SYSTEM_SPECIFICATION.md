# Especificacion del sistema

## 1. Contexto del sistema

El proyecto corresponde a un prototipo local/sandbox del Portal Ciudadano de ClaveUnica. Su proposito academico es demostrar, con trazabilidad y evidencia tecnica, una experiencia de portal publico y privado asociada a autenticacion demo, segundo factor demo, datos personales ficticios, sesiones mock, Domicilio Digital Unico (DDU) simulado, notificaciones mock y autorizaciones de datos sensibles genericas. El sistema se ejecuta localmente con un frontend estatico en `app/frontend/`, una API FastAPI local/mock en `app/backend/`, una base SQLite local y datos semilla ficticios idempotentes.

El prototipo no es un servicio productivo ni representa una integracion oficial. No conecta ClaveUnica real, CasillaUnica real, Plataforma de Notificaciones real ni servicios externos. No debe recibir datos personales reales, credenciales reales ni secretos. Las credenciales documentadas son de demostracion y sirven solo para recorrer el sandbox: usuario `demo.claveunica`, clave `DemoLocal2026` y OTP/factor `123456`.

El estado tecnico base ya cumple tres criterios minimos importantes: al menos 40 tablas, al menos 100 validaciones o restricciones `CHECK`, y al menos 40 endpoints API. La implementacion vigente declara 40 tablas SQLAlchemy/SQLite, 115 `CheckConstraint` y 55 endpoints metodo+ruta bajo `/api/`, mas `/health`. Este documento consolida la especificacion funcional y tecnica para formalizar criterios de revision relacionados con casos de uso, flujos, pantallas, reglas de negocio, pruebas y checklist de completitud.

## 2. Objetivo general

Disponer de un prototipo local/sandbox trazable del Portal Ciudadano de ClaveUnica que permita demostrar los principales recorridos ciudadanos y criterios tecnicos minimos de una entrega academica, sin usar integraciones reales, sin datos personales reales y sin afirmar operacion productiva.

## 3. Objetivos especificos

- Presentar un portal publico con accesos a inicio, ayuda, novedades, login, activacion y recuperacion.
- Simular autenticacion con credenciales demo y segundo factor OTP demo.
- Mostrar un dashboard privado con resumen de usuario ficticio, DDU, sesiones, notificaciones y autorizaciones.
- Permitir edicion local/mock de datos de contacto con factor demo.
- Representar gestion de sesiones y cierre remoto simulado.
- Representar configuracion de DDU con modal, pasarela simulada, cancelacion y retorno.
- Mostrar notificaciones mock condicionadas por estado DDU, detalle y marcado como leida.
- Gestionar autorizaciones ficticias de datos sensibles genericos mediante aprobacion, rechazo y revocacion con factor demo.
- Exponer una API local/mock amplia para soporte de evaluacion tecnica.
- Mantener base SQLite local con esquema suficiente para 40 tablas y mas de 100 `CHECK`.
- Documentar alcance, pantallas, reglas de negocio y brechas pendientes.

## 4. Alcance

El alcance implementado cubre frontend estatico, backend local/mock, persistencia SQLite local, seed ficticio idempotente, pruebas automatizadas y documentacion de evidencia. El frontend permite recorrer el portal desde un servidor HTTP local y usa mocks JSON y `sessionStorage` para mantener estados de demostracion. El backend provee endpoints bajo `/api/` para auth, usuarios, sesiones, dispositivos, DDU, notificaciones, autorizaciones, instituciones, integraciones, portal publico, ayuda, auditoria, evidencia, reglas, pantallas y objetivos de despliegue.

El alcance documental de este ciclo formaliza:

- 12 casos de uso en `docs/USE_CASE_CATALOG.md`.
- 44 funcionalidades o flujos en `docs/FUNCTIONAL_FLOW_CATALOG.md`.
- 35 pantallas, vistas, secciones o estados en `docs/SCREEN_INVENTORY.md`.
- 64 reglas de negocio en `docs/BUSINESS_RULES_CATALOG.md`.
- Checklist de completitud en `docs/PRODUCT_COMPLETENESS_CHECKLIST.md`.

## 5. Fuera de alcance

Queda fuera de alcance cualquier conexion real con ClaveUnica, CasillaUnica, Plataforma de Notificaciones, servicios estatales, proveedores de identidad, mensajeria real, correo real, SMS real, firma electronica, datos sensibles reales, monitoreo productivo, despliegue productivo y credenciales reales. Tambien queda fuera de alcance afirmar que el sistema esta en produccion o que tiene validez legal, operacional o institucional.

Siguen pendientes dos brechas mayores: cobertura automatizada 100% y despliegue online en Linux sobre EC2 AWS. El deploy EC2 debe abordarse en un ciclo futuro con gestion segura de secretos y sin integraciones reales no autorizadas.

## 6. Actores

| Actor | Descripcion | Permisos en prototipo |
|---|---|---|
| Visitante | Persona sin sesion que revisa informacion publica. | Ver portal, ayuda, novedades, login y recuperacion demo. |
| Ciudadano demo | Usuario ficticio autenticado con credenciales y OTP demo. | Acceder a dashboard, datos personales, sesiones, DDU, notificaciones y autorizaciones. |
| Evaluador | Revisor academico o tecnico del prototipo. | Ejecutar pruebas, revisar documentos y consultar endpoints de evidencia. |
| Sistema local/mock | Componentes frontend, API, SQLite y seed. | Responder con datos ficticios y estados controlados. |
| Servicios externos reales | ClaveUnica, CasillaUnica y otros servicios reales. | Sin acceso; explicitamente no conectados. |

## 7. Casos de uso

El catalogo formal se encuentra en `docs/USE_CASE_CATALOG.md`. Incluye los siguientes casos:

- CU-001 Consultar portal publico.
- CU-002 Iniciar sesion.
- CU-003 Validar segundo factor.
- CU-004 Consultar dashboard privado.
- CU-005 Gestionar datos personales.
- CU-006 Gestionar sesiones.
- CU-007 Configurar DDU.
- CU-008 Consultar notificaciones.
- CU-009 Revisar detalle de notificacion.
- CU-010 Gestionar autorizaciones de datos sensibles.
- CU-011 Recuperar acceso demo.
- CU-012 Revisar evidencia y estado del producto.

Cada caso documenta actor, objetivo, precondiciones, flujo principal, alternativos, resultado esperado, endpoints, pantallas, reglas relacionadas y estado.

## 8. Funcionalidades y flujos

El catalogo formal se encuentra en `docs/FUNCTIONAL_FLOW_CATALOG.md`. El inventario supera el minimo de 30 flujos e incluye portal publico, autenticacion, OTP, dashboard, perfil, contacto, sesiones, dispositivos, DDU, notificaciones, autorizaciones, ayuda, instituciones, integraciones, auditoria, evidencia, reglas, pantallas API, deploy pendiente y cierre de sesion.

Los flujos principales son:

- Portal publico, ayuda y novedades.
- Login, registro de intentos, OTP y factores demo.
- Dashboard privado.
- Perfil, contacto y preguntas de seguridad.
- Sesiones, sesion actual, cierre remoto y eventos.
- Dispositivos confiables y evaluacion de riesgo demo.
- DDU pendiente, modal, pasarela, configuracion, cancelacion y eventos.
- Bloqueo/listado/detalle/marcado de notificaciones.
- Resumen/detalle/aprobacion/rechazo/revocacion de autorizaciones.
- Evidencia tecnica, reglas, validaciones, pantallas y deploy pendiente.

## 9. Pantallas

El inventario formal se encuentra en `docs/SCREEN_INVENTORY.md`. Incluye 35 pantallas, vistas o estados. El frontend principal se monta sobre `app/frontend/index.html` y renderiza vistas desde `app/frontend/app.js`, con estilos en `app/frontend/styles.css`. Tambien se consideran vistas tecnicas de API docs y respuestas JSON de evidencia para evaluacion.

Pantallas destacadas:

- Portal publico, ayuda y novedades.
- Login y OTP.
- Dashboard privado.
- Datos personales vista y edicion.
- Sesiones y cierre remoto.
- DDU pendiente, modal, pasarela y configurado/cancelado.
- Notificaciones bloqueadas por DDU, listado, detalle y leida.
- Autorizaciones resumen, detalle pendiente, aprobada, rechazada y revocada.
- Estados de error, exito, responsive y vistas tecnicas API.

## 10. Endpoints

La API local/mock se implementa en FastAPI. `app/backend/main.py` registra routers para salud, auth, usuarios, DDU, sesiones, dispositivos, notificaciones, autorizaciones, instituciones, portal publico, ayuda, auditoria, evidencia y reglas. El inventario vigente es de 55 endpoints metodo+ruta bajo `/api/`, mas `/health`.

Resumen por modulo:

| Modulo | Endpoints representativos |
|---|---|
| Salud/estado | `GET /health`, `GET /api/status` |
| Auth | `POST /api/auth/login`, `POST /api/auth/verify-otp`, `POST /api/auth/logout`, `GET /api/auth/factors`, `POST /api/auth/factors/toggle`, `GET /api/auth/login-attempts`, `POST /api/auth/recovery/request`, `POST /api/auth/recovery/confirm` |
| Usuarios | `GET /api/users/me`, `GET /api/users/me/profile`, `PATCH /api/users/me/contact`, `GET /api/users/me/security-questions`, `POST /api/users/me/security-questions/verify` |
| Sesiones/dispositivos | `GET /api/sessions`, `GET /api/sessions/current`, `POST /api/sessions/{session_id}/close`, `GET /api/sessions/events`, `GET /api/devices/trusted`, `POST /api/devices/{device_id}/trust`, `DELETE /api/devices/{device_id}/trust` |
| DDU | `GET /api/ddu/status`, `POST /api/ddu/configure`, `POST /api/ddu/cancel`, `GET /api/ddu/events`, `GET /api/ddu/activation-summary` |
| Notificaciones | `GET /api/notifications`, `GET /api/notifications/categories`, `GET /api/notifications/priorities`, `GET /api/notifications/read-events`, `GET /api/notifications/delivery-attempts`, `GET /api/notifications/{notification_id}`, `POST /api/notifications/{notification_id}/read` |
| Autorizaciones | `GET /api/authorizations`, `GET /api/authorizations/history`, `GET /api/authorizations/sensitive-data-categories`, `GET /api/authorizations/{authorization_id}`, acciones approve/reject/revoke |
| Publico/ayuda | `GET /api/public/news`, `GET /api/public/service-cards`, `GET /api/help/categories`, `GET /api/help/articles` |
| Evidencia/reglas | `GET /api/evidence/tests`, `GET /api/product/checklist`, `GET /api/deployment-targets`, `GET /api/business-rules`, `GET /api/validation-rules`, `GET /api/screens` |

## 11. Modelo de datos resumido

El modelo local usa SQLAlchemy y SQLite en `app/backend/models/__init__.py`. La base local se crea automaticamente al importar `app.backend.main` y se alimenta con seed ficticio idempotente. El esquema contiene 40 tablas distribuidas en dominios:

- Identidad y autenticacion: `users`, `auth_factors`, `login_attempts`, `otp_challenges`, `password_recovery_requests`.
- Perfil y contacto: `user_profiles`, `user_contact_methods`, `security_questions`.
- Sesiones y dispositivos: `user_sessions`, `session_events`, `trusted_devices`, `device_risk_assessments`.
- DDU: `ddu_profiles`, `ddu_activation_events`, `ddu_cancellation_events`.
- Notificaciones: `notifications`, `notification_recipients`, `notification_read_events`, `notification_categories`, `notification_priorities`, `notification_delivery_attempts`.
- Autorizaciones: `authorization_requests`, `authorization_decisions`, `authorization_history`, `sensitive_data_categories`.
- Instituciones e integraciones: `institutions`, `institution_integrations`, `integration_status_events`.
- Contenido y evidencia: `help_articles`, `help_categories`, `public_news`, `public_service_cards`, `accessibility_checks`, `prototype_screens`, `business_rules`, `validation_rules`, `product_checklist_items`, `test_evidence_records`, `deployment_targets`, `audit_events`.

## 12. Reglas de negocio

El catalogo formal se encuentra en `docs/BUSINESS_RULES_CATALOG.md` con 64 reglas `RN-`. Cubre autenticacion, segundo factor, datos personales, sesiones, dispositivos, DDU, notificaciones, autorizaciones, auditoria, ayuda, instituciones, integraciones, validaciones, mocks, seguridad demo, no produccion, deploy pendiente y pruebas.

Reglas transversales:

- No se deben usar datos personales reales.
- No se deben agregar credenciales reales ni secretos.
- No se deben conectar servicios reales.
- El sistema debe mantener advertencias sandbox/no produccion.
- Los estados de negocio deben pertenecer a enumeraciones controladas por frontend/API/CHECK.
- Las pruebas existentes no deben eliminarse ni relajarse.

## 13. Validaciones y CHECK

El backend implementa 115 restricciones `CheckConstraint`, superando el minimo de 100 validaciones/CHECK. Las restricciones cubren estados, booleanos, rangos, tipos, canales, severidades, prioridades, codigos y longitudes minimas. Ejemplos:

- Usuarios: estado de ClaveUnica demo y factor booleano.
- Auth: tipo de factor, codigo de 6 caracteres, intentos success/failure.
- Sesiones: estado activa/cerrada demo, riesgo bajo/medio/alto.
- DDU: estado pendiente/configurado, canal de activacion demo, motivo de cancelacion.
- Notificaciones: estado pendiente/leida demo, prioridad, categoria, canal e intentos.
- Autorizaciones: estado pendiente/aprobada/rechazada/revocada, decisiones permitidas, factor verificado.
- Evidencia: estado de checklist, tipo de prueba, resultado de prueba y deploy pendiente.

Las pruebas `tests/backend/test_database_constraints.py` y `tests/backend/test_database_schema.py` validan el conteo y restricciones representativas.

## 14. Pruebas

La suite automatizada actual incluye pruebas de fabrica, frontend estatico y backend local/mock. Las pruebas backend validan salud, auth, recursos core, DDU, autorizaciones, sesiones, notificaciones, recursos publicos, auditoria/reglas, inventario de endpoints, esquema de base de datos, constraints y seed. Las pruebas frontend validan presencia estatica de flujos de login/2FA, datos personales, sesiones, DDU, notificaciones, autorizaciones, accesibilidad basica y seguridad demo.

Este ciclo agrega `tests/test_scope_catalogs_static.py`, que verifica existencia y conteos minimos de los catalogos, menciones de 40 tablas, 40 endpoints y 100 CHECK en la matriz de cumplimiento, y ausencia de afirmaciones de produccion real.

La cobertura automatizada 100% sigue pendiente. Para cerrarla se requiere definir alcance de medicion, agregar `pytest-cov`, cubrir routers y servicios restantes y eventualmente incorporar pruebas E2E del frontend.

## 15. Riesgos

| Riesgo | Impacto | Mitigacion actual | Brecha |
|---|---|---|---|
| Confundir sandbox con produccion | Alto | Advertencias en docs y README. | Mantener lenguaje cuidadoso. |
| Uso accidental de datos reales | Alto | Mocks ficticios y advertencias. | Reforzar checklist en demos. |
| Falta de cobertura 100% | Medio | Suite pytest existente. | Implementar ciclo de cobertura. |
| Falta de deploy EC2 | Alto para criterio final | Estado documentado como pendiente. | Crear agente de infraestructura. |
| Accesibilidad no auditada formalmente | Medio | Pruebas estaticas basicas. | Auditoria WCAG y lector de pantalla. |
| Integraciones reales no autorizadas | Alto | Restriccion explicita y sin secretos. | Revisiones antes de cualquier integracion. |

## 16. Limitaciones

El prototipo usa datos ficticios, API local/mock, SQLite local y estado de navegador. No implementa identidad real, validez legal, persistencia productiva, controles de seguridad productivos, monitoreo, CI/CD, observabilidad operacional ni despliegue real. Algunas vistas tecnicas se consideran para evaluacion, no para usuarios finales. La experiencia visual debe revisarse manualmente antes de una entrega formal renderizada.

## 17. Advertencia sandbox/no produccion

Este sistema es exclusivamente un prototipo local/sandbox para evaluacion academica y tecnica. No esta listo para produccion, no opera como servicio publico, no tiene validez legal u operacional, no conecta servicios reales de ClaveUnica o CasillaUnica, no envia notificaciones reales y no debe procesar datos personales reales. Cualquier despliegue futuro en EC2 debe ser tratado como sandbox controlado hasta que existan autorizaciones, seguridad, secretos gestionados, integraciones formales, monitoreo y pruebas suficientes.
