# Prototipo web local

Prototipo estatico del Portal Ciudadano de ClaveUnica, basado en `project/runs/RUN-22673eb11025`.

## Estado actual

Incluye portal publico, login simulado, OTP/2FA simulado, dashboard privado, datos personales, sesiones, DDU, notificaciones, autorizaciones y cierre de sesion. Carga mocks locales desde `app/mocks/` y usa `sessionStorage` solo para estado demo/local cuando aplica.

Ademas existe una API FastAPI local/mock en `app/backend/` con SQLite local y datos ficticios equivalentes a los mocks actuales. No usa backend real productivo, ClaveUnica real, CasillaUnica real, Plataforma de Notificaciones real ni servicios externos y no conecta servicios externos. No es produccion.

## Abrir localmente

Desde `app/`:

```powershell
python -m http.server 8000
```

Luego abrir:

```text
http://localhost:8000/frontend/
```

El prototipo debe abrirse mediante un servidor HTTP local para que `fetch()` pueda leer los mocks.

## Levantar backend local/mock

Desde la raiz del repositorio:

```powershell
python -m uvicorn app.backend.main:app --reload
```

API:

```text
http://localhost:8000
```

Prueba rapida sin servidor persistente:

```powershell
python -m app.backend.main
```

## Acceso demo

- Usuario demo: `demo.claveunica`
- Clave demo: `DemoLocal2026`
- Codigo OTP demo: `123456`

## Recorrido recomendado

1. Portal publico: inicio, ayuda, novedades, activar, recuperar e iniciar sesion.
2. Login: probar credenciales incorrectas y luego credenciales demo.
3. 2FA: probar OTP incorrecto y luego `123456`.
4. Dashboard: revisar resumen privado y accesos.
5. Datos personales: editar correo/telefono ficticios con factor demo.
6. Sesiones: revisar sesiones mock y cerrar una sesion remota simulada.
7. DDU: cancelar, volver, completar configuracion demo y revisar retorno.
8. Notificaciones: validar bloqueo con DDU pendiente, listado, detalle y marcado como leida.
9. Autorizaciones: aprobar, rechazar o revocar con factor demo.
10. Cerrar sesion.

## Datos personales demo

El cambio de correo y telefono es local y simulado. Para guardarlo se usa el factor de seguridad demo `123456`. No se guarda en backend y no usa servicios reales de ClaveUnica.

## Sesiones demo

Las sesiones son simuladas y se cargan desde `app/mocks/sessions.json`. no hay proteccion real productiva contra secuestro de sesion y no usa servicios reales.

## DDU demo

Estado inicial demo: DDU pendiente/no configurado. El recorrido permite cancelar desde el modal, continuar a una pasarela simulada, cancelar o completar la configuracion demo. No usa CasillaUnica real, no configura DDU real y No es una funcionalidad lista para produccion.

## Notificaciones demo

Con DDU pendiente se bloquea el listado. Luego de configurar DDU demo, se muestra un listado mock de notificaciones pendientes. Abrir el detalle permite revisar contenido local seguro y luego Marcar la notificacion como leida. No usa CasillaUnica real, no usa notificaciones reales y no es una funcionalidad lista para produccion.

## Autorizaciones demo

Permite revisar resumen por estados, aprobar o rechazar solicitudes pendientes, y revocarla cuando esta vigente con factor demo `123456`. No usa autorizaciones reales, no muestra datos sensibles reales y no es una funcionalidad lista para produccion.

## Documentacion relacionada

- `docs/SAFE_DEMO_SCRIPT.md`
- `docs/PROTOTYPE_EVIDENCE.md`
- `docs/FINAL_PROTOTYPE_REPORT.md`
- `docs/FINAL_HANDOFF.md`
- `docs/EVALUATOR_GUIDE.md`
- `docs/SCOPE_COMPLIANCE_MATRIX.md`
- `app/backend/README.md`

## QA y accesibilidad estatica

Desde la raiz:

```powershell
python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp
node --check app/frontend/app.js
```

Resultado vigente registrado: `55 passed`; `node --check` sin errores.

La suite backend vive en `tests/backend/` y valida salud, estado, login, OTP, inventario minimo de API, recursos principales, esquema minimo de 40 tablas, 115 CHECK constraints, seed ficticio y ausencia de URLs/secretos reales.

## Alcance y seguridad

- Autenticacion y OTP son simulados.
- No usar datos personales reales.
- No hay persistencia productiva.
- `sessionStorage` es solo estado demo/local del navegador.
- No hay validez legal, operacional ni productiva.
- Backend/API es local/mock con SQLite local.
- Criterio de 40 endpoints API: cumplido con 55 endpoints metodo+ruta bajo `/api/`.
- Criterio de 10 casos de uso: cumplido con `docs/USE_CASE_CATALOG.md`.
- Criterio de 30 funcionalidades/flujos: cumplido con `docs/FUNCTIONAL_FLOW_CATALOG.md`.
- Criterio de 30 pantallas: cumplido con `docs/SCREEN_INVENTORY.md`.
- Criterio de 60 reglas de negocio: cumplido con `docs/BUSINESS_RULES_CATALOG.md`.
- Checklist de completitud: cumplido con `docs/PRODUCT_COMPLETENESS_CHECKLIST.md`.
- Siguen pendientes cobertura 100% y deploy Linux EC2 AWS.
- Criterios de 40 tablas y 100 CHECK/validaciones SQL: cumplidos en backend local/mock.
