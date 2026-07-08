# Checklist final del prototipo

Estados permitidos: cumple, parcial, pendiente, no aplica.

| Area | Estado | Evidencia / observacion |
|---|---|---|
| Portal publico | cumple | Inicio, ayuda, novedades, activar, recuperar e iniciar sesion presentes en prototipo local. |
| Login | cumple | Login simulado con credenciales demo y errores comprensibles. |
| 2FA | cumple | OTP demo requerido y validado localmente. |
| Datos personales | cumple | Edicion local con factor demo obligatorio. |
| Sesiones | cumple | Sesiones mock y cierre remoto simulado. |
| DDU | cumple | Pendiente/configurado, modal, pasarela simulada, cancelacion y retorno. |
| Notificaciones | cumple | Bloqueo por DDU pendiente, listado, detalle y marcado como leida con estado local. |
| Autorizaciones | cumple | Resumen, detalle, aprobar, rechazar y revocar con factor demo. |
| Accesibilidad | parcial | Validacion estatica basica agregada; falta auditoria WCAG formal y tecnologias asistivas. |
| Responsividad | parcial | CSS tiene media query para vistas pequenas; falta matriz real de dispositivos. |
| Pruebas | parcial | Tests estaticos agregados; falta E2E de navegador estable. |
| Documentacion | cumple | Reporte QA, evidencia, guion seguro y checklist creados. |
| Seguridad demo | cumple | Sin backend real, sin servicios externos reales, mocks ficticios y `sessionStorage` demo/local. |
| No produccion | cumple | Advertencias documentadas; prototipo no tiene validez productiva. |
| Backend real | no aplica | Restriccion del ciclo: no implementar backend. |
| Integracion ClaveUnica real | no aplica | Restriccion del ciclo: no conectar servicio real. |
| Integracion CasillaUnica real | no aplica | Restriccion del ciclo: no conectar servicio real. |
| Validacion manual visual | cumple | Completada en navegador integrado con servidor local temporal; todos los flujos manuales definidos respondieron correctamente. |
