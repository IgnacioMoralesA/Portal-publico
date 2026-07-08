# Resumen final de pruebas

## Comandos ejecutados

```powershell
python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp
node --check app/frontend/app.js
python -m factory.cli verify --project project
```

## Resultado pytest

Resultado final: `35 passed`.

## Resultado node --check

`node --check app/frontend/app.js` finalizo sin errores de sintaxis.

## Resultado factory verify

Se intento ejecutar `python -m factory.cli verify --project project`, pero la CLI disponible respondio:

```text
invalid choice: 'verify' (choose from 'init', 'run')
```

Resultado: no aplicable en este snapshot de la fabrica.

## Resultado npm

No existe `package.json` en la raiz, por lo tanto npm no aplica y no se ejecutaron scripts npm.

## Validacion manual

Validacion manual registrada en navegador integrado sobre:

```text
http://127.0.0.1:8000/frontend/
```

Flujos revisados: portal publico, login incorrecto/correcto, OTP incorrecto/correcto, dashboard, datos personales con factor incorrecto/correcto, sesiones y cierre remoto, DDU con cancelacion/configuracion, notificaciones, autorizaciones y cierre de sesion.

## Pruebas por archivo/carpeta

| Archivo/carpeta | Cobertura |
|---|---|
| `tests/test_factory.py` | Fabrica, contexto, generacion de artefactos y validadores base. |
| `tests/frontend/test_login_2fa_static.py` | Marcadores de portal, login, OTP, dashboard y cierre de sesion. |
| `tests/frontend/test_personal_data_static.py` | Datos personales, factor demo, documentacion y ausencia de servicios reales. |
| `tests/frontend/test_sessions_static.py` | Sesiones mock, cierre remoto, datos seguros y documentacion. |
| `tests/frontend/test_ddu_static.py` | DDU, modal, pasarela simulada, cancelacion, estado local y documentacion. |
| `tests/frontend/test_notifications_static.py` | DDU gate, listado, detalle, marcado como leida y mocks seguros. |
| `tests/frontend/test_authorizations_static.py` | Resumen, detalle, decisiones, factor demo, historial y mocks seguros. |
| `tests/frontend/test_accessibility_static.py` | Semantica, labels, acciones, `aria-live`, modal, foco y responsive. |
| `tests/frontend/test_security_static.py` | Ausencia de integraciones reales, URLs productivas, secretos, IPs reales y datos personales reales. |

## Cobertura estatica

La cobertura es estatica/documental y valida presencia de estructuras, marcadores, datos mock seguros, ausencia de integraciones reales y contratos basicos de accesibilidad.

## Limitaciones

- No hay pruebas E2E reales automatizadas todavia.
- No se ejecuto Playwright.
- No se ejecuto Lighthouse.
- No se ejecuto auditoria WCAG formal.
- No hay pruebas backend, API ni integraciones externas.
- No hay pruebas de rendimiento, carga, seguridad productiva ni compatibilidad amplia.

## Pruebas pendientes

- E2E automatizado de flujos completos.
- Auditoria WCAG formal.
- Pruebas con lector de pantalla y teclado real.
- Matriz real de navegadores/dispositivos.
- Pruebas de contratos API cuando exista backend.
- Pruebas de seguridad productiva cuando exista arquitectura real.
