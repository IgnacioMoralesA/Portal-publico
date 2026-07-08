# Inventario de pantallas y estados de interfaz

Inventario del frontend estatico y de vistas tecnicas relacionadas. Se cuentan pantallas, vistas, secciones y estados de interfaz validos para el prototipo local/sandbox.

| ID | Nombre | Descripcion | Archivo relacionado | Flujo relacionado | Estado | Observacion |
|---|---|---|---|---|---|---|
| UI-001 | Portal publico inicio | Home con hero y accesos principales. | `app/frontend/app.js` | FUN-001 | implementada | Vista publica local. |
| UI-002 | Ayuda publica | Vista informativa de ayuda. | `app/frontend/app.js` | FUN-003 | implementada | Contenido demo. |
| UI-003 | Novedades publicas | Vista informativa de novedades. | `app/frontend/app.js` | FUN-002 | implementada | Contenido ficticio. |
| UI-004 | Login | Formulario de usuario y clave demo. | `app/frontend/app.js` | FUN-004, FUN-005 | implementada | No usa ClaveUnica real. |
| UI-005 | OTP / 2FA | Formulario de codigo OTP demo. | `app/frontend/app.js` | FUN-007 | implementada | Codigo fijo demo. |
| UI-006 | Dashboard privado | Resumen autenticado del usuario demo. | `app/frontend/app.js` | FUN-010 | implementada | Requiere sesion demo. |
| UI-007 | Datos personales vista | Panel de datos personales actuales. | `app/frontend/app.js` | FUN-011 | implementada | Datos ficticios. |
| UI-008 | Datos personales edicion | Formulario de correo/telefono y factor. | `app/frontend/app.js` | FUN-012 | implementada | Cambios locales. |
| UI-009 | Sesiones listado | Tabla/tarjetas de sesiones mock. | `app/frontend/app.js` | FUN-014, FUN-015 | implementada | Sesiones ficticias. |
| UI-010 | DDU pendiente | Estado con alerta de DDU no configurado. | `app/frontend/app.js` | FUN-019 | implementada | Bloquea notificaciones. |
| UI-011 | Modal DDU | Confirmacion de derivacion simulada. | `app/frontend/app.js` | FUN-020 | implementada | Modal accesible con role dialog. |
| UI-012 | Pasarela DDU | Pantalla de configuracion DDU demo. | `app/frontend/app.js` | FUN-021 | implementada | No conecta CasillaUnica. |
| UI-013 | DDU configurado/cancelado | Estado posterior a completar o cancelar demo. | `app/frontend/app.js` | FUN-022, FUN-023 | implementada | Estado local/sessionStorage. |
| UI-014 | Notificaciones bloqueadas por DDU | Alerta cuando DDU esta pendiente. | `app/frontend/app.js` | FUN-024 | implementada | Guia al modulo DDU. |
| UI-015 | Listado de notificaciones | Lista de notificaciones ficticias. | `app/frontend/app.js` | FUN-025 | implementada | Requiere DDU configurado. |
| UI-016 | Filtros/estado de notificaciones | Seccion de resumen y estados de notificaciones. | `app/frontend/app.js` | FUN-026 | implementada | Catalogos demo. |
| UI-017 | Detalle de notificacion | Vista de contenido de notificacion. | `app/frontend/app.js` | FUN-027 | implementada | Sin datos reales. |
| UI-018 | Notificacion leida/exito | Estado posterior a marcar como leida. | `app/frontend/app.js` | FUN-028 | implementada | Estado local demo. |
| UI-019 | Autorizaciones resumen | Panel con conteos y solicitudes. | `app/frontend/app.js` | FUN-030 | implementada | Datos sensibles genericos. |
| UI-020 | Autorizacion detalle pendiente | Detalle con accion aprobar/rechazar. | `app/frontend/app.js` | FUN-031 | implementada | Requiere factor demo. |
| UI-021 | Autorizacion aprobada | Estado aprobado y posible revocacion. | `app/frontend/app.js` | FUN-032 | implementada | Sin validez legal. |
| UI-022 | Autorizacion rechazada | Estado rechazado con historial demo. | `app/frontend/app.js` | FUN-033 | implementada | Decision local. |
| UI-023 | Recuperacion de acceso | Acceso publico a recuperacion demo. | `app/frontend/app.js` | FUN-004, CU-011 | implementada | Flujo visual/documentado. |
| UI-024 | Autorizacion revocada | Estado posterior a revocar autorizacion. | `app/frontend/app.js` | FUN-034 | implementada | Decision local. |
| UI-025 | Error de login | Estado de credenciales invalidas. | `app/frontend/app.js` | FUN-005, FUN-006 | implementada | Mensaje seguro. |
| UI-026 | Error de OTP | Estado de codigo incorrecto. | `app/frontend/app.js` | FUN-007 | implementada | No entrega detalles sensibles. |
| UI-027 | Navegacion privada | Shell lateral privado y rutas internas. | `app/frontend/app.js` | FUN-010 | implementada | Accesible por hash. |
| UI-028 | Error de factor en datos | Estado de factor incorrecto en edicion. | `app/frontend/app.js` | FUN-012, FUN-013 | implementada | Bloquea guardado. |
| UI-029 | Cierre remoto exitoso | Estado de sesion remota cerrada demo. | `app/frontend/app.js` | FUN-016 | implementada | Boton deshabilitado al cerrar. |
| UI-030 | API docs local | Documentacion OpenAPI generada por FastAPI. | `app/backend/main.py` | CU-012 | implementada | Disponible solo si servidor local esta activo. |
| UI-031 | Vistas tecnicas API | Respuestas JSON de evidencia, reglas, pantallas y deploy. | `app/backend/routers/` | FUN-036 a FUN-043 | implementada | Apoya evaluacion tecnica. |
| UI-032 | Cierre de sesion | Estado posterior a salir del area privada. | `app/frontend/app.js` | FUN-044 | implementada | Vuelve a portal publico. |
| UI-033 | Estado responsive movil | Layout adaptado a pantallas pequenas. | `app/frontend/styles.css` | FUN-001 a FUN-044 | implementada | Validacion estatica; falta matriz real. |
| UI-034 | Estado de exito generico | Mensajes de guardado, lectura o decision exitosa. | `app/frontend/app.js` | FUN-012, FUN-028, FUN-032 | implementada | Mensajes locales. |
| UI-035 | Estado de error generico | Mensajes de error por validacion o ID inexistente. | `app/frontend/app.js` | FUN-005, FUN-007, FUN-031 | implementada | No expone secretos. |
