# Proximos ciclos opcionales

## 1. E2E automatizado

- Objetivo: automatizar flujos completos con Playwright o alternativa liviana.
- Alcance: login, OTP, dashboard, datos personales, sesiones, DDU, notificaciones, autorizaciones y logout.
- Salida esperada: suite E2E reproducible y documentada.

## 2. Auditoria WCAG formal

- Objetivo: evaluar cumplimiento de accesibilidad con criterio formal.
- Alcance: WCAG 2.2, contraste, foco, nombres accesibles, semantica, formularios, modal y navegacion.
- Salida esperada: reporte de hallazgos y plan de remediacion.

## 3. Tecnologias asistivas

- Objetivo: probar con lector de pantalla y navegacion por teclado real.
- Alcance: NVDA/JAWS/VoiceOver segun disponibilidad.
- Salida esperada: evidencia practica y ajustes.

## 4. Matriz real de navegadores/dispositivos

- Objetivo: validar compatibilidad mas alla de revision estatica.
- Alcance: desktop, movil, distintos navegadores y tamanos.
- Salida esperada: matriz de resultados.

## 5. Backend mock/API local

- Objetivo: separar frontend de datos mock embebidos.
- Alcance: endpoints locales para usuario, sesiones, DDU, notificaciones y autorizaciones.
- Salida esperada: API local sin servicios reales.

## 6. Persistencia real local

- Objetivo: reemplazar `sessionStorage` por persistencia controlada para demo avanzada.
- Alcance: base local o storage backend.
- Salida esperada: estado reproducible sin datos reales.

## 7. Autenticacion institucional simulada robusta

- Objetivo: mejorar el modelo demo sin conectar ClaveUnica real.
- Alcance: sesiones, expiracion, renovacion y errores.
- Salida esperada: simulador local mas realista.

## 8. Contratos API

- Objetivo: definir contratos antes de backend/integracion.
- Alcance: OpenAPI o especificacion equivalente.
- Salida esperada: contratos versionados por modulo.

## 9. Hardening productivo

- Objetivo: preparar criterios de seguridad previos a produccion.
- Alcance: threat model, headers, validaciones, logging, monitoreo, secretos y controles de sesion.
- Salida esperada: plan de hardening y checklist.

## 10. Integracion real autorizada

- Objetivo: preparar integracion con servicios reales solo con aprobacion formal.
- Alcance: ClaveUnica, CasillaUnica y Plataforma de Notificaciones.
- Salida esperada: plan de integracion, ambientes autorizados y resguardos.

## 11. CI/CD

- Objetivo: automatizar pruebas y verificaciones.
- Alcance: pytest, `node --check`, E2E futuro y reportes.
- Salida esperada: pipeline reproducible.
