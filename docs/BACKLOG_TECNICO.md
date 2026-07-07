# Backlog técnico

Fuente: `project/runs/RUN-22673eb11025/traceability-matrix.md`.

## 1. Portal público

- Objetivo: habilitar los accesos públicos principales del servicio.
- Funcionalidades: activar cuenta; autenticar; recuperar acceso; ayuda; novedades.
- Criterios de aceptación: existen accesos para activar, autenticar, recuperar, ayuda y novedades; el flujo queda trazado a S06:HU01 y S08:CU_001.
- Prioridad: alta.
- Dependencias: ninguna identificada en la matriz.
- Archivos sugeridos a crear: `src/portal_publico/`, `tests/portal_publico/`.
- Estado inicial: pendiente.

## 2. Login y 2FA

- Objetivo: permitir autenticación con segundo factor opcional cuando corresponda.
- Funcionalidades: activación opcional de 2FA; exigencia de 2FA al login si está activo.
- Criterios de aceptación: el usuario puede activar 2FA; el login exige 2FA solo cuando está activo; el flujo queda trazado a S06:HU03 y S08:CU_003.
- Prioridad: alta.
- Dependencias: Portal público.
- Archivos sugeridos a crear: `src/auth/`, `src/security/2fa/`, `tests/auth/`.
- Estado: implementado parcialmente en prototipo local.
- Nota: existe flujo visual/mock de login y verificación OTP con datos locales; no incluye backend, integración real con ClaveÚnica ni servicios externos.

## 3. Datos personales

- Objetivo: gestionar cambios de datos de contacto con control de seguridad.
- Funcionalidades: cambio de teléfono; cambio de correo; validación mediante factor de seguridad.
- Criterios de aceptación: teléfono y correo pueden modificarse solo con factor de seguridad; el flujo queda trazado a S06:HU02 y S08:CU_002.
- Prioridad: alta.
- Dependencias: Login y 2FA.
- Archivos sugeridos a crear: `src/datos_personales/`, `tests/datos_personales/`.
- Estado: implementado en prototipo local.
- Nota: existe flujo visual/mock para ver y editar correo y telefono con factor de seguridad demo; no incluye backend ni integracion real con ClaveUnica.

## 4. Sesiones y multisesión

- Objetivo: aplicar política de multisesión y mitigación de secuestro de sesión.
- Funcionalidades: control de multisesión; mitigación de secuestro de sesión.
- Criterios de aceptación: existe política de multisesión aplicada; se incorporan controles contra secuestro de sesión; el flujo queda trazado a S06:HU04 y S08:CU_004.
- Prioridad: alta.
- Dependencias: Login y 2FA.
- Archivos sugeridos a crear: `src/sesiones/`, `tests/sesiones/`.
- Estado: implementado en prototipo local.
- Nota: existe gestion de sesiones activa ficticia con sesion actual, sesiones remotas mock, advertencia de multisesion y cierre remoto simulado; no incluye backend, persistencia real, IPs reales, ubicaciones reales, integracion real con ClaveUnica ni proteccion productiva contra secuestro de sesion.

## 5. DDU / Domicilio Digital Único

- Objetivo: implementar la derivación y gestión del Domicilio Digital Único.
- Funcionalidades: derivación; cancelación; retorno; alerta pendiente.
- Criterios de aceptación: se soportan derivación, cancelación, retorno y alerta pendiente; el flujo queda trazado a S06:HU05-HU12, S07 y S08:CU_005-CU_012.
- Prioridad: alta.
- Dependencias: Login y 2FA; Notificaciones / CasillaÚnica.
- Archivos sugeridos a crear: `src/ddu/`, `tests/ddu/`.
- Estado: implementado en prototipo local.
- Nota: existe flujo visual/mock de DDU con estado pendiente/configurado, alerta pendiente, modal de confirmacion, pasarela simulada, cancelacion, retorno al portal y acceso preparado hacia Notificaciones; no incluye backend, persistencia real, integracion real con ClaveUnica, CasillaUnica ni Plataforma de Notificaciones.

## 6. Notificaciones / CasillaÚnica

- Objetivo: mostrar notificaciones provenientes de CasillaÚnica.
- Funcionalidades: listado de notificaciones; detalle de notificaciones.
- Criterios de aceptación: el usuario puede listar y ver detalle desde CasillaÚnica; el flujo queda trazado a S06:HU09-HU11 y S07.
- Prioridad: media.
- Dependencias: Login y 2FA.
- Archivos sugeridos a crear: `src/notificaciones/`, `tests/notificaciones/`.
- Estado: implementado en prototipo local.
- Nota: existe modulo visual/mock de Notificaciones con validacion de DDU pendiente/configurado, listado de pendientes, detalle local, derivacion simulada/local a CasillaUnica y marcado como leida en `sessionStorage`; no incluye backend, persistencia real, notificaciones reales, Plataforma de Notificaciones real ni CasillaUnica real.

## 7. Autorizaciones de datos sensibles

- Objetivo: gestionar autorizaciones asociadas a datos sensibles.
- Funcionalidades: historial; pendientes; aprobación; rechazo; revocación.
- Criterios de aceptación: se consultan historial y pendientes; se permite aprobar, rechazar y revocar; el flujo queda trazado a S06:HU13-HU16 y S08:CU_013-CU_016.
- Prioridad: alta.
- Dependencias: Login y 2FA; Datos personales.
- Archivos sugeridos a crear: `src/autorizaciones/`, `tests/autorizaciones/`.
- Estado: implementado en prototipo local.
- Nota: existe modulo visual/mock de Autorizaciones de datos sensibles con resumen por estado, lista, detalle, aprobacion, rechazo y revocacion con factor demo obligatorio e historial local en `sessionStorage`; no incluye backend, persistencia real, autorizaciones reales, datos sensibles reales, validez legal ni integracion con servicios del Estado.

## 8. Calidad, accesibilidad y pruebas

- Objetivo: asegurar pruebas frontend, prototipo, accesibilidad y evidencia.
- Funcionalidades: pruebas frontend; validación de prototipo; revisión de accesibilidad; recopilación de evidencia.
- Criterios de aceptación: existen pruebas frontend; prototipo y accesibilidad quedan revisados; la evidencia queda registrada; el módulo queda trazado a S05.
- Prioridad: alta.
- Dependencias: módulos funcionales implementados.
- Archivos sugeridos a crear: `tests/frontend/`, `tests/accesibilidad/`, `docs/evidencias/`.
- Estado inicial: pendiente.

## 9. Garantía y evidencia

- Objetivo: documentar y verificar la cobertura mínima de garantía.
- Funcionalidades: calidad; funcionamiento; compatibilidad; rendimiento; seguridad; estabilidad.
- Criterios de aceptación: la evidencia cubre calidad, funcionamiento, compatibilidad, rendimiento, seguridad y estabilidad; el módulo queda trazado a S05.
- Prioridad: alta.
- Dependencias: Calidad, accesibilidad y pruebas.
- Archivos sugeridos a crear: `docs/evidencias/garantia/`, `tests/garantia/`.
- Estado inicial: pendiente.
