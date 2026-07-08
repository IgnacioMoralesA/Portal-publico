# Portal Ciudadano de ClaveUnica - Prototipo local

Proyecto final basado en una fabrica ARNES SDD para organizar, trazar y validar un prototipo funcional local/sandbox del Portal Ciudadano de ClaveUnica.

El run base validado es `project/runs/RUN-22673eb11025`, con estado `complete`, `missing: []`, 27 agentes ejecutados y presupuesto de tokens OK.

## Estado actual

El prototipo publico/privado esta implementado como frontend estatico local. Permite recorrer portal publico, login simulado, OTP/2FA simulado, dashboard, datos personales, sesiones, DDU, notificaciones, autorizaciones y cierre de sesion.

El ciclo `backend_scope_matrix_and_api_foundation` agrega una API FastAPI local/mock con SQLite local, seed ficticio, routers iniciales y pruebas backend minimas. Este proyecto no esta listo para produccion. No conecta ClaveUnica real, CasillaUnica real, Plataforma de Notificaciones real ni servicios externos. Usa datos ficticios, mocks locales, SQLite local y `sessionStorage` solo para estado demo/local.

## Estructura resumida

- `app/frontend/`: prototipo HTML, CSS y JavaScript estatico.
- `app/backend/`: API FastAPI local/mock con SQLite y seed ficticio.
- `app/mocks/`: datos ficticios para usuario, DDU, sesiones, notificaciones y autorizaciones.
- `docs/`: especificacion, evidencia, QA, guion demo y cierre final.
- `factory/`: arnes SDD local, sin cambios en este cierre documental.
- `project/`: entradas y runs de fabrica, incluyendo `RUN-22673eb11025`.
- `tests/`: pruebas estaticas de fabrica y frontend.

## Modulos implementados

- Portal publico.
- Login simulado y OTP/2FA simulado.
- Dashboard privado.
- Datos personales con factor demo.
- Sesiones y multisesion mock.
- DDU / Domicilio Digital Unico mock.
- Notificaciones / CasillaUnica mock.
- Autorizaciones de datos sensibles mock.
- QA estatico y accesibilidad basica.

## Credenciales demo

- Usuario: `demo.claveunica`
- Clave: `DemoLocal2026`
- OTP / factor demo: `123456`

No ingresar datos personales reales.

## Como ejecutar frontend

Desde `app/`:

```powershell
python -m http.server 8000
```

Abrir:

```text
http://127.0.0.1:8000/frontend/
```

## Como ejecutar backend local/mock

Desde la raiz:

```powershell
python -m uvicorn app.backend.main:app --reload
```

Verificacion de import sin servidor persistente:

```powershell
python -m app.backend.main
```

Endpoints base: `/health`, `/api/status`, `/api/auth/login`, `/api/auth/verify-otp`, `/api/users/me`, `/api/ddu/status`, `/api/sessions`, `/api/notifications`, `/api/authorizations`.

## Como probar

Desde la raiz del repositorio:

```powershell
python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp
node --check app/frontend/app.js
```

Resultado final registrado: `35 passed`; `node --check` sin errores.

El ciclo backend agrega pruebas en `tests/backend/`; el resultado vigente debe verificarse ejecutando la suite completa.

## Brechas del criterio minimo

- Faltan 31 endpoints para completar 40.
- Faltan 32 tablas para completar 40.
- Faltan 81 validaciones/CHECK para completar 100.
- Falta checklist de producto final actualizado a todos los criterios.
- Falta cobertura automatizada 100%.
- Falta deploy online en Linux EC2 AWS.

## Documentacion final

Indice maestro: `docs/FINAL_INDEX.md`.

Documentos principales:

- `docs/FINAL_PROTOTYPE_REPORT.md`
- `docs/FINAL_TRACEABILITY_MATRIX.md`
- `docs/FINAL_TEST_SUMMARY.md`
- `docs/FINAL_RISK_REGISTER.md`
- `docs/FINAL_HANDOFF.md`
- `docs/EVALUATOR_GUIDE.md`
- `docs/TECHNICAL_REVIEW_GUIDE.md`

## Riesgos residuales

Persisten riesgos por falta de auditoria WCAG formal, pruebas con lector de pantalla, matriz real de navegadores/dispositivos, E2E automatizado, backend real, persistencia real, hardening productivo, autenticacion institucional real e integraciones reales.

## Proximos pasos

Ver `docs/NEXT_CYCLES.md` para ciclos opcionales: E2E, WCAG formal, tecnologias asistivas, matriz de dispositivos, backend/API local, contratos API, hardening, CI/CD e integracion real solo con autorizacion formal.
