# Backend local/mock

API FastAPI local para el prototipo del Portal Ciudadano de ClaveUnica. Es una base de arquitectura y pruebas, no un sistema productivo.

## Advertencias

- No conecta ClaveUnica real.
- No conecta CasillaUnica real.
- No conecta Plataforma de Notificaciones real.
- No usa datos personales reales.
- No debe usarse en produccion.
- Las credenciales son ficticias: `demo.claveunica`, `DemoLocal2026`, OTP `123456`.

## Levantar API local

Desde la raiz del repositorio:

```powershell
python -m uvicorn app.backend.main:app --reload
```

API local:

```text
http://127.0.0.1:8000
```

Verificacion sin dejar servidor colgado:

```powershell
python -m app.backend.main
```

## Endpoints locales/mock

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/health` | Salud de la API |
| GET | `/api/status` | Estado local/mock |
| POST | `/api/auth/login` | Login demo |
| POST | `/api/auth/verify-otp` | OTP demo |
| GET | `/api/users/me` | Usuario demo |
| GET | `/api/ddu/status` | Estado DDU demo |
| GET | `/api/sessions` | Sesiones demo |
| GET | `/api/notifications` | Notificaciones demo |
| GET | `/api/authorizations` | Autorizaciones demo |

La expansion `api_40_endpoints_expansion` registra 55 endpoints metodo+ruta bajo `/api/` sobre FastAPI local/mock. Cubre auth demo, perfil/contacto, sesiones, dispositivos, DDU, notificaciones, autorizaciones, instituciones, integraciones, portal publico, ayuda, auditoria, evidencia, reglas, pantallas y objetivos de despliegue. Todos usan datos ficticios o SQLite local; no conectan servicios reales.

## Base de datos

SQLite local en `app/backend/local.db`, creada automaticamente al importar `app.backend.main`.

Estado del esquema local/mock:

- 40 tablas SQLAlchemy/SQLite.
- 115 restricciones `CHECK`.
- Seed ficticio idempotente para usuario demo, sesiones, DDU, notificaciones, autorizaciones, catalogos, evidencia y control de despliegue pendiente.
- Pruebas de esquema en `tests/backend/test_database_schema.py`, `tests/backend/test_database_constraints.py` y `tests/backend/test_seed_data.py`.

## Brechas pendientes

- Criterio de 40 endpoints API: cumplido con 55 endpoints metodo+ruta bajo `/api/`.
- Criterio de 40 tablas: cumplido.
- Criterio de 100 CHECK: cumplido.
- Criterio de 10 casos de uso: cumplido con `docs/USE_CASE_CATALOG.md`.
- Criterio de 30 funcionalidades/flujos: cumplido con `docs/FUNCTIONAL_FLOW_CATALOG.md`.
- Criterio de 30 pantallas: cumplido con `docs/SCREEN_INVENTORY.md`.
- Criterio de 60 reglas de negocio: cumplido con `docs/BUSINESS_RULES_CATALOG.md`.
- Checklist de completitud: cumplido con `docs/PRODUCT_COMPLETENESS_CHECKLIST.md`.
- Falta cobertura automatizada 100%.
- Falta despliegue online en Linux sobre EC2 AWS.
