# Evidencia del prototipo local

## Modulos implementados

- Portal publico.
- Login simulado.
- OTP/2FA simulado.
- Dashboard privado.
- Datos personales con factor demo.
- Sesiones y multisesion mock.
- DDU / Domicilio Digital Unico mock.
- Notificaciones / CasillaUnica mock.
- Autorizaciones de datos sensibles mock.
- Cierre de sesion.

## Archivos principales

- `app/frontend/index.html`
- `app/frontend/styles.css`
- `app/frontend/app.js`
- `app/README.md`
- `docs/BACKLOG_TECNICO.md`

## Mocks usados

- `app/mocks/user.json`
- `app/mocks/ddu.json`
- `app/mocks/sessions.json`
- `app/mocks/notifications.json`
- `app/mocks/authorizations.json`

## Credenciales demo

- Usuario: `demo.claveunica`
- Clave: `DemoLocal2026`
- OTP / factor demo: `123456`

Estas credenciales son ficticias y solo sirven para el prototipo local.

## Flujos disponibles

- Portal publico: inicio, ayuda, novedades, activar, recuperar e iniciar sesion.
- Login: credenciales incorrectas/correctas.
- 2FA: OTP incorrecto/correcto.
- Dashboard: resumen de persona, DDU, 2FA, notificaciones y autorizaciones.
- Datos personales: cambio local de correo/telefono con factor demo.
- Sesiones: revision de sesiones mock y cierre remoto simulado.
- DDU: alerta pendiente, modal, pasarela simulada, cancelacion y configuracion demo.
- Notificaciones: bloqueo por DDU pendiente, listado, detalle y marcar como leida.
- Autorizaciones: aprobar, rechazar y revocar con factor demo.
- Cierre de sesion.

## Comandos para ejecutar

Desde `app/`:

```powershell
python -m http.server 8000
```

Abrir:

```text
http://127.0.0.1:8000/frontend/
```

## Comandos de prueba

Desde la raiz:

```powershell
python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp
node --check app/frontend/app.js
```

## Evidencias de resultados

- Pruebas automatizadas: `35 passed in 0.44s`.
- Validacion JS: `node --check app/frontend/app.js` sin errores.
- Validacion manual: completada en navegador integrado con servidor local temporal en `http://127.0.0.1:8000/frontend/`.

Flujos manuales verificados: portal publico, login incorrecto/correcto, OTP incorrecto/correcto, dashboard, datos personales con factor incorrecto/correcto, sesiones y cierre remoto, DDU pendiente/cancelacion/configuracion, notificaciones con DDU configurado, detalle y marcado como leida, autorizaciones con factor incorrecto/aprobacion/revocacion y cierre de sesion.

## Advertencias sandbox / no produccion

- No usa ClaveUnica real.
- No usa CasillaUnica real.
- No usa Plataforma de Notificaciones real.
- No implementa backend real.
- No consume servicios externos reales.
- No debe utilizar datos personales reales.
- `sessionStorage` se usa solo para estado demo/local.
- No es un sistema listo para produccion ni tiene validez legal/operacional.
