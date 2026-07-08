# Catalogo de reglas de negocio

Reglas vigentes para el prototipo local/sandbox. Las reglas describen comportamiento esperado y restricciones documentales/tecnicas; no equivalen a reglas productivas de ClaveUnica ni CasillaUnica.

| ID | Modulo | Regla | Justificacion | Endpoints o pantallas relacionadas | Validacion/CHECK relacionada | Estado |
|---|---|---|---|---|---|---|
| RN-001 | Portal publico | El portal publico debe ser accesible sin sesion demo. | Permite revisar informacion general antes de autenticarse. | UI-001, UI-002, UI-003, `GET /api/public/service-cards` | `ck_public_service_cards_status` | vigente |
| RN-002 | Portal publico | Las novedades publicas deben usar contenido ficticio o no sensible. | Evita exponer informacion institucional real no controlada. | UI-003, `GET /api/public/news` | `ck_public_news_status` | vigente |
| RN-003 | Autenticacion | Solo las credenciales demo documentadas habilitan el avance a OTP. | Mantiene el sandbox deterministico. | UI-004, `POST /api/auth/login` | `ck_login_attempt_channel` | vigente |
| RN-004 | Autenticacion | Un login fallido no debe activar sesion privada. | Reduce confusion y evita estados inseguros. | UI-025, `POST /api/auth/login` | `ck_login_attempt_result` | vigente |
| RN-005 | Autenticacion | Todo intento de login debe poder auditarse como success o failure demo. | Soporta evidencia de seguridad. | `GET /api/auth/login-attempts` | `ck_login_attempt_result` | vigente |
| RN-006 | 2FA | El segundo factor demo usa codigos de 6 caracteres. | Alinea frontend, API y constraints. | UI-005, `POST /api/auth/verify-otp` | `ck_auth_factor_code_length`, `ck_otp_challenges_attempt_range` | vigente |
| RN-007 | 2FA | Un OTP incorrecto mantiene al usuario fuera del dashboard. | Evita bypass del flujo privado. | UI-026, `POST /api/auth/verify-otp` | `ck_otp_challenges_status` | vigente |
| RN-008 | 2FA | El factor demo puede estar activo o inactivo solo como booleano. | Simplifica el estado sandbox. | `GET /api/auth/factors`, `POST /api/auth/factors/toggle` | `ck_auth_factor_enabled_bool` | vigente |
| RN-009 | Dashboard | El dashboard requiere sesion privada demo. | Separa experiencia publica y privada. | UI-006 | frontend route guard | vigente |
| RN-010 | Dashboard | El dashboard solo muestra datos ficticios cargados localmente o desde SQLite mock. | Cumple restriccion de no datos personales reales. | UI-006, `GET /api/users/me` | `ck_users_clave_estado` | vigente |
| RN-011 | Dashboard | Las tarjetas privadas deben reflejar DDU, notificaciones y autorizaciones demo. | Da visibilidad rapida del alcance. | UI-006 | pruebas frontend estaticas | vigente |
| RN-012 | Datos personales | Correo y telefono solo pueden modificarse con factor demo valido. | Simula control de seguridad para datos de contacto. | UI-008, `PATCH /api/users/me/contact` | `ck_user_contact_verified_bool` | vigente |
| RN-013 | Datos personales | Los cambios de datos personales no tienen validez productiva. | Evita interpretacion operacional. | UI-007, UI-008 | advertencias documentales | vigente |
| RN-014 | Datos personales | No se deben ingresar datos personales reales en el prototipo. | Protege privacidad y alcance academico. | README, app/README, UI-008 | pruebas de seguridad estatica | vigente |
| RN-015 | Sesiones | La sesion actual debe distinguirse de sesiones remotas. | Evita acciones ambiguas. | UI-009, `GET /api/sessions/current` | `ck_user_sessions_actual_bool` | vigente |
| RN-016 | Sesiones | Solo sesiones remotas ficticias pueden cerrarse desde el listado. | Simula multisesion sin romper la demo. | UI-029, `POST /api/sessions/{session_id}/close` | `ck_user_sessions_estado` | vigente |
| RN-017 | Sesiones | Los eventos de sesion deben clasificar riesgo en valores permitidos. | Permite auditoria consistente. | `GET /api/sessions/events` | `ck_session_events_risk` | vigente |
| RN-018 | DDU | DDU solo puede estar pendiente o configurado en el sandbox. | Mantiene estados controlados. | UI-010, UI-013, `GET /api/ddu/status` | `ck_ddu_estado` | vigente |
| RN-019 | DDU | La derivacion DDU debe ser confirmada por modal antes de pasarela demo. | Evita cambios accidentales en la navegacion. | UI-011 | frontend dialog | vigente |
| RN-020 | DDU | La pasarela DDU es simulada y no configura CasillaUnica real. | Cumple restriccion de no integracion real. | UI-012, `POST /api/ddu/configure` | `ck_ddu_activation_channel` | vigente |
| RN-021 | DDU | La cancelacion DDU debe restaurar o mantener estado demo coherente. | Permite volver sin efectos reales. | UI-013, `POST /api/ddu/cancel` | `ck_ddu_cancellation_restored_bool` | vigente |
| RN-022 | Notificaciones | Si DDU esta pendiente, el listado de notificaciones debe bloquearse. | Representa dependencia funcional con domicilio digital. | UI-014, `GET /api/ddu/status` | `ck_ddu_alerta_bool` | vigente |
| RN-023 | Notificaciones | Las notificaciones solo usan estados pendiente o leida demo. | Mantiene trazabilidad simple. | UI-015, `GET /api/notifications` | `ck_notifications_estado` | vigente |
| RN-024 | Notificaciones | La prioridad de notificaciones debe pertenecer a catalogo permitido. | Ordena la visualizacion y validacion. | UI-015, `GET /api/notifications/priorities` | `ck_notifications_prioridad`, `ck_notification_priorities_code` | vigente |
| RN-025 | Notificaciones | Abrir una notificacion inexistente debe fallar de forma controlada. | Evita inconsistencias. | UI-017, `GET /api/notifications/{notification_id}` | pruebas API 404 | vigente |
| RN-026 | Notificaciones | Marcar como leida no debe invocar Plataforma de Notificaciones real. | Mantiene sandbox cerrado. | UI-018, `POST /api/notifications/{notification_id}/read` | `ck_notification_read_channel` | vigente |
| RN-027 | Notificaciones | Los intentos de entrega deben tener numero positivo y canal demo. | Evita registros imposibles. | `GET /api/notifications/delivery-attempts` | `ck_notification_delivery_attempt_positive`, `ck_notification_delivery_channel` | vigente |
| RN-028 | Autorizaciones | Toda solicitud debe estar en pendiente, aprobada, rechazada o revocada. | Define ciclo de vida auditable. | UI-019, `GET /api/authorizations` | `ck_authorizations_estado` | vigente |
| RN-029 | Autorizaciones | Aprobar, rechazar o revocar requiere factor demo valido. | Simula consentimiento reforzado. | UI-020, UI-021, UI-022, UI-024 | `ck_authorization_decisions_factor_bool` | vigente |
| RN-030 | Autorizaciones | Las categorias sensibles deben ser genericas y ficticias. | Evita datos sensibles reales. | `GET /api/authorizations/sensitive-data-categories` | `ck_sensitive_data_type` | vigente |
| RN-031 | Autorizaciones | Una autorizacion revocada no debe quedar como vigente en UI. | Preserva coherencia de decisiones. | UI-024 | `ck_authorizations_estado` | vigente |
| RN-032 | Recuperacion | Recuperacion de acceso es solo flujo demo y sin envio real. | Evita comunicaciones externas. | UI-023, `POST /api/auth/recovery/request` | `ck_password_recovery_channel` | vigente |
| RN-033 | Recuperacion | Los intentos de recuperacion deben contar intentos no negativos. | Evita estados invalidos. | `POST /api/auth/recovery/confirm` | `ck_password_recovery_attempts_nonnegative` | vigente |
| RN-034 | Evidencia | El backend debe exponer estado local/mock para evaluacion. | Facilita revision tecnica. | `GET /api/status`, `GET /health` | `HealthOut`, `ApiStatusOut` | vigente |
| RN-035 | Evidencia | El checklist API debe distinguir cumplido, pendiente o bloqueado internamente. | Permite seguimiento de cierre. | `GET /api/product/checklist` | `ck_product_checklist_status` | vigente |
| RN-036 | Auditoria | Eventos de auditoria deben usar tipos permitidos auth, read o seed. | Mantiene inventario auditable. | `GET /api/audit/events` | `ck_audit_event_type` | vigente |
| RN-037 | Auditoria | La severidad de auditoria local se limita a info o warning. | Evita simular incidentes productivos. | `GET /api/audit/events` | `ck_audit_severity` | vigente |
| RN-038 | Dispositivos | Dispositivos confiables solo aceptan estados confiable, revocado o pendiente. | Define ciclo de confianza demo. | `GET /api/devices/trusted` | `ck_trusted_devices_status` | vigente |
| RN-039 | Dispositivos | El puntaje de confianza debe estar entre 0 y 100. | Normaliza evaluacion de riesgo. | `POST /api/devices/{device_id}/trust` | `ck_trusted_devices_score_range` | vigente |
| RN-040 | Dispositivos | La accion de riesgo debe ser permitir, desafiar OTP o bloquear demo. | Simula decision de seguridad. | `GET /api/devices/trusted` | `ck_device_risk_action` | vigente |
| RN-041 | Instituciones | Las instituciones son ficticias y de tipo demo permitido. | Evita asociacion operacional real. | `GET /api/institutions` | `ck_institutions_type` | vigente |
| RN-042 | Instituciones | Las integraciones deben declararse mock, archivo demo o manual demo. | Prohibe conexiones reales en este ciclo. | `GET /api/integrations/status` | `ck_institution_integrations_type` | vigente |
| RN-043 | Integraciones | Eventos de integracion pueden ser ok, degradado demo o fallido demo. | Permite probar estados sin servicios externos. | `GET /api/integrations/events` | `ck_integration_status_events_status` | vigente |
| RN-044 | Ayuda | Articulos de ayuda deben tener audiencia publico, autenticado u operador demo. | Controla visibilidad del contenido. | `GET /api/help/articles` | `ck_help_articles_audience` | vigente |
| RN-045 | Ayuda | Categorias ocultas demo no deben tratarse como contenido productivo. | Evita confundir catalogo de prueba con real. | `GET /api/help/categories` | `ck_help_categories_status` | vigente |
| RN-046 | UI | Toda pantalla privada debe quedar dentro del shell privado. | Mantiene navegacion coherente. | UI-006 a UI-024, UI-027 | pruebas frontend estaticas | vigente |
| RN-047 | UI | Los mensajes de error no deben revelar secretos ni integraciones reales. | Reduce riesgo informativo. | UI-025, UI-026, UI-035 | tests frontend security | vigente |
| RN-048 | UI | El layout debe tener estado responsive documentado. | Cumple inventario de pantallas/estados. | UI-033, `app/frontend/styles.css` | media queries | vigente |
| RN-049 | Validaciones | Las validaciones SQL deben mantenerse sobre 100 CHECK. | Cumple criterio minimo tecnico. | `app/backend/models/__init__.py` | 115 `CheckConstraint` | vigente |
| RN-050 | Base de datos | El esquema local debe mantener al menos 40 tablas. | Cumple criterio minimo de modelo de datos. | `app/backend/models/__init__.py` | 40 `__tablename__` | vigente |
| RN-051 | API | La API debe mantener al menos 40 endpoints bajo `/api/`. | Cumple criterio minimo de servicios. | `app/backend/routers/` | tests endpoint inventory | vigente |
| RN-052 | Seed | El seed debe ser ficticio e idempotente. | Permite ejecuciones repetibles. | `app/backend/seed.py` | tests seed data | vigente |
| RN-053 | Seguridad demo | No se deben agregar credenciales reales ni secretos. | Protege el repositorio. | README, tests | tests seguridad estatica | vigente |
| RN-054 | Seguridad demo | El prototipo no debe afirmar operacion productiva real. | Mantiene alcance academico honesto. | Todos los docs | test documental | vigente |
| RN-055 | Seguridad demo | `sessionStorage` solo puede usarse para estado demo/local. | Evita prometer persistencia real. | `app/frontend/app.js`, app/README | pruebas frontend | vigente |
| RN-056 | Mocks | Los mocks deben contener datos ficticios. | Evita uso de datos personales reales. | `app/mocks/*.json` | tests seguridad estatica | vigente |
| RN-057 | Deploy | EC2 AWS debe permanecer pendiente hasta implementacion formal. | No se debe afirmar despliegue inexistente. | `GET /api/deployment-targets`, checklist | `ck_deployment_targets_environment` | vigente |
| RN-058 | Cobertura | Cobertura automatizada 100% sigue pendiente hasta medirla y alcanzarla. | Evita cierre falso del criterio. | tests, checklist | pytest-cov pendiente | vigente |
| RN-059 | Documentacion | Cada catalogo de alcance debe mantener evidencia y archivo relacionado. | Facilita revision academica. | docs/*CATALOG*, checklist | test_scope_catalogs_static | vigente |
| RN-060 | No produccion | Toda documentacion debe indicar sandbox/no produccion cuando describa el sistema. | Evita mal uso del prototipo. | README, app/README, backend README, SYSTEM_SPECIFICATION | test documental | vigente |
| RN-061 | Estados | Estados de autorizacion, DDU, notificacion y sesion deben pertenecer a enumeraciones CHECK. | Evita estados libres inconsistentes. | API y UI | checks de modelos | vigente |
| RN-062 | Pruebas | Las pruebas existentes no deben relajarse ni eliminarse. | Preserva evidencia acumulada. | `tests/` | suite pytest completa | vigente |
| RN-063 | Factory | El directorio `factory/` no debe modificarse en este ciclo. | Respeta restriccion del agente. | `factory/` | git status/manual | vigente |
| RN-064 | Documental | Los catalogos deben contar al menos 10 CU, 30 flujos, 30 pantallas y 60 RN. | Cierra criterios minimos de revision. | docs nuevos | `tests/test_scope_catalogs_static.py` | vigente |
