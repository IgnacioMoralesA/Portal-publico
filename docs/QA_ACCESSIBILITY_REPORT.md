# QA accesibilidad y validacion estatica

## Alcance revisado

- Portal publico, login, verificacion 2FA, dashboard privado.
- Datos personales, sesiones, DDU, notificaciones y autorizaciones.
- Mocks locales en `app/mocks/`.
- Documentacion de ejecucion y advertencias sandbox.

## Criterios de accesibilidad basica

- Estructura HTML con `lang`, viewport, header, main y footer.
- Headings asociados mediante `aria-labelledby`.
- Formularios con `label for` y campos identificables.
- Acciones con botones reales o enlaces reales.
- Mensajes de error/exito con `role="alert"` y `aria-live`.
- Navegacion privada con `aria-current="page"`.
- Modal DDU con `role="dialog"`, `aria-modal` y titulo accesible.
- Foco visible con `:focus-visible`.
- Reglas responsive para pantallas pequenas.

## Hallazgos

- La base ya tenia estructura semantica razonable, labels y botones reales.
- Faltaba exponer el estado activo de navegacion privada con `aria-current`.
- Los mensajes dinamicos podian anunciarse mejor a tecnologias asistivas.
- Los campos de usuario, clave y factor podian declarar `autocomplete` apropiado.
- No se encontro integracion real con ClaveUnica, CasillaUnica ni servicios externos.

## Correcciones realizadas

- Se agrego `aria-current="page"` al enlace activo de navegacion privada.
- Se agrego `aria-live` a mensajes de error/exito generados dinamicamente.
- Se agregaron hints `autocomplete="username"`, `current-password` y `one-time-code`.

## Pruebas ejecutadas

- `python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp`
- `node --check app/frontend/app.js`

Resultado: `35 passed in 0.44s`.

## Validacion manual

Se levanto servidor local temporal y se abrio `http://127.0.0.1:8000/frontend/` en el navegador integrado de Codex. La validacion manual se completo para portal publico, login incorrecto/correcto, OTP incorrecto/correcto, dashboard, datos personales con factor incorrecto/correcto, sesiones y cierre remoto, DDU con cancelacion/configuracion, notificaciones, autorizaciones y cierre de sesion.

`node --check app/frontend/app.js` finalizo sin errores.

## Limitaciones

- QA estatico, sin auditoria WCAG formal.
- Sin lector de pantalla ni matriz real de navegadores/dispositivos.
- Sin backend real, sin servicios reales y sin persistencia productiva.
- Evidencia visual solo valida si el navegador local responde.

## Riesgos residuales

- Falta prueba E2E automatizada de flujos completos.
- Falta validacion con tecnologias asistivas.
- Falta hardening productivo de autenticacion, sesiones, autorizaciones y notificaciones.
- Falta revision de rendimiento/compatibilidad amplia.
