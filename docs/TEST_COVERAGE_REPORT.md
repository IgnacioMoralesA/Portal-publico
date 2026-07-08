# Reporte de cobertura de pruebas

## Alcance

La cobertura instrumentada se mide sobre el backend Python local/mock en `app/backend`.

Se incluye logica de configuracion, base de datos, seed, modelos SQLAlchemy, schemas Pydantic, `main.py` y routers FastAPI. Se omiten solo `__init__.py` vacios de paquetes backend, carpetas de cache, tests y la base SQLite generada.

## Comando ejecutado

```powershell
python -m pytest --cov=app.backend --cov-report=term-missing --cov-report=html --cov-fail-under=100 tests -p no:cacheprovider --basetemp=.pytest-basetemp
```

## Resultado final

- Resultado: `89 passed`.
- Cobertura backend Python: `100.00%`.
- Umbral: `--cov-fail-under=100`, alcanzado.
- Reporte HTML generado en `htmlcov/`.

## Modulos cubiertos

- `app/backend/config.py`
- `app/backend/database.py`
- `app/backend/main.py`
- `app/backend/models/__init__.py`
- `app/backend/schemas/core.py`
- `app/backend/seed.py`
- `app/backend/routers/audit.py`
- `app/backend/routers/auth.py`
- `app/backend/routers/authorizations.py`
- `app/backend/routers/ddu.py`
- `app/backend/routers/devices.py`
- `app/backend/routers/evidence.py`
- `app/backend/routers/health.py`
- `app/backend/routers/help.py`
- `app/backend/routers/institutions.py`
- `app/backend/routers/notifications.py`
- `app/backend/routers/public.py`
- `app/backend/routers/rules.py`
- `app/backend/routers/sessions.py`
- `app/backend/routers/users.py`

## Advertencias

La corrida registra advertencias no bloqueantes:

- `StarletteDeprecationWarning` de `fastapi.testclient` por compatibilidad futura con `httpx`.
- `RuntimeWarning` de `runpy` al ejecutar `app.backend.main` como `__main__` durante una prueba de import/bootstrap.

## Limitaciones

Esta evidencia corresponde a cobertura instrumentada del backend Python local/mock. No demuestra despliegue productivo, seguridad productiva ni integraciones reales.

El frontend JavaScript se valida con pruebas estaticas y `node --check app/frontend/app.js`; no hay cobertura JS instrumentada en este ciclo.

El despliegue online en Linux sobre EC2 AWS permanece pendiente.
