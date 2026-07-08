# Registro final de riesgos

| Riesgo | Severidad | Impacto | Evidencia | Mitigacion actual | Accion futura recomendada | Responsable sugerido |
|---|---|---|---|---|---|---|
| Falta auditoria WCAG formal | Alta | Puede haber barreras no detectadas. | `docs/QA_ACCESSIBILITY_REPORT.md` declara revision basica. | Tests estaticos de accesibilidad. | Ejecutar auditoria WCAG 2.2 formal. | Especialista accesibilidad. |
| Falta prueba con lector de pantalla | Alta | Usuarios con tecnologias asistivas podrian encontrar bloqueos. | No hay evidencia de lector de pantalla. | Semantica, labels y `aria-live` revisados estaticamente. | Probar NVDA/JAWS/VoiceOver segun matriz. | QA accesibilidad. |
| Falta matriz real de dispositivos/navegadores | Media | Riesgo de fallas responsivas o incompatibilidades. | Solo hay CSS responsive y revision local. | Media query y tests estaticos. | Definir y ejecutar matriz real. | QA frontend. |
| Falta E2E automatizado | Alta | Regresiones de flujo podrian pasar sin detectar. | No hay Playwright ni E2E. | Validacion manual y pruebas estaticas. | Automatizar flujos criticos. | Agente/equipo E2E. |
| Falta backend real | Alta | No existe operacion ni persistencia productiva. | Arquitectura estatica documentada. | Mocks locales. | Disenar API local y luego backend real autorizado. | Equipo backend/API. |
| Falta hardening productivo | Alta | Autenticacion, sesiones y autorizaciones no son seguras para produccion. | `docs/FINAL_PROTOTYPE_REPORT.md`. | Advertencias sandbox/no produccion. | Threat modeling, controles de sesion, headers, validaciones y monitoreo. | Seguridad aplicativa. |
| Mocks no equivalen a integracion real | Alta | Puede haber brechas contra servicios institucionales reales. | `app/mocks/*.json`. | Datos ficticios y trazabilidad. | Definir contratos y ambientes autorizados. | Arquitectura/integraciones. |
| `sessionStorage` solo valido para demo | Media | Estados se pierden o no tienen garantias reales. | `app/frontend/app.js`. | Documentado como demo/local. | Persistencia real local o backend. | Frontend/backend. |
| No hay autenticacion real ClaveUnica | Alta | Login no valida identidad real. | Credenciales demo en `app/mocks/user.json`. | Avisos de simulacion. | Integracion institucional solo con autorizacion formal. | Seguridad/integraciones. |
| No hay CasillaUnica real | Alta | Notificaciones no representan bandeja real. | `app/mocks/notifications.json`. | Derivacion simulada/local. | Integracion autorizada y contratos. | Integraciones. |
| No hay persistencia real | Media | Cambios no sobreviven como datos reales. | Uso de memoria y `sessionStorage`. | Advertencias y mocks. | Persistencia controlada y migraciones. | Backend/datos. |
| No hay seguridad productiva | Alta | No hay controles reales contra ataques. | Sin backend ni autenticacion real. | Tests de ausencia de secretos/URLs reales. | Hardening, pentest y revision de arquitectura. | Seguridad. |
| No hay validacion legal/regulatoria | Alta | Flujos de DDU/autorizaciones podrian requerir reglas formales. | Documentacion declara sin validez legal. | Sandbox con datos ficticios. | Revision juridica/regulatoria antes de produccion. | Legal/compliance. |
