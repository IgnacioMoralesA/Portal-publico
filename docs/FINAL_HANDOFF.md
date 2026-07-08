# Handoff final

## Estado final

La etapa de prototipo funcional local/sandbox queda cerrada. El prototipo esta disponible como frontend estatico en `app/frontend/`, con mocks en `app/mocks/`, pruebas estaticas en `tests/` y documentacion final en `docs/`.

## Que esta listo

- Demo local controlada.
- Recorrido publico/privado completo.
- Credenciales y factor demo.
- Mocks seguros y ficticios.
- Pruebas estaticas pasando.
- Evidencia, QA, checklist, trazabilidad, riesgos e indice final.

## Que queda pendiente

- Backend/API real.
- Integraciones reales autorizadas.
- Persistencia real.
- E2E automatizado.
- Auditoria WCAG formal.
- Pruebas con tecnologias asistivas.
- Matriz real de navegadores/dispositivos.
- Hardening productivo.
- Validacion legal/regulatoria.

## Como revisar el prototipo

Desde `app/`:

```powershell
python -m http.server 8000
```

Abrir:

```text
http://127.0.0.1:8000/frontend/
```

Credenciales:

- Usuario: `demo.claveunica`
- Clave: `DemoLocal2026`
- OTP / factor demo: `123456`

## Como ejecutar pruebas

Desde la raiz:

```powershell
python -m pytest -q tests -p no:cacheprovider --basetemp=.pytest-basetemp
node --check app/frontend/app.js
```

`python -m factory.cli verify --project project` fue intentado durante el cierre, pero no aplica en esta CLI porque no existe el subcomando `verify`.

## Como hacer demo segura

Usar `docs/SAFE_DEMO_SCRIPT.md`. Reglas minimas:

- No ingresar datos personales reales.
- No presentar como produccion.
- No afirmar integracion real.
- No afirmar cumplimiento WCAG/legal completo.
- Usar solo credenciales demo.

## Archivos clave

- `README.md`
- `app/README.md`
- `app/frontend/index.html`
- `app/frontend/styles.css`
- `app/frontend/app.js`
- `app/mocks/*.json`
- `docs/FINAL_INDEX.md`
- `docs/FINAL_PROTOTYPE_REPORT.md`
- `docs/FINAL_TRACEABILITY_MATRIX.md`
- `docs/FINAL_TEST_SUMMARY.md`
- `docs/FINAL_RISK_REGISTER.md`
- `docs/HANDOFFS.md`

## Handoffs abiertos

Ver `docs/HANDOFFS.md` para continuidad hacia E2E, accesibilidad, backend/API, persistencia, hardening, CI/CD e integracion real autorizada.

## Recomendacion de continuacion

Priorizar E2E automatizado y auditoria de accesibilidad antes de aumentar alcance funcional. Luego definir contratos API y persistencia real local antes de cualquier integracion institucional.

## Advertencias sandbox/no produccion

No existe readiness productivo. La entrega es solo demo local/sandbox con trazabilidad y evidencia inicial.
