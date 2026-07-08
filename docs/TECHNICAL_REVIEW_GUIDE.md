# Guia de revision tecnica

## Estructura frontend

- `app/frontend/index.html`: estructura HTML minima y carga de assets.
- `app/frontend/styles.css`: estilos, layout responsive, foco visible y componentes.
- `app/frontend/app.js`: estado, carga de mocks, router hash, vistas y handlers.

No se agregaron frameworks frontend ni dependencias pesadas.

## Archivos principales

- `app/frontend/index.html`
- `app/frontend/styles.css`
- `app/frontend/app.js`
- `app/mocks/user.json`
- `app/mocks/ddu.json`
- `app/mocks/sessions.json`
- `app/mocks/notifications.json`
- `app/mocks/authorizations.json`

## Mocks

Los mocks son JSON locales y ficticios. No contienen IPs reales, RUN completo, datos personales reales, secretos ni URLs productivas.

## sessionStorage

Usado para:

- `claveunica_demo_auth`
- `claveunica_demo_pending_user`
- `claveunica_demo_ddu_state`
- `claveunica_demo_notification_reads`
- `claveunica_demo_authorization_state`

Este almacenamiento es solo demo/local.

## Pruebas

Pruebas disponibles:

- `tests/test_factory.py`
- `tests/frontend/test_login_2fa_static.py`
- `tests/frontend/test_personal_data_static.py`
- `tests/frontend/test_sessions_static.py`
- `tests/frontend/test_ddu_static.py`
- `tests/frontend/test_notifications_static.py`
- `tests/frontend/test_authorizations_static.py`
- `tests/frontend/test_accessibility_static.py`
- `tests/frontend/test_security_static.py`

Comandos:

```powershell
python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp
node --check app/frontend/app.js
```

## Puntos de extension

- Reemplazar carga de mocks por contratos API.
- Separar vistas en modulos si el frontend crece.
- Agregar capa de estado testeable.
- Agregar E2E automatizado.
- Introducir backend/API local sin conectar servicios reales.
- Agregar persistencia controlada.

## Riesgos tecnicos

- `app.js` concentra la logica y puede crecer demasiado.
- No hay tipado ni bundling.
- No hay E2E.
- `sessionStorage` no modela persistencia real.
- No hay autenticacion ni autorizacion reales.
- No hay control de errores de red productivo.

## Proximos pasos para backend real

1. Definir contratos API por modulo.
2. Crear backend mock/API local.
3. Agregar validaciones de servidor.
4. Agregar persistencia local controlada.
5. Incorporar autenticacion institucional simulada robusta.
6. Preparar integracion real solo con autorizacion formal.

## Proximos pasos para E2E

1. Elegir Playwright o alternativa liviana.
2. Automatizar login, OTP, DDU, notificaciones, autorizaciones y logout.
3. Ejecutar en CI cuando exista.
4. Capturar evidencia visual solo si el entorno es estable.

## Proximos pasos para hardening

1. Threat model.
2. Politicas de sesion.
3. Cabeceras de seguridad.
4. Gestion de secretos.
5. Validacion de entrada/salida.
6. Auditoria de dependencias si se agregan.
7. Revision legal/regulatoria antes de produccion.
